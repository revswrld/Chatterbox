import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class ChatterboxApp:
    def __init__(self, root):
        # initialize
        self.root = root
        self.root.title("Chatterbox - Contact Manager")
        self.root.geometry("300x350")  # Set initial window size
        self.contacts = self.load_contacts()

        # ui setup (contact list, add contact, remove contact)
        self.contact_listbox = tk.Listbox(root)
        self.contact_listbox.pack(fill=tk.BOTH, expand=True)
        self.contact_listbox.bind("<<ListboxSelect>>", self.display_contact_info)

        self.add_button = tk.Button(root, text="Add Contact", command=self.add_contact)
        self.add_button.pack(fill=tk.X)
        
        self.remove_button = tk.Button(root, text="Remove Contact", command=self.remove_contact)
        self.remove_button.pack(fill=tk.X)
        
        self.load_contact_list()
    
    def load_contacts(self):
        # loads contacts from a JSON file, returning an empty dictionary if the file does not exist
        try:
            with open("contacts.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
    
    def save_contacts(self):
        # saves contacts to JSON file
        with open("contacts.json", "w") as file:
            json.dump(self.contacts, file, indent=4)
    
    def load_contact_list(self):
        # loads contacts from JSON file to contact display list
        self.contact_listbox.delete(0, tk.END)
        for name in self.contacts:
            self.contact_listbox.insert(tk.END, name)
    
    def add_contact(self):
        # prompts contact detail when adding new contact
        name = simpledialog.askstring("Add Contact", "Enter contact name:")
        if name and name.strip():
            phone = simpledialog.askstring("Add Contact", "Enter phone number:")
            email = simpledialog.askstring("Add Contact", "Enter email:")
            birthday = simpledialog.askstring("Add Contact", "Enter birthday:")
            address = simpledialog.askstring("Add Contact", "Enter address:")
            notes = simpledialog.askstring("Add Contact", "Enter notes:")
            
            self.contacts[name] = {
                "phone": phone or "",
                "email": email or "",
                "birthday": birthday or "",
                "address": address or "",
                "notes": notes or ""
            }
            self.save_contacts()
            self.load_contact_list()
    
    def remove_contact(self):
        # removes the selected contact from the list after confirmation
        selected = self.contact_listbox.curselection()
        if selected:
            name = self.contact_listbox.get(selected)
            if messagebox.askyesno("Confirm", f"Are you sure you want to delete {name}?"):
                del self.contacts[name]
                self.save_contacts()
                self.load_contact_list()
    
    def display_contact_info(self, event):
        # displays the selected contact details in a message box
        selected = self.contact_listbox.curselection()
        if selected:
            name = self.contact_listbox.get(selected)
            details = self.contacts.get(name, {})
            info = f"Name: {name}\n"
            info += f"Phone: {details.get('phone', 'N/A')}\n"
            info += f"Email: {details.get('email', 'N/A')}\n"
            info += f"Birthday: {details.get('birthday', 'N/A')}\n"
            info += f"Address: {details.get('address', 'N/A')}\n"
            info += f"Notes: {details.get('notes', 'N/A')}"
            messagebox.showinfo("Contact Info", info)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatterboxApp(root)
    root.mainloop()
