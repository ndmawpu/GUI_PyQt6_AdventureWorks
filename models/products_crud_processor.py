from PyQt6.QtWidgets import *

class Products_CRUD:
    
    @staticmethod
    def show_table(obj):
        obj.label_page_num_4.setText(str(obj.page_num))

        try:
            QUERY_PRODUCTS = "SELECT * from firo_test.DimProduct   " \
                            "ORDER BY ProductID " \
                            f"OFFSET ({obj.page_num}-1)*{obj.row_num} ROWS " \
                            f"FETCH NEXT {obj.row_num} ROWS ONLY"
            print(QUERY_PRODUCTS)
            result = obj.myconnector.run_query(query=QUERY_PRODUCTS)
            print(result)
            obj.tableWidget_products.setRowCount(len(result))
            obj.tableWidget_products.setColumnCount(len(result.columns))

            obj.tableWidget_products.setHorizontalHeaderLabels(
                ['ProductID',"ProductNumber", "ProductName", "Color", "StandarCost", "ListPrice",'Model',"SubCategoryName","ProductCategoryName"])
            
            if result is not None:
                for row_number, row_data in enumerate(result.itertuples(index=False)):
                    obj.tableWidget_products.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        obj.tableWidget_products.setItem(
                            row_number, column_number, QTableWidgetItem(str(data))
                        )
        except Exception as e:
            print("Error connecting to database")

    @staticmethod
    def create_data(obj):
        try:
            productid = obj.lineEdit_productidd_product.text()
            productname = obj.lineEdit_productname_product.text()
            productnumber = obj.lineEdit_productnumber_product.text()
            color = obj.lineEdit_color_product.text()
            listprice = obj.lineEdit_listprice_product.text()
            model = obj.lineEdit_model_product.text()
            subcategory = obj.lineEdit_subcategory_product.text()
            category = obj.lineEdit_category_products.text()
            standardcost = obj.lineEdit_standardcot_product.text()

            QUERY_INSERT = """
            INSERT INTO firo_test.DimProduct (
                ProductID, ProductName, ProductNumber, Color, ListPrice, Model, SubCategoryName, ProductCategoryName, StandardCost
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (productid, productname, productnumber, color, listprice, model, subcategory, category, standardcost)
            obj.myconnector.execute_query(query=QUERY_INSERT, params=params)
            print("Insert success")
            Products_CRUD.show_table(obj)
        except Exception as e:
            print("Error inserting data into database")
            print(e)

    @staticmethod
    def delete_data(obj):
        try:
            productid = obj.lineEdit_productidd_product.text()
            QUERY_DELETE = f"DELETE FROM firo_test.DimProduct WHERE ProductID = {productid}"
            print(QUERY_DELETE)
            obj.myconnector.execute_query(query=QUERY_DELETE)
            Products_CRUD.show_table(obj)
        except Exception as e:
            print("Error deleting data from database")
            print(e)

    @staticmethod
    def clear_input(obj):
        obj.lineEdit_productidd_product.setText("")
        obj.lineEdit_productname_product.setText("")
        obj.lineEdit_productnumber_product.setText("")
        obj.lineEdit_color_product.setText("")
        obj.lineEdit_listprice_product.setText("")
        obj.lineEdit_model_product.setText("")
        obj.lineEdit_subcategory_product.setText("")
        obj.lineEdit_category_products.setText("")
        obj.lineEdit_standardcot_product.setText("")

    def on_table_item_selection_changed(obj):
        # Get the selected row index
        selected_row_index = obj.tableWidget_products.currentRow()

        # Ensure a row is selected
        if selected_row_index >= 0:
            # Retrieve data from the selected row
            product_id = obj.tableWidget_products.item(selected_row_index, 0).text()
            product_name = obj.tableWidget_products.item(selected_row_index, 2).text()
            product_number = obj.tableWidget_products.item(selected_row_index, 1).text()
            color = obj.tableWidget_products.item(selected_row_index, 3).text()
            list_price = obj.tableWidget_products.item(selected_row_index, 5).text()
            model = obj.tableWidget_products.item(selected_row_index, 6).text()
            subcategory = obj.tableWidget_products.item(selected_row_index, 7).text()
            category = obj.tableWidget_products.item(selected_row_index, 8).text()
            standard_cost = obj.tableWidget_products.item(selected_row_index, 4).text()

            # Update line edits with the selected row's data
            obj.lineEdit_productidd_product.setText(product_id)
            obj.lineEdit_productname_product.setText(product_name)
            obj.lineEdit_productnumber_product.setText(product_number)
            obj.lineEdit_color_product.setText(color)
            obj.lineEdit_listprice_product.setText(list_price)
            obj.lineEdit_model_product.setText(model)
            obj.lineEdit_subcategory_product.setText(subcategory)
            obj.lineEdit_category_products.setText(category)
            obj.lineEdit_standardcot_product.setText(standard_cost)

    @staticmethod    
    def next_page(obj):
        obj.page_num += 1
        Products_CRUD.show_table(obj)

    @staticmethod
    def prev_page(obj):
        if obj.page_num > 1:
            obj.page_num -= 1
        Products_CRUD.show_table(obj)
