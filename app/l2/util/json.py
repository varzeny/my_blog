#util/json.py

# lib
import json

# attribusion

# method
def read_json_from_file(path:str):
    print("open config file : ", path)
    try:
        with open( path, 'r' ) as file:
            return json.load( file )
    except Exception as e:
        print("error from util_manager : ", e)
        return None
