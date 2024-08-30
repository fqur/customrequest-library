import socket, ssl, json
from fake_useragent import UserAgent

def parse_url(url):
    scheme, rest = url.split('://', 1)
    if '/' in rest:
        host, path = rest.split('/', 1)
        path = '/' + path
    else:
        host = rest
        path = '/'
    return scheme, host, path

def create_socket(host, port, scheme):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if scheme == 'https':
        context = ssl.create_default_context()
        s = context.wrap_socket(s, server_hostname=host)
    s.connect((host, port))
    return s

def send_request(sock, method, host, path, headers, body):
    request = f"{method} {path} HTTP/1.1\r\n"
    request += f"Host: {host}\r\n" 
    request += "Connection: close\r\n"
    for key, value in headers.items():
        request += f"{key}: {value}\r\n"
    if body:
        request += f"Content-Length: {len(body)}\r\n"
        request += "Content-Type: application/json\r\n"  
    request += "\r\n"
    if body:
        request += body
    print(f"Request sent:\n{request}") #DebugPrint
    sock.sendall(request.encode())

def recieve_response(sock):
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    print(f"Response received:\n{response.decode()}") #DebugPrint
    return response.decode()

def http_request(method, url, headers=None, body=None, random_ua=False):
    if headers is None:
        headers = {}
    if random_ua:
        ua = UserAgent()
        headers['User-Agent'] = ua.random

    scheme, host, path = parse_url(url)
    port = 443 if scheme == 'https' else 80
    
    try:
        with create_socket(host, port, scheme) as sock:
            send_request(sock, method, host, path, headers, body)
            response = recieve_response(sock)
    except Exception as e:
        print(f"An error occurred: {e}") 
    
    return response

def get_request(url, headers=None, random_ua=False):
    return http_request("GET", url, headers, random_ua=random_ua)

def post_request(url, data=None, headers=None, random_ua=False):
    if data is not None:
        body = json.dumps(data)
    else:
        body = None
    if headers is None:
        headers = {}
    if random_ua:
        ua = UserAgent()
        headers['User-Agent'] = ua.random
    headers['Content-Type'] = 'application/json'  
    return http_request("POST", url, headers, body, random_ua=random_ua)

def delete_request(url, headers=None, random_ua=False):
    return http_request("DELETE", url, headers, random_ua=random_ua)


