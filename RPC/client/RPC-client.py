from xmlrpc.client import ServerProxy
import base64

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    server_url = f"http://{host}:{port}"

    try:
       
        proxy = ServerProxy(server_url)
        print("Connected to the XML-RPC Server.")

       
        filename = 'send.txt'
        try:
            with open(filename, "rb") as f:
                file_data = f.read()
                encoded_data = base64.b64encode(file_data).decode('utf-8')

            
            response = proxy.receive_file(encoded_data, 'recv.txt')
            print(response)

        except FileNotFoundError:
            print("File not found!")

    except Exception as e:
        print(f"Error: {e}")
