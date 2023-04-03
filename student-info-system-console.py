"""
Carl Christian G. Tilid BSCS 2
Simple Student Information Console Version
"""
import json
import requests
import tkinter as tk
import tkinter.font as font
import webbrowser

#Simple Console Version 
print("Simple Student Information")

#Load the File as a list of students
file = open('Simple-Student-InfoSys/studentinfo.txt', 'r')
read = file.readlines()

#Reads the text file and converts it into a list of students
student = []
for line in read:
    student.append(list(map(str, line[:-1].split(", "))))

#Selection Mode
while(True):
    print("\nAdd Student Information = 1")
    print("Edit Student Information = 2")
    print("Delete Student Information = 3")
    print("Display Students = 4")
    print("Close Enter Mode = 5")
    choice = int(input())

    if choice == 1: #Add Student Information Choice

        #Getting the information by splitting them into a list
        info = list(map(str, input("Enter Student Info: (firstName, course, year, idNumber): ").split(", ")))

        #Append Info As a List
        student.append(info)
    
    elif choice == 2: #Edit Student Information Choice
        replace = input("Enter Student idNumber to be Replaced (xxxx-xxxx): ")
        for i in range(len(student)):
            if student[i][3] == replace:
                print(student[i])
                info = list(map(str, input("Enter New Student Info: (firstName, course, year, idNumber): ").split(", ")))
                student[i] = info
                break
            
            elif i == len(student):
                print("Student Not Found")

    elif choice == 3: #Delete Student Information Choice

        #Deleting a student info using the idNumber
        delete = input("Enter Student idNumber (xxxx-xxxx): ")

        #Delete the student with the id number
        for i in range(len(student)):
            if student[i][3] == delete:
                print(student[i])
                print("Deleted")
                del student[i]

    elif choice == 4: #Display the List of students        
        print(student)
    
    elif choice == 5: #Close the Program Choice
        print("Program Closed")
        break

    else: #Loops the program
        continue

#Writes the txt file with the updated version of the student list
with open("Simple-Student-InfoSys/studentinfo.txt", "w") as p:
    for i in student:
        p.write((', '.join(str(e) for e in i))+'\n')