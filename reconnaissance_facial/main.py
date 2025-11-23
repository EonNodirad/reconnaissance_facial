import cv2
from face_database import Database
from face_recognizer import FaceRecognizer

def menu() :
    "affiche le menu"
    print("\n=== RECONNAISSANCE FACIALE ===")
    print("1. Enregistrer un visage")
    print("2. Reconnaissance en temps réel")
    print("3. Quitter")
    choix = input("Votre choix : ")
    print("le choix "+ choix + "bonne décision")
    return choix

def enregistrer_visage (db , recognizer) :
    """Capture des photos et enregistre dans la DB"""
    name = input("ton nom ?")
    photo_voulues = int(input("combien de photo"))
    photos_prises = 0
    print("Appuyez sur ESPACE pour prendre une photo, ESC pour annuler")
    cam = cv2.VideoCapture("rtsp://host.docker.internal:554/live")
    while photos_prises < photo_voulues :
        ret, frame = cam.read()
        
        cv2.imshow("Enregistrement", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == 32:  # ESPACE
            locations ,encodings = recognizer.face_detecter(frame)
            if len(encodings) >0 :
                encoding =encodings[0]
                db.add_face(name,encoding)
                photos_prises+=1
                print(f"Photo {photos_prises}/{photo_voulues} capturée !")
            else : print("aucun visage détecté !!")
            
    cam.release()                      
    cv2.destroyAllWindows()
    db.save()

def reconnaissance_temps_reel(db,recognizer) :

    known_encodings, known_names = db.get_all_encodings()

    cam =cv2.VideoCapture("http://host.docker.internal:4747/video")
    print ("appuyer sur 'q' pour quitter")

    while True :
        ret,frame = cam.read()
        locations ,encodings = recognizer.face_detecter(frame)
        #pour chaque visage
        for location, encoding in zip(locations,encodings) :
            #reconaitre le visage
            name, confidence = recognizer.face_recognize(encoding,known_encodings,known_names)
            #dessiner rectangle

            top,right,bottom,left = location
            cv2.rectangle(frame,(left, top),(right,bottom), (0,255,0),2)

            #afficher le nom

            label = f"{name} ({confidence:.0f}%)" if name else "Inconnu"
            cv2.putText(frame,label,(left,top - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Reconnaissance",frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cam.release()
    cv2.destroyAllWindows()

def main() :
    db=Database()
    recognizer = FaceRecognizer()
    while True :
        choix = menu()
        if choix =="1" :
            enregistrer_visage (db , recognizer)
        elif choix == "2" :
            reconnaissance_temps_reel(db, recognizer)
        elif choix =="3" :
            print("bye bye")
            break
        else : print ("mauvais choix")

if __name__ == "__main__":
    main()
