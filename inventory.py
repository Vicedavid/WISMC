import argparse
import json
import os
import datetime

DATA_FILE = 'inventory.json'


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"locations": [], "items": {}, "transactions": []}


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_location(args):
    data = load_data()
    if args.path not in data['locations']:
        data['locations'].append(args.path)
        print(f"Location {args.path} added.")
    else:
        print(f"Location {args.path} already exists.")
    save_data(data)


def add_item(args):
    data = load_data()
    if args.location not in data['locations']:
        print(f"Location {args.location} does not exist.")
        return
    item = data['items'].setdefault(args.name, {"total": 0, "locations": {}})
    item['locations'][args.location] = item['locations'].get(args.location, 0) + args.quantity
    item['total'] += args.quantity
    save_data(data)
    print(f"Added {args.quantity} {args.name} to {args.location}.")


def issue_item(args):
    data = load_data()
    item = data['items'].get(args.name)
    if not item:
        print(f"Item {args.name} not found.")
        return
    if args.location not in item['locations']:
        print(f"Item {args.name} not in {args.location}.")
        return
    if item['locations'][args.location] < args.quantity:
        print(f"Not enough {args.name} in {args.location}.")
        return
    item['locations'][args.location] -= args.quantity
    item['total'] -= args.quantity
    data['transactions'].append({
        "type": "issue",
        "item": args.name,
        "quantity": args.quantity,
        "user": args.user,
        "location": args.location,
        "date": datetime.datetime.now().isoformat()
    })
    save_data(data)
    print(f"Issued {args.quantity} {args.name} to {args.user} from {args.location}.")


def receive_item(args):
    data = load_data()
    if args.location not in data['locations']:
        print(f"Location {args.location} does not exist.")
        return
    item = data['items'].setdefault(args.name, {"total": 0, "locations": {}})
    item['locations'][args.location] = item['locations'].get(args.location, 0) + args.quantity
    item['total'] += args.quantity
    data['transactions'].append({
        "type": "receive",
        "item": args.name,
        "quantity": args.quantity,
        "user": args.user,
        "location": args.location,
        "date": datetime.datetime.now().isoformat()
    })
    save_data(data)
    print(f"Received {args.quantity} {args.name} from {args.user} into {args.location}.")


def show_inventory(args):
    data = load_data()
    print("Locations:")
    for loc in data['locations']:
        print(f"- {loc}")
    print("\nItems:")
    for name, item in data['items'].items():
        print(f"{name} (Total: {item['total']})")
        for loc, qty in item['locations'].items():
            print(f"  {loc}: {qty}")


def main():
    parser = argparse.ArgumentParser(description="Simple Warehouse Inventory System")
    subparsers = parser.add_subparsers(dest='command')

    sp = subparsers.add_parser('add-location', help='Add a location')
    sp.add_argument('path')
    sp.set_defaults(func=add_location)

    sp = subparsers.add_parser('add-item', help='Add item to location')
    sp.add_argument('name')
    sp.add_argument('quantity', type=int)
    sp.add_argument('location')
    sp.set_defaults(func=add_item)

    sp = subparsers.add_parser('issue', help='Issue item to user')
    sp.add_argument('name')
    sp.add_argument('quantity', type=int)
    sp.add_argument('user')
    sp.add_argument('location')
    sp.set_defaults(func=issue_item)

    sp = subparsers.add_parser('receive', help='Receive item from user')
    sp.add_argument('name')
    sp.add_argument('quantity', type=int)
    sp.add_argument('user')
    sp.add_argument('location')
    sp.set_defaults(func=receive_item)

    sp = subparsers.add_parser('show', help='Show inventory')
    sp.set_defaults(func=show_inventory)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
