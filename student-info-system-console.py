"""
Carl Christian G. Tilid BSCS 2
Simple Student Information Console Version
"""

import json
import tkinter as tk
import tkinter.font as font
import webbrowser

def updateStudent(student):
    with open("studentinfo.txt", "w") as p:
        for i in student:
            p.write((', '.join(str(e) for e in i))+'\n')

def updateCourse(courses):
    with open("courses.txt", "w") as p:
        for i in courses:
            p.write(i+'\n')

#Simple Console Version 
print("Simple Student Information System\n")

#Load the File as a list of students
file = open('studentinfo.txt', 'r')
read = file.readlines()

#Reads the text file and converts it into a list of students
student = []
for line in read:
    student.append(list(map(str, line[:-1].split(", "))))

file = open('courses.txt', 'r')
read = file.readlines()

courses = []
for line in read:
    courses.append(line[:-1])

print("Enter the number corresponding to your choice")
#Selection Mode
while(True):
    print("\nDisplay Courses Available = 1")
    print("Add Course = 2")
    print("Delete Course = 3")
    print("Edit Course Name = 4")
    print("Select Course = 5")
    print("Exit Program = 6\n")
    choice = int(input())

    match choice:

        case 1:
            print("\nCourses Available: ")
            for i in courses:
                print(i)

        case 2:
            print("Enter Course Name: ")
            course = input()
            courses.append(course)
            print("Added "+course+" to list of courses")
            updateCourse(courses)

        case 3:
            print("Input Course to be deleted")
            for i in courses:
                print(i)
            deletecourse = input("Delete: ")
            if deletecourse in courses:
                print("!!! Course Found !!!\nAre you sure you want to delete the course(This will delete student info in course)")
                confirm = str.lower(input("Yes or No: "))
                match confirm:
                    case "yes":
                        print("Deleting Course")
                        for i in reversed(student):
                            if i[2] == deletecourse:
                                student.remove(i)
                        courses.remove(deletecourse)
                        updateCourse(courses)
                        updateStudent(student)
                    case _:
                        print("Canceling Operation")
            else:
                print("Could Not Find the Course")

        case 4:
            print("Input Course to be renamed")
            for i in courses:
                print(i)
            editcourse = input("Edit: ")
            if editcourse in courses:
                print("!!! Course Found !!!")
                newcourse = input("Input new course name: ")
                for i in student:
                    if i[2] == editcourse:
                        i[2] = newcourse
                courses.remove(editcourse)
                courses.append(newcourse)
                updateCourse(courses)
            else:
                print("Could Not Find the Course")
            
        case 5:
            print("Select Course")
            for i in courses:
                print(i)
            selectedcourse = input("Select: ")
            if selectedcourse in courses:
                
                print("\nNow Viewing Course Student Options")
                while(True):
                    print("Add Student Information = 1")
                    print("Edit Student Information = 2")
                    print("Delete Student Information = 3")
                    print("Display Students = 4")
                    print("Close Enter Mode = 5")
                    choice = int(input())
                    match choice:
                        case 1: #Add Student Information Choice

                            #Getting the information by splitting them into a list
                            info = list(map(str, input("Enter Student Info: (firstName, idNumber): ").split(", ")))
                            info.append(selectedcourse)
                            #Append Info As a List
                            student.append(info)
                            updateStudent(student)
                        
                        case 2: #Edit Student Information Choice
                            replace = input("Enter Student idNumber to be Replaced (xxxx-xxxx): ")

                            for i in reversed(student):
                                if (i[2] == selectedcourse and i[1] == replace):
                                    print(i)
                                    info = list(map(str, input("Enter New Student Info: (firstName, idNumber): ").split(", ")))
                                    info.append(selectedcourse)
                                    student.remove(i)
                                    student.append(info)
                                    break
                            updateStudent(student)

                        case 3: #Delete Student Information Choice

                            #Deleting a student info using the idNumber
                            delete = input("Enter Student idNumber (xxxx-xxxx): ")

                            #Delete the student with the id number
                            for i in reversed(student):   
                                if (i[2] == selectedcourse and i[1] == delete):
                                    print(i)
                                    print("Deleted")
                                    student.remove(i)
                                    break
                            updateStudent(student)    

                        case 4: #Display the List of students\
                            for i in student:        
                                if i[2] == selectedcourse:
                                    print(i)

                        
                        case 5: #Close the Program Choice
                            print("Program Closed")
                            break

                        case _: #Loops the program
                            print("Invalid Option")
                            continue         
            else:
                print("Could Not Find the Course")
            
        case 6:
            break
        case _:
            print("Your Choice is not in the selection of choices. \nEnter the number corresponding to your choice\n")


#Writes the txt file with the updated version of the student list

with open("courses.txt", "w") as p:
    for i in courses:
        p.write(i+'\n')
