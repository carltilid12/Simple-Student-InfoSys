import tkinter as tk
from tkinter import ttk, Tk, Toplevel, Label, Entry, Button, StringVar, messagebox, OptionMenu
import sqlite3
from tkinter import messagebox
from tkinter import simpledialog

# COURSE FUNCTIONS

def add_course():
    dialog = Toplevel()
    dialog.title("Add Course")

    # CENTER POP UP
    dialog_width = 300
    dialog_height = 150

    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()

    x = (screen_width / 2) - (dialog_width / 2)
    y = (screen_height / 2) - (dialog_height / 2)

    dialog.geometry(f"{dialog_width}x{dialog_height}+{int(x)}+{int(y)}")

    fields = ["Course Code", "Course Name"]
    entries = {}

    for i, field in enumerate(fields):
        label = Label(dialog, text=field)
        label.grid(row=i, column=0, padx=5, pady=5)

        entry = Entry(dialog, width=32)
        entry.grid(row=i, column=1, padx=5, pady=5)

        entries[field] = entry
        entry.bind("<Return>", lambda event: save_course())

    def save_course(event=None):
        course_code = entries["Course Code"].get()
        course_name = entries["Course Name"].get()

        if course_code and course_name:
            conn = sqlite3.connect("students2.db")
            cursor = conn.cursor()

            cursor.execute("SELECT course_code FROM courses WHERE course_code=?", (course_code,))
            existing_course = cursor.fetchone()

            if existing_course:
                messagebox.showerror("Duplicate Course Code", "A Course with the same Course Code already exists.")
            else:
                # Insert the student into the students table
                cursor.execute("INSERT INTO courses (course_code, course_name) VALUES (?, ?)", (course_code, course_name))
 
            conn.commit()
            conn.close()

            dialog.destroy()

            # Update the course dropdown menu with the new course
            course_dropdown["values"] = [course[0] for course in get_courses()]
            show_all_students()

    save_button = Button(dialog, text="Save", command=save_course)
    save_button.grid(row=len(fields), columnspan=2, padx=5, pady=10)
    dialog.focus_set()
    dialog.mainloop()

def edit_course():
    selected_course = course_dropdown.get()

    dialog = Toplevel()
    dialog.title("Edit Course")

    courses = get_courses()

    selected_course_name = ""
    for course_code, course_name in courses:
        if course_code == selected_course:
            selected_course_name = course_name
            break
    
    # CENTER POP UP
    dialog_width = 300
    dialog_height = 200

    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()

    x = (screen_width / 2) - (dialog_width / 2)
    y = (screen_height / 2) - (dialog_height / 2)

    dialog.geometry(f"{dialog_width}x{dialog_height}+{int(x)}+{int(y)}")

    new_course_code_label = Label(dialog, text="Course Code")
    new_course_code_label.grid(row=0, column=0, padx=5, pady=5)

    new_course_code_entry = Entry(dialog, width=32)
    new_course_code_entry.grid(row=0, column=1, padx=5, pady=5)
    new_course_code_entry.insert(0, selected_course)
    new_course_code_entry.bind("<Return>", lambda event: save_course())

    new_course_name_label = Label(dialog, text="Course Name")
    new_course_name_label.grid(row=1, column=0, padx=5, pady=5)

    new_course_name_entry = Entry(dialog, width=32)
    new_course_name_entry.grid(row=1, column=1, padx=5, pady=5)
    new_course_name_entry.insert(0, selected_course_name)
    new_course_name_entry.bind("<Return>", lambda event: save_course())

    def save_course(event=None):
        new_course_code = new_course_code_entry.get()
        new_course_name = new_course_name_entry.get()
        conn = sqlite3.connect("students2.db")
        cursor = conn.cursor()

        if new_course_code and new_course_name:
            conn.execute("PRAGMA foreign_keys = 1")

            cursor.execute("SELECT course_code FROM courses WHERE course_code=?", (new_course_code,))
            existing_course = cursor.fetchone()

            if existing_course:
                messagebox.showerror("Duplicate Course Code", "A Course with the same Course Code already exists.")
            else:
                # Insert the student into the students table
                cursor.execute("UPDATE courses SET course_code = ?, course_name = ? WHERE course_code = ?", (new_course_code, new_course_name, selected_course))
            

            # Update the course dropdown menu with the new course code and name
            course_dropdown["values"] = [course[0] for course in get_courses()]
            course_dropdown.set(new_course_code)

            dialog.destroy()
            show_students()

        conn.commit()
        conn.close()
    save_button = Button(dialog, text="Save", command=save_course)
    save_button.grid(row=2, columnspan=2, padx=5, pady=10)
    dialog.focus_set()
    dialog.mainloop()

