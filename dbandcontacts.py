import tkinter as tk
from tkinter import messagebox
import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add contact
def add_contact(name, phone):
    if not name or not phone:
        messagebox.showerror("Error", "Name and phone cannot be empty.")
        return
    try:
        conn = sqlite3.connect('phonebook.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Contact '{name}' added successfully.")
        display_contacts()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Contact already exists.")

# Edit contact
def edit_contact(name, new_phone):
    if not name or not new_phone:
        messagebox.showerror("Error", "Name and new phone cannot be empty.")
        return
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE contacts SET phone = ? WHERE name = ?', (new_phone, name))
    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Contact not found.")
    else:
        messagebox.showinfo("Success", f"Contact '{name}' updated successfully.")
        display_contacts()
    conn.commit()
    conn.close()

# Delete contact
def delete_contact(name):
    if not name:
        messagebox.showerror("Error", "Name cannot be empty.")
        return
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE name = ?', (name,))
    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Contact not found.")
    else:
        messagebox.showinfo("Success", f"Contact '{name}' deleted successfully.")
        display_contacts()
    conn.commit()
    conn.close()

# Display contacts
def display_contacts():
    for widget in view_frame.winfo_children():
        if isinstance(widget, tk.Label) and widget.grid_info()['row'] > 0:
            widget.destroy()

    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, phone FROM contacts ORDER BY name')
    rows = cursor.fetchall()
    conn.close()

    row = 1
    for name, phone in rows:
        tk.Label(view_frame, text=f"{name}: {phone}").grid(row=row, column=0, sticky="w")
        row += 1

# GUI setup
root = tk.Tk()
root.title("Phonebook")
root.geometry("500x400")

init_db()

tk.Label(root, text="Phonebook", font=("Helvetica", 16)).pack(pady=10)

# Input Frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="e")
name_entry = tk.Entry(frame, width=30)
name_entry.grid(row=0, column=1)

tk.Label(frame, text="Phone:").grid(row=1, column=0, sticky="e")
phone_entry = tk.Entry(frame, width=30)
phone_entry.grid(row=1, column=1)

# Action Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add", command=lambda: add_contact(name_entry.get(), phone_entry.get())).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Edit", command=lambda: edit_contact(name_entry.get(), phone_entry.get())).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=lambda: delete_contact(name_entry.get())).grid(row=0, column=2, padx=5)

# View Contacts Frame
view_frame = tk.Frame(root)
view_frame.pack(pady=10)
tk.Label(view_frame, text="Contacts:", font=("Helvetica", 14)).grid(row=0, column=0, sticky="w")

display_contacts()

root.mainloop()