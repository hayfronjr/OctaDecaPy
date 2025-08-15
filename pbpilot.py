import tkinter as tk
from tkinter import messagebox

# Contact database: {name: [phone, email]}
contacts = {
    "Elijah Asamoah": ["050987124", "elijah@gmail.com"],
    "Selby Frimpong": ["050987621", "selbyfrim@gmail.com"],
    "Kwesi Kwateng": ["054789901", "kwesikwa@gmail.com"],
    "Kojo Bonsu": ["0243561720", "bonsuko@gmail.com"],
    "Kimberly Asante": ["0549087612", "kimberly@gmail.com"],
    "Paa Kwesi Arthur": ["050987621", "paakwesi@gmail.com"],
    "William Afrifah": ["0509577018", "willafrifah@gmail.com"]
}

# Function to add contact
def add_contact(name, phone, email):
    if not name or not phone or not email:
        messagebox.showerror("Error", "All fields must be filled.")
    elif name in contacts:
        messagebox.showerror("Error", "Contact already exists.")
    else:
        contacts[name] = [phone, email]
        messagebox.showinfo("Success", f"Contact '{name}' added successfully.")
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

# Function to edit contact (update phone and email)
def edit_contact(name, new_phone, new_email):
    if not name or not new_phone or not new_email:
        messagebox.showerror("Error", "All fields must be filled.")
    elif name in contacts:
        contacts[name] = [new_phone, new_email]
        messagebox.showinfo("Success", f"Contact '{name}' updated successfully.")
    else:
        messagebox.showerror("Error", "Contact not found.")
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

# Function to view all contacts
def view_contacts():
    if not contacts:
        messagebox.showinfo("Contacts", "No contacts available.")
    else:
        contact_list = "\n".join(f"{name}: {phone}, {email}" for name, (phone, email) in contacts.items())
        messagebox.showinfo("Contacts", contact_list)

# Function to delete contact
def delete_contact(name):
    if not name:
        messagebox.showerror("Error", "Name cannot be empty.")
    elif name in contacts:
        del contacts[name]
        messagebox.showinfo("Success", f"Contact '{name}' deleted successfully.")
    else:
        messagebox.showerror("Error", "Contact not found.")
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Autocomplete functions 
def update_suggestions(event):
    typed_text = name_entry.get().strip()
    listbox_suggestions.delete(0, tk.END)

    if typed_text:
        matches = [
            f"{name} : {phone} , {email}"
            for name, (phone, email) in contacts.items()
            if name.lower().startswith(typed_text.lower())
        ]
        if matches:
            listbox_suggestions.place(
                x=name_entry.winfo_x() + frame.winfo_x(),
                y=name_entry.winfo_y() + frame.winfo_y() + name_entry.winfo_height()
            )
            for match in matches:
                listbox_suggestions.insert(tk.END, match)
        else:
            listbox_suggestions.place_forget()
    else:
        listbox_suggestions.place_forget()

def fill_name_from_listbox(event):
    selected = listbox_suggestions.get(tk.ACTIVE)
    if " : " in selected:
        name_part = selected.split(" : ", 1)[1]
        phone_email = name_part.split(" , ")
        if len(phone_email) == 2:
            name = selected.split(" : ", 1)[0]
            phone, email = phone_email
            name_entry.delete(0, tk.END)
            name_entry.insert(0, name)
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, phone.strip())
            email_entry.delete(0, tk.END)
            email_entry.insert(0, email.strip())
    listbox_suggestions.place_forget()

# GUI setup
root = tk.Tk()
root.title("Phonebook")
root.geometry("500x400")

tk.Label(root, text="Phonebook", font=("Helvetica", 16)).pack(pady=10)

# Input Frame
frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="e")
name_entry = tk.Entry(frame, width=30)
name_entry.grid(row=0, column=1)

tk.Label(frame, text="Phone:").grid(row=1, column=0, sticky="e")
phone_entry = tk.Entry(frame, width=30)
phone_entry.grid(row=1, column=1)

tk.Label(frame, text="Email:").grid(row=2, column=0, sticky="e")
email_entry = tk.Entry(frame, width=30)
email_entry.grid(row=2, column=1)

# Suggestions Listbox (hidden initially)
listbox_suggestions = tk.Listbox(root, width=40, height=4)
listbox_suggestions.bind("<<ListboxSelect>>", fill_name_from_listbox)
listbox_suggestions.bind("<ButtonRelease-1>", fill_name_from_listbox)

# Bind typing event for autocomplete
name_entry.bind("<KeyRelease>", update_suggestions)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Contact", width=15,
          command=lambda: add_contact(name_entry.get(), phone_entry.get(), email_entry.get())).grid(row=0, column=0, padx=5, pady=5)

tk.Button(button_frame, text="Edit Contact", width=15,
          command=lambda: edit_contact(name_entry.get(), phone_entry.get(), email_entry.get())).grid(row=0, column=1, padx=5, pady=5)

tk.Button(button_frame, text="View Contacts", width=15,
          command=view_contacts).grid(row=1, column=0, padx=5, pady=5)

tk.Button(button_frame, text="Delete Contact", width=15,
          command=lambda: delete_contact(name_entry.get())).grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Exit", width=10, command=root.quit).pack(pady=10)

root.mainloop()