from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

# ===================== DATA MODELS =====================

# Model for placing an order with validation rules


class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = "delivery"   # delivery or pickup


# Model for adding new menu items
class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True


# Model for checkout process
class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=10)


# ===================== DATA STORAGE =====================

# Sample menu data
menu = [
    {"id": 1, "name": "Margherita Pizza", "price": 299,
        "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Veg Burger", "price": 149,
        "category": "Burger", "is_available": True},
    {"id": 3, "name": "Cold Coffee", "price": 99,
        "category": "Drink", "is_available": True},
    {"id": 4, "name": "Chocolate Cake", "price": 199,
        "category": "Dessert", "is_available": False},
    {"id": 5, "name": "Paneer Pizza", "price": 349,
        "category": "Pizza", "is_available": True},
    {"id": 6, "name": "French Fries", "price": 129,
        "category": "Snack", "is_available": True},
]

# Stores all placed orders
orders = []

# Auto-increment order ID
order_counter = 1

# Temporary cart storage
cart = []


# ===================== HELPER FUNCTIONS =====================

# Find a menu item by its ID
def find_menu_item(item_id: int):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None


# Calculate total price with optional delivery charge
def calculate_bill(price: int, quantity: int, order_type: str):
    total = price * quantity
    if order_type == "delivery":
        total += 30  # delivery charge
    return total


# Filter menu based on category, price, and availability
def filter_menu_logic(category=None, max_price=None, is_available=None):
    result = menu
    if category is not None:
        result = [i for i in result if i["category"] == category]
    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]
    if is_available is not None:
        result = [i for i in result if i["is_available"] == is_available]
    return result


# ===================== BASIC ROUTES =====================

# Home route
@app.get("/")
def home():
    return {"message": "Welcome to QuickBite Food Delivery"}


# Get all menu items
@app.get("/menu")
def get_menu():
    return {"menu": menu, "total": len(menu)}


# Get summary of menu (available, unavailable, categories)
@app.get("/menu/summary")
def menu_summary():
    available = [i for i in menu if i["is_available"]]
    unavailable = [i for i in menu if not i["is_available"]]
    categories = list(set(i["category"] for i in menu))

    return {
        "total_items": len(menu),
        "available": len(available),
        "unavailable": len(unavailable),
        "categories": categories
    }


# Filter menu items using query parameters
@app.get("/menu/filter")
def filter_menu(
    category: str = Query(None),
    max_price: int = Query(None),
    is_available: bool = Query(None)
):
    result = filter_menu_logic(category, max_price, is_available)
    return {"items": result, "count": len(result)}


# ===================== ORDER MANAGEMENT =====================

# Get all orders
@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}


# Search orders by customer name
@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    results = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not results:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(results),
        "orders": results
    }


# Place a new order
@app.post("/orders")
def place_order(order_data: OrderRequest):
    global order_counter

    item = find_menu_item(order_data.item_id)
    if not item:
        return {"error": "Item not found"}

    if not item["is_available"]:
        return {"error": "Item not available"}

    total = calculate_bill(
        item["price"], order_data.quantity, order_data.order_type)

    order = {
        "order_id": order_counter,
        "customer_name": order_data.customer_name,
        "item": item["name"],
        "quantity": order_data.quantity,
        "delivery_address": order_data.delivery_address,
        "order_type": order_data.order_type,
        "total_price": total
    }

    orders.append(order)
    order_counter += 1

    return {"message": "Order placed", "order": order}


# ===================== MENU CRUD =====================

# Add a new menu item
@app.post("/menu")
def add_item(new_item: NewMenuItem, response: Response):
    names = [i["name"].lower() for i in menu]
    if new_item.name.lower() in names:
        response.status_code = 400
        return {"error": "Item already exists"}

    new_id = max(i["id"] for i in menu) + 1

    item = {
        "id": new_id,
        "name": new_item.name,
        "price": new_item.price,
        "category": new_item.category,
        "is_available": new_item.is_available
    }

    menu.append(item)
    response.status_code = 201
    return {"item": item}


