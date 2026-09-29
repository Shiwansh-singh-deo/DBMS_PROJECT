# Hotel Management System

A database-driven **Hotel Management System** developed as a DBMS project using **MySQL** and **Python**. The system manages guests, rooms, reservations, check-in/check-out, hotel services, payments, and reports through a Python-based backend.

## 1. Project Overview

The Hotel Management System is designed to digitally manage the core operations of a hotel.

The project focuses on the **backend and database layer**. No graphical frontend is required.

The system uses:

- **MySQL** — Database management
- **Python** — Backend/application logic
- **mysql-connector-python** — Python–MySQL connectivity
- **Git & GitHub** — Version control and project management

---

## 2. Features

### Guest Management
- Add new guests
- View guest information
- Search guests by name
- Store contact and identification details

### Room Management
- View all rooms
- View available rooms
- View room types and prices
- Update room status

### Reservation Management
- Create reservations
- Check room availability
- Prevent conflicting reservations
- View reservations
- Cancel reservations

### Check-In / Check-Out
- Check guests into their reserved rooms
- Record actual check-in time
- Check guests out
- Calculate room charges
- Update room availability

### Hotel Services
- View available hotel services
- Order services for reservations
- Calculate service charges
- View service orders

### Payment Management
- Record payments
- Support multiple payment methods
- View payment history

### Reports
- Current reservations
- Revenue report
- Room type booking report
- Room occupancy report

---

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| MySQL | Relational database |
| Python | Backend application |
| mysql-connector-python | Database connectivity |
| Git | Version control |
| GitHub | Source code repository |

---

## 4. Database Design

The system is based on a relational database model.

The major entities include:

- Guest
- Room
- Room Type
- Reservation
- Stay
- Payment
- Service
- Service Order

The database uses **primary keys** to uniquely identify records and **foreign keys** to establish relationships between tables.

### Main Relationships

```text
Guest
  |
  | 1 : N
  ↓
Reservation
  |
  | N : 1
  ↓
Room
  |
  | N : 1
  ↓
Room Type

Reservation
  |
  | 1 : 1
  ↓
Stay

Reservation
  |
  | 1 : N
  ├──────────────→ Payment
  |
  └──────────────→ Service Order
                         |
                         | N : 1
                         ↓
                      Service
```

---

## 5. Project Structure

```text
DBMS_PROJECT/
│
├── app.py
├── database.py
├── HOTEL DB.sql
├── README.md
└── .gitignore
```

### `app.py`

Contains the Python backend and menu-driven hotel management operations.

### `database.py`

Contains the MySQL connection configuration.

### `HOTEL DB.sql`

Contains the database schema, tables, relationships, constraints, and initial/sample data.

---

## 6. Database Setup

### Step 1 — Install MySQL

Install MySQL Server and MySQL Workbench.

Make sure the MySQL server is running.

### Step 2 — Import the SQL File

Open MySQL Workbench.

Open:

```text
HOTEL DB.sql
```

Execute the complete SQL script.

Then verify the database:

```sql
SHOW DATABASES;
```

Select the hotel database:

```sql
USE hotel_management;
```

Check the tables:

```sql
SHOW TABLES;
```

---

## 7. Python Setup

Make sure Python is installed.

Check the installation:

```bash
python --version
```

Install the MySQL connector:

```bash
pip install mysql-connector-python
```

---

## 8. Configure Database Connection

Open:

```text
database.py
```

Configure your MySQL credentials:

```python
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="hotel_management"
    )
```

Replace:

```text
YOUR_MYSQL_PASSWORD
```

with your local MySQL password.

**Do not upload your real MySQL password to GitHub.**

---

## 9. Running the Project

Open a terminal in the project directory.

Run:

```bash
python app.py
```

If the connection is successful, the application displays:

```text
Database connection successful!

==========================================
       HOTEL MANAGEMENT SYSTEM
==========================================

1. Guest Management
2. Room Management
3. Reservation Management
4. Check-In
5. Check-Out
6. Payment
7. Hotel Services
8. Reports
9. Exit
```

---

## 10. Application Workflow

A typical hotel workflow is:

