import time
import os
import scripts.test as test
import easyocr
from scripts.storage_manager import storage_manager


def remove_files_from_local(paths=["./LR/", "./results/"]) :
    for path in paths :
        files = os.listdir(path)
        for file in files :
            file_path = path + file
            if os.path.exists(file_path) :
                os.remove(file_path)
                
                
def validate_plate_nos(all_plates_details) :
    for plate in all_plates_details :
        # removing all spaces from the plate no
        plate_no = "".join([i for i in plate["plate_no"] if i!=" "])
        if len(plate_no) == 6 and plate_no[:2].isalpha() and plate_no[2:].isnumeric() :
            plate["valid"] = True
        else :
            plate["valid"] = False
            
    return all_plates_details


def infinite_find_n_process_plates() :
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
            all_plates_details = list()
            for e_file in enhanced_files :
                reader = easyocr.Reader(['en'])
                result = reader.readtext("results/" + e_file)
                plate_details = {
                    "vehicle_id": e_file[5:-6],
                    "vehicle_counter": e_file[-5:-4],
                    "plate_no": "".join([i[1] for i in result]),
                    "plate_file": e_file
                }
                all_plates_details.append(plate_details)
            
            # Put the enhanced plate images to firebase storage
            storage_manager.put_to_firebase_storage()
            # Validate the plate numbers identified
            plates_details = validate_plate_nos(all_plates_details)
            # Put the vehicle's details into MongoDB
            storage_manager.put_to_mongodb(plates_details)
            # Clear all files in the LR and results directory
            remove_files_from_local()

        # Put porcess to sleep for 5 seconds
        time.sleep(5)


def find_n_process_plates() :
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
        all_plates_details = list()
        for e_file in enhanced_files :
            reader = easyocr.Reader(['en'], gpu=False)
            result = reader.readtext("results/" + e_file)
            plate_details = {
                "vehicle_id": e_file[5:-6],
                "vehicle_counter": e_file[-5:-4],
                "plate_no": "".join([i[1] for i in result]),
                "plate_file": e_file
            }
            all_plates_details.append(plate_details)
        
        # Put the enhanced plate images to firebase storage
        storage_manager.put_to_firebase_storage()
        # Validate the plate numbers identified
        plates_details = validate_plate_nos(all_plates_details)
        # Put the vehicle's details into MongoDB
        storage_manager.put_to_mongodb(plates_details)
        # Clear all files in the LR and results directory
        remove_files_from_local()

    ## Put porcess to sleep for 5 seconds
    # time.sleep(5)
 

if __name__ =="__main__" :
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    infinite_find_n_process_plates()