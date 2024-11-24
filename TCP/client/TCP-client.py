import socket

if __name__ == '__main__':
   
    host = '127.0.0.1'
    port = 8080

    try:
      
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client socket created successfully.")


        sock.connect((host, port))
        print("Connected to Server.")

        
        filename = 'send.txt'
        try:
            with open(filename, "r") as fi:
                data = fi.read()
                while data:
                    sock.send(data.encode())
                    data = fi.read()
            
            print("File data sent successfully.")

        except FileNotFoundError:
            print('File not found!')

    except Exception as e:
        print(f"An error occurred: {e}")

    
    print("Closing the connection.")
    sock.close()