def get_courses():
    conn = sqlite3.connect("students2.db")
    cursor = conn.cursor()

    cursor.execute("SELECT course_code, course_name FROM courses")
    courses = cursor.fetchall()

    conn.close()

    return courses

def delete_course():
    selected_course = course_dropdown.get()
    
    # Prompt for confirmation
    confirm = messagebox.askyesno("Delete Course", f"Are you sure you want to delete the course '{selected_course}'?")

    if confirm:
        conn = sqlite3.connect("students2.db")
        cursor = conn.cursor()

        conn.execute("PRAGMA foreign_keys = 1")
        # Delete the course from the courses table
        cursor.execute("DELETE FROM courses WHERE course_code=?", (selected_course,))

        conn.commit()
        conn.close()

        # Update the course dropdown menu with the updated list of courses
        course_dropdown["values"] = [course[0] for course in get_courses()]
        course_dropdown.current(0)
        show_all_students()



def clear_table():
    student_table.delete(*student_table.get_children())

############ STUDENT FUNCTIONS ######################

def add_student():
    dialog = Toplevel()
    dialog.title("Add Student")

    
    # CENTER POP UP
    dialog_width = 300
    dialog_height = 200

    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()

    x = (screen_width / 2) - (dialog_width / 2)
    y = (screen_height / 2) - (dialog_height / 2)

    dialog.geometry(f"{dialog_width}x{dialog_height}+{int(x)}+{int(y)}")

    fields = ["Name", "ID No"]
    entries = {}

    for i, field in enumerate(fields):
        label = Label(dialog, text=field)
        label.grid(row=i, column=0, padx=5, pady=5)

        entry = Entry(dialog, width=32)
        entry.grid(row=i, column=1, padx=5, pady=5)

        entries[field] = entry
        entry.bind("<Return>", lambda event: save_student())

    course_label = Label(dialog, text="Course Code")
    course_label.grid(row=len(fields), column=0, padx=5, pady=5)

    course_dropdown_values = course_dropdown["values"]  # Get the course dropdown values

    course_var = StringVar(dialog)
    course_var.set(course_dropdown.get())  # Set the default course

    course_dropdown_dialog = ttk.Combobox(dialog, textvariable=course_var, values=course_dropdown_values, state="readonly")
    course_dropdown_dialog.grid(row=len(fields), column=1, padx=5, pady=5)

    year_level_label = Label(dialog, text="Year Level")
    year_level_label.grid(row=len(fields)+1, column=0, padx=5, pady=5)

    year_level_var = StringVar(dialog)
    year_level_var.set("2nd")  # Set the default year

    year_level_dialog = ttk.Combobox(dialog, textvariable=year_level_var, values=["1st", "2nd", "3rd", "4th"], state="readonly")
    year_level_dialog.grid(row=len(fields)+1, column=1, padx=5, pady=5)

    gender_label = Label(dialog, text="Gender")
    gender_label.grid(row=len(fields)+2, column=0, padx=5, pady=5)

    gender_var = StringVar(dialog)
    gender_var.set("Male")  # Set the default gender

    gender_dropdown = ttk.Combobox(dialog, textvariable=gender_var, values=["Male", "Female", "Other"], state="readonly")
    gender_dropdown.grid(row=len(fields)+2, column=1, padx=5, pady=5)

    def save_student(event=None):
        name = entries["Name"].get()
        id_no = entries["ID No"].get()
        course = course_dropdown_dialog.get()  # Get the selected course from the dropdown menu
        year_level = year_level_dialog.get() # Get the selected year level from the dropdown menu
        gender = gender_dropdown.get()  # Get the selected gender from the dropdown menu

        if name and id_no and course and gender:
            if gender == "Other":
                other_gender = simpledialog.askstring("Other Gender", "Enter the specific gender:")
                if other_gender:
                    gender = other_gender
                else:
                    messagebox.showwarning("Missing Information", "Please enter a specific gender.")
                    return

            conn = sqlite3.connect("students2.db")
            cursor = conn.cursor()

            # Check if the ID number already exists in the database
            cursor.execute("SELECT id_no FROM students WHERE id_no=?", (id_no,))
            existing_student = cursor.fetchone()

            if existing_student:
                messagebox.showerror("Duplicate ID Number", "A student with the same ID number already exists.")
            else:
                # Insert the student into the students table
                cursor.execute("INSERT INTO students (ID_No, Name, Gender, Year_Level, Course_Code) VALUES (?, ?, ?, ?, ?)",
                            (id_no, name, gender, year_level, course))

                conn.commit()
                conn.close()

                dialog.destroy()
                show_all_students()


    save_button = Button(dialog, text="Save", command=save_student)
    save_button.grid(row=len(fields) + 3, columnspan=2, padx=5, pady=10)
    dialog.focus_set()
    dialog.mainloop()

