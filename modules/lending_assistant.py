# modules/lending_assistant.py
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ---------------------------
# Helpers: loading & safety
# ---------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

@st.cache_data
def load_df_json(path: Path) -> pd.DataFrame:
    try:
        return pd.read_json(path)
    except Exception:
        return pd.DataFrame()

@st.cache_data
def load_df_csv(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

@st.cache_data
def load_all_data():
    tx = load_df_json(DATA_DIR / "transactions.json")         # expected columns: date, amount, description, counterparty, type, currency?
    mb = load_df_csv(DATA_DIR / "multi_bank_profile.csv")     # optional overview/summary by bank
    acct = load_df_json(DATA_DIR / "account_summary.json")    # optional balances/avg balance by account
    chk = load_df_csv(DATA_DIR / "CBUAE_Corporate_Lending_Checklist.csv")  # optional checklist
    return tx, mb, acct, chk

# ---------------------------
# Feature engineering
# ---------------------------

def normalize_tx(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    # standardize columns
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    else:
        df["date"] = pd.to_datetime("today")
    if "amount" not in df.columns:
        df["amount"] = 0.0
    if "description" not in df.columns:
        df["description"] = ""
    if "counterparty" not in df.columns:
        df["counterparty"] = ""
    if "type" not in df.columns:
        df["type"] = np.where(df["amount"] >= 0, "CREDIT", "DEBIT")
    return df

def monthly_aggregates(tx: pd.DataFrame) -> pd.DataFrame:
    if tx.empty:
        return pd.DataFrame(columns=["month", "inflow", "outflow", "net"])
    df = tx.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)
    inflow = df[df["amount"] > 0].groupby("month")["amount"].sum()
    outflow = df[df["amount"] < 0].groupby("month")["amount"].sum().abs()
    m = pd.DataFrame({"inflow": inflow, "outflow": outflow}).fillna(0.0)
    m["net"] = m["inflow"] - m["outflow"]
    m = m.reset_index()
    return m

def bounced_indicator(tx: pd.DataFrame) -> int:
    """Count bounced/returned items heuristically from description/type."""
    if tx.empty:
        return 0
    desc = (tx.get("description", pd.Series([""]*len(tx))).fillna("") + " " +
            tx.get("type", pd.Series([""]*len(tx))).fillna(""))
    desc = desc.str.upper()
    hints = ["BOUNC", "RETURN", "UNPAID", "RD CHQ", "CHEQUE RETURN", "RJCT", "RTO"]
    return int(desc.apply(lambda s: any(h in s for h in hints)).sum())

def inflow_volatility(monthly: pd.DataFrame) -> float:
    if monthly.empty or monthly["inflow"].mean() == 0:
        return 0.0
    return float(np.std(monthly["inflow"]) / max(1e-9, monthly["inflow"].mean()))

# ---------------------------
# Other-bank loan detection
# ---------------------------

BANK_KEYWORDS = [
    "ENBD","EMIRATES NBD","FAB","FIRST ABU DHABI","ADCB","MASHREQ","RAKBANK","DIB","DUBAI ISLAMIC",
    "NBAD","NBK","ABK","SCB","STANDARD CHARTERED","HSBC","CITI","BARCLAYS",
    "EMI","LOAN","FINANCE","MORTGAGE","OD","TFC","INSTALLMENT","INSTALLMENT"
]
EMI_HINTS = ["EMI","E.M.I","INSTAL","INSTALLMENT","EASY PAY","LOAN REPAY","MORT","FINANCE"]

def detect_external_loans(tx_df: pd.DataFrame) -> pd.DataFrame:
    """
    Heuristics: recurring monthly debits with bank/loan hints.
    Returns columns: lender, product, emi, currency, estimated_outstanding, evidence
    """
    if tx_df.empty:
        return pd.DataFrame(columns=["lender","product","emi","currency","estimated_outstanding","evidence"])
    df = tx_df.copy()
    df["desc"] = (df.get("description","").astype(str) + " " + df.get("counterparty","").astype(str)).str.upper()
    debits = df[df["amount"] < 0].copy()

    def hit(s): return any(k in s for k in BANK_KEYWORDS) or any(h in s for h in EMI_HINTS)
    debits = debits[debits["desc"].apply(hit)]
    if debits.empty:
        return pd.DataFrame(columns=["lender","product","emi","currency","estimated_outstanding","evidence"])

    # lender token
    def lender_token(s):
        for k in BANK_KEYWORDS:
            if k in s: return k
        return "OTHER"

    debits["lender"] = debits["desc"].apply(lender_token)

    rows = []
    for lender, grp in debits.groupby("lender"):
        grp = grp.sort_values("date")
        grp["amt10"] = (grp["amount"].abs() / 10.0).round() * 10
        counts = grp["amt10"].value_counts()
        if counts.empty:
            continue
        emi = float(counts.index[0])  # most frequent debit magnitude
        dates = pd.to_datetime(grp["date"])
        if len(dates) >= 3:
            diffs = dates.diff().dt.days.dropna()
            monthlyish = (abs(diffs.median() - 30) <= 6)
            gap_txt = f"{diffs.median():.1f}d"
        else:
            monthlyish = False
            gap_txt = "n/a"
        product = "TERM LOAN" if monthlyish else "REVOLVING/OD?"
        # Rough outstanding using annuity PV if monthlyish
        outstanding = np.nan
        if monthlyish:
            r = 0.12/12  # 12% APR assumption (tunable in UI later)
            n = 24      # assume 24 months remaining
            outstanding = emi * (1 - (1+r)**(-n)) / r
        evidence = f"{len(grp)} debits; median gap {gap_txt}; top debit≈{emi:,.0f}"
        rows.append({
            "lender": lender,
            "product": product,
            "emi": round(emi,2),
            "currency": "AED",
            "estimated_outstanding": None if np.isnan(outstanding) else round(float(outstanding),2),
            "evidence": evidence
        })
    return pd.DataFrame(rows)

# ---------------------------
# Eligibility & policy math
# ---------------------------

def eligible_term_cap_from_cashflows(avg_inflow, avg_outflow, target_dscr=1.5, apr=0.12, tenor_months=24):
    ebitda_proxy = max(0.0, avg_inflow - avg_outflow)
    if ebitda_proxy <= 0:
        return 0.0, {"ebitda_proxy": ebitda_proxy, "annual_service": 0.0, "monthly_service": 0.0}
    annual_service = ebitda_proxy / max(1e-9, target_dscr)
    monthly_service = annual_service / 12.0
    r = apr/12.0
    n = tenor_months
    pv = monthly_service * (1 - (1+r)**(-n)) / r if r > 0 else monthly_service * n
    return float(pv), {"ebitda_proxy": ebitda_proxy, "annual_service": annual_service, "monthly_service": monthly_service}

def wc_limit_from_flows(avg_inflow, volatility, k_base=0.8):
    """Working-capital limit heuristic with volatility haircut."""
    k = max(0.4, min(0.95, k_base * (1 - volatility)))  # bound 40–95%
    return float(k * max(0.0, avg_inflow))

def compute_eligibility(ratios, of_signals, policies, tier1_capital_aed, exposure_to_obligor_aed, term_cap, wc_cap):
    reasons = []
    status = "Eligible"
    # Core policy checks
    if ratios.get("DSCR_proxy", np.inf) < policies["min_dscr"]:
        status = "Conditional"; reasons.append(f"DSCR {ratios['DSCR_proxy']:.2f} < {policies['min_dscr']:.2f}")
    if ratios.get("Leverage_proxy", 0) > policies["max_leverage"]:
        status = "Conditional"; reasons.append(f"Leverage {ratios['Leverage_proxy']:.2f}x > {policies['max_leverage']:.2f}x")
    if ratios.get("Inflow_volatility", 0) > policies["max_inflow_vol"]:
        status = "Conditional"; reasons.append(f"Inflow volatility {ratios['Inflow_volatility']:.2f} > {policies['max_inflow_vol']:.2f}")
    if of_signals.get("bounced_txn_6m", 0) > policies["max_bounced_txn_6m"]:
        status = "Conditional"; reasons.append(f"Bounced txns {of_signals['bounced_txn_6m']} > {policies['max_bounced_txn_6m']}")

    # CBUAE single obligor cap 25% Tier 1 (hard)
    single_obligor_pct = (exposure_to_obligor_aed / max(1.0, tier1_capital_aed)) * 100
    if single_obligor_pct > 25.0:
        status = "Decline"; reasons.append(f"Single obligor {single_obligor_pct:.1f}% > 25% of Tier 1")

    # Overall capacity
    policy_cap = 0.25 * tier1_capital_aed
    max_cap = min(policy_cap, max(term_cap, wc_cap))  # choose the larger of term/WC, then apply policy ceiling

    return status, reasons, {"single_obligor_pct": single_obligor_pct, "policy_cap": policy_cap, "max_cap": max_cap}

# ---------------------------
# Credit memo
# ---------------------------

def build_credit_memo(borrower_name, metrics):
    md = []
    md.append(f"# Credit Proposal — {borrower_name}")
    md.append(f"**Date:** {datetime.today().date().isoformat()}")
    md.append("")
    md.append("## Open Finance Insights (6–12m)")
    md.append(f"- Average inflow: AED {metrics['avg_inflow']:,.0f}")
    md.append(f"- Average outflow: AED {metrics['avg_outflow']:,.0f}")
    md.append(f"- Net cash flow: AED {metrics['net_cashflow']:,.0f}")
    md.append(f"- Inflow volatility (std/mean): {metrics['inflow_volatility']:.2f}")
    md.append(f"- Bounced transactions (6m): {metrics['bounced_txn_6m']}")
    md.append("")
    md.append("## External Loans (Detected)")
    if metrics["loans_df"].empty:
        md.append("- None detected from transaction patterns.")
    else:
        for _, r in metrics["loans_df"].iterrows():
            md.append(f"- {r['lender']} — {r['product']} — EMI ~ AED {r['emi']:,.0f} — "
                      f"Outstanding est: {('AED ' + format(r['estimated_outstanding'], ',.0f')) if pd.notnull(r['estimated_outstanding']) else 'n/a'} "
                      f"({r['evidence']})")
    md.append("")
    md.append("## Eligibility & Policy")
    md.append(f"- Status: **{metrics['status']}**")
    if metrics["reasons"]:
        md.append("- Reasons:")
        for r in metrics["reasons"]:
            md.append(f"  - {r}")
    else:
        md.append("- All core checks passed.")
    md.append(f"- Eligible amount (term): AED {metrics['eligible_new']:,.0f}")
    md.append(f"- Policy cap (25% Tier 1): AED {metrics['policy_cap']:,.0f}")
    md.append("")
    md.append("## Recommendation (Demo)")
    if metrics["status"] == "Decline":
        md.append("- Decline at this time; consider deleveraging or reducing single-obligor exposure.")
    elif metrics["status"] == "Conditional":
        md.append("- Approve conditionally with covenants (min DSCR, balance maintenance), and review mitigants.")
    else:
        md.append("- Approve within proposed limits and standard covenants.")
    md.append("")
    md.append("---")
    md.append("*This demo memo was generated automatically from Open Finance signals and simple policy rules.*")
    return "\n".join(md)

# ---------------------------
# Main entry
# ---------------------------

def run_lending_assistant():
    st.title("📄 AI Lending Assistant (Open Finance + CBUAE Checklist)")
    st.caption("Automates corporate credit proposals using Open Finance signals and a rules-based checklist.")

    # Sidebar: policy knobs & firm-level params
    st.sidebar.header("Policy Thresholds")
    policies = {
        "min_dscr": st.sidebar.slider("Min DSCR (proxy)", 0.5, 3.0, 1.50, 0.05),
        "max_leverage": st.sidebar.slider("Max Leverage (Debt/EBITDA proxy)", 1.0, 6.0, 3.00, 0.1),
        "max_inflow_vol": st.sidebar.slider("Max Inflow Volatility (std/mean)", 0.0, 0.8, 0.20, 0.01),
        "max_bounced_txn_6m": st.sidebar.slider("Max Bounced Txns (6m)", 0, 6, 0, 1),
    }

    st.sidebar.header("Capacity & Exposure Params")
    tier1_capital = st.sidebar.number_input("Tier 1 Capital (AED)", min_value=1_000_000.0, value=1_000_000_000.0, step=10_000_000.0, format="%.0f")
    internal_utilized = st.sidebar.number_input("Internal Utilized Exposure (AED)", min_value=0.0, value=0.0, step=1_000_000.0, format="%.0f")
    apr = st.sidebar.slider("APR assumption (Term Loan)", 0.02, 0.30, 0.12, 0.01)
    tenor_months = st.sidebar.slider("Tenor (months)", 6, 60, 24, 1)

    # Load data
    tx, mb, acct, chk = load_all_data()
    tx = normalize_tx(tx)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Open Finance Snapshot", "Loan Eligibility", "CBUAE Checklist", "Credit Memo"])

    # --------------- Tab 1: Open Finance Snapshot ---------------
    with tab1:
        st.subheader("Open Finance Snapshot")
        if tx.empty:
            st.warning("No transactions found in /data/transactions.json")
        else:
            m = monthly_aggregates(tx).tail(6)  # use last 6 months if available
            avg_in = m["inflow"].mean() if not m.empty else 0.0
            avg_out = m["outflow"].mean() if not m.empty else 0.0
            inflow_vol = inflow_volatility(m)
            bounced = bounced_indicator(tx)
            st.metric("Avg Inflow (6m)", f"AED {int(avg_in):,}")
            st.metric("Avg Outflow (6m)", f"AED {int(avg_out):,}")
            st.metric("Net Cash Flow (6m avg)", f"AED {int(avg_in-avg_out):,}")
            st.metric("Inflow Volatility (std/mean)", f"{inflow_vol:.2f}")
            st.metric("Bounced Txns (6m, heuristic)", int(bounced))
            st.write("Monthly aggregates (last 6):")
            st.dataframe(m, use_container_width=True)

        st.markdown("#### Loans at Other Banks (Detected)")
        loans_df = detect_external_loans(tx)
        if loans_df.empty:
            st.info("No external loans detected via EMI/OD patterns.")
        else:
            st.dataframe(loans_df, use_container_width=True)

        # Expose for later tabs via session state
        st.session_state["monthly_df"] = m if not tx.empty else pd.DataFrame()
        st.session_state["avg_in"] = float(avg_in) if not tx.empty else 0.0
        st.session_state["avg_out"] = float(avg_out) if not tx.empty else 0.0
        st.session_state["inflow_vol"] = float(inflow_vol) if not tx.empty else 0.0
        st.session_state["bounced"] = int(bounced) if not tx.empty else 0
        st.session_state["loans_df"] = loans_df

    # --------------- Tab 2: Loan Eligibility ---------------
    with tab2:
        st.subheader("Loan Eligibility (Policy & Exposure)")

        avg_in = st.session_state.get("avg_in", 0.0)
        avg_out = st.session_state.get("avg_out", 0.0)
        inflow_vol = st.session_state.get("inflow_vol", 0.0)
        bounced = st.session_state.get("bounced", 0)
        loans_df = st.session_state.get("loans_df", pd.DataFrame())

        # External obligations: EMI sum & outstanding
        ext_outstanding = float(loans_df["estimated_outstanding"].fillna(0).sum()) if not loans_df.empty else 0.0
        ext_monthly_emi = float(loans_df["emi"].fillna(0).sum()) if not loans_df.empty else 0.0

        # Proxies & ratios
        ebitda_proxy = max(0.0, avg_in - avg_out)
        # If no EMI detected, use tiny denom to avoid inf; DSCR_proxy is meaningful only with obligations
        denom = max(1.0, ext_monthly_emi)  # monthly obligations proxy
        dscr_proxy = (ebitda_proxy / 12.0) / denom  # monthly DSCR proxy
        leverage_proxy = (ext_outstanding + internal_utilized) / max(1.0, ebitda_proxy)

        ratios = {
            "DSCR_proxy": dscr_proxy,
            "Leverage_proxy": leverage_proxy,
            "Inflow_volatility": inflow_vol
        }
        of_signals = {"bounced_txn_6m": bounced}

        # Capacity calcs
        term_cap, meta_term = eligible_term_cap_from_cashflows(avg_in, avg_out, target_dscr=policies["min_dscr"], apr=apr, tenor_months=tenor_months)
        wc_cap = wc_limit_from_flows(avg_in, inflow_vol)

        # Exposure to obligor = internal utilized + external outstanding (simplified)
        exposure_to_obligor = internal_utilized + ext_outstanding

        status, reasons, meta = compute_eligibility(
            ratios, of_signals, policies, tier1_capital, exposure_to_obligor, term_cap, wc_cap
        )

        eligible_new = max(0.0, meta["max_cap"] - exposure_to_obligor)

        # UI
        if status == "Eligible":
            st.success("Eligible")
        elif status == "Conditional":
            st.warning("Conditional – address the items below")
        else:
            st.error("Decline – key policy/exposure breach")

        st.write("**Reasons:**")
        if reasons:
            for r in reasons:
                st.write("- " + r)
        else:
            st.write("- All core checks passed")

        st.metric("Eligible Amount (AED)", f"{int(eligible_new):,}")
        st.caption(f"Term cap≈ {int(term_cap):,} | WC cap≈ {int(wc_cap):,} | Policy cap (25% Tier1)≈ {int(meta['policy_cap']):,}")
        st.caption(f"External outstanding≈ {int(ext_outstanding):,} | Internal utilized≈ {int(internal_utilized):,}")
        st.caption(f"Single obligor (demo): {meta['single_obligor_pct']:.1f}% of Tier 1")

        # Keep handy for next tabs
        st.session_state["elig_status"] = status
        st.session_state["elig_reasons"] = reasons
        st.session_state["eligible_new"] = eligible_new
        st.session_state["policy_cap"] = meta["policy_cap"]

    # --------------- Tab 3: CBUAE Checklist ---------------
    with tab3:
        st.subheader("Compliance Checklist (CBUAE)")
        chk = load_df_csv(DATA_DIR / "CBUAE_Corporate_Lending_Checklist.csv")
        if chk.empty:
            st.info("Place 'CBUAE_Corporate_Lending_Checklist.csv' in /data to enable this section.")
        else:
            completed = 0
            total = len(chk)
            # Auto checks from our metrics
            auto_map = {
                "uw.dscr_value": st.session_state.get("elig_status") != "Decline" and ratios["DSCR_proxy"] >= policies["min_dscr"],
                "exp.single_obligor_pct": st.session_state.get("elig_status") != "Decline" and st.session_state.get("policy_cap", 0) >= 0 and (st.session_state.get("eligible_new", 0) >= 0),
                # ltv pending until collateral added
                "ls.ltv_ratio": False,
            }
            for _, row in chk.iterrows():
                fid = str(row.get("System Field ID (suggested)", ""))
                auto_flag = auto_map.get(fid, None)
                label = f"{row['Section']} – {row['Control']}: {row['Requirement']}"
                default_value = bool(auto_flag) if auto_flag is not None else False
                value = st.checkbox(label, value=default_value, key=fid)
                st.caption(f"Evidence: {row['Evidence Examples']} • Owner: {row['Control Owner']} • Freq: {row['Frequency']}")
                if value: completed += 1
            st.success(f"Checklist completion: {completed}/{total}")

    # --------------- Tab 4: Credit Memo ---------------
    with tab4:
        st.subheader("Auto-Generated Credit Memo")
        avg_in = st.session_state.get("avg_in", 0.0)
        avg_out = st.session_state.get("avg_out", 0.0)
        inflow_vol = st.session_state.get("inflow_vol", 0.0)
        bounced = st.session_state.get("bounced", 0)
        loans_df = st.session_state.get("loans_df", pd.DataFrame())
        status = st.session_state.get("elig_status", "Eligible")
        reasons = st.session_state.get("elig_reasons", [])
        eligible_new = st.session_state.get("eligible_new", 0.0)
        policy_cap = st.session_state.get("policy_cap", 0.0)

        memo = build_credit_memo(
            borrower_name="Demo Corporate (UAE)",
            metrics={
                "avg_inflow": avg_in,
                "avg_outflow": avg_out,
                "net_cashflow": avg_in - avg_out,
                "inflow_volatility": inflow_vol,
                "bounced_txn_6m": bounced,
                "loans_df": loans_df,
                "status": status,
                "reasons": reasons,
                "eligible_new": eligible_new,
                "policy_cap": policy_cap,
            }
        )
        st.markdown(memo)
        st.download_button(
            "⬇️ Download Memo (.md)",
            data=memo.encode("utf-8"),
            file_name="credit_memo_demo.md",
            mime="text/markdown"
        )
