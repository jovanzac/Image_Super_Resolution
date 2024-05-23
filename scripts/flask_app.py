from flask import Flask, request, jsonify
from flask_cors import CORS
from scripts.process import find_n_process_plates


app = Flask(__name__)
CORS(app)


@app.route("/update", methods=["GET"])
def home_route() :
    if request.method == "GET" :
        print("STARTING PLATE PROCESSING")
        
        try :
            find_n_process_plates()
            print("DONE WITH PLATE PROCESSING")
            
            return jsonify({
                "Status": "Success",
                "Response": "All new plates have been successfully enhanced and added to the database"
            }), 200
        except Exception as e :
            print(f"Exception '{e}' encountered")
            
            return jsonify({
                "Status": "Failure",
                "Response": f"Failed to enhance plates due to error: {e}"
            }), 401