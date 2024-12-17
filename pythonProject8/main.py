import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, timedelta

def connect_to_database():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="iceboy",
            database="clinic"
        )
        return db
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка БД", f"Не удается подключиться к базе данных: {err}")
        return None

def fetch_doctors():
    db = connect_to_database()
    if db is None:
        return []
    cursor = db.cursor()
    cursor.execute("SELECT doctor_id, name FROM doctors")
    doctors = cursor.fetchall()
    cursor.close()
    db.close()
    return doctors

def fetch_patients():
    db = connect_to_database()
    if db is None:
        return []
    cursor = db.cursor()
    cursor.execute("SELECT client_id, name FROM patients")
    patients = cursor.fetchall()
    cursor.close()
    db.close()
    return patients

def fetch_appointments():
    db = connect_to_database()
    if db is None:
        return []
    cursor = db.cursor()
    cursor.execute("""
        SELECT a.appointment_id, d.name AS doctor_name, p.name AS patient_name, a.appointment_date
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.doctor_id
        JOIN patients p ON a.patient_id = p.client_id
        ORDER BY a.appointment_date
    """)
    appointments = cursor.fetchall()
    cursor.close()
    db.close()
    return appointments

def show_appointments():
    appointments = fetch_appointments()
    if not appointments:
        messagebox.showinfo("Информация", "Нет ближайших приемов.")
        return

    appointments_window = tk.Toplevel(root)
    appointments_window.title("Ближайшие приемы")

    tree = ttk.Treeview(appointments_window, columns=("ID", "Врач", "Пациент", "Дата"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Врач", text="Врач")
    tree.heading("Пациент", text="Пациент")
    tree.heading("Дата", text="Дата")

    for appointment in appointments:
        tree.insert("", tk.END, values=appointment)

    tree.pack(expand=True, fill=tk.BOTH)

    ttk.Button(appointments_window, text="Закрыть", command=appointments_window.destroy).pack()

def update_doctor_combo():
    doctors = fetch_doctors()
    doctor_combo['values'] = [f"{doc[0]} {doc[1]}" for doc in doctors]
    doctor_combo.set('')

def update_patient_combo():
    patients = fetch_patients()
    patient_combo['values'] = [f"{pat[0]} {pat[1]}" for pat in patients]
    patient_combo.set('')

def add_doctor():
    name = doctor_name_entry.get()
    db = connect_to_database()
    if db is None:
        return
    cursor = db.cursor()
    cursor.execute("INSERT INTO doctors (name) VALUES (%s)", (name,))
    db.commit()
    cursor.close()
    db.close()
    messagebox.showinfo("Успех", "Врач успешно добавлен!")
    update_doctor_combo()

def add_patient():
    name = patient_name_entry.get()
    db = connect_to_database()
    if db is None:
        return
    cursor = db.cursor()
    cursor.execute("INSERT INTO patients (name) VALUES (%s)", (name,))
    db.commit()
    cursor.close()
    db.close()
    messagebox.showinfo("Успех", "Пациент успешно добавлен!")
    update_patient_combo()

def schedule_appointment():
    doctor_id = doctor_combo.get().split()[0]  # ID врача
    patient_id = patient_combo.get().split()[0]  # ID пациента
    date = appointment_date_combo.get()  # Получаем дату из комбобокса

    db = connect_to_database()
    if db is None:
        return
    cursor = db.cursor()
    cursor.execute("INSERT INTO appointments (doctor_id, patient_id, appointment_date) VALUES (%s, %s, %s)",
                   (doctor_id, patient_id, date))
    db.commit()
    cursor.close()
    db.close()
    messagebox.showinfo("Успех", "Прием успешно назначен!")

def generate_dates():
    today = datetime.now()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]  # Генерируем даты на неделю вперед

root = tk.Tk()
root.title("Система управления клиникой")

ttk.Label(root, text="Добавить врача:").grid(row=0, column=0)
doctor_name_entry = ttk.Entry(root)
doctor_name_entry.grid(row=0, column=1)
ttk.Button(root, text="Добавить врача", command=add_doctor).grid(row=0, column=2)

ttk.Label(root, text="Добавить пациента:").grid(row=1, column=0)
patient_name_entry = ttk.Entry(root)
patient_name_entry.grid(row=1, column=1)
ttk.Button(root, text="Добавить пациента", command=add_patient).grid(row=1, column=2)

ttk.Label(root, text="Записать на прием:").grid(row=2, column=0)
ttk.Label(root, text="Врач:").grid(row=3, column=0)
doctors = fetch_doctors()
doctor_combo = ttk.Combobox(root, values=[f"{doc[0]} {doc[1]}" for doc in doctors])
doctor_combo.grid(row=3, column=1)

ttk.Label(root, text="Пациент:").grid(row=4, column=0)
patients = fetch_patients()
patient_combo = ttk.Combobox(root, values=[f"{pat[0]} {pat[1]}" for pat in patients])
patient_combo.grid(row=4, column=1)

ttk.Label(root, text="Дата приема:").grid(row=5, column=0)
appointment_date_combo = ttk.Combobox(root, values=generate_dates())  # Генерируем даты
appointment_date_combo.grid(row=5, column=1)

ttk.Button(root, text="Назначить прием", command=schedule_appointment).grid(row=6, column=0, columnspan=2)

ttk.Button(root, text="Показать ближайшие приемы", command=show_appointments).grid(row=7, column=0, columnspan=2)

update_doctor_combo()
update_patient_combo()

root.mainloop()
