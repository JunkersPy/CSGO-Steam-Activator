Steam Account CS2 Adder
This script automates the process of adding Counter-Strike 2 (CS2) to multiple Steam accounts. It logs into each account and attempts to add CS2 to the account's library using the steam.webauth module.

The script performs the following tasks:

Loads a list of accounts from output.json.
Loads a list of accounts that already have CS2 added from verified_accounts.json.
Shuffles the accounts list randomly.
Iterates through each account:
Skips the account if CS2 is already added.
Attempts to log in using the account's credentials.
If successful, sends a POST request to add CS2 to the account.
Checks the response to determine if the game was successfully added.
If added, the account's username is saved to the verified_accounts.json file.
After adding CS2 to every two accounts, the script pauses and asks the user if they want to continue.
Waits for 8 seconds before moving on to the next account to avoid rapid requests.

Prerequisites
Ensure you have the required libraries installed:
pip install steam
