from dotenv import load_dotenv
load_dotenv(override=True)

from scripts.process import infinite_find_n_process_plates


if __name__ == "__main__" :
    infinite_find_n_process_plates()