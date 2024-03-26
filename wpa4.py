import socket
from ecc import generate_key, encrypt_message, decrypt_message , sha256 , generate_random_salt
import argparse


def append_to_file(pk,cm,rh):
    data = f"Public key: {pk}\nCiphertext: {cm}\nReceived hash: {rh}" 
    with open("logs.txt", "a") as f:
        f.write(data + "\n")

def client(password, port):
    password = str(password)
    s = socket.socket()
    s.connect(('localhost', port))
    (private_key, public_key) = generate_key()
    print("Public key: \n", public_key)
    s.send(public_key.encode())
    data = s.recv(1024)
    print("Received ciphertext: \n", data)
    plaintext = str(decrypt_message(private_key, data).decode('utf-8'))
    print("Decrypted message: \n", plaintext)
    hashed_msg = sha256(plaintext + password )
    s.send(hashed_msg.encode())
    response = s.recv(1024).decode()
    append_to_file(public_key, data, hashed_msg)
    if response == "OK":
        print("Authentication successful")
    else:
        print("Authentication failed")
    s.close()

def server(password, port):
    while True:
        try:
            password = str(password)
            s = socket.socket()
            s.bind(('localhost', port))
            s.listen(1)
            print("Waiting for a connection...")
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            public_key = conn.recv(1024).decode()
            agreed_word = generate_random_salt()
            hash_256=sha256(agreed_word + password)
            print("Agreed word: \n", agreed_word) 
            ciphertext = encrypt_message(public_key, agreed_word.encode())
            conn.send(ciphertext)
            hash_salt = conn.recv(1024).decode()
            print("Received hash: \n", hash_salt)
            print("Expected hash: \n", hash_256)
            if hash_salt == hash_256:
                conn.send("OK".encode())
            else:
                conn.send("NO".encode())
            conn.close()
            s.close()
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    """
    Initiates a secure communication session using Elliptic Curve Cryptography (ECC).

    This function serves as the entry point for setting up a secure communication channel
    either in client or server mode. The communication is secured using ECC, with a password
    provided for authentication purposes. The user must specify the mode of operation, the 
    password for authentication, and the port to be used for the communication. 

    In client mode, the function also accepts an optional parameter to repeat the communication 
    process a specified number of times. This feature is not available in server mode. If the 
    repeat option is mistakenly used in server mode, the function will issue a warning and 
    ignore the repeat parameter.

    Parameters:
    - mode (str): Specifies the mode of operation. It can be either 'client' or 'server'.
    - password (str): The password used for authentication purposes.
    - port (int): The port number to connect to or listen on for incoming connections.
    - repeat (int, optional): The number of times to repeat the process in client mode. Defaults to 1.

    Note: The 'repeat' option is only valid in client mode and will be ignored if specified in server mode.
    
    Example of usage:
    - To start as a client: python script.py client secret_password 8080 --repeat 5
    - To start as a server: python script.py server secret_password 8080

    Returns:
    None. The function's primary purpose is to set up and manage secure communications.
    """
    
    parser = argparse.ArgumentParser(description="ECC Secure Communication")
    parser.add_argument("mode", choices=["client", "server"], help="Mode: client or server")
    parser.add_argument("password", help="Password for authentication")
    parser.add_argument("port", type=int, help="Port to connect or listen on")
    parser.add_argument("-r","--repeat", type=int, help="Number of times to repeat the process as a client", default=1)
    args = parser.parse_args()
    if args.mode == "server" and args.repeat:
        print("Repeat option is only available in client mode. Ignoring...")
        return
    if args.mode == "client":
        for _ in range(args.repeat):
            client(args.password, args.port)
        
    else:
        server(args.password, args.port)

if __name__ == "__main__":
    main()