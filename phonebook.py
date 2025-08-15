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

# Function to edit contact (update phone number only)
def edit_contact(name, new_phone):
    if not name or not new_phone:
        messagebox.showerror("Error", "Name and new phone cannot be empty.")
    elif name in contacts:
        contacts[name] = new_phone
        messagebox.showinfo("Success", f"Contact '{name}' updated successfully.")
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

#View Contacts frame
view_frame = tk.Frame(root)
view_frame.pack(pady=10)
tk.Label(view_frame, text="Contacts:", font=("Helvetica", 14)).grid(row=0, column=0, sticky="w")
# Display contacts on startup
view_frame.grid_rowconfigure(1, weight=1)
view_frame.grid_columnconfigure(0, weight=1)    
def display_contacts():
    for widget in view_frame.winfo_children():
        if isinstance(widget, tk.Label) and widget.grid_info()['row'] > 0:
            widget.destroy()
        else:
            continue

    row = 1
    for name, phone in contacts.items():
        tk.Label(view_frame, text=f"{name}: {phone}").grid(row=row, column=0, sticky="w")
        row += 1
        display_contacts()
        






# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Contact", width=15,
          command=lambda: add_contact(name_entry.get(), phone_entry.get())).grid(row=0, column=0, padx=5, pady=5)

tk.Button(button_frame, text="Edit Contact", width=15,
          command=lambda: edit_contact(name_entry.get(), phone_entry.get())).grid(row=1, column=0, padx=5, pady=5)

tk.Button(button_frame, text="Delete Contact", width=15,
          command=lambda: delete_contact(name_entry.get())).grid(row=2, column=0, padx=5, pady=5)

tk.Button(root, text="Exit", width=10, command=root.quit).pack(pady=10)

root.mainloop()