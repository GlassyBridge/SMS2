import gspread
from google.oauth2.service_account import Credentials
import customtkinter as ctk
from tkinter import PhotoImage

# Google Sheets Setup
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# Google Sheets IDs
inventory_sheetid = "1FuJwUJqBWRJ_LrzId2UGue9BKaN4dGET5lEXJUh3NsQ"
credentials_sheetid = "12o99nw_bM8_ZEDbmyGZz0fceCEFuDLj3s3YZATDp454"


def fetch_credentials():
    sheet = client.open_by_key(credentials_sheetid).sheet1  # Assumes credentials are in the first sheet
    data = sheet.get_all_values()[1:]  # Skip header row
    credentials = {row[1]: (row[2], row[0]) for row in data}  # {email: (password, role)}
    return credentials


class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login Page")
        self.geometry("350x300")
        ctk.set_appearance_mode("dark")  # Dark mode to match the image
        ctk.set_default_color_theme("blue")

        self.credentials = fetch_credentials()  # Load credentials from Google Sheets
        self.setup_ui()
        self.mainloop()

    def setup_ui(self):
        # Main Frame
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title Label
        title_label = ctk.CTkLabel(frame, text="Log Into Your Account", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(20, 10))

        # Email Entry
        self.email_entry = ctk.CTkEntry(frame, placeholder_text="Username", width=250)
        self.email_entry.pack(pady=5)

        # Password Entry
        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=5)

        # Login Button (Blue)
        login_button = ctk.CTkButton(frame, text="Login", command=self.login_action, fg_color="#007BFF",
                                     hover_color="#0056b3")
        login_button.pack(pady=20)

        # Error Label
        self.error_label = ctk.CTkLabel(frame, text="", text_color="red")
        self.error_label.pack()

    def login_action(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        role = self.validate_credentials(email, password)

        if role == "admin":
            self.destroy()
            from admin_page import AdminPage
            AdminPage()
        elif role == "user":
            self.destroy()
            from user_page import UserPage
            UserPage(email)
        else:
            self.error_label.configure(text="Invalid Email or Password!")

    def validate_credentials(self, email, password):
        if email in self.credentials and self.credentials[email][0] == password:
            return self.credentials[email][1]  # Return role (admin/user)
        return None


# Run the Login Page
if __name__ == "__main__":
    LoginPage()
