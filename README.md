# Inventory & Supply Chain Tracker with Alerts

A Python-based inventory management system that tracks stock levels, logs
stock-in/stock-out transactions, flags items that fall below their reorder
threshold, and generates summary reports — conceptually similar to core
ideas behind enterprise Materials Management (MM) systems.

## Features
- **Item management**: Add items with quantity, reorder level, and unit price.
- **Stock transactions**: Record stock-in (purchases/returns) and stock-out
  (issues/sales) with quantity validation (can't remove more than available).
- **Low-stock alerts**: Automatically flags items at or below their reorder
  level after every transaction.
- **Reporting**: Generate a full inventory summary (with total stock value)
  and a dedicated low-stock alert report.
- **Persistence**: Exports current inventory and full transaction history to
  CSV files for record-keeping or further analysis (e.g., in Excel).

## Why this project
Stock/inventory tracking with reorder alerts is a foundational concept in
supply chain and ERP systems (such as SAP's Materials Management module).
This project recreates that logic in a simplified, dependency-free way,
useful as a talking point for understanding business processes even without
direct SAP experience.

## How to run
```bash
python inventory_tracker.py
```

This runs a demo: adds three items, performs several stock-in/stock-out
transactions (including one that triggers a low-stock alert), then prints
an inventory summary and a low-stock report. Data is saved to
`inventory.csv` and `transactions.csv`.

## Tech used
- Python 3
- Standard library only (`csv`, `datetime`) — no external dependencies

## Possible extensions
- Add a command-line menu for interactive item/transaction entry
- Integrate `matplotlib` to chart stock levels over time
- Add supplier information and automatic reorder request generation
- Build a simple Flask/Streamlit dashboard for visualization
