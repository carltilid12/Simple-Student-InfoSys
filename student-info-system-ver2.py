import tkinter as tk
from tkinter import ttk, Tk, Toplevel, Label, Entry, Button, StringVar, messagebox, OptionMenu
import sqlite3
from tkinter import messagebox
from tkinter import simpledialog

# COURSE FUNCTIONS

def add_course():
    course = course_dropdown.get()

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(f"CREATE TABLE IF NOT EXISTS {course} (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, id_no TEXT, gender TEXT, course_code TEXT)")

    conn.commit()
    conn.close()

    # Update the course dropdown menu with the new course
    course_dropdown["values"] = get_courses()

def edit_course():
    selected_course = course_dropdown.get()

    new_course = simpledialog.askstring("Edit Course", "Enter the new course name:", initialvalue=selected_course)
    if new_course:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        # Rename the table using ALTER TABLE statement
        cursor.execute(f"ALTER TABLE {selected_course} RENAME TO {new_course}")

        cursor.execute(f"UPDATE {new_course} SET Course_Code=? WHERE Course_Code=?", (new_course, selected_course))  # Update the course code for the students
        conn.commit()
        conn.close()

        # Update the course dropdown menu with the new course name
        course_dropdown["values"] = get_courses()
        course_dropdown.set(new_course)

        show_students()

def get_courses():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
    tables = cursor.fetchall()

    conn.close()

    courses = [table[0] for table in tables if table[0] != "students"]
    return courses

def delete_course():
    selected_course = course_dropdown.get()

    # Prompt for confirmation
    confirm = messagebox.askyesno("Delete Course", f"Are you sure you want to delete the course '{selected_course}'?")

    if confirm:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        # Delete the course table from the database
        cursor.execute(f"DROP TABLE IF EXISTS {selected_course}")

        conn.commit()
        conn.close()

        # Update the course dropdown menu with the updated list of courses
        course_dropdown["values"] = get_courses()

        # Clear the entry fields and student table
        course_dropdown.set("")

def clear_table():
    student_table.delete(*student_table.get_children())

## STUDENT FUNCTIONS

def add_student():
    dialog = Toplevel()
    dialog.title("Add Student")

    fields = ["Name", "ID No"]
    entries = {}

    for i, field in enumerate(fields):
        label = Label(dialog, text=field)
        label.grid(row=i, column=0, padx=5, pady=5)

        entry = Entry(dialog)
        entry.grid(row=i, column=1, padx=5, pady=5)

        entries[field] = entry

    course_label = Label(dialog, text="Course Code")
    course_label.grid(row=len(fields), column=0, padx=5, pady=5)

    course_dropdown_values = course_dropdown["values"]  # Get the course dropdown values

    course_dropdown_dialog = ttk.Combobox(dialog, values=course_dropdown_values)
    course_dropdown_dialog.grid(row=len(fields), column=1, padx=5, pady=5)

    gender_label = Label(dialog, text="Gender")
    gender_label.grid(row=len(fields)+1, column=0, padx=5, pady=5)

    gender_var = StringVar(dialog)
    gender_var.set("Male")  # Set the default gender

    gender_dropdown = ttk.Combobox(dialog, textvariable=gender_var, values=["Male", "Female", "Other"])
    gender_dropdown.grid(row=len(fields)+1, column=1, padx=5, pady=5)

    def save_student():
        name = entries["Name"].get()
        id_no = entries["ID No"].get()
        course = course_dropdown.get()  # Get the selected course from the dropdown menu
        gender = gender_dropdown.get()  # Get the selected gender from the dropdown menu

        if name and id_no and course and gender:
            if gender == "Other":
                other_gender = simpledialog.askstring("Other Gender", "Enter the specific gender:")
                if other_gender:
                    gender = other_gender
                else:
                    messagebox.showwarning("Missing Information", "Please enter a specific gender.")
                    return

            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()

            # Insert the student into the selected course table
            cursor.execute(f"INSERT INTO {course} (Name, ID_No, Gender, Course_Code) VALUES (?, ?, ?, ?)",
                           (name, id_no, gender, course))

            conn.commit()
            conn.close()

            dialog.destroy()
            show_students()

    save_button = Button(dialog, text="Save", command=save_student)
    save_button.grid(row=len(fields) + 2, columnspan=2, padx=5, pady=10)

    dialog.mainloop()

