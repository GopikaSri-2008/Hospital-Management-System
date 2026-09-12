from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

DATABASE = "hospital.db"


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# INITIALIZE DATABASE
# =========================

def init_db():

    conn = get_db_connection()
    cursor = conn.cursor()

    # Patients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT,
            gender TEXT,
            phone TEXT,
            blood_group TEXT,
            department TEXT,
            address TEXT
        )
    """)

    # Doctors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            experience TEXT,
            phone TEXT,
            email TEXT,
            status TEXT
        )
    """)

    # Appointments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doctor_name TEXT NOT NULL,
            date TEXT,
            time TEXT,
            department TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Scheduled'
        )
    """)

    # Billing table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS billing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            treatment TEXT,
            amount REAL,
            date TEXT,
            due_date TEXT,
            payment_method TEXT,
            status TEXT DEFAULT 'Unpaid'
        )
    """)

    # Add due_date if old database does not have it
    cursor.execute("PRAGMA table_info(billing)")
    billing_columns = [column["name"] for column in cursor.fetchall()]

    if "due_date" not in billing_columns:
        cursor.execute("""
            ALTER TABLE billing
            ADD COLUMN due_date TEXT
        """)

    conn.commit()
    conn.close()


# =========================
# DASHBOARD
# =========================

@app.route("/")
def dashboard():

    conn = get_db_connection()

    total_patients = conn.execute(
        "SELECT COUNT(*) AS count FROM patients"
    ).fetchone()["count"]

    total_doctors = conn.execute(
        "SELECT COUNT(*) AS count FROM doctors"
    ).fetchone()["count"]

    total_appointments = conn.execute(
        "SELECT COUNT(*) AS count FROM appointments"
    ).fetchone()["count"]

    total_revenue = conn.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM billing
        WHERE status = 'Paid'
    """).fetchone()["total"]

    today = date.today().isoformat()

    today_appointments = conn.execute("""
        SELECT COUNT(*) AS count
        FROM appointments
        WHERE date = ?
        AND status = 'Scheduled'
    """, (today,)).fetchone()["count"]

    available_doctors = conn.execute("""
        SELECT COUNT(*) AS count
        FROM doctors
        WHERE status = 'Available'
    """).fetchone()["count"]

    unpaid_bills = conn.execute("""
        SELECT COUNT(*) AS count
        FROM billing
        WHERE status = 'Unpaid'
    """).fetchone()["count"]

    cancelled_appointments = conn.execute("""
        SELECT COUNT(*) AS count
        FROM appointments
        WHERE status = 'Cancelled'
    """).fetchone()["count"]

    recent_appointments = conn.execute("""
        SELECT *
        FROM appointments
        ORDER BY id DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_appointments=total_appointments,
        total_revenue=total_revenue,
        today_appointments=today_appointments,
        available_doctors=available_doctors,
        unpaid_bills=unpaid_bills,
        cancelled_appointments=cancelled_appointments,
        recent_appointments=recent_appointments
    )


# =========================
# PATIENTS
# =========================

@app.route("/patients", methods=["GET", "POST"])
def patients():

    conn = get_db_connection()

    if request.method == "POST":

        name = request.form.get("name", "")
        age = request.form.get("age", "")
        gender = request.form.get("gender", "")
        phone = request.form.get("phone", "")
        blood_group = request.form.get("blood_group", "")
        department = request.form.get("department", "")
        address = request.form.get("address", "")

        conn.execute("""
            INSERT INTO patients
            (name, age, gender, phone, blood_group, department, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            age,
            gender,
            phone,
            blood_group,
            department,
            address
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("patients"))

    patient_records = conn.execute("""
        SELECT *
        FROM patients
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "patients.html",
        patients=patient_records
    )


# =========================
# EDIT PATIENT
# =========================

