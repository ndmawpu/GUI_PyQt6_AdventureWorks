import pandas as pd
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from models.models_processor import ModelProcess
class CustomerSegmentation:
    @staticmethod
    def show_table(obj):
        result = obj.df_cluster
        obj.tableWidget_customer_segmentation.setRowCount(len(result))
        obj.tableWidget_customer_segmentation.setColumnCount(len(result.columns))

        obj.tableWidget_customer_segmentation.setHorizontalHeaderLabels(
            ['Customer ID', 'Recency', 'Frequency', 'Monetary', 'Cluster', 'Labels'])
        
        if result is not None:
            for row_number, row_data in enumerate(result.itertuples(index=False)):
                obj.tableWidget_customer_segmentation.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    obj.tableWidget_customer_segmentation.setItem(
                        row_number, column_number, QTableWidgetItem(str(data))
                    )

    @staticmethod
    def add_customer(obj):
        customer_name = obj.lineEdit_name_cluster.text()
        orderdate = obj.dateEdit_date_cluster.date().toString("yyyy-MM-dd")
        quantity = obj.lineEdit_quantity_cluster.text()
        sales = obj.lineEdit_sales_cluster.text()


        print(obj.df_temp["CustomerName"].values)
        # Check if the customer name already exists in df_temp
        if customer_name not in obj.df_temp['CustomerName'].values:
        # Add new customer to the temporary DataFrame
            new_data = pd.DataFrame({'CustomerName': [customer_name], 'OrderDate': [orderdate], 'Quantity': [quantity], 'Sales': [sales]})
            obj.df_temp = pd.concat([obj.df_temp, new_data], ignore_index=True)

            # Update the table widget with the new data
            obj.tableWidget_addedCustomerslist.setRowCount(len(obj.df_temp))
            obj.tableWidget_addedCustomerslist.setColumnCount(len(obj.df_temp.columns))
            obj.tableWidget_addedCustomerslist.setHorizontalHeaderLabels(["CustomerName", "OrderDate", "Quantity", "Sales"])

            # Add new row to the table widget
            row_number = len(obj.df_temp) - 1
            for column_number, data in enumerate(new_data.values[0]):
                obj.tableWidget_addedCustomerslist.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )
        else:
            print("Warning", "Customer already exists!")

    @staticmethod
    def predict_cluster(obj):
        obj.df_time['DateKey'] = pd.to_datetime(obj.df_time['DateKey'])
        today_date = obj.df_time['DateKey'].max()
        model = ModelProcess.loadModel("assets\kmeans_model.pkl")
        obj.df_temp['OrderDate'] = pd.to_datetime(obj.df_temp['OrderDate'])

        df_RFM = obj.df_temp.groupby('CustomerName').agg({
            'OrderDate': lambda x: (today_date - x.max()).days,  # Recency
            'CustomerName': 'count',  # Frequency
            'Sales': 'sum'  # Monetary
        }).rename(columns={'OrderDate': 'Recency', 'CustomerName': 'Frequency', 'Sales': 'Monetary'}).reset_index()

        # Predict clusters using trained model
        cluster_pred = model.predict(df_RFM[['Recency', 'Frequency', 'Monetary']])
        df_RFM['Cluster'] = cluster_pred
        obj.tableWidget_predict_cluster.setRowCount(len(df_RFM))
        obj.tableWidget_predict_cluster.setColumnCount(len(df_RFM.columns))

        obj.tableWidget_predict_cluster.setHorizontalHeaderLabels(
            ['CustomerName', 'Recency', 'Frequency', 'Monetary', 'Cluster'])
        
        if df_RFM is not None:
            obj.tableWidget_predict_cluster.setRowCount(0)

            for row_number, row_data in enumerate(df_RFM.itertuples(index=False)):
                obj.tableWidget_predict_cluster.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                        obj.tableWidget_predict_cluster.setItem(
                        row_number, column_number, QTableWidgetItem(str(data))
                    )

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

