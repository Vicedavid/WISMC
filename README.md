# WISMC

This repository contains a simple command line based Warehouse Inventory System.

## Usage

The main script is `inventory.py`. It stores all data in `inventory.json` in the
same directory. Run the script with Python 3 and one of the subcommands below.

```
python3 inventory.py add-location LOCATION
python3 inventory.py add-item ITEM_NAME QUANTITY LOCATION
python3 inventory.py issue ITEM_NAME QUANTITY USER LOCATION
python3 inventory.py receive ITEM_NAME QUANTITY USER LOCATION
python3 inventory.py show
```

Locations are arbitrary strings that can represent nested paths (e.g.
`Warehouse1/ShelfA/Bin3`). Items are tracked per location and overall totals are
updated when issuing or receiving gear.
