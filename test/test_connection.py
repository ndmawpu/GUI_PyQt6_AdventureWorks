import pyodbc
import pandas as pd
import traceback
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connectors.mssqlconnector import Connector


myconnector = Connector()
QUERY_SALES = "SELECT SalesOrderID, CustomerID, ProductID, TerritoryID, OrderDate, OrderQty, UnitPrice, LineTotal, TotalDue from firo.FactSales "
df_sales = myconnector.run_query(query=QUERY_SALES)

QUERY_CUSTOMERS = "SELECT * FROM firo.DimCustomer"
df_customers = myconnector.run_query(query=QUERY_CUSTOMERS)

QUERY_PRODUCTS = "SELECT * FROM firo.DimProduct"
df_products = myconnector.run_query(query=QUERY_PRODUCTS)

QUERY_TIME = "SELECT DateKey, TheDay, TheWeek, TheMonth, TheQuarter, TheYear FROM firo.DimTime"
df_time = myconnector.run_query(query=QUERY_TIME)

QUERY_TERRITORY = "SELECT * FROM firo.DimTerritory"
df_territory = myconnector.run_query(query=QUERY_TERRITORY)

sales_by_country = df_sales.merge(df_territory[['TerritoryID', 'Country']], on='TerritoryID')
sales_by_country = sales_by_country.groupby('Country')['TotalDue'].sum().reset_index()

sales_by_region = pd.merge(df_sales, df_territory, on='TerritoryID', how='inner')
sales_by_region = sales_by_region.groupby('Group')['LineTotal'].sum().reset_index()

customer_sales = pd.merge(df_customers, df_sales, on='CustomerID', how='inner')
total_sales_by_customer = customer_sales.groupby('CustomerID')['TotalDue'].sum().reset_index()
top_10_customers = total_sales_by_customer.nlargest(10, 'TotalDue')
top_10_customers_info = pd.merge(top_10_customers, df_customers, on='CustomerID', how='inner')

df_cluster = pd.read_csv("assets/customer_segmentation.csv")
df_rfm = pd.read_csv("assets/accounts.csv")


print(df_rfm)
