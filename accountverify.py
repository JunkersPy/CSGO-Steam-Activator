import json
import os
import random
import steam.webauth as wa
from getpass import getpass
from pprint import pprint
import time

def load_json_file(file_path, default_value=[]):
    """Loads a JSON file, if it doesn't exist, creates it with a default value."""
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump(default_value, file)
    with open(file_path, "r") as file:
        return json.load(file)

def save_json_file(file_path, data):
    """Saves data to a JSON file."""
    with open(file_path, "w") as file:
        json.dump(data, file)

def verify_account(account, verified_accounts):
    """Verify a single Steam account."""
    user = wa.WebAuth(account["username"], account["password"])
    try:
        sess = user.login()
        if sess is None:
            raise ValueError("Failed to log in")

        idcookie = sess.cookies.get_dict(domain="steamcommunity.com").get("sessionid")
        if not idcookie:
            raise ValueError("sessionid cookie not found")

        resp = sess.post("https://store.steampowered.com/checkout/addfreelicense/303386", data={"sessionid": idcookie})
        if resp is not None and "<h2>Success!</h2>" in resp.text:
            print(f"Verified: {account['username']}, {account['password']}")
            verified_accounts.add(account['username'])
        else:
            print("Account verification failed")

    except Exception as e:
        print(f'Error for account {account["username"]}: {e}')

def main():
    accounts_file = "output.json"
    verified_accounts_file = "verified_accounts.json"

    accounts = load_json_file(accounts_file)
    verified_accounts = set(load_json_file(verified_accounts_file))

    random.shuffle(accounts)

    for i, account in enumerate(accounts, 1):
        if account['username'] in verified_accounts:
            print(f"Account {account['username']} already verified. Skipping...")
            continue

        verify_account(account, verified_accounts)

        if i % 2 == 0:
            user_input = input("Continue? (y/n): ")
            if user_input.lower() != "y":
                break

        time.sleep(8)

    save_json_file(verified_accounts_file, list(verified_accounts))

if __name__ == "__main__":
    main()
