# 基础标准库

# 字符串处理函数
def len(s):
    """返回字符串长度"""
    return len(s)

def split(s, sep=None):
    """分割字符串"""
    return s.split(sep)

def join(sep, *args):
    """连接字符串"""
    return sep.join(args)

def substring(s, start, end=None):
    """获取子字符串"""
    if end is None:
        return s[start:]
    else:
        return s[start:end]

def find(s, sub):
    """查找子字符串"""
    return s.find(sub)

def replace(s, old, new):
    """替换字符串"""
    return s.replace(old, new)

def lower(s):
    """转换为小写"""
    return s.lower()

def upper(s):
    """转换为大写"""
    return s.upper()

def trim(s):
    """去除首尾空白"""
    return s.strip()

# 数学运算函数
class Math:
    """数学函数类"""
    
    PI = 3.141592653589793
    E = 2.718281828459045
    
    @staticmethod
    def abs(x):
        """绝对值"""
        return abs(x)
    
    @staticmethod
    def sqrt(x):
        """平方根"""
        import math
        return math.sqrt(x)
    
    @staticmethod
    def pow(x, y):
        """幂运算"""
        return x ** y
    
    @staticmethod
    def sin(x):
        """正弦函数"""
        import math
        return math.sin(x)
    
    @staticmethod
    def cos(x):
        """余弦函数"""
        import math
        return math.cos(x)
    
    @staticmethod
    def tan(x):
        """正切函数"""
        import math
        return math.tan(x)
    
    @staticmethod
    def floor(x):
        """向下取整"""
        import math
        return math.floor(x)
    
    @staticmethod
    def ceil(x):
        """向上取整"""
        import math
        return math.ceil(x)
    
    @staticmethod
    def round(x, n=0):
        """四舍五入"""
        return round(x, n)

# 类型转换函数
def int(x):
    """转换为整数"""
    return int(x)

def float(x):
    """转换为浮点数"""
    return float(x)

def str(x):
    """转换为字符串"""
    return str(x)

def bool(x):
    """转换为布尔值"""
    return bool(x)

# 其他基础函数
def print(*args):
    """打印函数"""
    import sys
    sys.stdout.write(" ".join(map(str, args)) + "\n")

def input(prompt=""):
    """输入函数"""
    import sys
    sys.stdout.write(prompt)
    return sys.stdin.readline().strip()

def exit(code=0):
    """退出函数"""
    import sys
    sys.exit(code)

# 时间函数
class Time:
    """时间函数类"""
    
    @staticmethod
    def now():
        """获取当前时间"""
        import time
        return time.time()
    
    @staticmethod
    def sleep(seconds):
        """睡眠指定秒数"""
        import time
        time.sleep(seconds)
    
    @staticmethod
    def strftime(format):
        """格式化时间"""
        import time
        return time.strftime(format)

# 操作系统函数
class OS:
    """操作系统函数类"""
    
    @staticmethod
    def getcwd():
        """获取当前工作目录"""
        import os
        return os.getcwd()
    
    @staticmethod
    def chdir(path):
        """更改工作目录"""
        import os
        os.chdir(path)
    
    @staticmethod
    def listdir(path="."):
        """列出目录内容"""
        import os
        return os.listdir(path)
    
    @staticmethod
    def mkdir(path):
        """创建目录"""
        import os
        os.mkdir(path)
    
    @staticmethod
    def remove(path):
        """删除文件"""
        import os
        os.remove(path)
    
    @staticmethod
    def rename(src, dst):
        """重命名文件或目录"""
        import os
        os.rename(src, dst)