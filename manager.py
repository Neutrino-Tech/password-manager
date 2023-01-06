#Imports
import tkinter as tk
from tkinter import ttk
from tkinter import *
import mysql.connector
import random
import os

#Mainwindow executes after entering right master password
class MainWindow(tk.Tk):
    def __init__(self):
        # Connect SQL
        super().__init__()
        self.title("Password Manager")
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="password_manager"
        )
        #Creating table password_manager
        cursor = db.cursor()
        cursor.execute("CREATE TABLE password_manager ( id INTEGER PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, website VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL )")

        # Add the Name, Username, Website, and Password fields in tkinter
        name_label = tk.Label(self, text="Name:")
        name_label.grid(row=0, column=0)
        name_entry = tk.Entry(self)
        name_entry.grid(row=0, column=1)

        username_label = tk.Label(self, text="Username:")
        username_label.grid(row=1, column=0)
        username_entry = tk.Entry(self)
        username_entry.grid(row=1, column=1)

        website_label = tk.Label(self, text="Website:")
        website_label.grid(row=2, column=0)
        website_entry = tk.Entry(self)
        website_entry.grid(row=2, column=1)

        password_label = tk.Label(self, text="Password:")
        password_label.grid(row=3, column=0)
        password_entry = tk.Entry(self, show="*")
        password_entry.grid(row=3, column=1)

        # Password Generate Button
        generate_button = tk.Button(self, text="Generate Password")
        generate_button.grid(row=4, column=2)

        save_button = tk.Button(self, text="Save")
        save_button.grid(row=5, column=1)

        length_label = tk.Label(self, text="Length:")
        length_label.grid(row=4, column=0)

        length_entry = tk.Entry(self)
        length_entry.grid(row=4, column=1)

        #Function to create Random password of desired length
        def generate_password():
            length = int(length_entry.get())
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+=-"
            password = "".join(random.choice(chars) for i in range(length))
            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)


        # Attach the generate_password function to the Generate button
        generate_button["command"] = generate_password

        # Function to save the entered details to the database
        def save_details(name, username, website, password):
            cursor = db.cursor()
            cursor.execute("INSERT INTO password_manager (id, name, username, website, password) VALUES (NULL, %s, %s, %s, %s)", (name, username, website, password))
            db.commit()
            show_details()
        # Attach the save_details function to the Save button
        save_button["command"] = lambda: save_details(
            name_entry.get(),
            username_entry.get(),
            website_entry.get(),
            password_entry.get()
            )   

        # Create a Treeview widget to show the saved details
        tree = ttk.Treeview(self)
        tree["columns"] = ("name","username", "website", "password")
        tree.heading("name", text="Name")
        tree.heading("username", text="Username")
        tree.heading("website", text="Website")
        tree.heading("password", text="Password")
        tree.grid(row=6, column=0, columnspan=2)

        # Function to delete the selected item from the Treeview widget and the database
        def delete_item():
            item = tree.selection()[0]
            item_values = tree.item(item)["values"]
            cursor = db.cursor()
            # Delete the selected item from the password_manager table
            cursor.execute("DELETE FROM password_manager WHERE name = %s AND username = %s", (item_values[0], item_values[1]))
            db.commit()

            # Remove the selected item from the Treeview widget
            tree.detach(item)

        #Delete button
        delete_button = tk.Button(self, text="Delete", command=delete_item)

        # Place the Delete button in a column next to the Treeview
        delete_button.grid(row=7, column=1, sticky="nsew")
        # Function to show all the saved details
        def show_details():
            for i in tree.get_children():
                tree.delete(i)

            # Retrieve all the rows from the password_manager table
            cursor = db.cursor()
            cursor.execute("SELECT * FROM password_manager")
            rows = cursor.fetchall()

            for row in rows:
                tree.insert("", "end", text=row[0], values=(row[1], row[2], row[3], row[4]))

        # Show the saved details 
        show_details()
        db.close()

start_page = tk.Tk()
start_page.title("Start Page")
label = tk.Label(start_page, text="Welcome to My Password Manager")
label.grid(row=0, column=1, columnspan=2)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=1)

password_label = tk.Label(start_page, text="Enter master password:")
password_label.grid(row=2, column=0)

password_entry = tk.Entry(start_page, show="*")
password_entry.grid(row=2, column=1)


def check_password():
    entered_password = password_entry.get()

    # Read the password from the master.txt file, change the name here if you want
    with open("master.txt", "r") as file:
        password = file.read().strip() #strip otherwise \n will be readen

    if entered_password == password:
        start_page.destroy() #if matches close the start page window
        main_window = MainWindow()
        main_window.mainloop()
    else:
        error_message = tk.Label(start_page, text="Incorrect password. Please try again.")
        error_message.grid(row=2, column=0, columnspan=2)


submit_button = tk.Button(start_page, text="Submit", command=check_password)
submit_button.grid(row=2, column=2, columnspan=2)

start_page.mainloop()