```text
Add Guest
    ↓
Select Available Room
    ↓
Create Reservation
    ↓
Check-In
    ↓
Order Hotel Services
    ↓
Record Payment
    ↓
Check-Out
    ↓
Generate/View Reports
```

---

## 11. DBMS Concepts Used

This project demonstrates several important DBMS concepts.

### Relational Database

Data is stored in related tables instead of one large table.

### Primary Key

Each major entity has a unique identifier.

For example:

```text
guest_id
room_id
reservation_id
payment_id
service_id
```

### Foreign Key

Foreign keys connect related tables.

For example:

```text
reservation.guest_id
reservation.room_id
payment.reservation_id
service_order.service_id
```

### SQL Queries

The project uses:

- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- `JOIN`
- `WHERE`
- `GROUP BY`
- Aggregate functions
- Subqueries/conditional queries where applicable

### Joins

Multiple tables are combined using SQL joins to retrieve meaningful information.

Example:

```sql
SELECT
    g.name,
    rm.room_number,
    r.check_in_date,
    r.check_out_date
FROM reservation r
JOIN guest g
ON r.guest_id = g.guest_id
JOIN room rm
ON r.room_id = rm.room_id;
```

### Transactions

Database changes are committed after successful operations and rolled back when an error occurs.

### Normalization

The database separates different types of information into related tables to reduce unnecessary duplication and improve data consistency.

---

## 12. Example Queries

### Display all guests

```sql
SELECT * FROM guest;
```

### Display available rooms

```sql
SELECT *
FROM room
WHERE status = 'Available';
```

### Display reservations with guest names

```sql
SELECT
    r.reservation_id,
    g.name,
    r.check_in_date,
    r.check_out_date,
    r.status
FROM reservation r
JOIN guest g
ON r.guest_id = g.guest_id;
```

### Calculate total payments

```sql
SELECT SUM(amount) AS total_revenue
FROM payment
WHERE payment_status = 'Paid';
```

### Display service orders

```sql
SELECT
    g.name,
    s.service_name,
    so.quantity,
    s.price * so.quantity AS total
FROM service_order so
JOIN reservation r
ON so.reservation_id = r.reservation_id
JOIN guest g
ON r.guest_id = g.guest_id
JOIN service s
ON so.service_id = s.service_id;
```

---

## 13. Testing

The backend can be tested using the following sequence:

### Test 1 — Guest

Create a new guest and verify the record using:

```sql
SELECT * FROM guest;
```

### Test 2 — Room

Display available rooms and verify their status.

### Test 3 — Reservation

Create a reservation for an available room.

Verify:

```sql
SELECT * FROM reservation;
```

### Test 4 — Check-In

Check the guest into the reserved room.

### Test 5 — Services

Add a hotel service to the reservation.

### Test 6 — Payment

Record a payment and verify it using:

```sql
SELECT * FROM payment;
```

### Test 7 — Check-Out

Check out the guest and verify that the reservation is completed and the room becomes available.

---

## 14. Limitations

This project focuses on the **DBMS and backend functionality**.

The following are outside the scope of the current implementation:

- Graphical user interface
- Online booking
- User authentication
- Online payment gateway
- Email/SMS notifications
- Cloud deployment

---

## 15. Future Enhancements

Possible future improvements include:

- Web-based frontend
- Admin login system
- Customer login
- Online reservation system
- Online payment integration
- Automated invoices
- Email notifications
- Hotel dashboard
- Advanced analytics
- Cloud database deployment

---

## 16. How to Clone the Project

Clone the repository:

```bash
git clone https://github.com/Shiwansh-singh-deo/DBMS_PROJECT.git
```

Enter the project directory:

```bash
cd DBMS_PROJECT
```

Install the dependency:

```bash
pip install mysql-connector-python
```

Import `HOTEL DB.sql` into MySQL.

Configure `database.py`.

Run:

```bash
python app.py
```

---

## 17. Academic Project

**Project:** Hotel Management System  
**Course:** Database Management Systems (DBMS)  
**Database:** MySQL  
**Backend:** Python  

This project demonstrates the design and implementation of a relational database system for managing hotel operations.
