import pandas as pd
from PyQt6.QtWidgets import *
from models.statistic_processor import Chart_Visualize

class CLV_Process:
    @staticmethod
    def show_ggf(obj):
        ggf = pd.read_csv("assets\ggf_filter.csv")
        obj.tableWidget_ggf.setRowCount(len(ggf))
        obj.tableWidget_ggf.setColumnCount(len(ggf.columns))

        obj.tableWidget_ggf.setHorizontalHeaderLabels(
            ['frequency', 'recency',	'T',	'monetary_value',	'p_not_alive',	'p_alive',	'predicted_purchases',	'actual30',	'error',	'expected_avg_sales_',	'predicted_clv',	'profit_margin'])
        
        if ggf is not None:
            for row_number, row_data in enumerate(ggf.itertuples(index=False)):
                obj.tableWidget_ggf.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    obj.tableWidget_ggf.setItem(
                        row_number, column_number, QTableWidgetItem(str(data))
                    )
    
    @staticmethod
    def show_top_clv(obj):
        top = pd.read_csv(r"assets\top_clv_customers.csv")
        obj.tableWidget_top_value_customers.setRowCount(len(top))
        obj.tableWidget_top_value_customers.setColumnCount(len(top.columns))

        obj.tableWidget_top_value_customers.setHorizontalHeaderLabels(
            ['CustomerID', 'Customer Name', 'predicted_clv'])
        
        if top is not None:
            for row_number, row_data in enumerate(top.itertuples(index=False)):
                obj.tableWidget_top_value_customers.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    obj.tableWidget_top_value_customers.setItem(
                        row_number, column_number, QTableWidgetItem(str(data))
                    )

    @staticmethod
    def show_clv_segmentation(obj):
        Chart_Visualize.clear_layout(obj.layout_clv_segmentation)
        seg = pd.read_csv(r"assets\clv_cluster.csv")
        Chart_Visualize.plot_category_barchart(obj.layout_clv_segmentation, "Distribution of CLV Clusters", seg, 'CLV_Segment', 'Count', '', '')