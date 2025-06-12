import os

# Function to find highest bidder
def find_highest_bidder(bidding_record):
    highest_bid = 0
    winner = ""
    for bidder in bidding_record:
        bid_amount = bidding_record[bidder]
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            winner = bidder
    print(f"The winner is {winner} with a bid of ${highest_bid}.")

# Dictionary to store bids
bids = {}
bidding_finished = False

while not bidding_finished:
    print("Welcome to the secret auction program!")
    name = input("What is your name?: ")
    price = int(input("What's your bid?: $"))
    bids[name] = price
    should_continue = input("Are there any other bidders? Type 'yes' or 'no': ").lower()
    if should_continue == "no":
        bidding_finished = True
        find_highest_bidder(bids)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clears the screen for privacy
