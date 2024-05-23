import pyrebase
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime


class StorageManager :
    CONFIG = {
        "apiKey": os.environ.get("apiKey"),
        "authDomain": os.environ.get("authDomain"),
        "projectId": os.environ.get("projectId"),
        "storageBucket": os.environ.get("storageBucket"),
        "messagingSenderId": os.environ.get("messageSenderId"),
        "appId": os.environ.get("appId"),
        "measurementId": os.environ.get("measurementId"),
        "serviceAccount": os.environ.get("serviceAccount"),
        "databaseURL": os.environ.get("databaseURL")
    }
    
    FIREBASE_SAVE_LOC = "Speed_detection_AI/enhanced_plates/"
    FIREBASE_LOAD_LOC = "Speed_detection_AI/plates/"

    def __init__(self) -> None:
        # Initialize firebase
        self.firebase = pyrebase.initialize_app(self.CONFIG)
        self.storage = self.firebase.storage()
        self.old_plates = list()
        
        # Initialize mongodb
        self.uri = os.environ.get("MONGO_DB_URI")
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.speed_db = self.client["SpeedAI"]
        print("Connection established with mongodb")
        
        
    def load_old_plates(self) :
        traffic_coll = self.speed_db["Traffic_violation"]
        
        mongo_query = list(traffic_coll.find({}, {"_id": 0, "clip_loc": 1}))
        self.old_plates = [i["clip_loc"][len(self.FIREBASE_SAVE_LOC):] for i in mongo_query]
        print(f"self.old_plates: {self.old_plates}")
        
    
    def download_from_firebase_storage(self, firebase_path=FIREBASE_LOAD_LOC) :
        ## To list all the files in storage
        print("IN DOWNLOAD")
        esp = self.storage.list_files()
        new_plates = list()
        self.load_old_plates()
        for file in esp :
            if file.name[len(self.FIREBASE_LOAD_LOC):] not in self.old_plates and file.name[:len(firebase_path)] == firebase_path :
                new_plates.append(file.name)
        # To download a file from firebase
        for plate_file in new_plates :
            local_path = f"LR/{plate_file[len(firebase_path):]}"
            self.storage.child(firebase_path).download(path=plate_file, filename=local_path)
        
        
    def put_to_firebase_storage(self, results_dir="./results/")  :
        print("IN UPLOAD")
        plates = os.listdir(results_dir)
        for plate in plates :
            file_loc = results_dir + plate
            if os.path.exists(file_loc) :
                self.storage.path = None
                self.storage.child(f"{self.FIREBASE_SAVE_LOC}{plate}").put(file_loc)
                
                
    def put_to_mongodb(self, all_plates_details) :
        traffic_coll = self.speed_db["Traffic_violation"]
        
        for plate in all_plates_details :
            traffic_coll.insert_one(
                {
                    "plate_counter": f"{plate['vehicle_id']}-{plate['vehicle_counter']}",
                    "plate_no": plate["plate_no"],
                    "cam_id": "c_1",
                    "clip_loc": self.FIREBASE_SAVE_LOC + plate["plate_file"],
                    "valid": plate["valid"],
                    "timestamp": datetime.now()
                }
            )
        print("Added all plate details to mongodb")
        

storage_manager = StorageManager()