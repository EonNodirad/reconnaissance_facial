import face_recognition
import cv2
import numpy as np

class FaceRecognizer :
    def __init__(self,tolerance = 0.6):
        self.tolerance = tolerance
        
    def face_detecter(self, image):
        # convertir BGR en RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb_image)
        encoding = face_recognition.face_encodings(rgb_image, locations)
        return locations, encoding
    
    def face_recognize(self, face_encoding, known_encoding, know_names):
        if len(known_encoding) == 0:
            return None,0
        distances = face_recognition.face_distance(known_encoding,face_encoding)
         # compare la distance avec la tolérance
         # si bien le meme alors trouver le kow_names dans le disctionaire qui est relié au known_encoding

        best_match = np.argmin(distances)
        min_distance = distances[best_match]

        if min_distance<= self.tolerance :
            name = know_names[best_match]
            confidence = (1- min_distance) * 100
            return name,confidence
        return None,0


        
