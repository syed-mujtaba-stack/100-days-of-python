import tkinter as tk
from tkinter import messagebox

# Dictionary to store bids
bids = {}

# Function to submit a bid
def submit_bid():
    name = name_entry.get()
    bid = bid_entry.get()

    if name == "" or bid == "":
        messagebox.showwarning("Warning", "Please enter both name and bid.")
        return

    try:
        bid = int(bid)
    except ValueError:
        messagebox.showerror("Error", "Bid must be a number.")
        return

    bids[name] = bid
    name_entry.delete(0, tk.END)
    bid_entry.delete(0, tk.END)
    messagebox.showinfo("Success", f"Bid placed by {name} for ${bid}!")

# Function to find and show the winner
def show_winner():
    if not bids:
        messagebox.showinfo("Info", "No bids placed yet.")
        return

    highest_bid = 0
    winner = ""
    for bidder in bids:
        if bids[bidder] > highest_bid:
            highest_bid = bids[bidder]
            winner = bidder

    messagebox.showinfo("Winner", f"The winner is {winner} with a bid of ${highest_bid}.")

# Setup GUI
window = tk.Tk()
window.title("Secret Auction App")
window.geometry("400x300")
window.config(bg="#f5f5f5")

title = tk.Label(window, text="Secret Auction", font=("Arial", 20, "bold"), bg="#f5f5f5")
title.pack(pady=10)

name_label = tk.Label(window, text="Name:", font=("Arial", 12), bg="#f5f5f5")
name_label.pack()
name_entry = tk.Entry(window, font=("Arial", 12))
name_entry.pack()

bid_label = tk.Label(window, text="Bid Amount ($):", font=("Arial", 12), bg="#f5f5f5")
bid_label.pack()
bid_entry = tk.Entry(window, font=("Arial", 12))
bid_entry.pack()

submit_button = tk.Button(window, text="Submit Bid", font=("Arial", 12), command=submit_bid, bg="#4CAF50", fg="white")
submit_button.pack(pady=10)

winner_button = tk.Button(window, text="Show Winner", font=("Arial", 12), command=show_winner, bg="#2196F3", fg="white")
winner_button.pack()

window.mainloop()