def edit_student(event=None):
    selected_item = student_table.selection()
    if selected_item:
        id_no = student_table.item(selected_item, "values")[0]  # Get the ID_No of the selected student
        course = student_table.item(selected_item, "values")[4]

        conn = sqlite3.connect("students2.db")
        cursor = conn.cursor()

        cursor.execute("SELECT Name, Id_No, Gender, Year_Level, Course_Code FROM students WHERE ID_No=?", (id_no,))
        student_info = cursor.fetchone()

        conn.close()

        if student_info:
            dialog = Toplevel()
            dialog.title("Edit Student")

            # CENTER POP UP
            dialog_width = 300
            dialog_height = 200
            screen_width = dialog.winfo_screenwidth()
            screen_height = dialog.winfo_screenheight()
            x = (screen_width / 2) - (dialog_width / 2)
            y = (screen_height / 2) - (dialog_height / 2)
            dialog.geometry(f"{dialog_width}x{dialog_height}+{int(x)}+{int(y)}")

            fields = ["Name", "ID No"]
            entries = {}

            for i, field in enumerate(fields):
                label = Label(dialog, text=field,)
                label.grid(row=i, column=0, padx=5, pady=5)

                entry = Entry(dialog, width=32)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entry.insert(0, student_info[i])  # Set the current student information in the entry fields

                entries[field] = entry
                entry.bind("<Return>", lambda event: update_student())

            course_label = Label(dialog, text="Course Code")
            course_label.grid(row=len(fields), column=0, padx=5, pady=5)

            course_dropdown_values = course_dropdown["values"]  # Get the course dropdown values

            course_dropdown_dialog = ttk.Combobox(dialog, values=course_dropdown_values, state="readonly")
            course_dropdown_dialog.grid(row=len(fields), column=1, padx=5, pady=5)
            course_dropdown_dialog.set(course)  # Set the current course as the default value

            year_level_label = Label(dialog, text="Year Level")
            year_level_label.grid(row=len(fields)+1, column=0, padx=5, pady=5)

            year_level_var = StringVar(dialog)
            year_level_var.set(student_info[3])  # Set the default year

            year_level_dialog = ttk.Combobox(dialog, textvariable=year_level_var, values=["1st", "2nd", "3rd", "4th"], state="readonly")
            year_level_dialog.grid(row=len(fields)+1, column=1, padx=5, pady=5)

            gender_label = Label(dialog, text="Gender")
            gender_label.grid(row=len(fields)+2, column=0, padx=5, pady=5)

            gender_var = StringVar(dialog)
            gender_var.set(student_info[2])  # Set the current gender as the default value

            gender_dropdown = ttk.Combobox(dialog, textvariable=gender_var, values=["Male", "Female", "Other"], state="readonly")
            gender_dropdown.grid(row=len(fields)+2, column=1, padx=5, pady=5)

            def update_student(event=None):
                name = entries["Name"].get()
                new_id_no = entries["ID No"].get()
                new_course = course_dropdown_dialog.get()  # Get the selected course from the dropdown menu
                year_level = year_level_dialog.get() # Get the selected year level from the dropdown menu
                gender = gender_dropdown.get()  # Get the selected gender from the dropdown menu

                if name and new_id_no and new_course and gender:
                    if gender == "Other":
                        other_gender = simpledialog.askstring("Other Gender", "Enter the specific gender:")
                        if other_gender:
                            gender = other_gender
                        else:
                            messagebox.showwarning("Missing Information", "Please enter a specific gender.")
                            return

                    conn = sqlite3.connect("students2.db")
                    cursor = conn.cursor()

                    # Check if the new ID already exists in the database
                    cursor.execute("SELECT ID_No FROM students WHERE ID_No=?", (new_id_no,))
                    existing_id = cursor.fetchone()

                    if existing_id and existing_id[0] != id_no:
                        messagebox.showerror("Error", "Student ID already exists.")
                        conn.close()    
                        return
                    else:
                        # Update the student information in the database
                        cursor.execute("UPDATE students SET ID_No=?, Name=?, Gender=?, Year_Level=?, Course_Code=? WHERE ID_No=?",
                                    (new_id_no, name, gender, year_level, new_course, id_no))

                    conn.commit()
                    conn.close()

                    dialog.destroy()
                    show_all_students()


            update_button = Button(dialog, text="Update", command=update_student)
            update_button.grid(row=len(fields) + 3, columnspan=2, padx=5, pady=10)
            edit_student.running = False
            dialog.focus_set()
            dialog.mainloop()
        else:
            messagebox.showerror("Error", "Selected student not found.")

