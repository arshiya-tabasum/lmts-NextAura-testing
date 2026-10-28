# NextAura AI — Smart Home Appliance Repair & AI Doctor MVP

A full-stack prototype engineered strictly according to the **16-slide startup blueprint**:
- **Target Appliances**: Air Conditioners (ACs), Refrigerators, Washing Machines
- **Tech Stack**: Python (Flask backend), SQLite (database), HTML5 / CSS3 / Vanilla JS, Leaflet.js (map visualization).

---

## 🚀 The 6-Step Workflow Implemented

1. **Describe**: Customer enters appliance type, model details, and symptom description / error code.
2. **Understand**: "AI Appliance Doctor" API route evaluates symptoms, provides preliminary safe checks, and logs diagnostic notes.
3. **Estimate**: System displays an indicative cost range with labor and parts breakdown assumptions.
4. **Match & Schedule**: Filter verified technicians by skill, locality, and available appointment time slots on an interactive Leaflet.js map.
5. **Repair Approval**: Technician inspects appliance on-site and submits an itemized quotation requiring explicit customer approval before work proceeds.
6. **Repair Passport**: Tamper-proof digital logbook storing completed job details, warranty validity, and invoice in SQLite.

---

## 👥 Three Complete User Dashboards

- **Customer Dashboard (`/customer/dashboard`)**:
  - Appliance repair and maintenance budget tracking (annual budget gauge, replacement savings vs buying new).
  - Active booking pipeline with real-time status badges.
  - Interactive itemized quotation approval (one-click Approve / Decline).
  - Permanent Digital Repair Passports wallet with printable warranty certificate.
  - Dispute resolution trigger.

- **Technician Console (`/technician/dashboard`)**:
  - Assigned job queue.
  - Accept / Decline incoming requests.
  - Arrived & Physical Inspection status.
  - Itemized Quotation submission form (Inspection fee + Labor + Parts OEM + Tax + Warranty duration).
  - Complete job and issue the Digital Repair Passport.
  - Rating and earnings tracker.

- **Admin Dispatch & Operations (`/admin/dashboard`)**:
  - Gross Platform Volume (GMV), Total Bookings, Active Customers, Verified Specialists.
  - Technician credential verification manager (Approve / Revoke verification).
  - Live dispatch pipeline monitoring all bookings in real time.
  - Dispute & complaint resolution panel.

- **Appliance Budget & Financial Hub (`/budget-calculator`)**:
  - "Repair vs Replace" 50% Rule Calculator.
  - Annual household appliance maintenance planner.
  - Market parts and labor indicative price index (Bengaluru).

---

## 🔑 Demo Personas (1-Click Switch Available on Navbar)

| Persona | Role | Email | Password | Features Highlighted |
|---|---|---|---|---|
| **Rahul Mehta** | Customer | `customer@nextaura.ai` | `password123` | Active AC repair in "Quoted" status waiting for approval, completed Washing Machine Repair Passport |
| **Anand Verma** | Technician | `tech.anand@nextaura.ai` | `password123` | Assigned Voltas AC job, submit itemized quote, complete repair |
| **Priya Sharma** | Admin | `admin@nextaura.ai` | `password123` | Verify technician profiles, live dispatch table, resolve disputes |

---

## 🛠️ How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Server**:
   ```bash
   python app.py
   ```

3. **Open Browser**:
   Navigate to `http://127.0.0.1:5000`
