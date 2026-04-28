# 网络标准库

# HTTP 客户端
class Http:
    """HTTP 客户端类"""
    
    @staticmethod
    def get(url, headers=None):
        """发送 GET 请求"""
        import urllib.request
        import urllib.error
        
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req) as response:
                return {
                    'status_code': response.getcode(),
                    'headers': dict(response.getheaders()),
                    'body': response.read().decode('utf-8')
                }
        except urllib.error.URLError as e:
            return {
                'status_code': 500,
                'headers': {},
                'body': str(e)
            }
    
    @staticmethod
    def post(url, data=None, headers=None):
        """发送 POST 请求"""
        import urllib.request
        import urllib.error
        import json
        
        try:
            if data:
                if isinstance(data, dict):
                    data = json.dumps(data).encode('utf-8')
                    headers = headers or {}
                    headers['Content-Type'] = 'application/json'
                elif isinstance(data, str):
                    data = data.encode('utf-8')
            
            req = urllib.request.Request(url, data=data, headers=headers or {})
            with urllib.request.urlopen(req) as response:
                return {
                    'status_code': response.getcode(),
                    'headers': dict(response.getheaders()),
                    'body': response.read().decode('utf-8')
                }
        except urllib.error.URLError as e:
            return {
                'status_code': 500,
                'headers': {},
                'body': str(e)
            }
    
    @staticmethod
    def put(url, data=None, headers=None):
        """发送 PUT 请求"""
        import urllib.request
        import urllib.error
        import json
        
        try:
            if data:
                if isinstance(data, dict):
                    data = json.dumps(data).encode('utf-8')
                    headers = headers or {}
                    headers['Content-Type'] = 'application/json'
                elif isinstance(data, str):
                    data = data.encode('utf-8')
            
            req = urllib.request.Request(url, data=data, headers=headers or {})
            req.get_method = lambda: 'PUT'
            with urllib.request.urlopen(req) as response:
                return {
                    'status_code': response.getcode(),
                    'headers': dict(response.getheaders()),
                    'body': response.read().decode('utf-8')
                }
        except urllib.error.URLError as e:
            return {
                'status_code': 500,
                'headers': {},
                'body': str(e)
            }
    
    @staticmethod
    def delete(url, headers=None):
        """发送 DELETE 请求"""
        import urllib.request
        import urllib.error
        
        try:
            req = urllib.request.Request(url, headers=headers or {})
            req.get_method = lambda: 'DELETE'
            with urllib.request.urlopen(req) as response:
                return {
                    'status_code': response.getcode(),
                    'headers': dict(response.getheaders()),
                    'body': response.read().decode('utf-8')
                }
        except urllib.error.URLError as e:
            return {
                'status_code': 500,
                'headers': {},
                'body': str(e)
            }

# TCP 客户端
class TcpClient:
    """TCP 客户端类"""
    
    def __init__(self, host, port):
        """初始化 TCP 客户端"""
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self):
        """连接到服务器"""
        import socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def send(self, data):
        """发送数据"""
        if not self.socket:
            return False
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            self.socket.sendall(data)
            return True
        except Exception as e:
            print(f"Send error: {e}")
            return False
    
    def receive(self, buffer_size=1024):
        """接收数据"""
        if not self.socket:
            return None
        try:
            data = self.socket.recv(buffer_size)
            return data.decode('utf-8')
        except Exception as e:
            print(f"Receive error: {e}")
            return None
    
    def close(self):
        """关闭连接"""
        if self.socket:
            self.socket.close()
            self.socket = None

# TCP 服务器
class TcpServer:
    """TCP 服务器类"""
    
    def __init__(self, port):
        """初始化 TCP 服务器"""
        self.port = port
        self.socket = None
        self.running = False
    
    def listen(self, handler):
        """开始监听"""
        import socket
        import threading
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('0.0.0.0', self.port))
            self.socket.listen(5)
            self.running = True
            
            print(f"Server listening on port {self.port}")
            
            while self.running:
                client_socket, client_address = self.socket.accept()
                print(f"Connection from {client_address}")
                
                # 创建新线程处理客户端连接
                thread = threading.Thread(target=handler, args=(TcpClientWrapper(client_socket),))
                thread.daemon = True
                thread.start()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.close()
    
    def close(self):
        """关闭服务器"""
        self.running = False
        if self.socket:
            self.socket.close()
            self.socket = None

# TCP 客户端包装器
class TcpClientWrapper:
    """TCP 客户端包装器"""
    
    def __init__(self, socket):
        """初始化客户端包装器"""
        self.socket = socket
    
    def send(self, data):
        """发送数据"""
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            self.socket.sendall(data)
            return True
        except Exception as e:
            print(f"Send error: {e}")
            return False
    
    def receive(self, buffer_size=1024):
        """接收数据"""
        try:
            data = self.socket.recv(buffer_size)
            return data.decode('utf-8')
        except Exception as e:
            print(f"Receive error: {e}")
            return None
    
    def close(self):
        """关闭连接"""
        if self.socket:
            self.socket.close()

# UDP 客户端
class UdpClient:
    """UDP 客户端类"""
    
    def __init__(self, host, port):
        """初始化 UDP 客户端"""
        import socket
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send(self, data):
        """发送数据"""
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            self.socket.sendto(data, (self.host, self.port))
            return True
        except Exception as e:
            print(f"Send error: {e}")
            return False
    
    def receive(self, buffer_size=1024):
        """接收数据"""
        try:
            data, addr = self.socket.recvfrom(buffer_size)
            return data.decode('utf-8'), addr
        except Exception as e:
            print(f"Receive error: {e}")
            return None, None
    
    def close(self):
        """关闭连接"""
        if self.socket:
            self.socket.close()

# UDP 服务器
class UdpServer:
    """UDP 服务器类"""
    
    def __init__(self, port):
        """初始化 UDP 服务器"""
        import socket
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', self.port))
        self.running = False
    
    def listen(self, handler):
        """开始监听"""
        self.running = True
        print(f"UDP server listening on port {self.port}")
        
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                print(f"Message from {addr}: {data.decode('utf-8')}")
                handler(data.decode('utf-8'), addr, self.socket)
            except Exception as e:
                print(f"Server error: {e}")
    
    def close(self):
        """关闭服务器"""
        self.running = False
        if self.socket:
            self.socket.close()