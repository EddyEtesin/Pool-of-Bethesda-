import random
import csv
from datetime import date, timedelta

random.seed(42)

FIRST_NAMES = ["Chinedu", "Amaka", "Ifeoma", "Emeka", "Ngozi", "Tunde", "Bisi",
               "Femi", "Aisha", "Musa", "Yusuf", "Halima", "Adaeze", "Obinna",
               "Folake", "Segun", "Uche", "Chidinma", "Kelechi", "Zainab",
               "Ibrahim", "Fatima", "Bola", "Kunle", "Ngozi", "Chiamaka"]
LAST_NAMES = ["Okafor", "Eze", "Bello", "Adeyemi", "Nwosu", "Okoro", "Abubakar",
              "Ibrahim", "Balogun", "Nnamdi", "Chukwu", "Yusuf", "Aliyu",
              "Adekunle", "Ogunleye", "Uba", "Danjuma", "Etim", "Ekong", "Umeh"]

START_DATE = date(2026, 1, 20)
END_DATE = date(2026, 7, 20)

DRUG_IDS = [f"D{str(i).zfill(3)}" for i in range(1, 11)]
DIAGNOSIS_IDS = [f"DX{str(i).zfill(3)}" for i in range(1, 9)]
STAFF_DOCTORS = ["S001", "S002"]
STAFF_NURSES = ["S003", "S004"]
STAFF_PHARMACISTS = ["S005"]
STAFF_LAB = ["S006"]

def random_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def random_dob():
    start = date(1950, 1, 1)
    end = date(2020, 1, 1)
    return random_date(start, end)

# 1. Patients
patients = []
for i in range(1, 201):
    pid = f"P{str(i).zfill(4)}"
    name_gender = random.choice(["M", "F"])
    patients.append({
        "patient_id": pid,
        "dob": random_dob().isoformat(),
        "gender": name_gender,
        "registration_date": random_date(date(2023,1,1), END_DATE).isoformat()
    })

with open("seeds/raw_patients.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=patients[0].keys())
    writer.writeheader()
    writer.writerows(patients)

# 2. Visits (grain: visit-diagnosis), Consultations, Dispensing, Labs, Payments
visits_rows = []
consultations_rows = []
dispensing_rows = []
labs_rows = []
payments_rows = []

visit_counter = 1
for _ in range(600):
    visit_id = f"V{str(visit_counter).zfill(5)}"
    visit_counter += 1
    patient_id = random.choice(patients)["patient_id"]
    visit_date = random_date(START_DATE, END_DATE)
    attending_staff = random.choice(STAFF_DOCTORS)

    num_diagnoses = random.choices([1, 2], weights=[0.8, 0.2])[0]
    diagnoses = random.sample(DIAGNOSIS_IDS, num_diagnoses)

    for dx in diagnoses:
        visits_rows.append({
            "visit_id": visit_id,
            "patient_id": patient_id,
            "diagnosis_id": dx,
            "attending_staff_id": attending_staff,
            "visit_date": visit_date.isoformat()
        })

        # dispensing: 0-3 drugs per diagnosis
        for _ in range(random.randint(0, 3)):
            drug_id = random.choice(DRUG_IDS)
            dispensing_rows.append({
                "visit_id": visit_id,
                "patient_id": patient_id,
                "diagnosis_id": dx,
                "drug_id": drug_id,
                "dispensed_by_staff_id": random.choice(STAFF_PHARMACISTS + STAFF_NURSES),
                "quantity": random.randint(1, 20),
                "unit_price": round(random.uniform(30, 900), 2),
                "dispense_date": visit_date.isoformat()
            })

        # labs: 0-1 test per diagnosis
        if random.random() < 0.4:
            labs_rows.append({
                "visit_id": visit_id,
                "patient_id": patient_id,
                "diagnosis_id": dx,
                "conducted_by_staff_id": random.choice(STAFF_LAB),
                "test_type": random.choice(["blood_test", "malaria_test", "widal_test", "urinalysis", "xray"]),
                "test_cost": round(random.uniform(500, 5000), 2),
                "test_date": visit_date.isoformat(),
                "result": random.choice(["positive", "negative", "pending"])
            })

    # consultation: one per visit
    consultations_rows.append({
        "visit_id": visit_id,
        "patient_id": patient_id,
        "consultation_fee": round(random.uniform(1000, 3000), 2),
        "visit_date": visit_date.isoformat()
    })

    # payment: one per visit
    insurance_status = random.choices(["none", "hmo", "nhis"], weights=[0.5, 0.3, 0.2])[0]
    coverage = None
    if insurance_status == "hmo":
        coverage = random.choice([70, 80, 90])
    elif insurance_status == "nhis":
        coverage = random.choice([50, 60, 100])

    payments_rows.append({
        "visit_id": visit_id,
        "patient_id": patient_id,
        "payment_method": random.choice(["cash", "card", "transfer"]),
        "insurance_status": insurance_status,
        "insurance_coverage_pct": coverage if coverage is not None else "",
        "amount_paid": round(random.uniform(1000, 15000), 2),
        "amount_owed": round(random.uniform(0, 2000), 2),
        "payment_date": visit_date.isoformat()
    })

def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

write_csv("seeds/raw_visits.csv", visits_rows)
write_csv("seeds/raw_consultations.csv", consultations_rows)
write_csv("seeds/raw_dispensing.csv", dispensing_rows)
write_csv("seeds/raw_labs.csv", labs_rows)
write_csv("seeds/raw_payments.csv", payments_rows)

# 3. Restocks (independent of visits)
restocks_rows = []
suppliers = ["MedPlus Distributors", "HealthLink Supplies", "PharmaCore Nigeria", "Emzor Wholesale"]
for i in range(120):
    restocks_rows.append({
        "drug_id": random.choice(DRUG_IDS),
        "quantity": random.randint(50, 500),
        "supplier": random.choice(suppliers),
        "unit_cost": round(random.uniform(20, 700), 2),
        "restock_date": random_date(START_DATE, END_DATE).isoformat()
    })

write_csv("seeds/raw_restocks.csv", restocks_rows)

print(f"Generated: {len(patients)} patients, {len(visits_rows)} visit-diagnosis rows, "
      f"{len(consultations_rows)} consultations, {len(dispensing_rows)} dispensing rows, "
      f"{len(labs_rows)} lab rows, {len(payments_rows)} payments, {len(restocks_rows)} restocks")