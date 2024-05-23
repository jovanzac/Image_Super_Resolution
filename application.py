from dotenv import load_dotenv
load_dotenv(override=True)

from scripts.flask_app import app as application


if __name__ == "__main__" :
    application.run()