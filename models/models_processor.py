import pickle
import traceback
from sklearn.cluster import KMeans

class ModelProcess:
    @staticmethod
    def saveModel(model,filename):
        try:
            pickle.dump(model,open(f'saved_models/{filename}.pkl','wb'))
            return True
        except:
            traceback.print_exc()
            return False
    @staticmethod
    def loadModel(filename):
        try:
            model=pickle.load(open(filename,'rb'))
            return model
        except:
            traceback.print_exc()
            return None
        
    @staticmethod
    def rfm_train_model(df, n_clusters, init, max_iter, n_init, random_state):
        model = KMeans(n_clusters=3, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
        model.fit(df.values)