import pyrebase
import os


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

    def __init__(self) -> None:
        self.firebase = pyrebase.initialize_app(self.CONFIG)
        self.storage = self.firebase.storage()
        self.old_plates = list()
        
    
    def download_from_firebase_storage(self, firebase_path="Speed_detection_AI/plates") :
        ## To list all the files in storage
        print("IN DOWNLOAD")
        esp = self.storage.list_files()
        new_plates = list()
        for file in esp :
            if file.name not in self.old_plates and file.name[:len(firebase_path)] == firebase_path :
                new_plates.append(file.name)
        # To download a file from firebase
        for plate_file in new_plates :
            local_path = f"LR{plate_file[len(firebase_path):]}"
            self.storage.child(firebase_path).download(path=plate_file, filename=local_path)
            
        # Add the processed plates to old_plates list
        self.old_plates.extend(new_plates)
        
        
    def put_to_firebase_storage(self, results_dir="./results/")  :
        print("IN UPLOAD")
        plates = os.listdir(results_dir)
        for plate in plates :
            file_loc = results_dir + plate
            if os.path.exists(file_loc) :
                self.storage.path = None
                self.storage.child(f"Speed_detection_AI/enhanced_plates/{plate}").put(file_loc)