def delete_student():
    selected_items = student_table.selection()

    if selected_items:
        confirm = messagebox.askyesno("Delete Student(s)", "Are you sure you want to delete the selected student(s)?")
        if confirm:
            conn = sqlite3.connect("students2.db")
            cursor = conn.cursor()

            for selected_item in selected_items:
                id_no = student_table.item(selected_item, "values")[0]  # Get the ID_No of the selected student

                cursor.execute("SELECT ID_No, Name, Gender, Year_Level, Course_Code FROM students WHERE ID_No=?", (id_no,))
                student_info = cursor.fetchone()

                if student_info:
                    # Delete the student from the students table
                    cursor.execute("DELETE FROM students WHERE ID_No=?", (id_no,))

            conn.commit()
            conn.close()

            show_all_students()
    else:
        messagebox.showerror("Error", "No students selected.")


def show_students(event=None):
    course = course_dropdown.get()
    course_name.configure(text=[course[1] for course in get_courses() if course[0] == course_dropdown.get()][0] or "")

    conn = sqlite3.connect("students2.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id_no, name, gender, year_level, course_code FROM students WHERE course_code = ?", (course,))
    students = cursor.fetchall()

    conn.close()

    # Clear previous student information table
    clear_table()

    # Display student information in a table
    for student in students:
        student_table.insert('', 'end', values=(student[0], student[1], student[2], student[3], student[4]))


def show_all_students():
    # Clear existing items in the tree view
    clear_table()

    conn = sqlite3.connect("students2.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id_no, name, gender, year_level, course_code FROM students")
    students = cursor.fetchall()

    conn.close()

    # Add students to the tree view
    for student in students:
        student_table.insert('', 'end', values=(student[0], student[1], student[2], student[3], student[4]))


# SEARCH FUNCTIONS

def search_students(event=None):
    search_query = search_entry.get().lower()  # Get the search query from an Entry widget

    # Clear previous selections
    student_table.selection_remove(student_table.selection())

    for child in student_table.get_children():
        values = student_table.item(child, "values")
        if any(search_query in str(value).lower() for value in values):
            student_table.selection_add(child)  # Add the matching item to the selection

    num_matches = len(student_table.selection())
    student_table.see(student_table.selection())
    if num_matches > 0:
        return
    else:
        messagebox.showinfo("Search", "No matching students found.")

# SORT TABLE
def sort_column(tree, column, reverse=False):
    data = [(tree.set(child, column), child) for child in tree.get_children("")]
    data.sort(reverse=reverse)
    for index, (_, child) in enumerate(data):
        tree.move(child, "", index)
    tree.heading(column, command=lambda c=column: sort_column(tree, c, not reverse))



