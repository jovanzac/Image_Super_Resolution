import time
import os
import scripts.test as test
import easyocr
from scripts.storage_manager import StorageManager


def remove_files_from_local(paths=["./LR/", "./results/"]) :
    for path in paths :
        files = os.listdir(path)
        for file in files :
            file_path = path + file
            if os.path.exists(file_path) :
                os.remove(file_path)


def search_loop() :
    while True :
        print(time.ctime())
        # Download all the new files to LR folder
        storage_manager.download_from_firebase_storage()
        # List all the files in LR
        files = os.listdir("LR/")
        if files :
            for file in files :
                # Perform image super resolution on each of the images
                test.main(path=f"./LR/{file}")
                enhanced_files = os.listdir("results/")
                plate_nos = list()
                for e_file in enhanced_files :
                    reader = easyocr.Reader(['ch_sim','en'])
                    result = reader.readtext("results/" + e_file)
                    plate_nos.append("".join([i[1] for i in result])+"\n")
        
            with open("plates.txt", "w+") as f :
                f.writelines(plate_nos)
                
            # Put the enhanced plate images to firebase storage
            storage_manager.put_to_firebase_storage()
            # Clear all files in the LR and results directory
            remove_files_from_local(["./LR/"])

        # Put porcess to sleep for 5 seconds
        time.sleep(5)
        
storage_manager = StorageManager()
 

if __name__ =="__main__" :
    search_loop()