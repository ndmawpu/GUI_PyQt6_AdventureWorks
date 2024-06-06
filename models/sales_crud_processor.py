from PyQt6.QtWidgets import *
from PyQt6.QtCore import QDate, QDateTime

class Sales_CRUD:
    
    @staticmethod
    def show_table(obj):
        obj.label_page_num.setText(str(obj.page_num))

        try:
            QUERY_SALES = "SELECT SalesOrderID, CustomerID, ProductID, TerritoryID, OrderDate, OrderQty, UnitPrice, LineTotal from firo_test.FactSales   " \
                            "ORDER BY SalesOrderID " \
                            f"OFFSET ({obj.page_num}-1)*{obj.row_num} ROWS " \
                            f"FETCH NEXT {obj.row_num} ROWS ONLY"
            print(QUERY_SALES)
            result = obj.myconnector.run_query(query=QUERY_SALES)
            print(result)
            obj.tableWidget_sales.setRowCount(len(result))
            obj.tableWidget_sales.setColumnCount(len(result.columns))

            obj.tableWidget_sales.setHorizontalHeaderLabels(
                ['SalesOrderID', 'CustomerID', 'ProductID', 'TerritoryID', 'OrderDate', 'OrderQty', 'UnitPrice', 'Total'])
            
            if result is not None:
                for row_number, row_data in enumerate(result.itertuples(index=False)):
                    obj.tableWidget_sales.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        obj.tableWidget_sales.setItem(
                            row_number, column_number, QTableWidgetItem(str(data))
                        )
        except Exception as e:
            print("Error connecting to database")

    @staticmethod
    def create_data(obj):
        try:
            sales_order_id = obj.lineEdit_SalesOrderID_sales.text()
            customer_id = obj.lineEdit_CustomerID_sales.text()
            product_id = obj.lineEdit_ProductID_sales.text()
            territory_id = obj.lineEdit_TerritoryID_sales.text()
            order_date = obj.dateEdit_OrderDate_sales.date().toString("yyyy-MM-dd")
            order_qty = obj.lineEdit_OrderQty_sales.text()
            unit_price = obj.lineEdit_UnitPrice_sales.text()
            line_total = Sales_CRUD.calculate_line_total(unit_price, order_qty)

            print(sales_order_id, customer_id, product_id, territory_id, order_date, order_qty, unit_price, line_total)

            QUERY_INSERT = "INSERT INTO firo_test.FactSales (SalesOrderID, CustomerID, ProductID, TerritoryID, OrderDate, OrderQty, UnitPrice, LineTotal) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            params = (sales_order_id, customer_id, product_id, territory_id, order_date, order_qty, unit_price, line_total)
            obj.myconnector.execute_query(query=QUERY_INSERT, params=params)
            print("Insert success")
            Sales_CRUD.show_table(obj)
        except Exception as e:
            print("Error inserting data into database")
            print(e)

    @staticmethod
    def delete_data(obj):
        try:
            sales_order_id = obj.lineEdit_SalesOrderID_sales.text()

            QUERY_DELETE = f"DELETE FROM firo_test  .FactSales WHERE SalesOrderID = {sales_order_id}"
            print(QUERY_DELETE)
            obj.myconnector.execute_query(query=QUERY_DELETE)
            Sales_CRUD.show_table(obj)
        except Exception as e:
            print("Error deleting data from database")
            print(e)

    @staticmethod
    def clear_input(obj):
        obj.lineEdit_SalesOrderID_sales.setText("")
        obj.lineEdit_CustomerID_sales.setText("")
        obj.lineEdit_ProductID_sales.setText("")
        obj.lineEdit_TerritoryID_sales.setText("")
        obj.dateEdit_OrderDate_sales.setDate(QDate.currentDate())
        obj.lineEdit_OrderQty_sales.setText("")
        obj.lineEdit_UnitPrice_sales.setText("")
        obj.lineEdit_LineTotal_sales.setText("")         

    def on_table_item_selection_changed(obj):
        # Get the selected row index
        selected_row_index = obj.tableWidget_sales.currentRow()

        # Ensure a row is selected
        if selected_row_index >= 0:
            # Retrieve data from the selected row
            sales_order_id = obj.tableWidget_sales.item(selected_row_index, 0).text()
            customer_id = obj.tableWidget_sales.item(selected_row_index, 1).text()
            product_id = obj.tableWidget_sales.item(selected_row_index, 2).text()
            territory_id = obj.tableWidget_sales.item(selected_row_index, 3).text()
            order_date_text = obj.tableWidget_sales.item(selected_row_index, 4).text()
            order_date = QDate.fromString(order_date_text, "yyyy-MM-dd") 
            order_qty = obj.tableWidget_sales.item(selected_row_index, 5).text()
            unit_price = obj.tableWidget_sales.item(selected_row_index, 6).text()
            line_total = obj.tableWidget_sales.item(selected_row_index, 7).text()

            # Update line edits with the selected row's data
            obj.lineEdit_SalesOrderID_sales.setText(sales_order_id)
            obj.lineEdit_CustomerID_sales.setText(customer_id)
            obj.lineEdit_ProductID_sales.setText(product_id)
            obj.lineEdit_TerritoryID_sales.setText(territory_id)
            obj.dateEdit_OrderDate_sales.setDate(order_date)
            obj.lineEdit_OrderQty_sales.setText(order_qty)
            obj.lineEdit_UnitPrice_sales.setText(unit_price)
            obj.lineEdit_LineTotal_sales.setText(line_total)   

    @staticmethod
    def calculate_line_total(unit_price, order_qty):
        try:
            return float(unit_price) * int(order_qty)
        except ValueError:
            return 0
        
    @staticmethod    
    def next_page(obj):
        obj.page_num += 1
        Sales_CRUD.show_table(obj)

    @staticmethod
    def prev_page(obj):
        if obj.page_num > 1:
            obj.page_num -= 1
        Sales_CRUD.show_table(obj)
