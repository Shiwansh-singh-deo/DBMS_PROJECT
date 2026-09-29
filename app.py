from database import get_connection
from datetime import datetime


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def pause():
    input("\nPress Enter to continue...")


def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid amount.")


def get_date(prompt):
    while True:
        date_string = input(prompt)

        try:
            return datetime.strptime(
                date_string,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            print("Invalid date.")
            print("Use format: YYYY-MM-DD")


def execute_query(query, values=None, fetch=False):
    db = None
    cursor = None

    try:
        db = get_connection()
        cursor = db.cursor()

        cursor.execute(query, values or ())

        if fetch:
            return cursor.fetchall()

        db.commit()

    except Exception as e:
        if db:
            db.rollback()

        print("Database error:", e)
        return None

    finally:
        if cursor:
            cursor.close()

        if db:
            db.close()


# ============================================================
# GUEST MANAGEMENT
# ============================================================

def add_guest():

    print("\n========== ADD GUEST ==========")

    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    address = input("Address: ")
    id_proof = input("ID Proof: ")

    query = """
        INSERT INTO guest
        (name, email, phone, address, id_proof)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        name,
        email,
        phone,
        address,
        id_proof
    )

    result = execute_query(query, values)

    if result is not None:
        print("\nGuest added successfully!")


def view_guests():

    print("\n========== ALL GUESTS ==========")

    query = """
        SELECT
            guest_id,
            name,
            email,
            phone,
            address,
            id_proof
        FROM guest
        ORDER BY guest_id
    """

    guests = execute_query(query, fetch=True)

    if not guests:
        print("No guests found.")
        return

    for guest in guests:

        print("----------------------------------------")

        print("Guest ID :", guest[0])
        print("Name     :", guest[1])
        print("Email    :", guest[2])
        print("Phone    :", guest[3])
        print("Address  :", guest[4])
        print("ID Proof :", guest[5])


def search_guest():

    print("\n========== SEARCH GUEST ==========")

    search = input("Enter guest name: ")

    query = """
        SELECT
            guest_id,
            name,
            email,
            phone
        FROM guest
        WHERE name LIKE %s
    """

    guests = execute_query(
        query,
        (f"%{search}%",),
        fetch=True
    )

    if not guests:
        print("No guests found.")
        return

    for guest in guests:

        print("--------------------------------")

        print("ID    :", guest[0])
        print("Name  :", guest[1])
        print("Email :", guest[2])
        print("Phone :", guest[3])


def guest_menu():

    while True:

        print("\n================================")
        print("       GUEST MANAGEMENT")
        print("================================")

        print("1. Add Guest")
        print("2. View Guests")
        print("3. Search Guest")
        print("4. Back")

        choice = input("\nEnter choice: ")

        if choice == "1":
            add_guest()
            pause()

        elif choice == "2":
            view_guests()
            pause()

        elif choice == "3":
            search_guest()
            pause()

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


# ============================================================
# ROOM MANAGEMENT
# ============================================================

def view_rooms():

    print("\n========== ALL ROOMS ==========")

    query = """
        SELECT
            r.room_id,
            r.room_number,
            rt.type_name,
            rt.price_per_night,
            rt.capacity,
            r.floor,
            r.status
        FROM room r
        JOIN room_type rt
        ON r.room_type_id = rt.room_type_id
        ORDER BY r.room_number
    """

    rooms = execute_query(query, fetch=True)

    if not rooms:
        print("No rooms found.")
        return

    for room in rooms:

        print("----------------------------------------")

        print("Room ID :", room[0])
        print("Number  :", room[1])
        print("Type    :", room[2])
        print("Price   :", room[3])
        print("Capacity:", room[4])
        print("Floor   :", room[5])
        print("Status  :", room[6])


def available_rooms():

    print("\n========== AVAILABLE ROOMS ==========")

    query = """
        SELECT
            r.room_id,
            r.room_number,
            rt.type_name,
            rt.price_per_night,
            rt.capacity
        FROM room r
        JOIN room_type rt
        ON r.room_type_id = rt.room_type_id
        WHERE r.status = 'Available'
        ORDER BY r.room_number
    """

    rooms = execute_query(query, fetch=True)

    if not rooms:
        print("No rooms are currently available.")
        return

    for room in rooms:

        print("--------------------------------")

        print("Room ID :", room[0])
        print("Number  :", room[1])
        print("Type    :", room[2])
        print("Price   :", room[3])
        print("Capacity:", room[4])


def update_room_status():

    print("\n========== UPDATE ROOM STATUS ==========")

    room_id = get_integer("Enter room ID: ")

    print("\n1. Available")
    print("2. Occupied")
    print("3. Maintenance")

    choice = input("Choose status: ")

    statuses = {
        "1": "Available",
        "2": "Occupied",
        "3": "Maintenance"
    }

    if choice not in statuses:
        print("Invalid status.")
        return

    query = """
        UPDATE room
        SET status = %s
        WHERE room_id = %s
    """

    execute_query(
        query,
        (statuses[choice], room_id)
    )

    print("Room status updated.")


def room_menu():

    while True:

        print("\n================================")
        print("        ROOM MANAGEMENT")
        print("================================")

        print("1. View All Rooms")
        print("2. View Available Rooms")
        print("3. Update Room Status")
        print("4. Back")

        choice = input("\nEnter choice: ")

        if choice == "1":
            view_rooms()
            pause()

        elif choice == "2":
            available_rooms()
            pause()

        elif choice == "3":
            update_room_status()
            pause()

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


# ============================================================
# RESERVATION MANAGEMENT
# ============================================================

def make_reservation():

    print("\n========== MAKE RESERVATION ==========")

    # Display guests
    view_guests()

    guest_id = get_integer("\nEnter Guest ID: ")

    # Check guest exists
    query = """
        SELECT guest_id
        FROM guest
        WHERE guest_id = %s
    """

    guest = execute_query(
        query,
        (guest_id,),
        fetch=True
    )

    if not guest:
        print("Guest does not exist.")
        return

    # Display available rooms
    available_rooms()

    room_id = get_integer("\nEnter Room ID: ")

    # Check room availability
    query = """
        SELECT
            r.room_id,
            r.status,
            rt.capacity,
            rt.price_per_night
        FROM room r
        JOIN room_type rt
        ON r.room_type_id = rt.room_type_id
        WHERE r.room_id = %s
    """

    room = execute_query(
        query,
        (room_id,),
        fetch=True
    )

    if not room:

        print("Room does not exist.")
        return

    room = room[0]

    if room[1] != "Available":

        print("This room is not available.")
        return

    capacity = room[2]

    check_in = get_date(
        "Check-in date (YYYY-MM-DD): "
    )

    check_out = get_date(
        "Check-out date (YYYY-MM-DD): "
    )

    if check_out <= check_in:

        print("Check-out must be after check-in.")
        return

    number_of_guests = get_integer(
        "Number of guests: "
    )

    if number_of_guests <= 0:

        print("Number of guests must be positive.")
        return

    if number_of_guests > capacity:

        print(
            f"This room can accommodate only "
            f"{capacity} guests."
        )

        return

    # Check overlapping reservations
    query = """
        SELECT reservation_id
        FROM reservation
        WHERE room_id = %s
        AND status IN ('Confirmed', 'Checked-In')
        AND check_in_date < %s
        AND check_out_date > %s
    """

    conflicts = execute_query(
        query,
        (
            room_id,
            check_out,
            check_in
        ),
        fetch=True
    )

    if conflicts:

        print(
            "This room is already reserved "
            "for those dates."
        )

        return

    # Create reservation
    query = """
        INSERT INTO reservation
        (
            guest_id,
            room_id,
            check_in_date,
            check_out_date,
            number_of_guests,
            status
        )
        VALUES (%s, %s, %s, %s, %s, 'Confirmed')
    """

    values = (
        guest_id,
        room_id,
        check_in,
        check_out,
        number_of_guests
    )

    execute_query(query, values)

    # Since this simple project uses room status,
    # mark it reserved.
    query = """
        UPDATE room
        SET status = 'Occupied'
        WHERE room_id = %s
    """

    execute_query(query, (room_id,))

    print("\nReservation created successfully!")


def view_reservations():

    print("\n========== RESERVATIONS ==========")

    query = """
        SELECT
            r.reservation_id,
            g.name,
            rm.room_number,
            rt.type_name,
            r.check_in_date,
            r.check_out_date,
            r.number_of_guests,
            r.status
        FROM reservation r
        JOIN guest g
        ON r.guest_id = g.guest_id
        JOIN room rm
        ON r.room_id = rm.room_id
        JOIN room_type rt
        ON rm.room_type_id = rt.room_type_id
        ORDER BY r.reservation_id
    """

    reservations = execute_query(
        query,
        fetch=True
    )

    if not reservations:

        print("No reservations found.")
        return

    for r in reservations:

        print("----------------------------------------")

        print("Reservation ID:", r[0])
        print("Guest         :", r[1])
        print("Room          :", r[2])
        print("Room Type     :", r[3])
        print("Check-in      :", r[4])
        print("Check-out     :", r[5])
        print("Guests        :", r[6])
        print("Status        :", r[7])


def cancel_reservation():

    print("\n========== CANCEL RESERVATION ==========")

    reservation_id = get_integer(
        "Enter reservation ID: "
    )

    query = """
        SELECT room_id, status
        FROM reservation
        WHERE reservation_id = %s
    """

    reservation = execute_query(
        query,
        (reservation_id,),
        fetch=True
    )

    if not reservation:

        print("Reservation not found.")
        return

    room_id = reservation[0][0]
    status = reservation[0][1]

    if status == "Cancelled":

        print("Reservation is already cancelled.")
        return

    if status == "Completed":

        print("Completed reservation cannot be cancelled.")
        return

    query = """
        UPDATE reservation
        SET status = 'Cancelled'
        WHERE reservation_id = %s
    """

    execute_query(
        query,
        (reservation_id,)
    )

    query = """
        UPDATE room
        SET status = 'Available'
        WHERE room_id = %s
    """

    execute_query(
        query,
        (room_id,)
    )

    print("Reservation cancelled successfully.")


def reservation_menu():

    while True:

        print("\n================================")
        print("     RESERVATION MANAGEMENT")
        print("================================")

        print("1. Make Reservation")
        print("2. View Reservations")
        print("3. Cancel Reservation")
        print("4. Back")

        choice = input("\nEnter choice: ")

        if choice == "1":
            make_reservation()
            pause()

        elif choice == "2":
            view_reservations()
            pause()

        elif choice == "3":
            cancel_reservation()
            pause()

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


# ============================================================
# CHECK-IN
# ============================================================

def check_in():

    print("\n========== CHECK-IN ==========")

    reservation_id = get_integer(
        "Enter reservation ID: "
    )

    query = """
        SELECT
            reservation_id,
            room_id,
            status
        FROM reservation
        WHERE reservation_id = %s
    """

    reservation = execute_query(
        query,
        (reservation_id,),
        fetch=True
    )

    if not reservation:

        print("Reservation not found.")
        return

    reservation = reservation[0]

    room_id = reservation[1]
    status = reservation[2]

    if status != "Confirmed":

        print(
            f"Cannot check in a reservation "
            f"with status '{status}'."
        )

        return

    # Create stay
    query = """
        INSERT INTO stay
        (reservation_id, actual_check_in)
        VALUES (%s, NOW())
    """

    execute_query(
        query,
        (reservation_id,)
    )

    # Update reservation
    query = """
        UPDATE reservation
        SET status = 'Checked-In'
        WHERE reservation_id = %s
    """

    execute_query(
        query,
        (reservation_id,)
    )

    # Update room
    query = """
        UPDATE room
        SET status = 'Occupied'
        WHERE room_id = %s
    """

    execute_query(
        query,
        (room_id,)
    )

    print("Guest checked in successfully.")


# ============================================================
# CHECK-OUT
# ============================================================

def check_out():

    print("\n========== CHECK-OUT ==========")

    reservation_id = get_integer(
        "Enter reservation ID: "
    )

    query = """
        SELECT
            r.room_id,
            r.check_in_date,
            r.check_out_date,
            rt.price_per_night
        FROM reservation r
        JOIN room rm
        ON r.room_id = rm.room_id
        JOIN room_type rt
        ON rm.room_type_id = rt.room_type_id
        WHERE r.reservation_id = %s
        AND r.status = 'Checked-In'
    """

    reservation = execute_query(
        query,
        (reservation_id,),
        fetch=True
    )

    if not reservation:

        print(
            "Active checked-in reservation "
            "not found."
        )

        return

    reservation = reservation[0]

    room_id = reservation[0]
    check_in_date = reservation[1]
    check_out_date = reservation[2]
    price_per_night = float(reservation[3])

    # Calculate nights
    today = datetime.now().date()

    nights = (today - check_in_date).days

    if nights <= 0:
        nights = 1

    room_charge = nights * price_per_night

    # Service charges
    query = """
        SELECT
            COALESCE(
                SUM(s.price * so.quantity),
                0
            )
        FROM service_order so
        JOIN service s
        ON so.service_id = s.service_id
        WHERE so.reservation_id = %s
    """

    result = execute_query(
        query,
        (reservation_id,),
        fetch=True
    )

    service_charge = float(result[0][0])

    total = room_charge + service_charge

    print("\n========== FINAL BILL ==========")

    print("Nights         :", nights)
    print("Room Charge    : ₹", room_charge)
    print("Service Charge : ₹", service_charge)
    print("Total          : ₹", total)

    # Update stay
    query = """
        UPDATE stay
        SET actual_check_out = NOW()
        WHERE reservation_id = %s
    """

    execute_query(
        query,
        (reservation_id,)
    )

    # Update reservation
    query = """
        UPDATE reservation
        SET status = 'Completed'
        WHERE reservation_id = %s
    """

    execute_query(
        query,
        (reservation_id,)
    )

    # Make room available
    query = """
        UPDATE room
        SET status = 'Available'
        WHERE room_id = %s
    """

    execute_query(
        query,
        (room_id,)
    )

    print("\nCheck-out completed.")
    print("Room is now available.")


# ============================================================
# PAYMENT
# ============================================================

def make_payment():

    print("\n========== PAYMENT ==========")

    reservation_id = get_integer(
        "Reservation ID: "
    )

    amount = get_float(
        "Payment amount: ₹"
    )

    print("\nPayment methods:")
    print("1. Cash")
    print("2. Card")
    print("3. UPI")
    print("4. Net Banking")

    choice = input("Choose method: ")

    methods = {
        "1": "Cash",
        "2": "Card",
        "3": "UPI",
        "4": "Net Banking"
    }

    if choice not in methods:

        print("Invalid payment method.")
        return

    query = """
        INSERT INTO payment
        (
            reservation_id,
            amount,
            payment_method,
            payment_status
        )
        VALUES (%s, %s, %s, 'Paid')
    """

    execute_query(
        query,
        (
            reservation_id,
            amount,
            methods[choice]
        )
    )

    print("Payment recorded successfully.")


def view_payments():

    print("\n========== PAYMENT HISTORY ==========")

    query = """
        SELECT
            p.payment_id,
            g.name,
            p.amount,
            p.payment_date,
            p.payment_method,
            p.payment_status
        FROM payment p
        JOIN reservation r
        ON p.reservation_id = r.reservation_id
        JOIN guest g
        ON r.guest_id = g.guest_id
        ORDER BY p.payment_date DESC
    """

    payments = execute_query(
        query,
        fetch=True
    )

    if not payments:

        print("No payments found.")
        return

    for p in payments:

        print("----------------------------------------")

        print("Payment ID :", p[0])
        print("Guest      :", p[1])
        print("Amount     :", p[2])
        print("Date       :", p[3])
        print("Method     :", p[4])
        print("Status     :", p[5])


def payment_menu():

    while True:

        print("\n================================")
        print("          PAYMENTS")
        print("================================")

        print("1. Record Payment")
        print("2. View Payments")
        print("3. Back")

        choice = input("\nEnter choice: ")

        if choice == "1":
            make_payment()
            pause()

        elif choice == "2":
            view_payments()
            pause()

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


# ============================================================
# HOTEL SERVICES
# ============================================================

def view_services():

    print("\n========== HOTEL SERVICES ==========")

    query = """
        SELECT
            service_id,
            service_name,
            price
        FROM service
        ORDER BY service_id
    """

    services = execute_query(
        query,
        fetch=True
    )

    if not services:

        print("No services found.")
        return

    for service in services:

        print("--------------------------------")

        print("ID    :", service[0])
        print("Name  :", service[1])
        print("Price :", service[2])


def order_service():

    print("\n========== ORDER SERVICE ==========")

    reservation_id = get_integer(
        "Reservation ID: "
    )

    # Verify reservation
    query = """
        SELECT reservation_id
        FROM reservation
        WHERE reservation_id = %s
        AND status IN ('Confirmed', 'Checked-In')
    """

    reservation = execute_query(
        query,
        (reservation_id,),
        fetch=True
    )

    if not reservation:

        print("Active reservation not found.")
        return

    view_services()

    service_id = get_integer(
        "\nService ID: "
    )

    quantity = get_integer(
        "Quantity: "
    )

    if quantity <= 0:

        print("Quantity must be positive.")
        return

    query = """
        SELECT service_id
        FROM service
        WHERE service_id = %s
    """

    service = execute_query(
        query,
        (service_id,),
        fetch=True
    )

    if not service:

        print("Service not found.")
        return

    query = """
        INSERT INTO service_order
        (
            reservation_id,
            service_id,
            quantity
        )
        VALUES (%s, %s, %s)
    """

    execute_query(
        query,
        (
            reservation_id,
            service_id,
            quantity
        )
    )

    print("Service ordered successfully.")


def view_service_orders():

    print("\n========== SERVICE ORDERS ==========")

    query = """
        SELECT
            so.service_order_id,
            g.name,
            s.service_name,
            s.price,
            so.quantity,
            s.price * so.quantity AS total,
            so.order_date
        FROM service_order so
        JOIN reservation r
        ON so.reservation_id = r.reservation_id
        JOIN guest g
        ON r.guest_id = g.guest_id
        JOIN service s
        ON so.service_id = s.service_id
        ORDER BY so.order_date DESC
    """

    orders = execute_query(
        query,
        fetch=True
    )

    if not orders:

        print("No service orders found.")
        return

    for order in orders:

        print("----------------------------------------")

        print("Order ID :", order[0])
        print("Guest    :", order[1])
        print("Service  :", order[2])
        print("Price    :", order[3])
        print("Quantity :", order[4])
        print("Total    :", order[5])
        print("Date     :", order[6])


def service_menu():

    while True:

        print("\n================================")
        print("        HOTEL SERVICES")
        print("================================")

        print("1. View Services")
        print("2. Order Service")
        print("3. View Service Orders")
        print("4. Back")

        choice = input("\nEnter choice: ")

        if choice == "1":
            view_services()
            pause()

        elif choice == "2":
            order_service()
            pause()

        elif choice == "3":
            view_service_orders()
            pause()

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


# ============================================================
# REPORTS
# ============================================================

def current_reservations():

    print("\n========== CURRENT RESERVATIONS ==========")

    query = """
        SELECT
            r.reservation_id,
            g.name,
            rm.room_number,
            r.check_in_date,
            r.check_out_date,
            r.status
        FROM reservation r
        JOIN guest g
        ON r.guest_id = g.guest_id
        JOIN room rm
        ON r.room_id = rm.room_id
        WHERE r.status IN ('Confirmed', 'Checked-In')
        ORDER BY r.check_in_date
    """

    data = execute_query(
        query,
        fetch=True
    )

    if not data:

        print("No current reservations.")
        return

    for row in data:

        print("--------------------------------")

        print("Reservation:", row[0])
        print("Guest      :", row[1])
        print("Room       :", row[2])
        print("Check-in   :", row[3])
        print("Check-out  :", row[4])
        print("Status     :", row[5])


def revenue_report():

    print("\n========== REVENUE REPORT ==========")

    query = """
        SELECT
            COUNT(*) AS transactions,
            COALESCE(SUM(amount), 0) AS revenue
        FROM payment
        WHERE payment_status = 'Paid'
    """

    result = execute_query(
        query,
        fetch=True
    )

    print("Transactions :", result[0][0])
    print("Total Revenue: ₹", result[0][1])


def room_type_report():

    print("\n========== ROOM TYPE REPORT ==========")

    query = """
        SELECT
            rt.type_name,
            COUNT(r.reservation_id) AS bookings
        FROM room_type rt
        LEFT JOIN room rm
        ON rt.room_type_id = rm.room_type_id
        LEFT JOIN reservation r
        ON rm.room_id = r.room_id
        GROUP BY rt.room_type_id, rt.type_name
        ORDER BY bookings DESC
    """

    data = execute_query(
        query,
        fetch=True
    )

    for row in data:

        print(
            f"{row[0]} : {row[1]} bookings"
        )


def occupancy_report():

    print("\n========== ROOM OCCUPANCY ==========")

    query = """
        SELECT
            status,
            COUNT(*) AS total
        FROM room
        GROUP BY status
    """

    data = execute_query(
        query,
        fetch=True
    )

    for row in data:

        print(
            f"{row[0]} : {row[1]}"
        )


def reports_menu():

    while True:

        print("\n================================")
        print("            REPORTS")
        print("================================")

        print("1. Current Reservations")
        print("2. Revenue Report")
        print("3. Room Type Report")
        print("4. Room Occupancy")
        print("5. Back")

        choice = input("\nEnter choice: ")

        if choice == "1":
            current_reservations()
            pause()

        elif choice == "2":
            revenue_report()
            pause()

        elif choice == "3":
            room_type_report()
            pause()

        elif choice == "4":
            occupancy_report()
            pause()

        elif choice == "5":
            break

        else:
            print("Invalid choice.")


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():

    while True:

        print("\n")
        print("==========================================")
        print("       HOTEL MANAGEMENT SYSTEM")
        print("==========================================")

        print("1. Guest Management")
        print("2. Room Management")
        print("3. Reservation Management")
        print("4. Check-In")
        print("5. Check-Out")
        print("6. Payment")
        print("7. Hotel Services")
        print("8. Reports")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            guest_menu()

        elif choice == "2":

            room_menu()

        elif choice == "3":

            reservation_menu()

        elif choice == "4":

            check_in()
            pause()

        elif choice == "5":

            check_out()
            pause()

        elif choice == "6":

            payment_menu()

        elif choice == "7":

            service_menu()

        elif choice == "8":

            reports_menu()

        elif choice == "9":

            print("\nThank you for using Hotel Management System!")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    try:

        # Test database connection
        db = get_connection()
        db.close()

        print("\nDatabase connection successful!")

        main_menu()

    except Exception as e:

        print("\nCould not connect to MySQL.")
        print("Error:", e)
        print("\nCheck:")
        print("1. MySQL Server is running")
        print("2. Your MySQL password is correct")
        print("3. Database 'hotel_management' exists")