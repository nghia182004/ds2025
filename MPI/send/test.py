from mpi4py import MPI
import base64
import os

def send_file(filename, comm, dest_rank):
    try:
        with open(filename, "rb") as f:
            file_data = f.read()
            encoded_data = base64.b64encode(file_data).decode('utf-8')
        
        # Send filename first, then the data
        comm.send(filename, dest=dest_rank, tag=1)
        comm.send(encoded_data, dest=dest_rank, tag=2)
        return True
    except Exception as e:
        print(f"Error sending file: {e}")
        return False

def receive_file(comm, source_rank):
    try:
        # Receive filename first, then the data
        filename = comm.recv(source=source_rank, tag=1)
        encoded_data = comm.recv(source=source_rank, tag=2)
        
        # Create 'received' directory if it doesn't exist
        os.makedirs("received", exist_ok=True)
        save_path = os.path.join("received", f"received_{filename}")
        
        with open(save_path, "wb") as f:
            f.write(base64.b64decode(encoded_data))
        return True
    except Exception as e:
        print(f"Error receiving file: {e}")
        return False

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        print("This program requires at least 2 MPI processes")
        return

    if rank == 0:  # Sender process
        filename = "send.txt"
        print(f"Process {rank}: Attempting to send {filename}")
        
        if send_file(filename, comm, dest_rank=1):
            print(f"Process {rank}: File sent successfully")
        else:
            print(f"Process {rank}: Failed to send file")

    elif rank == 1:  # Receiver process
        print(f"Process {rank}: Waiting to receive file...")
        
        if receive_file(comm, source_rank=0):
            print(f"Process {rank}: File received successfully")
        else:
            print(f"Process {rank}: Failed to receive file")

if __name__ == "__main__":
    main()