import time
import os
from dotenv import load_dotenv

load_dotenv()

def retry_on_error(func, retries=5, delay=5, *args, **kwargs):
    for _ in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    print(f"Failed after {retries} retries.")
    return None