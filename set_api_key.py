import os
import sys

def set_api_key():
    if len(sys.argv) < 2:
        print("Please provide the API key as a command-line argument.")
        sys.exit(1)

    # Get the API key from the command-line argument
    api_key = sys.argv[1]

    # Setting environment variable
    os.environ['API_KEY'] = api_key
    api_key = sys.argv[1]
    api_key = os.environ.get('GOOGLE_API_KEY_VARIABLE')

    # try:
    #     api_key = os.environ.get('GOOGLE_API_KEY_VARIABLE')
    #     print('------ API KEY IS SET -------')
    # except Exception as e:
    #     print('------ Setting API KEY AS ENV VAR -----')
    #     os.environ['GOOGLE_API_KEY_VARIABLE'] = api_key
    
    
if __name__ == "__main__":
    set_api_key()