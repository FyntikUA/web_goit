from http.server import BaseHTTPRequestHandler, HTTPServer
import socket, urllib
import json
import os
import threading 
from datetime import datetime

# Клас для обробки HTTP запитів
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    # Обробка GET запитів
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/message.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('message.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/error.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('error.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/style.css':
            self.send_static_file('style.css', 'text/css')
        elif self.path == '/logo.png':
            self.send_static_file('logo.png', 'image/png')
        else:
            #self.send_error(404, 'Not Found')
            self.send_response(302)  # Redirect response code
            self.send_header('Location', '/error.html')  # Redirect to error.html
            self.end_headers()
    # Обробка POST запитів
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_pairs = data_parse.split('&')    # Розбиваємо рядок на окремі пари ключ-значення
        print(data_pairs)
        data_dict = {}                          # Створюємо словник для збереження даних
    
        for pair in data_pairs:                 # Отримуємо значення для ключів "username" і "message"
            key, value = pair.split('=')
            data_dict[key] = value

        send_data_to_server(data_dict)

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        self.wfile.write(b'Message sent successfully!')

    # Функція для відправки статичних файлів
    def send_static_file(self, filename, content_type):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

# Функція для відправки даних на сервер через сокети
def send_data_to_server(data_dict, server_ip='127.0.0.1', server_port=5000):
    # Створення UDP сокету
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        json_data = json.dumps(data_dict)
        # Перетворення рядка JSON у байтовий об'єкт
        bytes_data = json_data.encode('utf-8')
        # Відправка даних на сервер
        client_socket.sendto(bytes_data, (server_ip, server_port))
        print(f'Data sent to {server_ip}:{server_port}')

# Функція для збереження даних у файл JSON
def save_to_json(data):
    print('save_to_json')
    with open('storage/data.json', 'a') as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        json.dump({timestamp: data}, file)
        file.write('\n')


# Клас для обробки даних на UDP сервері
class UDPServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.ip, self.port))

    def start(self):
        print(f'UDP Server listening on {self.ip}:{self.port}...')
        while True:
            data, address = self.server_socket.recvfrom(1024)
            try:
                received_data = json.loads(data.decode())
                print(f'Received data: {received_data} from: {address}')
                # Збереження даних у файл JSON
                save_to_json(received_data)
            except json.JSONDecodeError as e:
                print(f'Error decoding JSON: {e}')

# Функція для запуску HTTP сервера
def run_http_server(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=3000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    # Запускаємо HTTP сервер на порті 3000 у окремому потоці
    http_thread = threading.Thread(target=run_http_server)
    http_thread.start()

    # Запускаємо UDP сервер на порті 5000 у головному потоці
    UDP_IP = '127.0.0.1'
    UDP_PORT = 5000
    udp_server = UDPServer(UDP_IP, UDP_PORT)
    udp_server.start()
