from PyQt6.QtWidgets import *

class Customers_CRUD:
    
    @staticmethod
    def show_table(obj):
        obj.label_page_num_3.setText(str(obj.page_num))

        try:
            QUERY_CUSTOMERS = "SELECT * from firo_test.DimCustomer   " \
                            "ORDER BY CustomerID " \
                            f"OFFSET ({obj.page_num}-1)*{obj.row_num} ROWS " \
                            f"FETCH NEXT {obj.row_num} ROWS ONLY"
            print(QUERY_CUSTOMERS)
            result = obj.myconnector.run_query(query=QUERY_CUSTOMERS)
            print(result)
            obj.tableWidget_customers.setRowCount(len(result))
            obj.tableWidget_customers.setColumnCount(len(result.columns))

            obj.tableWidget_customers.setHorizontalHeaderLabels(
                ['CustomerID', 'CustomerName', 'TerritoryID'])
            
            if result is not None:
                for row_number, row_data in enumerate(result.itertuples(index=False)):
                    obj.tableWidget_customers.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        obj.tableWidget_customers.setItem(
                            row_number, column_number, QTableWidgetItem(str(data))
                        )
        except Exception as e:
            print("Error connecting to database")

    @staticmethod
    def create_data(obj):
        try:
            customer_id = obj.lineEdit_customerid_customer.text()
            customer_name = obj.lineEdit_customername_customer.text()
            territory_id = obj.lineEdit_territoryid_customer.text()

            QUERY_INSERT = "INSERT INTO firo_test.DimCustomer (CustomerID, TerritoryID, [Customer Name]) VALUES (?, ?, ?)"
            params = (customer_id, territory_id, customer_name)
            obj.myconnector.execute_query(query=QUERY_INSERT, params=params)
            print("Insert success")
            Customers_CRUD.show_table(obj)
        except Exception as e:
            print("Error inserting data into database")
            print(e)

    @staticmethod
    def delete_data(obj):
        try:
            customer_id = obj.lineEdit_customerid_customer.text()

            QUERY_DELETE = f"DELETE FROM firo_test.DimCustomer WHERE CustomerID = {customer_id}"
            print(QUERY_DELETE)
            obj.myconnector.execute_query(query=QUERY_DELETE)
            Customers_CRUD.show_table(obj)
        except Exception as e:
            print("Error deleting data from database")
            print(e)

    @staticmethod
    def clear_input(obj):
        obj.lineEdit_customerid_customer.setText("")
        obj.lineEdit_customername_customer.setText("")
        obj.lineEdit_territoryid_customer.setText("")        

    def on_table_item_selection_changed(obj):
        # Get the selected row index
        selected_row_index = obj.tableWidget_customers.currentRow()

        # Ensure a row is selected
        if selected_row_index >= 0:
            # Retrieve data from the selected row
            customer_id = obj.tableWidget_customers.item(selected_row_index, 0).text()
            customer_name = obj.tableWidget_customers.item(selected_row_index, 1).text()
            territory_id = obj.tableWidget_customers.item(selected_row_index, 2).text()

            # Update line edits with the selected row's data
            obj.lineEdit_customerid_customer.setText(customer_id)
            obj.lineEdit_customername_customer.setText(customer_name)
            obj.lineEdit_territoryid_customer.setText(territory_id)

    @staticmethod    
    def next_page(obj):
        obj.page_num += 1
        Customers_CRUD.show_table(obj)

    @staticmethod
    def prev_page(obj):
        if obj.page_num > 1:
            obj.page_num -= 1
        Customers_CRUD.show_table(obj)
