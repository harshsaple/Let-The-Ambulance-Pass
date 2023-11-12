from cryptography.fernet import Fernet
import base64
import os

# File where the encrypted API key will be stored
ENCRYPTED_FILE = 'encrypted_api_key.bin'

def generate_key(pin):
    """Generate a key based on the pin code."""
    pin_str = str(pin)  # Convert pin to string
    return base64.urlsafe_b64encode(pin_str.zfill(32).encode())

def setup_api_key(api_key, pin):
    """Encrypt and save the API key using the pin code."""
    key = generate_key(pin)
    fernet = Fernet(key)
    encrypted_api_key = fernet.encrypt(api_key.encode())

    with open(ENCRYPTED_FILE, 'wb') as file:
        file.write(encrypted_api_key)
    return "API key encrypted and saved."

def read_api_key(pin):
    """Read and decrypt the API key using the pin code."""
    if not os.path.exists(ENCRYPTED_FILE):
        return "No encrypted API key found."

    key = generate_key(pin)
    fernet = Fernet(key)

    try:
        with open(ENCRYPTED_FILE, 'rb') as file:
            encrypted_api_key = file.read()
        return fernet.decrypt(encrypted_api_key).decode()
    except Exception:
        return "Invalid pin or error in decryption."

def delete_api_key():
    """Delete the file containing the encrypted API key."""
    if os.path.exists(ENCRYPTED_FILE):
        os.remove(ENCRYPTED_FILE)
        return "API key deleted."
    else:
        return "No API key to delete."

def main():
    while True:
        print("\nAPI Key Manager")
        print("1. Set up a new API Key")
        print("2. Read API Key")
        print("3. Delete API Key")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            api_key = input("Enter the API key: ")
            pin = input("Enter a pin code for encryption: ")
            response = setup_api_key(api_key, pin)
            print(response)
        elif choice == '2':
            pin = input("Enter your pin code to decrypt the API key: ")
            api_key = read_api_key(pin)
            print("API Key:", api_key)
        elif choice == '3':
            response = delete_api_key()
            print(response)
        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
