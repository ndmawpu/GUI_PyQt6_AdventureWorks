import pandas as pd
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from UI.MainWindow_ui import Ui_MainWindow
from connectors.mssqlconnector import Connector
from models.login_processor import Login_Process
from models.signup_processor import Signup_process
from models.sales_crud_processor import Sales_CRUD
from models.customers_crud_processor import Customers_CRUD
from models.products_crud_processor import Products_CRUD
from models.statistic_processor import Chart_Visualize
from models.customer_segmentation_processor import CustomerSegmentation
from models.rfm_processor import RFM_process
from models.clv_processor import CLV_Process
from models.models_processor import ModelProcess

class MainWindowEx(Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.myconnector = Connector()
        self.init_data()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.MainWindow.setFixedSize(self.MainWindow.size())

        self.page_num = 1
        self.row_num = 20

        # login tab
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menubar.setVisible(False)
        self.pushButton_login.clicked.connect(self.handle_login)
        self.pushButton_signup.clicked.connect(self.handle_signup)

        self.lineEdit_username.setText('admin')
        self.lineEdit_password.setText('firo')  

        # Sign up tab
        self.pushButton_create_account.clicked.connect(self.handle_signup)
        self.pushButton_returntologin.clicked.connect(self.handle_return_to_login)

        # Sales tab
        self.pushButton_sales_next.clicked.connect(lambda: Sales_CRUD.next_page(self))
        self.pushButton_sales_previous.clicked.connect(lambda: Sales_CRUD.prev_page(self))

        self.tableWidget_sales.itemSelectionChanged.connect(lambda: Sales_CRUD.on_table_item_selection_changed(self))

        self.pushButton_sales_create.clicked.connect(lambda: Sales_CRUD.create_data(self))
        self.pushButton_sales_clear.clicked.connect(lambda: Sales_CRUD.clear_input(self))
        self.pushButton_sales_delete.clicked.connect(lambda: Sales_CRUD.delete_data(self))
        self.dateEdit_OrderDate_sales.setDate(QDate.currentDate())

        # Customers tab
        self.pushButton_customers_next.clicked.connect(lambda: Customers_CRUD.next_page(self))
        self.pushButton_customers_previous.clicked.connect(lambda: Customers_CRUD.prev_page(self))

        self.tableWidget_customers.itemSelectionChanged.connect(lambda: Customers_CRUD.on_table_item_selection_changed(self))

        self.pushButton_customers_create.clicked.connect(lambda: Customers_CRUD.create_data(self))
        self.pushButton_customers_clear.clicked.connect(lambda: Customers_CRUD.clear_input(self))
        self.pushButton_customers_delete.clicked.connect(lambda: Customers_CRUD.delete_data(self))

        # products
        self.pushButton_product_next.clicked.connect(lambda: Products_CRUD.next_page(self))
        self.pushButton_product_previous.clicked.connect(lambda: Products_CRUD.prev_page(self))

        self.tableWidget_products.itemSelectionChanged.connect(lambda: Products_CRUD.on_table_item_selection_changed(self))

        self.pushButton_product_create.clicked.connect(lambda: Products_CRUD.create_data(self))
        self.pushButton_clear_products.clicked.connect(lambda: Products_CRUD.clear_input(self))
        self.pushButton_delete_product.clicked.connect(lambda: Products_CRUD.delete_data(self))

        # customer segmentation tab
        self.pushButton_add_customers_seg.clicked.connect(lambda: CustomerSegmentation.add_customer(self))
        self.pushButton_predict_cluster.clicked.connect(lambda: CustomerSegmentation.predict_cluster(self))
        self.pushButton_clear_customer_seg.clicked.connect(lambda: CustomerSegmentation.clear_input(self))
        self.df_temp = pd.DataFrame(columns=['CustomerName', 'OrderDate', 'Quantity', 'Sales']) # Temporary DataFrame to hold added customers

        # rfm model tab
        self.pushButton_generate_elbow.clicked.connect(lambda: RFM_process.elbow(self))
        self.pushButton_clear_rfm.clicked.connect(lambda: RFM_process.clear_input(self))
        self.pushButton_save_rfm.clicked.connect(lambda: RFM_process.save_rfm(self))
        self.pushButton_train_rfm.clicked.connect(lambda: RFM_process.train_rfm(self))
        self.rfm_model = ModelProcess.loadModel("assets\kmeans_model.pkl")

        # trigger action for menu bar
        self.actionSales_Management.triggered.connect(self.handle_sales_crud)
        self.actionSales_Statistics.triggered.connect(self.handle_sales_statistics)
        self.actionCustomers_Management.triggered.connect(self.handle_customers_crud)
        self.actionCustomers_Statistics.triggered.connect(self.handle_customers_statistics)
        self.actionProducts_Management.triggered.connect(self.handle_products_crud)
        self.actionProducts_Statistics.triggered.connect(self.handle_products_statistics)
        self.actionCustomer_Cluster.triggered.connect(self.handle_customer_segmentation)
        self.actionRFM_model.triggered.connect(self.handle_rfm_model)
        self.actionCLV_segmentation.triggered.connect(self.handle_clv)
        self.actionLogout.triggered.connect(self.handle_logout)
        self.actionWelcome_Page.triggered.connect(self.handle_homepage)

    def show(self):
        self.MainWindow.show()

    def init_data(self):
        QUERY_SALES = "SELECT SalesOrderID, CustomerID, ProductID, TerritoryID, OrderDate, OrderQty, UnitPrice, LineTotal, TotalDue, SubTotal from firo.FactSales "
        self.df_sales = self.myconnector.run_query(query=QUERY_SALES)
        self.df_sales["OrderDate"] = pd.to_datetime(self.df_sales["OrderDate"])

        QUERY_CUSTOMERS = "SELECT * FROM firo.DimCustomer"
        self.df_customers = self.myconnector.run_query(query=QUERY_CUSTOMERS)

        QUERY_PRODUCTS = "SELECT * FROM firo.DimProduct"
        self.df_products = self.myconnector.run_query(query=QUERY_PRODUCTS)

        QUERY_TIME = "SELECT DateKey, TheDay, TheWeek, TheMonth, TheQuarter, TheYear FROM firo.DimTime"
        self.df_time = self.myconnector.run_query(query=QUERY_TIME)
        self.df_time['DateKey'] = pd.to_datetime(self.df_time['DateKey'])
       
        QUERY_TERRITORY = "select * from firo.DimTerritory"
        self.df_territory = self.myconnector.run_query(query=QUERY_TERRITORY)

        self.df_cluster = pd.read_csv("assets/customer_segmentation.csv")
        self.df_rfm = pd.read_csv("assets/rfm.csv")

    def handle_return_to_login(self):
        self.tabWidget.setCurrentIndex(0)

    def handle_login(self):
        Login_Process.process_login(self)

    def handle_signup(self):
        self.tabWidget.setCurrentIndex(11)
        Signup_process.process_signup(self)

    def handle_sales_crud(self):
        self.tabWidget.setCurrentIndex(2)
        Sales_CRUD.show_table(self)
    
    def handle_sales_statistics(self):
        self.tabWidget.setCurrentIndex(3)
        Chart_Visualize.sales_statistic(self)

    def handle_customers_crud(self):
        self.tabWidget.setCurrentIndex(4)
        Customers_CRUD.show_table(self)

    def handle_customers_statistics(self):
        self.tabWidget.setCurrentIndex(5)
        Chart_Visualize.customers_statistic(self)
        
    def handle_products_crud(self):
        self.tabWidget.setCurrentIndex(6)
        Products_CRUD.show_table(self)

    def handle_products_statistics(self):
        self.tabWidget.setCurrentIndex(7)
        Chart_Visualize.products_statistic(self)

    def handle_customer_segmentation(self):
        self.tabWidget.setCurrentIndex(8)
        Chart_Visualize.customer_segmentation_statistic(self)
        CustomerSegmentation.show_table(self)
  
    def handle_rfm_model(self):
        self.lineEdit_max_iter_elbow.setText('300')
        self.lineEdit_randomstate_elbow.setText('0')

        self.tabWidget.setCurrentIndex(9)
        RFM_process.show_table(self)
        RFM_process.elbow(self)

    def handle_clv(self):
        self.tabWidget.setCurrentIndex(10)
        CLV_Process.show_clv_segmentation(self)
        CLV_Process.show_ggf(self)
        CLV_Process.show_top_clv(self)
        
    def handle_logout(self):
        self.menubar.setVisible(False)
        self.tabWidget.setCurrentIndex(0)
        
    def handle_homepage(self):
        self.menubar.setVisible(True)
        self.tabWidget.setCurrentIndex(1)