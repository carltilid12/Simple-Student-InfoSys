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

#Load the JSON file as a list to be updated
with open("Simple-Student-InfoSys/studentinfo.json", "r") as read:
    student = json.load(read)

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
        student.append(dict(firstName = info[0].capitalize(), 
                       course = info[1],
                       year = int(info[2]),
                       idNumber = int(info[3].replace('-',''))
                       ))
        
    elif choice == 2: #Delete Student Information Choice
        #Deleting a student info using the idNumber
        delete = input("Enter Student idNumber (xxxx-xxxx): ")
        delete = int(delete.replace('-',''))

        #updating the student list by not including the one that is deleted
        student[:] = [d for d in student if d.get('idNumber') != delete]
    
    elif choice == 3: #Close the Program Choice
        print("Program Closed")
        break

    else: #Loops the program
        continue

#Making the list into a JSON file and formatting it
with open("Simple-Student-InfoSys/studentinfo.json", "w") as p:
            json.dump(student, p, indent=2)