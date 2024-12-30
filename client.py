# client.py
import socket
import threading

def start_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    
    # Handle incoming messages in a separate thread
    def receive_messages():
        while True:
            try:
                msg = client.recv(1024)
                if not msg:
                    break
                print(msg.decode('utf-8'))
            except:
                break

    threading.Thread(target=receive_messages, daemon=True).start()

    try:
        while True:
            msg = input()
            if msg.lower() == 'exit':
                break
            client.send(msg.encode('utf-8'))
    except KeyboardInterrupt:
        print("\nDisconnected from the server.")
    finally:
        client.close()

if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    start_client(server_ip, server_port)
