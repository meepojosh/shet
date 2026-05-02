import sqlite3
import re


itemCount = 0

def connect_db():
    return sqlite3.connect('students.db')

def get_valid_input(prompt, pattern, error_message):
    while True:
        user_input = input(prompt).strip()
        if re.match(pattern, user_input):
            return user_input
        print(f"Error: {error_message}")

def update_item_count():
    global itemCount
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    itemCount = cursor.fetchone()[0]
    conn.close()

def add_student():
    print("\nAdd Student")
    
    student_id = get_valid_input("Student ID (20YY-XXX): ", r"^20\d{2}-\d{3}$", "Must be in 20YY-XXX format.")
    first_name = get_valid_input("First Name: ", r"^[a-zA-Z0-9 .]+$", "Alphanumerical, spaces, and periods only.")
    middle_name = get_valid_input("Middle Name: ", r"^[a-zA-Z0-9 .]+$", "Alphanumerical, spaces, and periods only.")
    last_name = get_valid_input("Last Name: ", r"^[a-zA-Z0-9 .]+$", "Cannot be empty.")
    gender = get_valid_input("Gender (Male, Female, Others please specify): ", r"^(Male|Female|Others.*)$", "Specify Male, Female, or Others.")
    birthdate = get_valid_input("Birthdate (MM/DD/YYYY): ", r"^(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/\d{4}$", "Must be MM/DD/YYYY.")
    birthplace = get_valid_input("Birthplace: ", r"^.+$", "Cannot be empty.")
    email = get_valid_input("Email: ", r"^[\w\.-]+@[\w\.-]+\.\w+$", "Standard email format required.")
    contact_number = get_valid_input("Contact Number: ", r"^(09|\+639)\d{9}$", "Must be +639 or 09 format.")
    section = get_valid_input("Section (Dahlia, Kamia, Rosal, Sampaguita): ", r"^(Dahlia|Kamia|Rosal|Sampaguita)$", "Invalid section.")
    league_color = get_valid_input("League Color (Red, Yellow, Green, Blue): ", r"^(Red|Yellow|Green|Blue)$", "Invalid color.")

    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO students (id, first_name, middle_name, last_name, gender, birthdate, place_of_birth, email_address, contact_number, section, league_color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, first_name, middle_name, last_name, gender, birthdate, birthplace, email, contact_number, section, league_color))
        
        conn.commit()
        print("Student added successfully.")
        update_item_count()
    except sqlite3.IntegrityError:
        print("Error: Student ID or Email already exists!")
    finally:
        conn.close()

def view_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    conn.close()

    if not records:
        print("\nNo student records found in the database.") # Handling empty case [cite: 38]
        return

    print("\nStudent List")
    for row in records:
        print(row)

def update_student():
    student_id = input("\nEnter the Student ID of the record to update (20YY-XXX): ").strip()
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    if not cursor.fetchone():
        print("Student ID not found.")
        conn.close()
        return

    print("Enter new details. The Student ID remains fixed.")
    
    new_email = get_valid_input("New Email: ", r"^[\w\.-]+@[\w\.-]+\.\w+$", "Standard email format required.")
    new_contact = get_valid_input("New Contact Number: ", r"^(09|\+639)\d{9}$", "Must be +639 or 09 format.")
    new_section = get_valid_input("New Section (Dahlia, Kamia, Rosal, Sampaguita): ", r"^(Dahlia|Kamia|Rosal|Sampaguita)$", "Invalid section.")
     
    cursor.execute('''
        UPDATE students 
        SET email_address = ?, contact_number = ?, section = ?
        WHERE id = ?
    ''', (new_email, new_contact, new_section, student_id))
    
    conn.commit()
    conn.close()
    print("Student record updated successfully.")

def delete_student():
    student_id = input("\nEnter the Student ID of the record to delete: ").strip()
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    
    if not cursor.fetchone():
        print("Student ID not found.")
        conn.close()
        return

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    
    update_item_count()
    print("Student deleted successfully.")

def main():
    try:
        update_item_count()
    except sqlite3.OperationalError:
        print("Database or table not found. Please ensure students.db and the schema exist.")
        return

    while True:
        print("\nStudent Information System ====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("Exiting...") 
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()