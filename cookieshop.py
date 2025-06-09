def show_menu():
    print("\n🍪 COOKIE MENU:")
    cookie_menu = {
        "Triple Choco": 35000,
        "Biscoff Caramel": 35000,
        "Salted Egg": 35000,
        "Marshma Matcha": 35000,
        "Pistachio": 35000,
        "Choco Velvet": 35000,
    }
    for i, (flavor, price) in enumerate(cookie_menu.items(), start=1):
        print(f"{i}. {flavor} - {price:,} VND")
    print("\n* Discounts: Box of 4 (any flavors) for 130,000 VND, Box of 6 (any flavors) for 190,000 VND *")

def get_order(cookie_menu):
    print("\nEnter quantity for each cookie flavor (0 if none):")
    order = {}
    for flavor in cookie_menu:
        while True:
            try:
                qty = int(input(f"- {flavor}: "))
                if qty < 0:
                    print("Quantity cannot be negative. Try again.")
                else:
                    allergy_note = ""
                    if qty > 0:
                        allergy_note = input(f"Any allergy note for '{flavor}'? (press Enter if none): ").strip()
                    order[flavor] = {"qty": qty, "price": cookie_menu[flavor], "allergy": allergy_note}
                    break
            except:
                print("Please enter a valid number.")
    return order

def calculate_discount(order):
    total_cookies = sum(item["qty"] for item in order.values())
    # Calculate how many boxes of 6 and boxes of 4 can be formed for max discount
    # Prioritize boxes of 6, then boxes of 4, leftovers pay full price
    
    box6_count = total_cookies // 6
    remainder_after_6 = total_cookies % 6
    box4_count = remainder_after_6 // 4
    leftover = remainder_after_6 % 4

    price_box4 = 130000
    price_box6 = 190000

    # Calculate total discount price
    discount_price = box6_count * price_box6 + box4_count * price_box4

    # Calculate leftover price full price
    # For leftover cookies, calculate full price based on flavor proportions
    # We will allocate leftover cookies proportionally from flavors
    
    # Flatten order into list of (flavor, qty)
    flavor_list = []
    for flavor, data in order.items():
        if data["qty"] > 0:
            flavor_list.append({"flavor": flavor, "qty": data["qty"], "price": data["price"], "allergy": data["allergy"]})
    
    # Sort by qty descending to allocate leftover starting from largest qty flavor
    flavor_list.sort(key=lambda x: x["qty"], reverse=True)

    # Calculate how many cookies allocated to discount boxes
    cookies_covered = box6_count * 6 + box4_count * 4
    # Remaining cookies = leftover

    # Allocate leftover cookies by flavor (from the largest quantity down)
    leftover_cookies_price = 0
    cookies_left_to_charge = leftover

    for f in flavor_list:
        if cookies_left_to_charge == 0:
            break
        qty = f["qty"]
        # Calculate how many cookies of this flavor are leftover after discount allocation
        # Total qty - allocated qty to discount boxes (proportionally)
        # But since discount applies to total, we approximate leftover distribution:
        # Let's assume leftover cookies come from the largest quantity flavors
        if qty <= cookies_left_to_charge:
            leftover_cookies_price += qty * f["price"]
            cookies_left_to_charge -= qty
        else:
            leftover_cookies_price += cookies_left_to_charge * f["price"]
            cookies_left_to_charge = 0

    total_price = discount_price + leftover_cookies_price
    return box6_count, box4_count, leftover, total_price

def show_summary(order, box6_count, box4_count, leftover, total_price):
    print("\n🧾 Your order summary:")
    for flavor, data in order.items():
        if data["qty"] > 0:
            allergy_text = f" (Allergy note: {data['allergy']})" if data['allergy'] else ""
            print(f"- {flavor}: {data['qty']} pcs{allergy_text}")
    print(f"\nDiscounts applied:")
    print(f"- Boxes of 6: {box6_count} x 190,000 VND")
    print(f"- Boxes of 4: {box4_count} x 130,000 VND")
    if leftover > 0:
        print(f"- Leftover cookies (full price): {leftover} pcs")
    print(f"\nTotal to pay: {total_price:,} VND")

def get_customer_info():
    print("\n📝 Please provide your information:")
    name = input("Full name: ")
    phone = input("Phone number: ")
    fb_name = input("Facebook name: ")
    address = input("Delivery address: ")

    return {
        "name": name,
        "phone": phone,
        "fb_name": fb_name,
        "address": address
    }

def show_payment_info(customer_info, total_price):
    print("\n💳 PAYMENT INFO")
    print("Please transfer 50% of your order total to confirm your order.")
    print("Account Name: Cookie O'Clock Coffee Shop")
    print("Bank: Vietcombank")
    print("Account Number: 1221 2980 7448 9249")
    print(f"\nImportant: In the payment description, please include your full name, Facebook name, and phone number:")
    print(f"{customer_info['name']} | {customer_info['fb_name']} | {customer_info['phone']}")
    print("\nAfter transfer, please send the payment screenshot to our Facebook page at:")
    print("https://www.facebook.com/CookieOClockShop")

def main():
    cookie_menu = {
        "Triple Choco": 35000,
        "Biscoff Caramel": 35000,
        "Salted Egg": 35000,
        "Marshma Matcha": 35000,
        "Pistachio": 35000,
        "Choco Velvet": 35000,
    }

    show_menu()
    order = get_order(cookie_menu)

    total_qty = sum(item["qty"] for item in order.values())
    if total_qty == 0:
        print("You did not order any cookies. Goodbye!")
        return

    box6_count, box4_count, leftover, total_price = calculate_discount(order)
    show_summary(order, box6_count, box4_count, leftover, total_price)

    customer_info = get_customer_info()
    show_payment_info(customer_info, total_price)

    confirm = input("\nType 'yes' to confirm your order: ").strip().lower()
    if confirm == 'yes':
        print("\nThank you for your order! We will contact you soon.")
    else:
        print("\nOrder cancelled.")

if __name__ == "__main__":
    main()