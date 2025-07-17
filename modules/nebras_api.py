import json

def get_account_summary():
    with open("data/account_summary.json") as f:
        return json.load(f)

def get_transactions():
    with open("data/transactions.json") as f:
        return json.load(f)
