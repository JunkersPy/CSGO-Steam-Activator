import json
import os
import random
import steam.webauth as wa
from getpass import getpass
from pprint import pprint
import time

# Load accounts from output.json
if not os.path.exists("output.json"):
    with open("output.json", "w") as file:
        json.dump([], file)

with open("output.json", "r") as file:
    accounts = json.load(file)

# Check if the verified_accounts.json file exists, if not create and initialize it with an empty list
if not os.path.exists("verified_accounts.json"):
    with open("verified_accounts.json", "w") as file:
        json.dump([], file)

# Load verified accounts from verified_accounts.json
with open("verified_accounts.json", "r") as file:
    verified_accounts = json.load(file)

# Shuffle the accounts randomly
random.shuffle(accounts)

for i, account in enumerate(accounts, 1):
    print(account["username"])
    
    # Check if account is already verified
    if account['username'] in verified_accounts:
        print(f"Account {account['username']} already verified. Skipping...")
        continue
    
    user = wa.WebAuth(account["username"], account["password"])
    try:
        sess = user.login()
    except Exception as e:
        print(f'Error: {e}')
        continue

    if sess is None:
        print("Error: Failed to log in")
        continue

    idcookie = sess.cookies.get_dict(domain="steamcommunity.com")["sessionid"]
    if idcookie is None or idcookie == "":
        print("Error: sessionid cookie not found")
        continue

    resp = sess.post("https://store.steampowered.com/checkout/addfreelicense/303386", data={
        "sessionid": idcookie
    })
    print(resp.status_code)
    print(resp.text)

    # Check if the verification was successful (adjust the condition based on your needs)
    if resp is not None and "<h2>Success!</h2>" in resp.text:
        # Do whatever you need to do with the verified account
        # For example, you can print the username and password
        print(f"Verified: {account['username']}, {account['password']}")
        # Add the verified username to the list
        verified_accounts.append(account['username'])
        with open("verified_accounts.json", "w") as file:
            json.dump(verified_accounts, file)
    else:
        # Account verification failed
        print("Account verification failed")

    # Pause every 2 accounts and ask for user input to continue
    if i % 2 == 0:
        user_input = input("Continue? (y/n): ")
        if user_input.lower() != "y":
            break

    # Pause for 8 seconds before verifying the next account
    time.sleep(8)