
# ==========================================
# ONLINE FOOD ORDERING SYSTEM
# Based on the 7 UML Classes
# ==========================================

# 1. DELIVERY CLASS
class Delivery:

    def __init__(self, id, name, date, address):
        self.id = id
        self.name = name
        self.date = date
        self.address = address
        self.delivery_status = "Preparing"

    def update(self, status=None):
        if status:
            self.delivery_status = status

        print("\n--- DELIVERY DETAILS ---")
        print("Delivery ID:", self.id)
        print("Customer Name:", self.name)
        print("Date:", self.date)
        print("Address:", self.address)
        print("Delivery Status:", self.delivery_status)


# 2. PAYMENT CLASS
class Payment:

    def __init__(self, payment_id, payment_method, amount):
        self.payment_id = payment_id
        self.payment_method = payment_method
        self.amount = amount
        self.payment_status = "Pending"

    def process_payment(self):
        print("\n--- PAYMENT PROCESSING ---")
        print("Payment Method:", self.payment_method)
        print("Amount: Rs.", self.amount)

        if self.payment_method.lower() == "cash":
            self.payment_status = "Cash on Delivery"
        else:
            self.payment_status = "Successful"

        self.confirm_payment()

    def confirm_payment(self):
        print("Payment Status:", self.payment_status)


# 3. ORDER CLASS
class Order:

    def __init__(self, order_id, order_date, total_amt):
        self.order_id = order_id
        self.order_date = order_date
        self.total_amt = total_amt

        # Additional objects connected to Order
        self.dishes = []
        self.payment = None
        self.delivery = None
        self.status = "Order Placed"

    def createOrder(self):
        print("\nOrder Created Successfully!")
        print("Order ID:", self.order_id)
        print("Order Date:", self.order_date)

        print("\nOrdered Items:")
        for dish in self.dishes:
            print(dish.names, "- Rs.", dish.price)

        print("Total Amount: Rs.", self.total_amt)

    def cancel_order(self):
        if self.status == "Delivered":
            print("Delivered orders cannot be cancelled.")
            return

        if self.status == "Cancelled":
            print("Order is already cancelled.")
            return

        self.status = "Cancelled"

        if self.delivery:
            self.delivery.update("Cancelled")

        print("\nOrder Cancelled Successfully!")

    def track_order(self):
        print("\n--- ORDER TRACKING ---")
        print("Order ID:", self.order_id)
        print("Order Status:", self.status)

        if self.payment:
            print("Payment Status:", self.payment.payment_status)

        if self.delivery:
            self.delivery.update()


# 4. CUSTOMER CLASS
class Customer:

    def __init__(self, address, name, email, phone):
        self.address = address
        self.name = name
        self.email = email
        self.phone = phone
        self.orders = []
        self.is_logged_in = False

    def register(self):
        print("\nCustomer Registered Successfully!")
        print("Name:", self.name)
        print("Email:", self.email)

    def login(self):
        self.is_logged_in = True
        print("\nWelcome,", self.name)
        print("Login Successful!")

    def view_menu(self, menu):
        menu.display_menu()

    def place_order(self, menu, order_id, food_ids,
                    payment_method, date):

        if not self.is_logged_in:
            print("Please login before placing an order.")
            return

        selected_dishes = []

        # Search and select dishes
        for food_id in food_ids:
            dish = menu.search_food(food_id)

            if dish is not None:
                selected_dishes.append(dish)
            else:
                print("Food ID", food_id, "not found.")

        if not selected_dishes:
            print("No valid food items selected.")
            return

        # Calculate total amount
        total = sum(dish.price for dish in selected_dishes)

        # Create Order
        order = Order(order_id, date, total)
        order.dishes = selected_dishes

        # Create Payment
        payment = Payment(order_id, payment_method, total)
        order.payment = payment

        # Process Payment
        payment.process_payment()

        # Create Delivery
        delivery = Delivery(
            order_id,
            self.name,
            date,
            self.address
        )

        order.delivery = delivery

        # Save Order
        self.orders.append(order)

        # Display Order Details
        order.createOrder()
        delivery.update()

        print("\nThank you for ordering!")


# 5. ADMIN CLASS
class Admin:

    def __init__(self, id, name, age, concatnum,
                 username, password):

        self.id = id
        self.name = name
        self.age = age
        self.concatnum = concatnum
        self.username = username
        self.password = password

    def create(self, menu, dish):
        menu.fooditemlist.append(dish)
        print("\nFood Item Added Successfully!")

    def update(self, menu, food_id, new_price):

        dish = menu.search_food(food_id)

        if dish is not None:
            dish.price = new_price
            print("\nFood Price Updated Successfully!")
        else:
            print("\nFood Item Not Found!")

        print("Admin:", self.name)


# 6. DISH CLASS
class Dish:

    def __init__(self, food_id, names, price, category):
        self.food_id = food_id
        self.names = names
        self.price = price
        self.category = category

    def display_details(self):
        print("\n--- FOOD DETAILS ---")
        print("Food ID:", self.food_id)
        print("Name:", self.names)
        print("Price: Rs.", self.price)
        print("Category:", self.category)


