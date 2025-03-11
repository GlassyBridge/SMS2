import gspread
from google.oauth2.service_account import Credentials
import customtkinter as ctk
from tkinter import messagebox
from login import LoginPage

# Google Sheets Authentication
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Google Sheets IDs
inventory_sheetid = "1FuJwUJqBWRJ_LrzId2UGue9BKaN4dGET5lEXJUh3NsQ"
credentials_sheetid = "12o99nw_bM8_ZEDbmyGZz0fceCEFuDLj3s3YZATDp454"

# Access the sheets
inventory_sheet = client.open_by_key(inventory_sheetid).sheet1
credentials_sheet = client.open_by_key(credentials_sheetid).sheet1

class AdminPage:
    def __init__(self):
        self.display = ctk.CTk()
        self.display.title("Admin Page")
        self.display.geometry("550x500")
        self.display.config(background="#2E2E2E")
        self.setup_ui()
        self.display.mainloop()

    # Sets up the UI
    def setup_ui(self):
        # Log Out Button
        ctk.CTkButton(self.display, text="Log Out", fg_color="red", text_color="white", font=("Helvetica", 12, 'bold'),
                      command=self.logout).place(x=10, y=10)

        # Admin Dashboard Label
        ctk.CTkLabel(self.display, text="Admin Dashboard", font=("Helvetica", 24, 'bold'), text_color="#4CAF50").pack(pady=20)

        # Inventory Management Frame
        inventory_frame = ctk.CTkFrame(self.display, fg_color="#ffffff", corner_radius=10)
        inventory_frame.pack(pady=20, padx=20, fill="x")
        ctk.CTkLabel(inventory_frame, text="Inventory Management", font=("Helvetica", 18, 'bold'), text_color="#4CAF50").pack(pady=10)
        ctk.CTkButton(inventory_frame, text="Add Material", command=self.add_material, width=200, fg_color="#4CAF50",
                      text_color="white", font=("Helvetica", 12)).pack(pady=5)
        ctk.CTkButton(inventory_frame, text="Update Material", command=self.update_material, width=200, fg_color="#FF9800",
                      text_color="white", font=("Helvetica", 12)).pack(pady=5)
        ctk.CTkButton(inventory_frame, text="Remove Material", command=self.remove_material, width=200, fg_color="#F44336",
                      text_color="white", font=("Helvetica", 12)).pack(pady=5)
        ctk.CTkButton(inventory_frame, text="Show All Inventory", command=self.show_all_inventory, width=200, fg_color="#2196F3",
                      text_color="white", font=("Helvetica", 12)).pack(pady=10)

        # User Management Frame
        user_frame = ctk.CTkFrame(self.display, fg_color="#ffffff", corner_radius=10)
        user_frame.pack(pady=20, padx=20, fill="x")
        ctk.CTkLabel(user_frame, text="User Management", font=("Helvetica", 18, 'bold'), text_color="#4CAF50").pack(pady=10)
        ctk.CTkButton(user_frame, text="Add User", command=self.add_user, width=200, fg_color="#4CAF50", text_color="white",
                      font=("Helvetica", 12)).pack(pady=5)
        ctk.CTkButton(user_frame, text="Remove User", command=self.remove_user, width=200, fg_color="#F44336", text_color="white",
                      font=("Helvetica", 12)).pack(pady=5)

    # Logs out the admin and opens the login page
    def logout(self):
        self.display.destroy()
        LoginPage()

    # Modifies the accounts in the credentials sheet
    def modify_credentials(self, email, password, role="user", remove=False):
        try:
            if remove:
                # Remove user by email
                cell = credentials_sheet.find(email)
                if cell:
                    credentials_sheet.delete_row(cell.row)
                    messagebox.showinfo("Success", "User removed successfully!")
                else:
                    messagebox.showerror("Error", "User not found!")
            else:
                # Adding a new user to the credentials sheet
                credentials_sheet.append_row([role, email, password])
                messagebox.showinfo("Success", "User added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Modifies the inventory in the inventory sheet
    def modify_inventory(self, name, quantity=None, remove=False):
        try:
            if remove:
                # Remove material by name
                cell = inventory_sheet.find(name)
                if cell:
                    inventory_sheet.delete_row(cell.row)
                    messagebox.showinfo("Success", "Material removed successfully!")
                else:
                    messagebox.showerror("Error", "Material not found!")
            else:
                # Update or add material
                cell = inventory_sheet.find(name)
                if cell:
                    if quantity:
                        inventory_sheet.update_cell(cell.row, 2, quantity)  # Update quantity
                        messagebox.showinfo("Success", "Material updated successfully!")
                else:
                    if quantity:
                        inventory_sheet.append_row([name, quantity])  # Add new material
                        messagebox.showinfo("Success", "Material added successfully!")
        except gspread.exceptions.CellNotFound:
            if not remove:
                inventory_sheet.append_row([name, quantity])  # Add new material if not found
                messagebox.showinfo("Success", "Material added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Adds a new user
    def add_user(self):
        self.manage_users("add")

    # Removes an existing user
    def remove_user(self):
        self.manage_users("remove")

    # Manages user actions (add/remove)
    def manage_users(self, action):
        top = ctk.CTkToplevel(self.display)
        top.title("Manage Users")
        top.geometry("400x300")

        # Role selection
        ctk.CTkLabel(top, text="Role (admin/user):", font=("Helvetica", 12)).pack(pady=10)
        role_entry = ctk.CTkEntry(top, width=200, font=("Helvetica", 12))
        role_entry.pack(pady=5)
        role_entry.insert(0, "user")  # Default value is 'user'

        # Email/Username
        ctk.CTkLabel(top, text="Username (Email):", font=("Helvetica", 12)).pack(pady=10)
        email_entry = ctk.CTkEntry(top, width=200, font=("Helvetica", 12))
        email_entry.pack(pady=5)

        # Password
        ctk.CTkLabel(top, text="Password:", font=("Helvetica", 12)).pack(pady=10)
        password_entry = ctk.CTkEntry(top, width=200, show="*", font=("Helvetica", 12))
        password_entry.pack(pady=5)

        def save_user():
            role = role_entry.get()
            email = email_entry.get()
            password = password_entry.get()

            # Validate role
            if role not in ["admin", "user"]:
                messagebox.showerror("Error", "Invalid role! Please choose 'admin' or 'user'.")
                return

            if action == "add":
                # Add new user (role, email, password)
                self.modify_credentials(email, password, role)
            elif action == "remove":
                self.modify_credentials(email, password, remove=True)
            top.destroy()

        ctk.CTkButton(top, text="Submit", command=save_user, width=200, fg_color="#4CAF50", text_color="white",
                      font=("Helvetica", 12)).pack(pady=20)

    # Adds a new material to the inventory
    def add_material(self):
        self.manage_inventory("add")

    # Updates an existing material in the inventory
    def update_material(self):
        self.manage_inventory("update")

    # Removes a material from the inventory
    def remove_material(self):
        self.manage_inventory("remove")

    # Manages inventory actions (add/update/remove)
    def manage_inventory(self, action):
        top = ctk.CTkToplevel(self.display)
        top.title("Manage Inventory")
        top.geometry("400x300")

        ctk.CTkLabel(top, text="Material Name:", font=("Helvetica", 12)).pack(pady=10)
        name_entry = ctk.CTkEntry(top, width=200, font=("Helvetica", 12))
        name_entry.pack(pady=5)

        ctk.CTkLabel(top, text="Quantity:", font=("Helvetica", 12)).pack(pady=10)
        quantity_entry = ctk.CTkEntry(top, width=200, font=("Helvetica", 12))
        quantity_entry.pack(pady=5)

        def save_inventory():
            name = name_entry.get()
            quantity = quantity_entry.get()
            if action == "add":
                self.modify_inventory(name, quantity)
            elif action == "update":
                self.modify_inventory(name, quantity)
            elif action == "remove":
                self.modify_inventory(name, remove=True)
            top.destroy()

        ctk.CTkButton(top, text="Submit", command=save_inventory, width=200, fg_color="#4CAF50", text_color="white",
                      font=("Helvetica", 12)).pack(pady=20)

    # Displays all the inventory in a new window
    def show_all_inventory(self):
        top = ctk.CTkToplevel(self.display)
        top.title("All Inventory")
        top.geometry("600x500")

        ctk.CTkLabel(top, text="Inventory List", font=("Helvetica", 18, 'bold'), text_color="#4CAF50").pack(pady=10)

        # Search input with clear indication
        search_frame = ctk.CTkFrame(top, fg_color="transparent")
        search_frame.pack(pady=5)

        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame, textvariable=search_var, placeholder_text="🔍 Search Inventory", width=300
        )
        search_entry.pack(side="left", padx=5)

        frame = ctk.CTkScrollableFrame(top, fg_color="#16191a")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        def update_inventory():
            for widget in frame.winfo_children():
                widget.destroy()

            search_text = search_var.get().lower()
            try:
                rows = inventory_sheet.get_all_values()
                if not rows:
                    ctk.CTkLabel(frame, text="No inventory found", font=("Helvetica", 12), text_color="#888").pack(
                        pady=10)
                else:
                    for i, row in enumerate(rows):
                        name, qty = row
                        if search_text in name.lower():
                            row_color = "#04090a"
                            item_frame = ctk.CTkFrame(frame, fg_color=row_color, corner_radius=5)
                            item_frame.pack(fill="x", pady=5, padx=10)
                            ctk.CTkLabel(item_frame, text=f"{name}", font=("Helvetica", 12),
                                         text_color="#ffffff").pack(side="left", padx=10)
                            ctk.CTkLabel(item_frame, text=f"{qty}", font=("Helvetica", 12),
                                         text_color="#ffffff").pack(side="right", padx=10)
            except Exception as e:
                ctk.CTkLabel(frame, text=f"Error: {e}", font=("Helvetica", 12), text_color="#888").pack(pady=10)

        search_entry.bind("<KeyRelease>", lambda event: update_inventory())
        update_inventory()

