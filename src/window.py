import tkinter as tk
from tkinter import messagebox, ttk
from cryptography.fernet import Fernet
import json
import os

def generate_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists("encryption_key.key"):
        generate_key()
    with open("encryption_key.key", "rb") as key_file:
        key = key_file.read()
    return key

def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    data = {'Website': website, 'Username': username, 'Password': password}
    
    try:
        with open('passwords.json', 'r') as file:
            existing_data = file.read()
            if not existing_data:
                existing_data = '[]'
            passwords = json.loads(existing_data)
    except FileNotFoundError:
        passwords = []

    key = load_key()
    encrypted_data = encrypt_data(json.dumps(data), key)
    
    passwords.append(encrypted_data.decode())
    
    with open('passwords.json', 'w') as file:
        file.write(json.dumps(passwords))
    
    messagebox.showinfo("Success", "Password saved successfully!")

def retrieve_passwords():
    key = load_key()
    try:
        with open('passwords.json', 'r') as file:
            data = file.read()
            passwords = json.loads(data)
            decrypted_passwords = [decrypt_data(password.encode(), key) for password in passwords]
            password_tab = ttk.Frame(notebook)
            notebook.add(password_tab, text='Passwords')

            text_widget = tk.Text(password_tab)
            text_widget.pack()
            text_widget.insert(tk.END, "\n".join(decrypted_passwords))
    except FileNotFoundError:
        messagebox.showinfo("No Passwords", "No passwords stored yet.")

root = tk.Tk()
root.title("Password Manager")

# GUI setup
website_label = tk.Label(root, text="Website:")
website_label.pack()
website_entry = tk.Entry(root)
website_entry.pack()

username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

save_button = tk.Button(root, text="Save Password", command=save_password)
save_button.pack()

retrieve_button = tk.Button(root, text="Retrieve Passwords", command=retrieve_passwords)
retrieve_button.pack()

notebook = ttk.Notebook(root)
notebook.pack()

root.mainloop()
