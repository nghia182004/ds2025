import socket

if __name__ == '__main__':
   
    host = '127.0.0.1'
    port = 8080

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server socket created successfully.")
        
        sock.bind((host, port))
        print("Binding successful.")

        sock.listen(1) 
        print("Listening....")

       
        conn, addr = sock.accept()
        print(f"Connected with client: {addr}")

        
        data = conn.recv(1024).decode()
        if data:
           
            filename = 'recv.txt'
            with open(filename, "w") as fo:
                while data:
                    fo.write(data)
                    data = conn.recv(1024).decode()
            
            print("Data written in the file successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    conn.close()
    sock.close()