###################### Create the main window ###########################

window = tk.Tk()
window.title("Student Information Management System")
window.geometry("800x640")
window.configure(bg="#a41c20")
window.resizable(False, False)

# STYLE
buttonStyle = ttk.Style()
buttonStyle.configure("TButton", 
                      width=13, # Set Width
                      )

treeViewStyle = ttk.Style()
treeViewStyle.configure("Treeview",
                background="#f0f0f0",
                foreground="#000000",
                height=20,
                relief="ridge"
                )

# Create tables if tables do not exist

conn = sqlite3.connect("students2.db")
cursor = conn.cursor()
conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support if not already enabled
cursor.execute("CREATE TABLE IF NOT EXISTS courses (course_code TEXT PRIMARY KEY, course_name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS students (id_no TEXT PRIMARY KEY, name TEXT, gender TEXT, year_level TEXT, course_code TEXT, FOREIGN KEY(course_code) REFERENCES courses(course_code) ON DELETE CASCADE ON UPDATE CASCADE)")
conn.commit()
conn.close()

# COURSE 
course_button = ttk.Button(window, text="Select Course", command=show_students, style="TButton")
course_button.place(x=10, y=10)

course_dropdown = ttk.Combobox(window, values=[course[0] for course in get_courses()], width=23, state="readonly")
course_dropdown.bind("<<ComboboxSelected>>", show_students)
course_dropdown.place(x=110, y=10)
if len([course[0] for course in get_courses()]) > 0:
    course_dropdown.current(0)

course_name = ttk.Label(window, text=[course[1] for course in get_courses() if course[0] == course_dropdown.get()][0] or "", width=34)
course_name.place(x=580, y=10)

add_course_button = ttk.Button(window, text="Add Course ", command=add_course, style="TButton")
add_course_button.place(x=280, y=10)

edit_course_button = ttk.Button(window, text="Edit Course", command=edit_course, style="TButton")
edit_course_button.place(x=380, y=10)

delete_course_button = ttk.Button(window, text="Delete Course ", command=delete_course, style="TButton")
delete_course_button.place(x=480, y=10)

# STUDENTS
search_button = ttk.Button(window, text="Search Student", command=search_students, style="TButton")
search_button.place(x=10, y=40)

search_entry = ttk.Entry(window, width=26)
search_entry.bind("<Return>", search_students)
search_entry.place(x=110, y=40)

add_student_button = ttk.Button(window, text="Add Student", command=add_student, style="TButton")
add_student_button.place(x=280, y=40)

edit_student_button = ttk.Button(window, text="Edit Student", command=edit_student, style="TButton")
edit_student_button.place(x=380, y=40)

delete_student_button = ttk.Button(window, text="Delete Student", command=delete_student, style="TButton")
delete_student_button.place(x=480, y=40)

show_all_students_button = ttk.Button(window, text="Show ALL Students", command=show_all_students, width=33)
show_all_students_button.place(x=580, y=40)

# Create a table to display student information
student_table = ttk.Treeview(window, columns=("ID No.", "Name", "Gender", "Year Level", "Course Code"), show="headings", height=25, style="Treeview")

student_table.column("ID No.", width=100, stretch='no')
student_table.column("Name", width=384, stretch=False)
student_table.column("Gender", width=100)
student_table.column("Year Level", width=100)
student_table.column("Course Code", width=100)

student_table.heading("ID No.", text="ID No")
student_table.heading("Name", text="Name")
student_table.heading("Gender", text="Gender")
student_table.heading("Year Level", text="Year Level")
student_table.heading("Course Code", text="Course Code")
student_table.place(x=0,y=80)
edit_student.running = False
student_table.bind("<Double-Button-1>", lambda event: edit_student() if student_table.focus() else None)

scrollbar = ttk.Scrollbar(window, orient="vertical", command=student_table.yview)
student_table.configure(yscrollcommand=scrollbar.set)

# Place the Treeview and scrollbar
scrollbar.place(x=785, y=80, height=525)

for column in ("ID No.", "Name", "Gender", "Year Level", "Course Code"):
    student_table.heading(column, text=column, command=lambda c=column: sort_column(student_table, c))

# Run the main event loop
show_all_students()
window.mainloop()