def edit_student():
    selected_item = student_table.selection()
    if selected_item:
        id_no = student_table.item(selected_item, "values")[1]  # Get the ID_No of the selected student
        course = course_dropdown.get()

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(f"SELECT Name, ID_No, Gender, Course_Code FROM {course} WHERE ID_No=?", (id_no,))
        student_info = cursor.fetchone()

        conn.close()

        if student_info:
            dialog = Toplevel()
            dialog.title("Edit Student")

            fields = ["Name", "ID No"]
            entries = {}

            for i, field in enumerate(fields):
                label = Label(dialog, text=field)
                label.grid(row=i, column=0, padx=5, pady=5)

                entry = Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entry.insert(0, student_info[i])  # Set the current student information in the entry fields

                entries[field] = entry

            course_label = Label(dialog, text="Course Code")
            course_label.grid(row=len(fields), column=0, padx=5, pady=5)

            course_dropdown_values = course_dropdown["values"]  # Get the course dropdown values

            course_dropdown_dialog = ttk.Combobox(dialog, values=course_dropdown_values)
            course_dropdown_dialog.grid(row=len(fields), column=1, padx=5, pady=5)
            course_dropdown_dialog.set(course)  # Set the current course as the default value

            gender_label = Label(dialog, text="Gender")
            gender_label.grid(row=len(fields)+1, column=0, padx=5, pady=5)

            gender_var = StringVar(dialog)
            gender_var.set(student_info[2])  # Set the current gender as the default value

            gender_dropdown = ttk.Combobox(dialog, textvariable=gender_var, values=["Male", "Female", "Other"])
            gender_dropdown.grid(row=len(fields)+1, column=1, padx=5, pady=5)

            def update_student():
                name = entries["Name"].get()
                new_id_no = entries["ID No"].get()
                new_course = course_dropdown_dialog.get()  # Get the selected course from the dropdown menu
                gender = gender_dropdown.get()  # Get the selected gender from the dropdown menu

                if name and new_id_no and new_course and gender:
                    if gender == "Other":
                        other_gender = simpledialog.askstring("Other Gender", "Enter the specific gender:")
                        if other_gender:
                            gender = other_gender
                        else:
                            messagebox.showwarning("Missing Information", "Please enter a specific gender.")
                            return

                    conn = sqlite3.connect("students.db")
                    cursor = conn.cursor()

                    if course != new_course:
                        # Move the student to a different course
                        cursor.execute(f"INSERT INTO {new_course} (Name, ID_No, Gender, Course_Code) VALUES (?, ?, ?, ?)",
                                       (name, new_id_no, gender, new_course))

                        # Delete the student from the current course
                        cursor.execute(f"DELETE FROM {course} WHERE ID_No=?", (id_no,))
                    else:
                        # Update the student information in the current course
                        cursor.execute(f"UPDATE {course} SET Name=?, ID_No=?, Gender=? WHERE ID_No=?", (name, new_id_no, gender, id_no))

                    conn.commit()
                    conn.close()

                    dialog.destroy()
                    show_students()

            update_button = Button(dialog, text="Update", command=update_student)
            update_button.grid(row=len(fields) + 2, columnspan=2, padx=5, pady=10)

            dialog.mainloop()
        else:
            messagebox.showerror("Error", "Selected student not found.")

def show_students():
    course = course_dropdown.get()

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT name, id_no, gender, course_code FROM {course}")
    students = cursor.fetchall()

    conn.close()

    # Clear previous student information table
    clear_table()

    # Display student information in a table
    for student in students:
        student_table.insert('', 'end', values=(student[0], student[1], student[2], student[3]))

###################### Create the main window ###########################

window = tk.Tk()
window.title("Student Information Management System")
window.geometry("800x600")
window.resizable(False, False)

# COURSE 
course_label = tk.Label(window, text="Course:")
course_label.place(x=10, y=10)

course_dropdown = ttk.Combobox(window, values=get_courses())
course_dropdown.place(x=100, y=10)

add_course_button = tk.Button(window, text="Add Course", command=add_course)
add_course_button.place(x=280, y=10)

edit_course_button = tk.Button(window, text="Edit Course", command=edit_course)
edit_course_button.place(x=380, y=10)

delete_course_button = tk.Button(window, text="Delete Course", command=delete_course)
delete_course_button.place(x=480, y=10)

# STUDENT
search_label = tk.Label(window, text="Search Student:")
search_label.place(x=10, y=40)

search_label = tk.Entry(window, text="Search Student:")
search_label.place(x=100, y=40)

add_student_button = tk.Button(window, text="Add Student", command=add_student)
add_student_button.place(x=280, y=40)

show_students_button = tk.Button(window, text="Show Students", command=show_students)
show_students_button.place(x=380, y=40)

edit_student_button = tk.Button(window, text="Edit Student", command=edit_student)
edit_student_button.place(x=480, y=40)

# Create a table to display student information
student_table = ttk.Treeview(window, columns=("Name", "ID No", "Gender", "Course Code"), show="headings")
student_table.heading("Name", text="Name")
student_table.heading("ID No", text="ID No")
student_table.heading("Gender", text="Gender")
student_table.heading("Course Code", text="Course Code")
student_table.place(x=0,y=150)

# Run the main event loop
window.mainloop()