# Update price or availability of a menu item
@app.put("/menu/{item_id}")
def update_item(item_id: int, price: int = None, is_available: bool = None):
    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}

    if price is not None:
        item["price"] = price
    if is_available is not None:
        item["is_available"] = is_available

    return {"updated": item}


# Delete a menu item
@app.delete("/menu/{item_id}")
def delete_item(item_id: int):
    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}

    menu.remove(item)
    return {"message": f"{item['name']} deleted"}


# ===================== CART SYSTEM =====================

# Add item to cart or update quantity
@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_menu_item(item_id)

    if not item:
        return {"error": "Item not found"}

    if not item["is_available"]:
        return {"error": "Item not available"}

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            c["subtotal"] = c["quantity"] * item["price"]
            return {"message": "Cart updated", "item": c}

    cart_item = {
        "item_id": item_id,
        "name": item["name"],
        "quantity": quantity,
        "price": item["price"],
        "subtotal": item["price"] * quantity
    }

    cart.append(cart_item)
    return {"message": "Added", "item": cart_item}


# View cart with total amount
@app.get("/cart")
def view_cart():
    total = sum(i["subtotal"] for i in cart)
    return {"cart": cart, "total": total}


# Checkout all items in cart and create orders
@app.post("/cart/checkout")
def checkout(data: CheckoutRequest, response: Response):
    global order_counter

    if not cart:
        response.status_code = 400
        return {"error": "Cart empty"}

    placed = []
    total = 0

    for c in cart:
        order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "item": c["name"],
            "quantity": c["quantity"],
            "delivery_address": data.delivery_address,
            "total_price": c["subtotal"]
        }

        orders.append(order)
        placed.append(order)
        total += c["subtotal"]
        order_counter += 1

    cart.clear()
    response.status_code = 201

    return {"orders": placed, "grand_total": total}


# Remove item from cart
@app.delete("/cart/{item_id}")
def remove_cart(item_id: int):
    for c in cart:
        if c["item_id"] == item_id:
            cart.remove(c)
            return {"message": "Removed"}
    return {"error": "Not found"}


# ===================== ADVANCED FEATURES =====================

# Search menu items by keyword
@app.get("/menu/search")
def search_menu(keyword: str):
    result = [
        i for i in menu
        if keyword.lower() in i["name"].lower()
        or keyword.lower() in i["category"].lower()
    ]

    if not result:
        return {"message": "No items found"}

    return {"results": result, "total_found": len(result)}


# Sort menu by price, name, or category
@app.get("/menu/sort")
def sort_menu(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name", "category"]:
        return {"error": "Invalid sort field"}

    if order not in ["asc", "desc"]:
        return {"error": "Invalid order"}

    return {
        "menu": sorted(menu, key=lambda x: x[sort_by], reverse=(order == "desc"))
    }


# Paginate menu results
@app.get("/menu/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    return {
        "page": page,
        "items": menu[start:start+limit],
        "total": len(menu),
        "total_pages": -(-len(menu)//limit)
    }


# Combined endpoint: search + sort + pagination
@app.get("/menu/browse")
def browse(keyword: str = None, sort_by: str = "price", order: str = "asc", page: int = 1, limit: int = 4):
    result = menu

    if keyword:
        result = [i for i in result if keyword.lower() in i["name"].lower()]

    result = sorted(
        result, key=lambda x: x[sort_by], reverse=(order == "desc"))

    start = (page - 1) * limit
    return {
        "results": result[start:start+limit],
        "total": len(result),
        "page": page
    }


# Get a single menu item by ID (placed last to avoid route conflicts)
@app.get("/menu/{item_id}")
def get_item(item_id: int):
    item = find_menu_item(item_id)
    if not item:
        return {"error": "Item not found"}
    return {"item": item}
