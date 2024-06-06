import pandas as pd

class Login_Process:
    @staticmethod
    def process_login(obj):  
        username = obj.lineEdit_username.text()
        password = obj.lineEdit_password.text()
        # Check if username and password are not empty
        if not username or not password:
            obj.label_loginerror.setText("Both fields are required!")
            return

        # Admin credentials for quick access
        if username == 'admin' and password == 'firo':
            obj.menubar.setVisible(True)
            obj.tabWidget.setCurrentIndex(1)  # home
            return
        
        else:
            try:
                # Read accounts.csv
                accounts_df = pd.read_csv('assets/accounts.csv')

                # Check if the username exists and the password matches
                if ((accounts_df['username'] == username) & (accounts_df['password'] == password)).any():
                    obj.menubar.setVisible(True)
                    obj.tabWidget.setCurrentIndex(1)  # home
                else:
                    raise ValueError("Invalid credentials")

            except FileNotFoundError:
                obj.label_loginerror.setText("No accounts found! Please sign up first.")
                return