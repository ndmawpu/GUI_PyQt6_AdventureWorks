import pyqtgraph as pg
import calendar
import pandas as pd
import textwrap
from PyQt6.QtWidgets import *


from matplotlib.dates import date2num       
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import FuncFormatter

class Chart_Visualize:
    @staticmethod
    def sales_statistic(obj):

        Chart_Visualize.clear_layout(obj.layout_salesbydate)
        Chart_Visualize.clear_layout(obj.layout_salesbymonth)
        Chart_Visualize.clear_layout(obj.layout_salesbyquarter)
        Chart_Visualize.clear_layout(obj.layout_salesbyyear)
        Chart_Visualize.clear_layout(obj.layout_salesbycountry)
        Chart_Visualize.clear_layout(obj.layout_salesbyregion)
    
        merged_data = obj.df_sales.merge(obj.df_time, left_on='OrderDate', right_on='DateKey')

        sales_by_date = merged_data.groupby('OrderDate')['TotalDue'].sum().reset_index()
        sales_by_date["OrderDate"] = sales_by_date["OrderDate"].apply(date2num)
        sales_by_month = merged_data.groupby('TheMonth')['TotalDue'].sum().reset_index()
        sales_by_month['TheMonth'] = sales_by_month['TheMonth'].apply(lambda x: calendar.month_abbr[x])

        month_order = list(calendar.month_abbr)[1:]
        sales_by_month['TheMonth'] = pd.Categorical(sales_by_month['TheMonth'], categories=month_order, ordered=True)
        sales_by_quarter = merged_data.groupby('TheQuarter')['TotalDue'].sum().reset_index()
        sales_by_year = merged_data.groupby('TheYear')['TotalDue'].sum().reset_index()
        sales_by_country = obj.df_sales.merge(obj.df_territory[['TerritoryID', 'Country']], on='TerritoryID')
        # Define a mapping dictionary for country names
        country_mapping = {'United Kingdom': 'UK', 'United States': 'US'}

        # Replace country names in the "Country" column using the mapping dictionary
        sales_by_country["Country"].replace(country_mapping, inplace=True)

        sales_by_country = sales_by_country.groupby('Country')['TotalDue'].sum().reset_index()

        sales_by_region = pd.merge(obj.df_sales, obj.df_territory, on='TerritoryID', how='inner')
        sales_by_region = sales_by_region.groupby('Group')['TotalDue'].sum().reset_index()

        # Plotting Sales by Date
        Chart_Visualize.plot_barchart(obj.layout_salesbydate, 'Sales by Date', sales_by_date, 'OrderDate', 'TotalDue', 'Day' , 'Total Sales')

        # Plotting Sales by Month
        Chart_Visualize.plot_barchart(obj.layout_salesbymonth, 'Sales by Month', sales_by_month, 'TheMonth', 'TotalDue', 'Month', "Total Sales" ,categorical=True, categories=month_order)

        # Plotting Sales by Quarter
        Chart_Visualize.plot_barchart(obj.layout_salesbyquarter, 'Sales by Quarter', sales_by_quarter, 'TheQuarter', 'TotalDue', 'Quarter', 'Total Sales', x_ticks=[(1, 'Q1'), (2, 'Q2'), (3, 'Q3'), (4, 'Q4')])

        # Plotting Sales by Year
        Chart_Visualize.plot_barchart(obj.layout_salesbyyear, 'Sales by Year', sales_by_year, 'TheYear', 'TotalDue', 'Year', "Total Sales")

        # Plotting Sales by Country
        Chart_Visualize.plot_category_barchart(obj.layout_salesbycountry, 'Sales by Country', sales_by_country, 'Country', "TotalDue", "", "Total Sales")

        # Plotting Sales by Region
        Chart_Visualize.plot_category_barchart(obj.layout_salesbyregion, "Sales by Region", sales_by_region, "Group", "TotalDue", "", "Total Sales")

        # Compute total sales, total orders, total cost, and total profit
        total_sales = obj.df_sales['TotalDue'].sum()
        total_orders = obj.df_sales['SalesOrderID'].nunique()
        total_cost = obj.df_sales['SubTotal'].sum()
        total_profit = total_sales - total_cost
        profit_margin = (total_profit / total_sales) * 100

        obj.label_totalsales.setText(Chart_Visualize.format_number(total_sales))
        obj.label_totalorders.setText(Chart_Visualize.format_number(total_orders))
        obj.label_totalprofit.setText(Chart_Visualize.format_number(total_profit))
        obj.label_profitmargin.setText(Chart_Visualize.format_number(profit_margin))

    @staticmethod
    def customers_statistic(obj):
        Chart_Visualize.clear_layout(obj.layout_customerordersbyyear)
        Chart_Visualize.clear_layout(obj.layout_top10customers)
        Chart_Visualize.clear_layout(obj.layout_totalcustomersbycountry)

        # Customer orders by Year
        customer_orders = pd.merge(obj.df_sales, obj.df_customers, on='CustomerID', how='inner')
        customer_orders = pd.merge(customer_orders, obj.df_time, left_on='OrderDate', right_on='DateKey' ,how='inner')

        # Group by year and count the number of orders for each customer
        customer_orders_by_year = customer_orders.groupby(['TheYear', 'CustomerID']).size().reset_index(name='Orders')
        customer_orders_by_year = customer_orders_by_year.groupby('TheYear').sum().reset_index()

        # Top 10 customers by Sales
        customer_sales = pd.merge(obj.df_customers, obj.df_sales, on='CustomerID', how='inner')
        total_sales_by_customer = customer_sales.groupby('CustomerID')['TotalDue'].sum().reset_index()
        top_10_customers = total_sales_by_customer.nlargest(10, 'TotalDue')
        top_10_customers_info = pd.merge(top_10_customers, obj.df_customers, on='CustomerID', how='inner')

        # Total customer by Country
        customer_country = pd.merge(obj.df_customers, obj.df_territory, on='TerritoryID', how='inner')

        # Group by Country and count the number of customers
        customer_country = customer_country.groupby('Country')['CustomerID'].count().reset_index()
        country_mapping = {'United Kingdom': 'UK', 'United States': 'US'}
        customer_country["Country"].replace(country_mapping, inplace=True)

        Chart_Visualize.plot_barchart(obj.layout_customerordersbyyear, "Customer Orders By Year", customer_orders_by_year, "TheYear", "CustomerID", "Year", "Number of Orders")
        Chart_Visualize.plot_category_barchart(obj.layout_top10customers, "Top 10 Customers by Sales", top_10_customers_info, "Customer Name", "TotalDue", "Customer Name", "Total Sales", horizontal=True)
        Chart_Visualize.plot_category_barchart(obj.layout_totalcustomersbycountry, "Total Customers by Country", customer_country, "Country", "CustomerID", "Country", "Total Customers", horizontal=True)

        total_customers = int(round(len(obj.df_customers['CustomerID'].unique())))
        total_territories = len(obj.df_territory['TerritoryID'].unique())
        total_countries = len(obj.df_territory['Country'].unique())
        total_continents = len(obj.df_territory['Group'].unique())

        obj.label_totalcustomers.setText(Chart_Visualize.format_number(total_customers))
        obj.label_territories.setText(str(total_territories))
        obj.label_countries.setText(str(total_countries))
        obj.label_continents.setText(str(total_continents))

    @staticmethod
    def products_statistic(obj):
        Chart_Visualize.clear_layout(obj.layout_topbysales)
        Chart_Visualize.clear_layout(obj.layout_productcategory)
        Chart_Visualize.clear_layout(obj.layout_topbyorders)
        Chart_Visualize.clear_layout(obj.layout_subcategory)

        top_products = obj.df_sales.groupby('ProductID')['TotalDue'].sum().reset_index()
        top_products = top_products.sort_values(by='TotalDue', ascending=False).head(10)
        top_products = pd.merge(top_products, obj.df_products[['ProductID', 'ProductName']], on='ProductID', how='left')
        top_products["ProductID"] = top_products["ProductID"].astype(str)

        top_products_order = obj.df_sales.groupby('ProductID')['OrderQty'].sum().reset_index()
        top_products_order = top_products_order.sort_values(by='OrderQty', ascending=False).head(10)
        top_products_order = pd.merge(top_products_order, obj.df_products[['ProductID', 'ProductName']], on='ProductID', how='left')
        top_products_order["ProductID"] = top_products_order["ProductID"].astype(str)


        sales_by_category = pd.merge(obj.df_sales, obj.df_products, on='ProductID', how='inner')
        sales_by_category = sales_by_category.groupby('ProductCategoryName')['TotalDue'].sum().reset_index()

        sales_by_subcategory = pd.merge(obj.df_sales, obj.df_products, on='ProductID', how='inner')
        sales_by_subcategory = sales_by_subcategory.groupby('SubCategoryName')['TotalDue'].sum().reset_index()
        top_subcategories = sales_by_subcategory.sort_values(by='TotalDue', ascending=False).head(10)

        Chart_Visualize.plot_category_barchart(obj.layout_topbysales, 'Top 10 Products by Sales', top_products, 'ProductID', 'TotalDue', '' , '', horizontal=True)
        Chart_Visualize.plot_category_barchart(obj.layout_topbyorders, 'Top 10 Products by Orders', top_products_order, 'ProductID', 'OrderQty', '' , '', horizontal=True)
        Chart_Visualize.plot_category_barchart(obj.layout_productcategory, "Sales by Product Category", sales_by_category, "ProductCategoryName", "TotalDue", "", "", horizontal=True)
        Chart_Visualize.plot_category_barchart(obj.layout_subcategory, "Top 10 Sybcategories by Sales", top_subcategories, "SubCategoryName", "TotalDue", "", "", horizontal=True)

        total_products = len(obj.df_sales['ProductID'].unique())
        total_orders = obj.df_sales['SalesOrderID'].nunique()
        total_quantity_sold = obj.df_sales['OrderQty'].sum()
        total_due = obj.df_sales['TotalDue'].sum()
        avg_order_value = total_due / total_orders

        obj.label_totalsales_products.setText(Chart_Visualize.format_number(total_due))
        obj.label_totalproducts.setText(str(total_products))
        obj.label_total_quantity_sold.setText(Chart_Visualize.format_number(total_quantity_sold))
        obj.label_avg_order_value.setText(Chart_Visualize.format_number(avg_order_value))


    @staticmethod
    def customer_segmentation_statistic(obj):
        Chart_Visualize.clear_layout(obj.layout_cluster_distribution)

        cluster_counts = obj.df_cluster['Labels'].value_counts().reset_index()
        cluster_counts.columns = ['Labels', 'Count']
        cluster_counts = cluster_counts.sort_values('Labels')

        cluster_mapping = {'Lost/Needed Attention Customers': 'Cluster 0', 'Top/Best Customers': 'Cluster 1', 'Current Customer': 'Cluster 2'}
        cluster_counts["Labels"].replace(cluster_mapping, inplace=True)
        Chart_Visualize.plot_category_barchart(obj.layout_cluster_distribution, "", cluster_counts, 'Labels', 'Count', 'Customer Segmentation', 'Count')
      
    def plot_category_barchart(layout, title, data, x_col, y_col, x_label, y_label, horizontal=False):
        fig = Figure()
        ax = fig.add_subplot(111)
        if horizontal:
            bars = ax.barh(data[x_col], data[y_col], color='#004080')
        else:
            bars = ax.bar(data[x_col], data[y_col], color='#004080')

        ax.set_title(title, color='#df2e38', fontweight='bold', fontstyle='italic', fontsize=12)  # Bold and italic title
        ax.set_xlabel(x_label, fontsize=8, color ="#004080")
        ax.set_ylabel(y_label, fontsize=8, color ="#004080")

        if horizontal:
            ax.set_yticks(range(len(data[x_col])))
            # wrapped_labels = ['\n'.join(textwrap.wrap(label, 5)) for label in data[x_col]]
            # ax.set_yticklabels(wrapped_labels)
            for bar in bars:
                width = bar.get_width()
                ax.text(width / 2, bar.get_y() + bar.get_height() / 2, Chart_Visualize.format_number(width), ha='center', va='center', color='white', fontsize=6)
        else:
            ax.set_xticks(range(len(data[x_col])))
            wrapped_labels = ['\n'.join(textwrap.wrap(label, 10)) for label in data[x_col]]
            ax.set_xticklabels(wrapped_labels, rotation=0, ha='right')
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height / 2, Chart_Visualize.format_number(height), ha='center', va='center', color='white', fontsize=6)
        ax.spines['top'].set_color('#898989')  # Set color for x-axis
        ax.spines['right'].set_color('#898989')  # Set color for x-axis
        ax.spines['bottom'].set_color('#898989')  # Set color for x-axis
        ax.spines['bottom'].set_linewidth(0.5)     # Set width for x-axis
        ax.spines['left'].set_color('#898989')    # Set color for y-axis
        ax.spines['left'].set_linewidth(0.5) 
        ax.tick_params(colors ="#898989", which="both", labelsize=8)
        # ax.yaxis.set_major_formatter(FuncFormatter(Chart_Visualize.millions_formatter))

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)


    @staticmethod
    def plot_barchart(layout, title, data, x_col, y_col, x_label, y_label, categorical=False, categories=None, x_ticks=None, value=False):
        graphWidget = pg.PlotWidget()
        graphWidget.setTitle(title, color="#df2e38", size="15pt", bold=True, italic=True)
        graphWidget.setBackground('w')
        labelStyle = {"color": "#004080", "font-size": "12px"}
        graphWidget.setLabel("left", y_label, **labelStyle)
        graphWidget.setLabel("bottom", x_label, **labelStyle)

        if categorical:
            x_vals = [categories.index(val) + 1 for val in data[x_col]]
        else:
            x_vals = data[x_col]
        if x_ticks:
            x_axis = graphWidget.getAxis('bottom')
            x_axis.setTicks([x_ticks])

        bargraphItem = pg.BarGraphItem(x=x_vals, height=data[y_col], width=0.6, brush='#004080')
        graphWidget.addItem(bargraphItem)

        graphWidget.getAxis('left').enableAutoSIPrefix(False)
        # graphWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addWidget(graphWidget)
        
    # def millions_formatter(x, pos):
    #     return '{:.0f}M'.format(x * 1e-6)
    
    def format_number(number):
        if abs(number) >= 1e9:
            return f'{number / 1e9:.2f}B'
        elif abs(number) >= 1e6:
            return f'{number / 1e6:.2f}M'
        elif abs(number) >= 1e3:
            return f'{number / 1e3:.2f}K'
        else:
            return f'{number:.2f}'
        
    @staticmethod
    def clear_layout(layout):
        for i in reversed(range(layout.count())): 
            widgetToRemove = layout.itemAt(i).widget()
            # remove it from the layout list
            layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)