# 7. MENU CLASS
class Menu:

    def __init__(self, menu_id):
        self.menu_id = menu_id
        self.fooditemlist = []

    def display_menu(self):

        print("\n========== FOOD MENU ==========")
        print("ID\tFood\t\tPrice\tCategory")
        print("--------------------------------")

        for dish in self.fooditemlist:
            print(
                dish.food_id, "\t",
                dish.names, "\t",
                dish.price, "\t",
                dish.category
            )

        print("--------------------------------")

    def search_food(self, food_id):

        for dish in self.fooditemlist:
            if dish.food_id == food_id:
                return dish

        return None


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    from datetime import date

    # Create Menu
    menu = Menu(101)

    # Add Initial Food Items
    menu.fooditemlist = [
        Dish(1, "Pizza", 200, "Fast Food"),
        Dish(2, "Burger", 120, "Fast Food"),
        Dish(3, "Dosa", 60, "South Indian"),
        Dish(4, "Biryani", 180, "Main Course"),
        Dish(5, "IceCream", 80, "Dessert")
    ]

    # Create Admin
    admin = Admin(
        1, "Admin", 30, "9876543210",
        "admin", "1234"
    )

    # Create Customer
    customer = Customer(
        "Bangalore",
        "Rahul",
        "rahul@gmail.com",
        "9876543210"
    )

    # Generate unique order IDs during this run
    next_order_id = 1001

    # Main Menu
    while True:

        print("\n================================")
        print("     ONLINE FOOD ORDERING SYSTEM")
        print("================================")
        print("1. Customer Registration")
        print("2. Customer Login")
        print("3. View Food Menu")
        print("4. Search Food")
        print("5. Place Order")
        print("6. Track Order")
        print("7. Cancel Order")
        print("8. Update Delivery Status")
        print("9. Admin - Add Food")
        print("10. Admin - Update Food Price")
        print("11. Admin Details")
        print("12. Exit")

        choice = input("\nEnter your choice: ").strip()

        try:

            if choice == "1":
                customer.register()

            elif choice == "2":
                customer.login()

            elif choice == "3":
                customer.view_menu(menu)

            elif choice == "4":

                food_id = int(input("Enter Food ID: "))
                dish = menu.search_food(food_id)

                if dish:
                    dish.display_details()
                else:
                    print("Food Item Not Found!")

            elif choice == "5":

                if not customer.is_logged_in:
                    print("Please login first.")
                    continue

                menu.display_menu()

                food_ids = list(map(
                    int,
                    input(
                        "Enter Food IDs separated by spaces: "
                    ).split()
                ))

                print("\nPayment Methods")
                print("1. UPI")
                print("2. Card")
                print("3. Cash on Delivery")

                payment_choice = input(
                    "Select Payment Method: "
                ).strip()

                methods = {
                    "1": "UPI",
                    "2": "Card",
                    "3": "Cash"
                }

                if payment_choice not in methods:
                    print("Invalid Payment Method!")
                    continue

                customer.place_order(
                    menu,
                    next_order_id,
                    food_ids,
                    methods[payment_choice],
                    str(date.today())
                )

                # Increase ID only after a successful order
                if (customer.orders and
                    customer.orders[-1].order_id == next_order_id):
                    next_order_id += 1

            elif choice == "6":

                if customer.orders:
                    customer.orders[-1].track_order()
                else:
                    print("No Orders Found!")

            elif choice == "7":

                if customer.orders:
                    customer.orders[-1].cancel_order()
                else:
                    print("No Orders to Cancel!")

            elif choice == "8":

                if customer.orders:
                    order = customer.orders[-1]

                    if order.delivery and order.status != "Cancelled":

                        print("\n1. Preparing")
                        print("2. Out for Delivery")
                        print("3. Delivered")

                        status_choice = input(
                            "Select New Status: "
                        ).strip()

                        statuses = {
                            "1": "Preparing",
                            "2": "Out for Delivery",
                            "3": "Delivered"
                        }

                        if status_choice in statuses:
                            new_status = statuses[status_choice]
                            order.delivery.update(new_status)
                            order.status = new_status
                        else:
                            print("Invalid Status!")

                    else:
                        print("No active delivery found.")

                else:
                    print("No Orders Found!")

            elif choice == "9":

                print("\n--- ADD NEW FOOD ---")

                food_id = int(input("Enter Food ID: "))
                name = input("Enter Food Name: ")
                price = float(input("Enter Price: Rs. "))
                category = input("Enter Category: ")

                if menu.search_food(food_id):
                    print("Food ID already exists!")
                elif price < 0:
                    print("Price cannot be negative!")
                else:
                    dish = Dish(food_id, name, price, category)
                    admin.create(menu, dish)

            elif choice == "10":

                food_id = int(input("Enter Food ID: "))
                new_price = float(input("Enter New Price: Rs. "))

                if new_price < 0:
                    print("Price cannot be negative!")
                else:
                    admin.update(menu, food_id, new_price)

            elif choice == "11":
                print("\n--- ADMIN DETAILS ---")
                print("ID:", admin.id)
                print("Name:", admin.name)
                print("Age:", admin.age)
                print("Contact:", admin.concatnum)

            elif choice == "12":
                print("\nThank you for using our system!")
                break

            else:
                print("Invalid Choice! Please Try Again.")

        except ValueError:
            print("Invalid Input! Please enter the correct value.")
