import pickle
import os

class Database :
    def __init__(self):
        self.chemin = "data/encodings/database.pkl"
        self.data = {}  #stoackage principale
        self.load()
    def add_face(self, name, encoding):
        if name not in self.data :
            self.data[name]=[]
        self.data[name].append(encoding)
    
    def get_all_encodings(self):
        all_name =[]
        all_encoding =[]
        for name ,encoding_list in self.data.items() :
            for encoding in encoding_list :
                all_encoding.append(encoding)
                all_name.append(name)

        return all_encoding,all_name
    
    def save(self):
        #sauvegarde
        os.makedirs(os.path.dirname(self.chemin), exist_ok=True)
        with open(self.chemin, "wb") as f:
            pickle.dump(self.data, f)
        
    def load(self):
        # Charger
        if os.path.exists(self.chemin):
            with open(self.chemin, "rb") as f:
                self.data = pickle.load(f)