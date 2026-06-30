"""
Inventory & Supply Chain Tracker with Alerts
---------------------------------------------
Tracks stock levels for items, records stock-in/stock-out transactions,
flags low-inventory items, and generates summary reports.

Conceptually mirrors core ideas behind enterprise Materials Management (MM)
modules — stock tracking, reorder alerts, and transaction history — without
requiring any specific ERP platform.

Concepts demonstrated:
- Object-Oriented Programming (classes, encapsulation)
- CSV-based persistence (simulating data export/import)
- Business logic for threshold-based alerts
- Transaction logging
"""

import csv
import os
from datetime import datetime


class Item:
    def __init__(self, item_id, name, quantity, reorder_level, unit_price):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level
        self.unit_price = unit_price

    def is_low_stock(self):
        return self.quantity <= self.reorder_level

    def stock_value(self):
        return round(self.quantity * self.unit_price, 2)

    def to_row(self):
        return [self.item_id, self.name, self.quantity, self.reorder_level, self.unit_price]


class Transaction:
    def __init__(self, item_id, change, txn_type, remarks=""):
        self.timestamp = datetime.now().isoformat(timespec="seconds")
        self.item_id = item_id
        self.change = change
        self.txn_type = txn_type  # "IN" or "OUT"
        self.remarks = remarks

    def to_row(self):
        return [self.timestamp, self.item_id, self.txn_type, self.change, self.remarks]


class InventoryTracker:
    def __init__(self, inventory_file="inventory.csv", log_file="transactions.csv"):
        self.items = {}
        self.transactions = []
        self.inventory_file = inventory_file
        self.log_file = log_file

    # ---------- Item Management ----------
    def add_item(self, item_id, name, quantity, reorder_level, unit_price):
        item = Item(item_id, name, quantity, reorder_level, unit_price)
        self.items[item_id] = item
        print(f"Added item: {name} (Qty: {quantity})")
        return item

    # ---------- Stock Transactions ----------
    def stock_in(self, item_id, quantity, remarks=""):
        item = self.items.get(item_id)
        if not item:
            print(f"Item ID {item_id} not found.")
            return
        item.quantity += quantity
        self.transactions.append(Transaction(item_id, quantity, "IN", remarks))
        print(f"Stocked IN {quantity} units of {item.name}. New quantity: {item.quantity}")
        self._check_alert(item)

    def stock_out(self, item_id, quantity, remarks=""):
        item = self.items.get(item_id)
        if not item:
            print(f"Item ID {item_id} not found.")
            return
        if quantity > item.quantity:
            print(f"Cannot remove {quantity} units — only {item.quantity} in stock.")
            return
        item.quantity -= quantity
        self.transactions.append(Transaction(item_id, -quantity, "OUT", remarks))
        print(f"Stocked OUT {quantity} units of {item.name}. New quantity: {item.quantity}")
        self._check_alert(item)

    def _check_alert(self, item: Item):
        if item.is_low_stock():
            print(f"  ALERT: '{item.name}' is at or below reorder level "
                  f"({item.quantity} <= {item.reorder_level})")

    # ---------- Reporting ----------
    def low_stock_report(self):
        print("\n--- Low Stock Alert Report ---")
        low_items = [i for i in self.items.values() if i.is_low_stock()]
        if not low_items:
            print("No items currently below reorder level.")
        for item in low_items:
            print(f"{item.name}: {item.quantity} units (Reorder level: {item.reorder_level})")
        print()

    def inventory_summary(self):
        print("\n--- Inventory Summary ---")
        total_value = 0
        for item in self.items.values():
            print(f"{item.name}: {item.quantity} units @ ₹{item.unit_price} "
                  f"= ₹{item.stock_value()}")
            total_value += item.stock_value()
        print(f"Total Inventory Value: ₹{round(total_value, 2)}\n")

    # ---------- Persistence ----------
    def save_inventory(self):
        with open(self.inventory_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["item_id", "name", "quantity", "reorder_level", "unit_price"])
            for item in self.items.values():
                writer.writerow(item.to_row())
        print(f"Inventory saved to {self.inventory_file}")

    def save_transactions(self):
        with open(self.log_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "item_id", "type", "change", "remarks"])
            for txn in self.transactions:
                writer.writerow(txn.to_row())
        print(f"Transaction log saved to {self.log_file}")


def demo():
    tracker = InventoryTracker()

    # Add items
    tracker.add_item(1, "Laptop", quantity=20, reorder_level=5, unit_price=55000)
    tracker.add_item(2, "Wireless Mouse", quantity=8, reorder_level=10, unit_price=600)
    tracker.add_item(3, "Office Chair", quantity=15, reorder_level=3, unit_price=4500)

    # Simulate transactions
    tracker.stock_out(1, 3, remarks="Issued to new hires")
    tracker.stock_out(2, 2, remarks="Issued to dev team")  # triggers low stock alert
    tracker.stock_in(3, 10, remarks="New office furniture order received")
    tracker.stock_out(2, 1)  # further depletes already-low item

    # Reports
    tracker.inventory_summary()
    tracker.low_stock_report()

    # Save data
    tracker.save_inventory()
    tracker.save_transactions()


if __name__ == "__main__":
    demo()
