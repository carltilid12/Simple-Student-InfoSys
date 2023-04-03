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
student = []
for line in read:
    student.append(list(map(str, line[:-1].split(", "))))
        
print(student)
#Selection Mode
while(True):
    print("\nAdd Student Information = 1")
    print("Delete Student Information = 2")
    print("Close Enter Mode = 3")
    choice = int(input())

    if choice == 1: #Add Student Information Choice
        #Getting the information by splitting them into a list
        info = list(map(str, input("Enter Student Info: (firstName, course, year, idNumber): ").split(", ")))
        #Converting the list into a dictionary then appending it to the student list
        student.append(info)
        
    elif choice == 2: #Delete Student Information Choice
        #Deleting a student info using the idNumber
        delete = input("Enter Student idNumber (xxxx-xxxx): ")

        #updating the student list by not including the one that is deleted
        for i in range(len(student)-1):
            print(student[i][3])
            if student[i][3] == delete:
                print("Deleted")
                del student[i]
            
    
    elif choice == 3: #Close the Program Choice
        print("Program Closed")
        break

    else: #Loops the program
        continue

#Making the list into a JSON file and formatting it
with open("Simple-Student-InfoSys/studentinfo.txt", "w") as p:
    for i in student:
        p.write((', '.join(str(e) for e in i))+'\n')