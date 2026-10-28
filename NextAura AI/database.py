import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "nextaura.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    seed_demo_data()

def seed_demo_data():
    conn = get_db()
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # 1. Create Default Users
    # Password for all demo accounts is 'password123'
    hashed_pwd = generate_password_hash("password123")

    users_data = [
        ("admin@nextaura.ai", hashed_pwd, "Priya Sharma (Admin)", "+91 98450 11001", "admin", "NextAura HQ, Indiranagar", "Indiranagar"),
        ("customer@nextaura.ai", hashed_pwd, "Rahul Mehta", "+91 98765 43210", "customer", "Flat 402, Sunshine Apts, 12th Main, Indiranagar", "Indiranagar"),
        ("tech.rajesh@nextaura.ai", hashed_pwd, "Rajesh Kumar", "+91 98220 54321", "technician", "Service Hub 3, Koramangala", "Koramangala"),
        ("tech.anand@nextaura.ai", hashed_pwd, "Anand Verma", "+91 98330 65432", "technician", "Service Hub 1, Indiranagar", "Indiranagar"),
        ("tech.deepak@nextaura.ai", hashed_pwd, "Deepak Joshi", "+91 98440 76543", "technician", "Service Hub 5, HSR Layout", "HSR Layout"),
    ]

    cursor.executemany("""
        INSERT INTO users (email, password_hash, full_name, phone, role, address, locality)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, users_data)

    # 2. Link Technicians
    # Rajesh (id: 3) -> AC & Fridge specialist
    # Anand (id: 4) -> Washing Machine & AC specialist
    # Deepak (id: 5) -> All-round Master Technician
    technicians_data = [
        (3, "Air Conditioners, Refrigerators", 8, 4.9, 142, 310, 299.0, 450.0, 1, 12.9352, 77.6245, "Koramangala", "Certified HVAC & Inverter Refrigerator Specialist with 8+ years experience. Expert in Daikin, LG, Samsung, Voltas."),
        (4, "Washing Machines, Air Conditioners", 6, 4.8, 98, 220, 249.0, 400.0, 1, 12.9784, 77.6408, "Indiranagar", "Front-load & Top-load drum, motor, and PCB repair technician. Whirlpool, Bosch, IFB authorized background."),
        (5, "Air Conditioners, Refrigerators, Washing Machines", 10, 4.95, 215, 520, 349.0, 500.0, 1, 12.9121, 77.6446, "HSR Layout", "Senior Master Technician. Advanced compressor analysis, gas charge testing, inverter PCB diagnostics."),
    ]

    cursor.executemany("""
        INSERT INTO technicians (user_id, specialties, experience_years, rating, reviews_count, jobs_completed, base_inspection_fee, hourly_rate, verified, latitude, longitude, locality, bio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, technicians_data)

    # 3. Seed Sample Diagnostic Log
    cursor.execute("""
        INSERT INTO diagnostic_logs (user_id, appliance_type, brand_model, symptoms_input, error_code, symptom_summary, safe_checks, cost_min, cost_max, cost_breakdown_labor, cost_breakdown_parts, urgency_level, escalation_warning)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        2,
        "Air Conditioners",
        "Voltas 1.5 Ton Split Inverter",
        "AC is blowing room-temperature air, outdoor unit makes buzzing sound every 2 minutes.",
        "None",
        "AC running but not cooling properly; outdoor compressor attempting to start.",
        '["Verify remote is set to COOL mode at 22°C (not FAN mode)", "Inspect indoor air filters for thick dust blockage", "Check if outdoor unit fan blades are obstructed by debris"]',
        1200.0,
        2800.0,
        "₹450 - ₹650 (Coil cleaning, electrical terminal check)",
        "₹750 - ₹2150 (Run capacitor replacement / relay check)",
        "Medium",
        "DO NOT attempt to open outdoor electrical casing or inspect refrigerant piping. High voltage risk."
    ))
    diag_id = cursor.lastrowid

    # 4. Seed Sample Active Booking in 'quoted' status
    cursor.execute("""
        INSERT INTO bookings (booking_code, customer_id, technician_id, appliance_type, brand_model, issue_category, symptom_description, diagnostic_log_id, preferred_date, time_slot, service_address, locality, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "NXA-BK-2026-901",
        2,
        2, # Anand Verma (technician id 2 in technicians table)
        "Air Conditioners",
        "Voltas 1.5 Ton Split Inverter",
        "Cooling Failure",
        "Blowing warm air, outdoor unit humming.",
        diag_id,
        "2026-10-30",
        "10:00 AM - 12:00 PM",
        "Flat 402, Sunshine Apts, 12th Main, Indiranagar",
        "Indiranagar",
        "quoted"
    ))
    booking_id = cursor.lastrowid

    # 5. Seed Itemized Quote for the booking (waiting for customer approval!)
    cursor.execute("""
        INSERT INTO quotes (booking_id, technician_id, inspection_fee, labor_cost, parts_cost, parts_breakdown, tax_amount, total_amount, warranty_months, technician_notes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        booking_id,
        2,
        249.0,
        450.0,
        850.0,
        '{"items": [{"name": "Heavy-duty 45uF Run Capacitor (Voltas OEM)", "cost": 850.0}]}',
        80.0,
        1629.0,
        3,
        "Physical inspection revealed degraded motor capacitor (measured 12uF instead of 45uF). Fan motor and compressor windings tested safe. Replacing capacitor will restore full 100% cooling capacity.",
        "pending"
    ))

    # 6. Seed a Historical Completed Booking + Digital Repair Passport
    cursor.execute("""
        INSERT INTO bookings (booking_code, customer_id, technician_id, appliance_type, brand_model, issue_category, symptom_description, preferred_date, time_slot, service_address, locality, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "NXA-BK-2026-804",
        2,
        1, # Rajesh Kumar
        "Washing Machines",
        "LG 7kg Front Load Wi-Fi Inverter",
        "Drain Pump / Spin Error",
        "Error OE displayed on screen, water not draining during spin cycle.",
        "2026-09-14",
        "02:00 PM - 04:00 PM",
        "Flat 402, Sunshine Apts, 12th Main, Indiranagar",
        "Indiranagar",
        "completed"
    ))
    prev_booking_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO repair_passports (passport_code, booking_id, customer_id, technician_id, appliance_type, brand_model, work_summary, replaced_parts, total_paid, warranty_period, warranty_expiry_date, rating, customer_feedback)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "NXA-RP-2026-4491",
        prev_booking_id,
        2,
        1,
        "Washing Machines",
        "LG 7kg Front Load Wi-Fi Inverter",
        "Drain filter cleared of coin obstruction, drain impeller inspected, high-speed spin cycle tested with zero leakage.",
        "Drain Pump Impeller Seal OEM",
        1150.0,
        "6 Months NextAura Guarantee",
        "2027-03-14",
        5,
        "Super transparent estimate from AI Doctor beforehand, technician arrived on time and showed old vs new part!"
    ))

    conn.commit()
    conn.close()
    print("Database seeded successfully with realistic NextAura AI prototype data.")

if __name__ == "__main__":
    init_db()
