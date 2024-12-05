from xmlrpc.server import SimpleXMLRPCServer
import base64

def receive_file(file_data, filename):
    try:
        with open(filename, "wb") as f:
            f.write(base64.b64decode(file_data))
        return f"File {filename} saved successfully."
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080

    try:
      
        server = SimpleXMLRPCServer((host, port), allow_none=True)
        print("RPC Server started successfully.")

        
        server.register_function(receive_file, "receive_file")
        print("Server is listening...")

     
        server.serve_forever()

    except Exception as e:
        print(f"Error: {e}")
