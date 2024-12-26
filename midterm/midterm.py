from mpi4py import MPI
import subprocess
import sys
import os

def execute_command(command):
    try:
        process = subprocess.Popen(
            ['powershell.exe', '-Command', command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        output, error = process.communicate()
        if error:
            return f"Error: {error}"
        return output if output else "Command executed successfully (no output)"
    except Exception as e:
        return f"Error executing command: {str(e)}"

def server_process(comm, rank):
    print(f"[Server {rank}] Started", flush=True)
    while True:
        status = MPI.Status()
        command = comm.recv(source=MPI.ANY_SOURCE, tag=1, status=status)
        client_rank = status.Get_source()
        
        print(f"[Server] Received command '{command}' from client {client_rank}", flush=True)
        
        if command.lower() == 'exit':
            response = "Goodbye!"
        else:
            response = execute_command(command)
        
        comm.send(response, dest=client_rank, tag=2)
        
        if command.lower() == 'exit' and client_rank == comm.Get_size() - 1:
            break

def client_process(comm, rank):
    # Create a new console window for this client
    if sys.platform == 'win32':
        subprocess.run(['start', 'cmd', '/k', 'title', f'Client {rank}'], shell=True)
    
    print(f"[Client {rank}] Started", flush=True)
    
    while True:
        try:
            command = input(f"\n[Client {rank}]$ ")
            comm.send(command, dest=0, tag=1)
            response = comm.recv(source=0, tag=2)
            print(f"\nResponse:\n{response}", flush=True)
            
            if command.lower() == 'exit':
                break
                
        except Exception as e:
            print(f"[Client {rank}] Error: {e}", flush=True)
            break
    
    print(f"[Client {rank}] Disconnected", flush=True)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 3:
        print("Need at least 3 processes (1 server + 2 clients)")
        return

    try:
        if rank == 0:
            server_process(comm, rank)
        else:
            client_process(comm, rank)
    except Exception as e:
        print(f"Process {rank} error: {e}", flush=True)

if __name__ == "__main__":
    main()