@app.route("/edit_patient/<int:patient_db_id>", methods=["POST"])
def edit_patient(patient_db_id):

    name = request.form.get("name", "")
    age = request.form.get("age", "")
    gender = request.form.get("gender", "")
    phone = request.form.get("phone", "")
    blood_group = request.form.get("blood_group", "")
    department = request.form.get("department", "")
    address = request.form.get("address", "")

    conn = get_db_connection()

    conn.execute("""
        UPDATE patients
        SET name = ?,
            age = ?,
            gender = ?,
            phone = ?,
            blood_group = ?,
            department = ?,
            address = ?
        WHERE id = ?
    """, (
        name,
        age,
        gender,
        phone,
        blood_group,
        department,
        address,
        patient_db_id
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("patients"))


# =========================
# DELETE PATIENT
# =========================

@app.route("/delete_patient/<int:patient_db_id>", methods=["POST"])
def delete_patient(patient_db_id):

    conn = get_db_connection()

    conn.execute("""
        DELETE FROM patients
        WHERE id = ?
    """, (patient_db_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("patients"))


# =========================
# DOCTORS
# =========================

@app.route("/doctors", methods=["GET", "POST"])
def doctors():

    conn = get_db_connection()

    if request.method == "POST":

        name = request.form.get("name", "")
        specialization = request.form.get("specialization", "")
        experience = request.form.get("experience", "")
        phone = request.form.get("phone", "")
        email = request.form.get("email", "")
        status = request.form.get("status", "")

        conn.execute("""
            INSERT INTO doctors
            (name, specialization, experience, phone, email, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            specialization,
            experience,
            phone,
            email,
            status
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("doctors"))

    doctor_records = conn.execute("""
        SELECT *
        FROM doctors
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "doctors.html",
        doctors=doctor_records
    )


# =========================
# EDIT DOCTOR
# =========================

@app.route("/edit_doctor/<int:doctor_db_id>", methods=["POST"])
def edit_doctor(doctor_db_id):

    name = request.form.get("name", "")
    specialization = request.form.get("specialization", "")
    experience = request.form.get("experience", "")
    phone = request.form.get("phone", "")
    email = request.form.get("email", "")
    status = request.form.get("status", "")

    conn = get_db_connection()

    conn.execute("""
        UPDATE doctors
        SET name = ?,
            specialization = ?,
            experience = ?,
            phone = ?,
            email = ?,
            status = ?
        WHERE id = ?
    """, (
        name,
        specialization,
        experience,
        phone,
        email,
        status,
        doctor_db_id
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("doctors"))


# =========================
# DELETE DOCTOR
# =========================

@app.route("/delete_doctor/<int:doctor_db_id>", methods=["POST"])
def delete_doctor(doctor_db_id):

    conn = get_db_connection()

    conn.execute("""
        DELETE FROM doctors
        WHERE id = ?
    """, (doctor_db_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("doctors"))


# =========================
# APPOINTMENTS
# =========================

@app.route("/appointments", methods=["GET", "POST"])
def appointments():

    conn = get_db_connection()

    if request.method == "POST":

        patient_name = request.form.get("patient_name", "")
        doctor_name = request.form.get("doctor_name", "")
        appointment_date = request.form.get("date", "")
        appointment_time = request.form.get("time", "")
        department = request.form.get("department", "")
        reason = request.form.get("reason", "")

        conn.execute("""
            INSERT INTO appointments
            (patient_name, doctor_name, date, time, department, reason, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Scheduled')
        """, (
            patient_name,
            doctor_name,
            appointment_date,
            appointment_time,
            department,
            reason
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("appointments"))

    appointment_records = conn.execute("""
        SELECT *
        FROM appointments
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "appointments.html",
        appointments=appointment_records
    )


# =========================
# EDIT APPOINTMENT
# =========================

@app.route("/edit_appointment/<int:appointment_db_id>", methods=["POST"])
def edit_appointment(appointment_db_id):

    patient_name = request.form.get("patient_name", "")
    doctor_name = request.form.get("doctor_name", "")
    appointment_date = request.form.get("date", "")
    appointment_time = request.form.get("time", "")
    department = request.form.get("department", "")
    reason = request.form.get("reason", "")

    conn = get_db_connection()

    conn.execute("""
        UPDATE appointments
        SET patient_name = ?,
            doctor_name = ?,
            date = ?,
            time = ?,
            department = ?,
            reason = ?
        WHERE id = ?
    """, (
        patient_name,
        doctor_name,
        appointment_date,
        appointment_time,
        department,
        reason,
        appointment_db_id
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("appointments"))


# =========================
# CANCEL APPOINTMENT
# =========================

@app.route("/cancel_appointment/<int:appointment_db_id>", methods=["POST"])
def cancel_appointment(appointment_db_id):

    conn = get_db_connection()

    conn.execute("""
        UPDATE appointments
        SET status = 'Cancelled'
        WHERE id = ?
    """, (appointment_db_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("appointments"))


# =========================
# RESCHEDULE APPOINTMENT
# =========================

@app.route("/reschedule_appointment/<int:appointment_db_id>", methods=["POST"])
def reschedule_appointment(appointment_db_id):

    appointment_date = request.form.get("date", "")
    appointment_time = request.form.get("time", "")

    conn = get_db_connection()

    conn.execute("""
        UPDATE appointments
        SET date = ?,
            time = ?,
            status = 'Scheduled'
        WHERE id = ?
    """, (
        appointment_date,
        appointment_time,
        appointment_db_id
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("appointments"))


# =========================
# BILLING
# =========================

@app.route("/billing", methods=["GET", "POST"])
def billing():

    conn = get_db_connection()

    if request.method == "POST":

        patient_name = request.form.get("patient_name", "")
        treatment = request.form.get("treatment", "")
        amount = request.form.get("amount", "0")
        bill_date = request.form.get("date", "")
        due_date = request.form.get("due_date", "")
        payment_method = request.form.get("payment_method", "")
        status = request.form.get("status", "Unpaid")

        try:
            amount = float(amount)
        except ValueError:
            amount = 0

        conn.execute("""
            INSERT INTO billing
            (patient_name, treatment, amount, date, due_date,
             payment_method, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_name,
            treatment,
            amount,
            bill_date,
            due_date,
            payment_method,
            status
        ))

        conn.commit()

        conn.close()

        return redirect(url_for("billing"))

    bill_records = conn.execute("""
        SELECT *
        FROM billing
        ORDER BY id DESC
    """).fetchall()

    total_revenue = conn.execute("""
        SELECT COALESCE(SUM(amount), 0) AS total
        FROM billing
        WHERE status = 'Paid'
    """).fetchone()["total"]

    total_bills = conn.execute("""
        SELECT COUNT(*) AS count
        FROM billing
    """).fetchone()["count"]

    paid_bills = conn.execute("""
        SELECT COUNT(*) AS count
        FROM billing
        WHERE status = 'Paid'
    """).fetchone()["count"]

    unpaid_bills = conn.execute("""
        SELECT COUNT(*) AS count
        FROM billing
        WHERE status = 'Unpaid'
    """).fetchone()["count"]

    conn.close()

    return render_template(
        "billing.html",
        bills=bill_records,
        total_revenue=total_revenue,
        total_bills=total_bills,
        paid_bills=paid_bills,
        unpaid_bills=unpaid_bills
    )


# =========================
# EDIT BILL
# =========================

@app.route("/edit_bill/<int:bill_db_id>", methods=["POST"])
def edit_bill(bill_db_id):

    patient_name = request.form.get("patient_name", "")
    treatment = request.form.get("treatment", "")
    amount = request.form.get("amount", "0")
    bill_date = request.form.get("date", "")
    due_date = request.form.get("due_date", "")
    payment_method = request.form.get("payment_method", "")
    status = request.form.get("status", "Unpaid")

    try:
        amount = float(amount)
    except ValueError:
        amount = 0

    conn = get_db_connection()

    conn.execute("""
        UPDATE billing
        SET patient_name = ?,
            treatment = ?,
            amount = ?,
            date = ?,
            due_date = ?,
            payment_method = ?,
            status = ?
        WHERE id = ?
    """, (
        patient_name,
        treatment,
        amount,
        bill_date,
        due_date,
        payment_method,
        status,
        bill_db_id
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("billing"))


# =========================
# GLOBAL SEARCH
# =========================

@app.route("/search")
def search():

    query = request.args.get("q", "").strip()

    conn = get_db_connection()

    if query:

        search_pattern = f"%{query}%"

        patient_records = conn.execute("""
            SELECT *
            FROM patients
            WHERE name LIKE ?
               OR phone LIKE ?
               OR department LIKE ?
               OR blood_group LIKE ?
            ORDER BY id DESC
        """, (
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern
        )).fetchall()

        doctor_records = conn.execute("""
            SELECT *
            FROM doctors
            WHERE name LIKE ?
               OR specialization LIKE ?
               OR phone LIKE ?
               OR email LIKE ?
            ORDER BY id DESC
        """, (
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern
        )).fetchall()

        appointment_records = conn.execute("""
            SELECT *
            FROM appointments
            WHERE patient_name LIKE ?
               OR doctor_name LIKE ?
               OR department LIKE ?
               OR status LIKE ?
            ORDER BY id DESC
        """, (
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern
        )).fetchall()

        bill_records = conn.execute("""
            SELECT *
            FROM billing
            WHERE patient_name LIKE ?
               OR treatment LIKE ?
               OR payment_method LIKE ?
               OR status LIKE ?
            ORDER BY id DESC
        """, (
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern
        )).fetchall()

    else:

        patient_records = conn.execute("""
            SELECT *
            FROM patients
            ORDER BY id DESC
        """).fetchall()

        doctor_records = conn.execute("""
            SELECT *
            FROM doctors
            ORDER BY id DESC
        """).fetchall()

        appointment_records = conn.execute("""
            SELECT *
            FROM appointments
            ORDER BY id DESC
        """).fetchall()

        bill_records = conn.execute("""
            SELECT *
            FROM billing
            ORDER BY id DESC
        """).fetchall()

    conn.close()

    return render_template(
        "search.html",
        query=query,
        patients=patient_records,
        doctors=doctor_records,
        appointments=appointment_records,
        bills=bill_records
    )


# =========================
# START APPLICATION
# =========================

init_db()


if __name__ == "__main__":
    app.run(debug=True)