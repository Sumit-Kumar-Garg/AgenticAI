
import csv
import json
import random
import os

from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------
# 1. Customers
# -------------------------

customers = []

for i in range(1, 501):
    customers.append({
        "customer_id": f"CUST{i:04d}",
        "name": fake.name(),
        "email": fake.email()
    })

# -------------------------
# 2. Hotels
# -------------------------

hotels = []

for i in range(1, 101):
    hotels.append({
        "hotel_id": f"HOTEL{i:04d}",
        "name": fake.company() + " Hotel",
        "location": fake.city()
    })

# -------------------------
# 3. Bookings
# -------------------------

booking_statuses = [
    "CONFIRMED",
    "CANCELLED",
    "PENDING",
    "FAILED"
]

bookings = []

for i in range(1, 1001):
    customer = random.choice(customers)
    hotel = random.choice(hotels)

    bookings.append({
        "booking_id": f"BOOK{i:05d}",
        "customer_id": customer["customer_id"],
        "hotel_id": hotel["hotel_id"],
        "status": random.choice(booking_statuses),
        "amount": round(random.uniform(100, 1000), 2)
    })

# -------------------------
# 4. Support tickets
# -------------------------

issues = [
    "Booking not received by hotel",
    "Customer charged twice",
    "Booking cancellation request",
    "Refund not received",
    "Payment failed",
    "Hotel confirmation missing",
    "Unable to login",
    "Booking details incorrect"
]

tickets = []

for i in range(1, 501):
    customer = random.choice(customers)

    tickets.append({
        "ticket_id": f"TKT{i:05d}",
        "customer_id": customer["customer_id"],
        "booking_id": random.choice(bookings)["booking_id"],
        "description": random.choice(issues),
        "priority": random.choice(["LOW", "MEDIUM", "HIGH"]),
        "status": random.choice(["OPEN", "CLOSED", "IN_PROGRESS"])
    })

# -------------------------
# 5. Historical resolutions
# -------------------------

resolutions = []

for i in range(1, 301):
    ticket = random.choice(tickets)

    resolutions.append({
        "resolution_id": f"RES{i:05d}",
        "ticket_id": ticket["ticket_id"],
        "root_cause": random.choice([
            "Payment gateway timeout",
            "Hotel synchronization failure",
            "Booking confirmation delay",
            "Customer input error"
        ]),
        "resolution": random.choice([
            "Retry booking synchronization",
            "Verify payment transaction",
            "Initiate refund",
            "Escalate to hotel operations"
        ])
    })

# -------------------------
# 6. Knowledge base
# -------------------------

knowledge_base = []

for i, issue in enumerate(issues, start=1):
    knowledge_base.append({
        "article_id": f"KB{i:04d}",
        "issue": issue,
        "solution": random.choice([
            "Verify booking status before retrying",
            "Check payment gateway transaction logs",
            "Validate cancellation policy",
            "Check hotel confirmation synchronization"
        ])
    })


# -------------------------
# Export CSV files
# -------------------------

def save_csv(filename, records):

    if not records:
        return

    with open(
        os.path.join(DATA_DIR, filename),
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=records[0].keys()
        )

        writer.writeheader()
        writer.writerows(records)


save_csv("customers.csv", customers)
save_csv("hotels.csv", hotels)
save_csv("bookings.csv", bookings)
save_csv("tickets.csv", tickets)
save_csv("resolutions.csv", resolutions)

with open(
    os.path.join(DATA_DIR, "knowledge_base.json"),
    "w",
    encoding="utf-8"
) as file:

    json.dump(knowledge_base, file, indent=4)


print("Dummy data generated successfully!")
print("Customers:", len(customers))
print("Hotels:", len(hotels))
print("Bookings:", len(bookings))
print("Tickets:", len(tickets))
print("Resolutions:", len(resolutions))
print("Knowledge articles:", len(knowledge_base))
