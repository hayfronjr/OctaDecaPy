import tkinter as tk
from tkinter import messagebox

# Contact database
contacts = {}
      



# Function to add contact
def add_contact(name, phone):
    if not name or not phone:
        messagebox.showerror("Error", "Name and phone cannot be empty.")
    elif name in contacts:
        messagebox.showerror("Error", "Contact already exists.")
    else:
        contacts[name] = phone
        messagebox.showinfo("Success", f"Contact '{name}' added successfully.")
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)

# Function to edit contact (update phone number only)
def edit_contact(name, new_phone):
    if not name or not new_phone:
        messagebox.showerror("Error", "Name and new phone cannot be empty.")
    elif name in contacts:
        contacts[name] = new_phone
        messagebox.showinfo("Success", f"Contact '{name}' updated successfully.")
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Contact not found.")



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



    # Autocomplete functions 
def update_suggestions(event):
    typed_text = name_entry.get().strip()
    listbox_suggestions.delete(0, tk.END)

    if typed_text:
        # Match both name and phone
        matches = [f"{name} : {phone}" for name, phone in contacts.items() if name.lower().startswith(typed_text.lower())]
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
        name, rest = selected.split(" : ", 1)
        if ", " in rest:
            phone, email = rest.split(", ", 1)
        else:
            phone, email = rest, ""
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)
        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, phone)
    listbox_suggestions.place_forget()


# Function to view all contacts
def view_contacts():
    if not contacts:
        messagebox.showinfo("Contacts", "No contacts available.")
    else:
        contact_list = "\n".join(f"{name}: {phone}" for name, phone in contacts.items())
        messagebox.showinfo("Contacts", contact_list)



# GUI setup
root = tk.Tk()
root.title("Phonebook")
root.geometry("500x350")

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


# Suggestions Listbox (hidden initially)
listbox_suggestions = tk.Listbox(root, width=30, height=4)
listbox_suggestions.bind("<<ListboxSelect>>", fill_name_from_listbox)
listbox_suggestions.bind("<ButtonRelease-1>", fill_name_from_listbox)

# Bind typing event for autocomplete
name_entry.bind("<KeyRelease>", update_suggestions)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Contact", width=15,
          command=lambda: add_contact(name_entry.get(), phone_entry.get())).grid(row=1, column=0, padx=5, pady=5)

tk.Button(button_frame, text="Edit Contact", width=15,
          command=lambda: edit_contact(name_entry.get(), phone_entry.get())).grid(row=1, column=1, padx=5, pady=5)

tk.Button(button_frame, text="View Contacts", width=15,
          command=view_contacts).grid(row=2, column=0, padx=5, pady=5)

tk.Button(button_frame, text="Delete Contact", width=15,
          command=lambda: delete_contact(name_entry.get())).grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="Exit", width=10, command=root.quit).pack(pady=10)

root.mainloop()