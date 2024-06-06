from PyQt6.QtWidgets import QMessageBox
import pandas as pd
    
class Signup_process:
    @staticmethod
    def process_signup(obj):
        username = obj.lineEdit_signup_username.text()
        password = obj.lineEdit_signup_password.text()
        
        if username and password:
            try:
                accounts_df = pd.read_csv('assets/accounts.csv')
                if username in accounts_df['username'].values:
                    obj.label_signup_error.setText("Username already exists!")
                    return
            except FileNotFoundError:
                accounts_df = pd.DataFrame(columns=['username', 'password'])

            new_account = pd.DataFrame([[username, password]], columns=['username', 'password'])
            accounts_df = pd.concat([accounts_df, new_account], ignore_index=True)
            accounts_df.to_csv('assets/accounts.csv', index=False)
            
            obj.tabWidget.setCurrentIndex(0)  # Go back to login tab
        else:
            obj.label_signup_error.setText("Both fields are required!")
