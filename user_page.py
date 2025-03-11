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
user_assignments_sheetid = "12o99nw_bM8_ZEDbmyGZz0fceCEFuDLj3s3YZATDp454"

# Access the sheets
inventory_sheet = client.open_by_key(inventory_sheetid).sheet1
user_assignments_sheet = client.open_by_key(user_assignments_sheetid).sheet1


class UserPage:
    def __init__(self, email):
        self.email = email
        self.display = ctk.CTk()
        self.display.title("User Dashboard")
        self.display.geometry("600x400")
        self.display.config(bg="#2E2E2E")
        self.setup_ui()
        self.display.mainloop()

    def setup_ui(self):
        ctk.CTkButton(self.display, text="Log Out", fg_color="red", text_color="white", font=("Helvetica", 12, 'bold'),
                      command=self.logout).place(x=10, y=10)

        ctk.CTkLabel(self.display, text=f"User Dashboard", font=("Helvetica", 20, 'bold'),
                     text_color="#4CAF50").pack(pady=20)

        inventory_frame = ctk.CTkFrame(self.display, fg_color="#ffffff", corner_radius=10)
        inventory_frame.pack(pady=20, padx=20, fill="x")
        ctk.CTkLabel(inventory_frame, text="Inventory Access", font=("Helvetica", 16, 'bold'),
                     text_color="#4CAF50").pack(pady=10)
        ctk.CTkButton(inventory_frame, text="View Inventory", command=self.view_inventory, width=200,
                      fg_color="#4CAF50", text_color="white").pack(pady=5)

        material_frame = ctk.CTkFrame(self.display, fg_color="#ffffff", corner_radius=10)
        material_frame.pack(pady=20, padx=20, fill="x")
        ctk.CTkLabel(material_frame, text="Material Management", font=("Helvetica", 16, 'bold'),
                     text_color="#4CAF50").pack(pady=10)
        ctk.CTkButton(material_frame, text="Add/Update Material", command=self.add_update_material, width=200,
                      fg_color="#FF9800", text_color="white").pack(pady=5)

    def logout(self):
        self.display.destroy()
        LoginPage()

    def view_inventory(self):
        top = ctk.CTkToplevel(self.display)
        top.title("View Inventory")
        top.geometry("600x500")

        ctk.CTkLabel(top, text="Inventory List", font=("Helvetica", 18, 'bold'), text_color="#4CAF50").pack(pady=10)

        search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(top, textvariable=search_var, placeholder_text="Search Inventory", width=300)
        search_entry.pack(pady=5)

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
                            row_color = "#04090a" if i % 2 == 0 else "#04090a"
                            item_frame = ctk.CTkFrame(frame, fg_color=row_color, corner_radius=5)
                            item_frame.pack(fill="x", pady=5, padx=10)
                            ctk.CTkLabel(item_frame, text=f"{name}", font=("Helvetica", 12),
                                         text_color="#ffffff").pack(
                                side="left", padx=10)
                            ctk.CTkLabel(item_frame, text=f"{qty}", font=("Helvetica", 12),
                                         text_color="#ffffff").pack(
                                side="right", padx=10)
            except Exception as e:
                ctk.CTkLabel(frame, text=f"Error: {e}", font=("Helvetica", 12), text_color="#888").pack(pady=10)

        search_entry.bind("<KeyRelease>", lambda event: update_inventory())
        update_inventory()

    def add_update_material(self):
        top = ctk.CTkToplevel(self.display)
        top.title("Add/Update Material")
        top.geometry("400x300")

        ctk.CTkLabel(top, text="Material Name:", font=("Helvetica", 12)).pack(pady=10)
        name_entry = ctk.CTkEntry(top, width=200)
        name_entry.pack(pady=5)

        ctk.CTkLabel(top, text="Quantity:", font=("Helvetica", 12)).pack(pady=10)
        quantity_entry = ctk.CTkEntry(top, width=200)
        quantity_entry.pack(pady=5)

        def save_material():
            material_name = name_entry.get()
            quantity = quantity_entry.get()
            try:
                rows = user_assignments_sheet.get_all_values()
                found = False

                for i, row in enumerate(rows, start=1):
                    if len(row) >= 3 and row[0] == self.email and row[1].lower() == material_name.lower():
                        user_assignments_sheet.update_cell(i, 3, quantity)
                        found = True
                        break

                if not found:
                    user_assignments_sheet.append_row([self.email, material_name, quantity])
                messagebox.showinfo("Success", "Material added/updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

            top.destroy()

        ctk.CTkButton(top, text="Submit", command=save_material, width=200, fg_color="#4CAF50",
                      text_color="white").pack(pady=20)
