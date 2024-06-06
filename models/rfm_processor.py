from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from models.statistic_processor import Chart_Visualize

from models.models_processor import ModelProcess
class RFM_process:
    @staticmethod
    def show_table(obj):
        result = obj.df_rfm
        obj.tableWidget_rfm.setRowCount(len(result))
        obj.tableWidget_rfm.setColumnCount(len(result.columns))

        obj.tableWidget_rfm.setHorizontalHeaderLabels(
            ['Recency', 'Frequency', 'Monetary', "Cluster"])
        
        if result is not None:
            for row_number, row_data in enumerate(result.itertuples(index=False)):
                obj.tableWidget_rfm.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    obj.tableWidget_rfm.setItem(
                        row_number, column_number, QTableWidgetItem(str(data))
                    )
    @staticmethod
    def elbow(obj):
        max_iter = obj.lineEdit_max_iter_elbow.text()
        random_state = obj.lineEdit_randomstate_elbow.text()
        distortions = []
        K = range(1, 10)
        for k in K:
            kmean_model = KMeans(n_clusters=k, init='k-means++', max_iter=int(max_iter), n_init=10, random_state=int(random_state))
            kmean_model.fit(obj.df_rfm)
            distortions.append(kmean_model.inertia_)
        Chart_Visualize.clear_layout(obj.layout_elbow)
        
        fig = Figure()
        ax = fig.add_subplot(111)

        ax.plot(K, distortions, 'bo-')
        # ax.set_xlabel('Number of clusters (k)')
        ax.set_ylabel('Distortion')
        ax.set_title('Elbow Method For Optimal k')
        canvas = FigureCanvas(fig)
        obj.layout_elbow.addWidget(canvas)
        obj.label_message_elbow.setText(f"successfully generate eblow at max_iter: {max_iter} and random_state: {random_state}")
        print("generate successed")
    
    @staticmethod
    def train_rfm(obj):
        n_clusters = obj.lineEdit_nclusters_rfm.text()
        max_iter = obj.lineEdit_maxiter_rfm.text()
        random_state = obj.lineEdit_randomstate_rfm.text()
        name = obj.lineEdit_modelname_rfm.text()


        # obj.rfm_model = ModelProcess.loadModel("assets\kmeans_model.pkl")
        obj.rfm_model = KMeans(n_clusters=int(n_clusters), init = 'k-means++', max_iter = int(max_iter), n_init = 10, random_state = int(random_state))
        obj.rfm_model.fit(obj.df_rfm.values)
        labels = obj.rfm_model.labels_

        Chart_Visualize.clear_layout(obj.layout_cluster)
        fig = plt.figure(figsize=(7,7))
        ax = plt.subplot(111, projection='3d')
        ax.scatter(obj.df_rfm['Recency'], obj.df_rfm['Frequency'], obj.df_rfm['Monetary'], s=300, c=labels, marker='o', cmap = 'plasma')

        # ax.set_title("Distribution of Clusters", font={'weight':'bold', 'size':20})
        ax.set_xlabel('Recency', fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_zlabel('Monetary', fontweight='bold')
        canvas = FigureCanvas(fig)
        obj.layout_cluster.addWidget(canvas)
        obj.label_rfm_model_message.setText(f"Model {name} trained at {n_clusters} clusters")

    @staticmethod
    def save_rfm(obj):
        name = obj.lineEdit_modelname_rfm.text()
        ModelProcess.saveModel(obj.rfm_model, name)
        obj.label_rfm_model_message.setText(f"Model {name} saved!!!")

    @staticmethod
    def clear_input(obj):
        obj.lineEdit_modelname_rfm.setText("")
        obj.lineEdit_nclusters_rfm.setText("")
        obj.lineEdit_maxiter_rfm.setText("")
        obj.lineEdit_randomstate_rfm.setText("")
        obj.lineEdit_randomstate_elbow.setText("")
        obj.label_message_elbow.setText("")
        obj.lineEdit_randomstate_elbow.setText("") 
