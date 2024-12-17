import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="iceboy",
            database="student_management"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка подключения к базе данных", f"Ошибка: {err}")
        return None


def get_students():
    conn = connect_to_db()
    if conn is None:
        return []
    cursor = conn.cursor()
    query = "SELECT id, name, surname FROM students"
    cursor.execute(query)
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return students


def get_teachers():
    conn = connect_to_db()
    if conn is None:
        return []
    cursor = conn.cursor()
    query = "SELECT id, name, surname FROM teachers"
    cursor.execute(query)
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()
    return teachers


def add_attendance():
    student_id = student_combobox.get().split()[0]  # Получаем часть с ID
    teacher_id = teacher_combobox.get().split()[0]  # Получаем часть с ID
    date = date_entry.get()
    present = 1 if present_var.get() else 0  # Преобразуем в целое

    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    query = "INSERT INTO attendance (student_id, teacher_id, date, present) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (student_id, teacher_id, date, present))
        conn.commit()
        messagebox.showinfo("Успех", "Посещение успешно добавлено.")
        display_attendance()  # Обновляем данные после добавления
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка: {err}")
    finally:
        cursor.close()
        conn.close()


def display_attendance():
    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    query = "SELECT a.id, s.name, s.surname, a.date, a.present FROM attendance a JOIN students s ON a.student_id = s.id"
    cursor.execute(query)
    attendance = cursor.fetchall()
    cursor.close()
    conn.close()

    attendance_table.delete(*attendance_table.get_children())
    for row in attendance:
        attendance_table.insert("", "end", values=row)


def add_student():
    def save_student():
        name = name_entry.get()
        surname = surname_entry.get()

        conn = connect_to_db()
        if conn is None:
            return
        cursor = conn.cursor()
        query = "INSERT INTO students (name, surname) VALUES (%s, %s)"
        try:
            cursor.execute(query, (name, surname))
            conn.commit()
            messagebox.showinfo("Успех", "Студент успешно добавлен.")
            add_student_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Ошибка", f"Ошибка: {err}")
        finally:
            cursor.close()
            conn.close()

    add_student_window = tk.Toplevel(root)
    add_student_window.title("Добавить студента")

    tk.Label(add_student_window, text="Имя:").grid(row=0, column=0)
    name_entry = tk.Entry(add_student_window)
    name_entry.grid(row=0, column=1)

    tk.Label(add_student_window, text="Фамилия:").grid(row=1, column=0)
    surname_entry = tk.Entry(add_student_window)
    surname_entry.grid(row=1, column=1)

    save_button = tk.Button(add_student_window, text="Сохранить", command=save_student)
    save_button.grid(row=2, column=0, columnspan=2)


def add_teacher():
    def save_teacher():
        name = name_entry.get()
        surname = surname_entry.get()

        conn = connect_to_db()
        if conn is None:
            return
        cursor = conn.cursor()
        query = "INSERT INTO teachers (name, surname) VALUES (%s, %s)"
        try:
            cursor.execute(query, (name, surname))
            conn.commit()
            messagebox.showinfo("Успех", "Преподаватель успешно добавлен.")
            add_teacher_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Ошибка", f"Ошибка: {err}")
        finally:
            cursor.close()
            conn.close()

    add_teacher_window = tk.Toplevel(root)
    add_teacher_window.title("Добавить преподавателя")

    tk.Label(add_teacher_window, text="Имя:").grid(row=0, column=0)
    name_entry = tk.Entry(add_teacher_window)
    name_entry.grid(row=0, column=1)

    tk.Label(add_teacher_window, text="Фамилия:").grid(row=1, column=0)
    surname_entry = tk.Entry(add_teacher_window)
    surname_entry.grid(row=1, column=1)

    save_button = tk.Button(add_teacher_window, text="Сохранить", command=save_teacher)
    save_button.grid(row=2, column=0, columnspan=2)


root = tk.Tk()
root.title("Управление посещениями")

# Размещение элементов интерфейса
tk.Label(root, text="Студент:").grid(row=0, column=0)
student_combobox = ttk.Combobox(root, values=[f"{student[0]} {student[1]} {student[2]}" for student in get_students()])
student_combobox.grid(row=0, column=1)

tk.Label(root, text="Преподаватель:").grid(row=1, column=0)
teacher_combobox = ttk.Combobox(root, values=[f"{teacher[0]} {teacher[1]} {teacher[2]}" for teacher in get_teachers()])
teacher_combobox.grid(row=1, column=1)

tk.Label(root, text="Дата посещения:").grid(row=2, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=2, column=1)

present_var = tk.BooleanVar()
present_checkbutton = tk.Checkbutton(root, text="Присутствовал", variable=present_var)
present_checkbutton.grid(row=3, column=0, columnspan=2)

# Размещение кнопок в ряд
button_frame = tk.Frame(root)
button_frame.grid(row=4, column=0, columnspan=2)

add_button = tk.Button(button_frame, text="Добавить посещение", command=add_attendance)
add_button.grid(row=0, column=0, padx=5)

display_button = tk.Button(button_frame, text="Показать посещения", command=display_attendance)
display_button.grid(row=0, column=1, padx=5)

add_student_button = tk.Button(button_frame, text="Добавить студента", command=add_student)
add_student_button.grid(row=0, column=2, padx=5)

add_teacher_button = tk.Button(button_frame, text="Добавить преподавателя", command=add_teacher)
add_teacher_button.grid(row=0, column=3, padx=5)

attendance_table = ttk.Treeview(root, columns=("id", "name", "surname", "date", "present"), show="headings")
attendance_table.heading("id", text="ID")
attendance_table.heading("name", text="Имя")
attendance_table.heading("surname", text="Фамилия")
attendance_table.heading("date", text="Дата")
attendance_table.heading("present", text="Присутствовал")
attendance_table.grid(row=5, column=0, columnspan=2)

root.mainloop()