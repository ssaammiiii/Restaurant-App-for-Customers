import json 
from datetime import datetime, timedelta 
 
def load_data(filename): 
    try: 
        with open(filename, 'r') as file: 
            data = json.load(file) 
    except FileNotFoundError: 
        data = {} 
    return data 
 
def save_data(data, filename): 
    with open(filename, 'w') as file: 
        json.dump(data, file) 
 
#getting the customer name  
def get_username(): 
    return input("Enter your name: ") 
 
#display menu function  
def display_menu(): 
    print("\nMenu:") 
    for key, value in menu.items(): 
        print(f"{key}. {value} - ${prices[key]}") 
 
#place order function with the time  
def place_order(username): 
    display_menu() 
    current_time = datetime.now() 
     
# Check if the user has a pending order within the last 12 hours 
    if username in orders: 
        last_order_time = datetime.strptime(orders[username][-1]["order_time"], "%Y-%m-%d %H:%M:%S") 
        if (current_time - last_order_time) < timedelta(hours=12): 
            print("You already have a pending order placed within the last 12 hours.") 
            confirm = input("Are you aware of this? (yes/no): ").lower() 
            if confirm != "yes": 
                return 
     
    choice = input("Enter item number to order (or 'done' to finish): ") 
    order = [] 
    while choice != 'done': 
        if choice in menu: 
            order.append(choice) 
        elif choice == 'cancel': 
            print("Order canceled.") 
            return 
        else: 
            print("Invalid item number.") 
        choice = input("Enter item number to order (or 'done' to finish): ") 
     
    if order: 
        order_time = current_time.strftime("%Y-%m-%d %H:%M:%S") 
        orders[username] = orders.get(username, []) + [{"items": order, "order_time": order_time}] 
        save_data(orders, 'orders.json') 
        print("\nOrder placed successfully!") 
 
  
#view order history function  
def view_order_history(): 
    username = get_username() 
    if username in orders: 
        if orders[username]: 
            print(f"\nOrder History for {username}:") 
            for index, order in enumerate(orders[username], start=1): 
                order_time = datetime.strptime(order['order_time'], "%Y-%m-%d %H:%M:%S") 
                current_time = datetime.now() 
                time_difference = current_time - order_time 
                if time_difference.total_seconds() < 1200:  # 20 minutes in seconds 
                    status = "Pending" 
                else: 
                    status = "Delivered" 
                items = [menu[item] for item in order['items']] 
                print(f"{index}. Items: {', '.join(items)}, Order Time: {order['order_time']} ({status})") 
        else: 
            print(f"No orders placed yet for {username}.") 
    else: 
        print(f"No orders found for {username}.") 
 
#calculate total price to be paid (the total price will be shown on the receipt) 
def calculate_total_price(order): 
    total_price = 0 
    for item in order['items']: 
        if item in prices: 
            total_price += prices[item] 
    return total_price 
 
#giving the table number to the user when showing the receipt  
def assign_table_number(username): 
    if username not in table_numbers: 
        table_numbers[username] = len(table_numbers) + 1 
    return table_numbers[username] 
 
def show_receipt(): 
    username = get_username() 
    if username in orders: 
        latest_order = orders[username][-1] 
        if latest_order: 
            print(f"Latest Order for {username}:") 
            items = [menu[item] for item in latest_order['items']] 
            print(f"Items: {', '.join(items)}") 
            total_price = calculate_total_price(latest_order) 
            print(f"Total Price: ${total_price}") 
        else: 
            print(f"No orders found for {username}.") 
    else: 
        print(f"No orders found for {username}.") 
 
#main menu with 6 options 
def main_menu(): 
    while True: 
        print("\n----- Welcome to Our Restaurant -----") 
        print("1. Display Menu") 
        print("2. Place Order") 
        print("3. View Order History") 
        print("4. Show Receipt") 
        print("5. Cancel Current Order") 
        print("6. Exit") 
        choice = input("Enter your choice: ") 
        if choice == '1': 
            display_menu() 
        elif choice == '2': 
            username = get_username() 
            place_order(username) 
        elif choice == '3': 
            view_order_history() 
        elif choice == '4': 
            show_receipt() 
        elif choice == '5': 
            username = get_username() 
            if username in orders: 
                del orders[username][-1]  # Delete the last order 
                save_data(orders, 'orders.json') 
                print("Current order canceled.") 
            else: 
                print("No orders found for this user.") 
        elif choice == '6': 
            print("Exiting...") 
            break 
        else: 
            print("Invalid choice! Please try again.") 
 
if __name__ == "__main__": 
    menu = { 
        "1": "Pasta", 
        "2": "Pizza", 
        "3": "Burger", 
        "4": "Salad", 
        "5": "Soup" 
    } 
    prices = { 
        "1": 10, 
        "2": 12, 
        "3": 8, 
        "4": 9, 
        "5": 6 
    } 
    orders = load_data('orders.json') 
    table_numbers = {} 
    main_menu()
