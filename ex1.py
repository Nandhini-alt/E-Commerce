from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
products_collection = db["products"]
orders_collection = db["orders"]


# Function to add a new product
def add_product(name, price, quantity):
    product = {
        "name": name,
        "price": price,
        "quantity": quantity
    }
    products_collection.insert_one(product)
    print("Product added successfully.")



# Function to update product quantity
def update_product_quantity(name, quantity_change):
    product = products_collection.find_one({"name": name})
    if product:
        new_quantity = product["quantity"] + quantity_change
        if new_quantity >= 0:
            products_collection.update_one({"name": name}, {"$set": {"quantity": new_quantity}})
            print("Product quantity updated successfully.")
        else:
            print("Error: Quantity cannot be negative.")
    else:
        print("Error: Product not found.")


# Function to get product details
def get_product_details(name):
    product = products_collection.find_one({"name": name})
    if product:
        print("Product Id:", product["id"])
        print("Product Name:", product["name"])
        print("Price:", product["price"])
        print("Quantity:", product["quantity"])
    else:
        print("Error: Product not found.")


# Function to place an order
def place_order(customer_name, product_name, quantity):
    product = products_collection.find_one({"name": product_name})
    if product:
        if product["quantity"] >= quantity:
            order = {
                "customer_name": customer_name,
                "product_name": product_name,
                "quantity": quantity
            }
            orders_collection.insert_one(order)
            new_quantity = product["quantity"] - quantity
            products_collection.update_one({"name": product_name}, {"$set": {"quantity": new_quantity}})
            print("Order placed successfully.")
        else:
            print("Error: Ordered quantity is more than available quantity.")
    else:
        print("Error: Product not found.")


# Function to generate sales report
def generate_sales_report():
    pipeline = [
        {"$group": {"_id": "$product_name", "total_sales": {"$sum": "$quantity"}}}
    ]
    sales_report = orders_collection.aggregate(pipeline)
    print("Sales Report:")
    for item in sales_report:
        print("Product:", item["_id"])
        print("Total Sales:", item["total_sales"])
        print()


# Menu-driven program
while True:
    print("-----------------------------------------------")
    print("****** Inventory Management System ******")
    print("-----------------------------------------------")
    print("1. Add Product")
    print("2. Update Product Quantity")
    print("3. Get Product Details")
    print("4. Place Order")
    print("5. Generate Sales Report")
    print("6. Exit")
    print()

    choice = input("Enter your choice(1-6): ")

    if choice == "1":
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))
        add_product(name, price, quantity)

    elif choice == "2":
        name = input("Enter product name: ")
        quantity_change = int(input("Enter quantity change (+/-): "))
        update_product_quantity(name, quantity_change)

    elif choice == "3":
        name = input("Enter product name: ")
        get_product_details(name)

    elif choice == "4":
        customer_name = input("Enter customer name: ")
        product_name = input("Enter product name: ")
        quantity = int(input("Enter quantity: "))
        place_order(customer_name, product_name, quantity)

    elif choice == "5":
        generate_sales_report()

    elif choice == "6":
        print("Exiting...")
        break

    else:
        print("Invalid choice. Please try again.")
