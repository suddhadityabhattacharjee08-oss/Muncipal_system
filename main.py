import mysql.connector
from datetime import datetime
from decimal import Decimal, InvalidOperation

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""

DATABASES = {
    "municipal": "AMC",
    "medical": "hospital_service",
    "financial": "financial_services"
}

def get_connection(database):
    return mysql.connector.connect(
        host=MYSQL_HOST, user=MYSQL_USER,
        password=MYSQL_PASSWORD, database=database
    )

def pause():
    input("\nPress Enter to continue...")

# ---------------- MUNICIPAL SYSTEM ----------------

def municipal_system():
    try:
        conn = get_connection(DATABASES["municipal"])
        cur = conn.cursor()
    except mysql.connector.Error as err:
        print("Could not connect to Municipal database:", err)
        pause()
        return

    while True:
        print("\n===== MUNICIPAL SYSTEM =====")
        print("1. Login as Official")
        print("2. Login as Citizen")
        print("3. Return to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            municipal_official_menu(cur, conn)
        elif choice == "2":
            municipal_citizen_menu(cur, conn)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

    cur.close()
    conn.close()

def municipal_official_menu(cur, conn):
    official_id = input("Enter your Official ID: ")
    cur.execute("SELECT * FROM officialdata1 WHERE OfficialID = %s", (official_id,))
    official = cur.fetchone()

    if not official:
        print("Wrong Official ID.")
        pause()
        return

    print("Login Successful. Welcome", official[0])

    while True:
        print("\n--- Municipal Official Menu ---")
        print("1. View Municipal Data")
        print("2. Delete Citizen Record")
        print("3. Update Citizen Details")
        print("4. Update Complaint/Other Status")
        print("5. Add New Official")
        print("6. Return")
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                cur.execute("SELECT * FROM muncipdata13 ORDER BY UNIQUEID")
                rows = cur.fetchall()
                if not rows:
                    print("No citizen records found.")
                for row in rows:
                    print("\nName:", row[0], "| UNIQUEID:", row[1])
                    print("Age:", row[2], "| Area:", row[3], "| Ward:", row[4])
                    print("Gender:", row[5])
                    print("Complaint:", row[6], "| Status:", row[7])
                    print("Other Request:", row[8], "| Status:", row[9])

            elif choice == "2":
                unique_id = input("Enter UNIQUEID to delete: ")
                cur.execute("DELETE FROM muncipdata13 WHERE UNIQUEID = %s", (unique_id,))
                conn.commit()
                print("Citizen record deleted." if cur.rowcount else "No record found.")

            elif choice == "3":
                update_citizen(cur, conn)

            elif choice == "4":
                update_request_status(cur, conn)

            elif choice == "5":
                name = input("Enter official name: ")
                official_id = input("Enter Official ID: ")
                age = input("Enter age: ")
                cur.execute("SELECT OfficialID FROM officialdata1 WHERE OfficialID = %s", (official_id,))
                if cur.fetchone():
                    print("Official ID already exists.")
                else:
                    cur.execute(
                        "INSERT INTO officialdata1 (Name, OfficialID, Age) VALUES (%s, %s, %s)",
                        (name, official_id, age)
                    )
                    conn.commit()
                    print("New official inserted.")

            elif choice == "6":
                break
            else:
                print("Invalid choice.")
        except mysql.connector.Error as err:
            conn.rollback()
            print("Database error:", err)
        pause()

def update_citizen(cur, conn):
    unique_id = input("Enter the person's UNIQUEID: ")
    cur.execute("SELECT UNIQUEID FROM muncipdata13 WHERE UNIQUEID = %s", (unique_id,))
    if not cur.fetchone():
        print("No citizen found.")
        return

    print("1. Name\n2. UNIQUEID\n3. Age\n4. Area\n5. Ward")
    choice = input("Enter your choice: ")
    fields = {
        "1": ("Name", "Enter new name: "),
        "2": ("UNIQUEID", "Enter new UNIQUEID: "),
        "3": ("Age", "Enter new age: "),
        "4": ("Area", "Enter new area: "),
        "5": ("Ward", "Enter new ward: ")
    }
    if choice not in fields:
        print("Wrong choice.")
        return

    field, prompt = fields[choice]
    value = input(prompt)
    cur.execute(f"UPDATE muncipdata13 SET {field} = %s WHERE UNIQUEID = %s", (value, unique_id))
    conn.commit()
    print(field, "updated successfully.")

def update_request_status(cur, conn):
    unique_id = input("Enter UNIQUEID: ")
    print("1. Complaint Status")
    print("2. Other Request Status")
    choice = input("Enter your choice: ")
    field = "Complainapp" if choice == "1" else "Otherapp" if choice == "2" else None
    if field is None:
        print("Wrong choice.")
        return

    status = input("Enter new status (Waiting/Approved/Rejected): ")
    cur.execute(f"UPDATE muncipdata13 SET {field} = %s WHERE UNIQUEID = %s", (status, unique_id))
    conn.commit()
    print("Status updated." if cur.rowcount else "No record found.")

def citizen_details():
    return (
        input("Enter your name: "),
        input("Enter your UNIQUEID: "),
        input("Enter your age: "),
        input("Enter your area: "),
        input("Enter your ward: "),
        input("Enter your gender: ")
    )

def municipal_citizen_menu(cur, conn):
    while True:
        print("\n--- Municipal Citizen Menu ---")
        print("1. View Profile")
        print("2. Lodge a Complaint")
        print("3. Lodge Other Request")
        print("4. View Request Status")
        print("5. Return")
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                uid = input("Enter your UNIQUEID: ")
                cur.execute("SELECT * FROM muncipdata13 WHERE UNIQUEID = %s", (uid,))
                row = cur.fetchone()
                if row:
                    print("Name:", row[0], "\nUNIQUEID:", row[1], "\nAge:", row[2])
                    print("Area:", row[3], "\nWard:", row[4], "\nGender:", row[5])
                else:
                    print("Wrong ID.")

            elif choice in ("2", "3"):
                name, uid, age, area, ward, gender = citizen_details()
                text = input("Enter your complaint: " if choice == "2" else "Enter your other request: ")
                if choice == "2":
                    query = """INSERT INTO muncipdata13
                    (Name, UNIQUEID, Age, Area, Ward, Gender, Complains, Complainapp)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                    values = (name, uid, age, area, ward, gender, text, "Waiting")
                else:
                    query = """INSERT INTO muncipdata13
                    (Name, UNIQUEID, Age, Area, Ward, Gender, Other, Otherapp)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                    values = (name, uid, age, area, ward, gender, text, "Waiting")
                cur.execute(query, values)
                conn.commit()
                print("Request lodged successfully.")

            elif choice == "4":
                uid = input("Enter your UNIQUEID: ")
                cur.execute("SELECT Complains, Complainapp, Other, Otherapp FROM muncipdata13 WHERE UNIQUEID = %s", (uid,))
                row = cur.fetchone()
                if row:
                    print("Complaint:", row[0], "| Status:", row[1])
                    print("Other Request:", row[2], "| Status:", row[3])
                else:
                    print("Wrong ID.")

            elif choice == "5":
                break
            else:
                print("Invalid choice.")
        except mysql.connector.Error as err:
            conn.rollback()
            print("Database error:", err)
        pause()

# ---------------- MEDICAL SYSTEM ----------------

def medical_system():
    try:
        conn = get_connection(DATABASES["medical"])
        cur = conn.cursor()
    except mysql.connector.Error as err:
        print("Could not connect to Medical database:", err)
        pause()
        return

    while True:
        print("\n===== MEDICAL SYSTEM =====")
        print("1. Login as Official")
        print("2. Login as Patient")
        print("3. Return to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            medical_official_menu(cur, conn)
        elif choice == "2":
            medical_patient_menu(cur, conn)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

    cur.close()
    conn.close()

def view_hospitals(cur):
    cur.execute("SELECT hospital_id, name, address FROM hospitals ORDER BY hospital_id")
    rows = cur.fetchall()
    for row in rows:
        print(f"{row[0]}. {row[1]} - {row[2]}")

def view_doctors(cur):
    cur.execute("""SELECT d.doctor_id, d.name, d.specialty, h.name
                   FROM doctors d JOIN hospitals h ON d.hospital_id = h.hospital_id
                   ORDER BY d.doctor_id""")
    for row in cur.fetchall():
        print(f"{row[0]}. {row[1]} | {row[2]} | {row[3]}")

def book_appointment(cur, conn):
    name = input("Enter patient name: ")
    age = input("Enter age: ")
    gender = input("Enter gender: ")
    phone = input("Enter phone number: ")

    cur.execute("SELECT patient_id FROM patients WHERE phone = %s AND name = %s", (phone, name))
    patient = cur.fetchone()
    if patient:
        patient_id = patient[0]
    else:
        cur.execute("INSERT INTO patients (name, age, gender, phone) VALUES (%s,%s,%s,%s)",
                    (name, age, gender, phone))
        conn.commit()
        patient_id = cur.lastrowid

    view_doctors(cur)
    doctor_id = input("Enter doctor ID: ")
    cur.execute("SELECT doctor_id FROM doctors WHERE doctor_id = %s", (doctor_id,))
    if not cur.fetchone():
        print("Doctor not found.")
        return

    date_text = input("Enter appointment date (YYYY-MM-DD): ")
    try:
        appointment_date = datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date.")
        return

    cur.execute("""INSERT INTO appointments
                   (patient_id, doctor_id, appointment_date)
                   VALUES (%s,%s,%s)""", (patient_id, doctor_id, appointment_date))
    conn.commit()
    print("Appointment booked successfully.")

def view_appointments(cur, phone=None):
    query = """SELECT a.appointment_id, p.name, p.phone, d.name,
                      d.specialty, a.appointment_date
               FROM appointments a
               JOIN patients p ON a.patient_id = p.patient_id
               JOIN doctors d ON a.doctor_id = d.doctor_id"""
    if phone:
        query += " WHERE p.phone = %s"
        cur.execute(query, (phone,))
    else:
        cur.execute(query)
    rows = cur.fetchall()
    if not rows:
        print("No appointments found.")
    for row in rows:
        print(f"Appointment ID: {row[0]} | Patient: {row[1]} | Phone: {row[2]}")
        print(f"Doctor: {row[3]} ({row[4]}) | Date: {row[5]}")

def cancel_appointment(cur, conn):
    appointment_id = input("Enter appointment ID to cancel: ")
    cur.execute("DELETE FROM appointments WHERE appointment_id = %s", (appointment_id,))
    conn.commit()
    print("Appointment canceled." if cur.rowcount else "Appointment not found.")

def medical_official_menu(cur, conn):
    while True:
        print("\n--- Medical Official Menu ---")
        print("1. View Hospitals")
        print("2. View Doctors")
        print("3. View All Appointments")
        print("4. Return")
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                view_hospitals(cur)
            elif choice == "2":
                view_doctors(cur)
            elif choice == "3":
                view_appointments(cur)
            elif choice == "4":
                break
            else:
                print("Invalid choice.")
        except mysql.connector.Error as err:
            print("Database error:", err)
        pause()

def medical_patient_menu(cur, conn):
    while True:
        print("\n--- Medical Patient Menu ---")
        print("1. View Hospitals")
        print("2. View Doctors")
        print("3. Book Appointment")
        print("4. See Appointment Status")
        print("5. Cancel Appointment")
        print("6. Return")
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                view_hospitals(cur)
            elif choice == "2":
                view_doctors(cur)
            elif choice == "3":
                book_appointment(cur, conn)
            elif choice == "4":
                phone = input("Enter your phone number: ")
                view_appointments(cur, phone)
            elif choice == "5":
                cancel_appointment(cur, conn)
            elif choice == "6":
                break
            else:
                print("Invalid choice.")
        except mysql.connector.Error as err:
            conn.rollback()
            print("Database error:", err)
        pause()

# ---------------- FINANCIAL SYSTEM ----------------

def financial_system():
    try:
        conn = get_connection(DATABASES["financial"])
        cur = conn.cursor()
    except mysql.connector.Error as err:
        print("Could not connect to Financial database:", err)
        pause()
        return

    while True:
        print("\n===== FINANCIAL SYSTEM =====")
        print("1. Login as Official")
        print("2. Login as Bank Customer")
        print("3. Return to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            financial_official_menu(cur, conn)
        elif choice == "2":
            financial_customer_menu(cur, conn)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

    cur.close()
    conn.close()

def list_banks(cur):
    cur.execute("SELECT id, name FROM banks ORDER BY id")
    for bank in cur.fetchall():
        print(f"{bank[0]}. {bank[1]}")

def create_account(cur, conn):
    name = input("Enter your name: ")
    aadhar = input("Enter your Aadhar number: ")
    cur.execute("SELECT id FROM users WHERE aadhar = %s", (aadhar,))
    user = cur.fetchone()

    if user:
        user_id = user[0]
    else:
        cur.execute("INSERT INTO users (name, aadhar) VALUES (%s,%s)", (name, aadhar))
        conn.commit()
        user_id = cur.lastrowid

    list_banks(cur)
    bank_id = input("Enter bank ID: ")
    cur.execute("SELECT id FROM banks WHERE id = %s", (bank_id,))
    if not cur.fetchone():
        print("Bank not found.")
        return

    cur.execute("SELECT id FROM bank_accounts WHERE user_id = %s AND bank_id = %s", (user_id, bank_id))
    if cur.fetchone():
        print("This bank account already exists.")
        return

    cur.execute("""INSERT INTO bank_accounts
                   (user_id, bank_id, balance, last_transaction)
                   VALUES (%s,%s,%s,%s)""",
                (user_id, bank_id, Decimal("0.00"), datetime.now()))
    conn.commit()
    print("Account created successfully.")

def get_account(cur, aadhar):
    cur.execute("""SELECT ba.id, ba.balance, b.name, u.name
                  FROM bank_accounts ba
                  JOIN users u ON ba.user_id = u.id
                  JOIN banks b ON ba.bank_id = b.id
                  WHERE u.aadhar = %s
                  ORDER BY ba.id""", (aadhar,))
    return cur.fetchone()

def deposit(cur, conn):
    account = get_account(cur, input("Enter your Aadhar number: "))
    if not account:
        print("Account not found.")
        return
    try:
        amount = Decimal(input("Enter amount to deposit: "))
    except InvalidOperation:
        print("Invalid amount.")
        return
    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    account_id, balance, bank, name = account
    cur.execute("UPDATE bank_accounts SET balance=%s, last_transaction=%s WHERE id=%s",
                (balance + amount, datetime.now(), account_id))
    conn.commit()
    print(f"Deposited ₹{amount:.2f} successfully.")

def withdraw(cur, conn):
    account = get_account(cur, input("Enter your Aadhar number: "))
    if not account:
        print("Account not found.")
        return
    try:
        amount = Decimal(input("Enter amount to withdraw: "))
    except InvalidOperation:
        print("Invalid amount.")
        return
    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    account_id, balance, bank, name = account
    if balance < amount:
        print("Insufficient balance.")
        return

    cur.execute("UPDATE bank_accounts SET balance=%s, last_transaction=%s WHERE id=%s",
                (balance - amount, datetime.now(), account_id))
    conn.commit()
    print(f"Withdrew ₹{amount:.2f} successfully.")

def check_balance(cur):
    account = get_account(cur, input("Enter your Aadhar number: "))
    if not account:
        print("Account not found.")
        return
    account_id, balance, bank, name = account
    cur.execute("SELECT last_transaction FROM bank_accounts WHERE id = %s", (account_id,))
    last = cur.fetchone()[0]
    print(f"Bank: {bank}\nCustomer: {name}")
    print(f"Current Balance: ₹{balance:.2f}")
    print("Last Transaction:", last)

def financial_official_menu(cur, conn):
    while True:
        print("\n--- Financial Official Menu ---")
        print("1. View Banks")
        print("2. Create Bank Account")
        print("3. View All Accounts")
        print("4. Return")
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                list_banks(cur)
            elif choice == "2":
                create_account(cur, conn)
            elif choice == "3":
                cur.execute("""SELECT ba.id, u.name, u.aadhar, b.name,
                                      ba.balance, ba.last_transaction
                               FROM bank_accounts ba
                               JOIN users u ON ba.user_id=u.id
                               JOIN banks b ON ba.bank_id=b.id
                               ORDER BY ba.id""")
                for row in cur.fetchall():
                    print(row)
            elif choice == "4":
                break
            else:
                print("Invalid choice.")
        except mysql.connector.Error as err:
            conn.rollback()
            print("Database error:", err)
        pause()

def financial_customer_menu(cur, conn):
    while True:
        print("\n--- Bank Customer Menu ---")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Return")
        choice = input("Enter your choice: ")
        try:
            if choice == "1":
                deposit(cur, conn)
            elif choice == "2":
                withdraw(cur, conn)
            elif choice == "3":
                check_balance(cur)
            elif choice == "4":
                break
            else:
                print("Invalid choice.")
        except mysql.connector.Error as err:
            conn.rollback()
            print("Database error:", err)
        pause()

# ---------------- MAIN MENU ----------------

def main():
    print("Welcome To Public Service Software")
    while True:
        print("\n========== PUBLIC SERVICE SOFTWARE ==========")
        print("1. Municipal System")
        print("2. Medical System")
        print("3. Financial System")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            municipal_system()
        elif choice == "2":
            medical_system()
        elif choice == "3":
            financial_system()
        elif choice == "4":
            print("Thank You For Visiting The Public Service Software")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
