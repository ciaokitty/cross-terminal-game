# server.py
import socket
import threading

# Store room data
rooms = {}

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")
    try:
        client_socket.send(b"Enter room code: ")
        room_code = client_socket.recv(1024).decode('utf-8').strip()
        
        if room_code not in rooms:
            rooms[room_code] = []
        
        rooms[room_code].append(client_socket)
        client_socket.send(b"Connected to the room! Type messages to chat.\n")
        
        # Relay messages to others in the same room
        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            for sock in rooms[room_code]:
                if sock != client_socket:
                    sock.send(msg)
    except ConnectionResetError:
        print(f"Connection lost with {addr}")
    finally:
        # Remove the client from the room
        if room_code in rooms:
            rooms[room_code].remove(client_socket)
            if not rooms[room_code]:  # Cleanup empty room
                del rooms[room_code]
        client_socket.close()

def start_server(host='0.0.0.0', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")
    
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()
