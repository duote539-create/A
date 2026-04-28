# A 语言规范

## 1. 语法规则

### 1.1 基本语法

- **注释**：单行注释使用 `//`，多行注释使用 `/* */`
- **语句**：每个语句以分号 `;` 结束
- **代码块**：使用大括号 `{ }` 包围代码块
- **缩进**：建议使用 4 个空格进行缩进，但不强制

### 1.2 变量声明

```nova
// 显式类型声明
int x = 10;
float y = 3.14;
bool z = true;
string s = "Hello";

// 类型推断
var a = 20; // 推断为 int
var b = 2.718; // 推断为 float
var c = "World"; // 推断为 string
```

### 1.3 控制流

#### 1.3.1 条件语句

```nova
if (condition) {
    // 代码块
} else if (anotherCondition) {
    // 代码块
} else {
    // 代码块
}
```

#### 1.3.2 循环语句

```nova
// for 循环
for (int i = 0; i < 10; i++) {
    // 代码块
}

// while 循环
while (condition) {
    // 代码块
}

// do-while 循环
do {
    // 代码块
} while (condition);

// foreach 循环
foreach (var item in collection) {
    // 代码块
}
```

### 1.4 函数定义

```nova
// 函数定义
int add(int a, int b) {
    return a + b;
}

// 函数调用
int result = add(5, 3);
```

### 1.5 类和结构体

```nova
// 结构体定义
struct Point {
    int x;
    int y;
}

// 类定义
class Person {
    string name;
    int age;
    
    // 构造函数
    Person(string n, int a) {
        name = n;
        age = a;
    }
    
    // 方法
    void sayHello() {
        print("Hello, my name is " + name);
    }
}
```

## 2. 关键字定义

| 关键字 | 描述 |
|-------|------|
| `var` | 变量声明（类型推断） |
| `int` | 整数类型 |
| `float` | 浮点数类型 |
| `bool` | 布尔类型 |
| `char` | 字符类型 |
| `string` | 字符串类型 |
| `array` | 数组类型 |
| `struct` | 结构体定义 |
| `class` | 类定义 |
| `interface` | 接口定义 |
| `enum` | 枚举定义 |
| `function` | 函数定义 |
| `return` | 返回语句 |
| `if` | 条件语句 |
| `else` | 条件语句的 else 分支 |
| `for` | for 循环 |
| `while` | while 循环 |
| `do` | do-while 循环 |
| `foreach` | foreach 循环 |
| `break` | 跳出循环 |
| `continue` | 继续循环 |
| `try` | 异常处理 |
| `catch` | 异常处理 |
| `throw` | 抛出异常 |
| `import` | 导入模块 |
| `export` | 导出模块 |
| `public` | 公共访问修饰符 |
| `private` | 私有访问修饰符 |
| `protected` | 保护访问修饰符 |
| `static` | 静态成员 |
| `const` | 常量 |
| `let` | 不可变变量 |
| `async` | 异步函数 |
| `await` | 等待异步操作 |
| `go` | 启动协程 |
| `channel` | 通道类型 |

## 3. 操作符优先级

| 优先级 | 操作符 | 描述 |
|-------|--------|------|
| 1 | `()` | 括号 |
| 2 | `!`, `~`, `-` | 一元操作符 |
| 3 | `*`, `/`, `%` | 乘法、除法、取模 |
| 4 | `+`, `-` | 加法、减法 |
| 5 | `<<`, `>>` | 左移、右移 |
| 6 | `<`, `<=`, `>`, `>=` | 比较操作符 |
| 7 | `==`, `!=` | 相等、不等 |
| 8 | `&` | 按位与 |
| 9 | `^` | 按位异或 |
| 10 | `|` | 按位或 |
| 11 | `&&` | 逻辑与 |
| 12 | `||` | 逻辑或 |
| 13 | `?:` | 三元操作符 |
| 14 | `=`, `+=`, `-=`, `*=`, `/=`, `%=` | 赋值操作符 |

## 4. 数据类型

### 4.1 基本类型

| 类型 | 描述 | 大小 | 范围 |
|------|------|------|------|
| `int` | 整数 | 32 位 | -2^31 到 2^31-1 |
| `float` | 浮点数 | 64 位 | 双精度浮点数 |
| `bool` | 布尔值 | 1 位 | `true` 或 `false` |
| `char` | 字符 | 16 位 | Unicode 字符 |
| `string` | 字符串 | 可变长度 |  Unicode 字符串 |

### 4.2 复合类型

#### 4.2.1 数组

```nova
// 数组声明
int[] numbers = [1, 2, 3, 4, 5];
string[] names = ["Alice", "Bob", "Charlie"];

// 数组访问
int first = numbers[0];
string last = names[names.length - 1];
```

#### 4.2.2 结构体

```nova
struct Point {
    int x;
    int y;
}

// 结构体实例化
Point p = Point(10, 20);

// 结构体成员访问
int x = p.x;
int y = p.y;
```

#### 4.2.3 枚举

```nova
enum Color {
    RED,
    GREEN,
    BLUE
}

// 枚举使用
Color c = Color.RED;
```

### 4.3 引用类型

#### 4.3.1 类

```nova
class Person {
    string name;
    int age;
    
    Person(string n, int a) {
        name = n;
        age = a;
    }
    
    void sayHello() {
        print("Hello, my name is " + name);
    }
}

// 类实例化
Person person = Person("Alice", 30);

// 方法调用
person.sayHello();
```

#### 4.3.2 接口

```nova
interface Shape {
    float area();
}

class Circle implements Shape {
    float radius;
    
    Circle(float r) {
        radius = r;
    }
    
    float area() {
        return 3.14159 * radius * radius;
    }
}
```

## 5. 标准库接口

### 5.1 基础库

#### 5.1.1 字符串处理

```nova
// 字符串长度
int length = "Hello".length();

// 字符串连接
string combined = "Hello" + " " + "World";

// 字符串分割
string[] parts = "a,b,c".split(",");

// 字符串查找
int index = "Hello World".indexOf("World");

// 字符串替换
string replaced = "Hello World".replace("World", "A");
```

#### 5.1.2 数学运算

```nova
// 绝对值
int abs = Math.abs(-10);

// 平方根
float sqrt = Math.sqrt(16);

// 幂运算
float pow = Math.pow(2, 3);

// 三角函数
float sin = Math.sin(Math.PI / 2);
float cos = Math.cos(0);
float tan = Math.tan(Math.PI / 4);
```

#### 5.1.3 文件操作

```nova
// 读取文件
string content = File.read("example.txt");

// 写入文件
File.write("example.txt", "Hello A");

// 检查文件是否存在
bool exists = File.exists("example.txt");

// 获取文件大小
int size = File.size("example.txt");
```

### 5.2 网络库

#### 5.2.1 HTTP 客户端

```nova
// 发送 GET 请求
HttpResponse response = Http.get("https://api.example.com/data");
string body = response.body;
int statusCode = response.statusCode;

// 发送 POST 请求
HttpResponse postResponse = Http.post("https://api.example.com/data", "{\"name\": \"A\"}");
```

#### 5.2.2 TCP/IP 通信

```nova
// 创建 TCP 服务器
TcpServer server = TcpServer(8080);
server.listen((client) => {
    string message = client.read();
    client.write("Hello " + message);
    client.close();
});

// 创建 TCP 客户端
TcpClient client = TcpClient("localhost", 8080);
client.write("A");
string response = client.read();
client.close();
```

### 5.3 并发库

#### 5.3.1 线程

```nova
// 创建线程
Thread thread = Thread(() => {
    for (int i = 0; i < 10; i++) {
        print("Thread: " + i);
        Thread.sleep(100);
    }
});

// 启动线程
thread.start();

// 等待线程完成
thread.join();
```

#### 5.3.2 协程

```nova
// 异步函数
async function fetchData() {
    HttpResponse response = await Http.get("https://api.example.com/data");
    return response.body;
}

// 调用异步函数
string data = await fetchData();
print(data);
```

#### 5.3.3 通道

```nova
// 创建通道
Channel<int> channel = Channel<int>();

// 发送数据
go {
    for (int i = 0; i < 5; i++) {
        channel.send(i);
    }
    channel.close();
};

// 接收数据
foreach (var value in channel) {
    print("Received: " + value);
}
```

### 5.4 数据结构

#### 5.4.1 集合

```nova
// 列表
List<int> numbers = [1, 2, 3];
numbers.add(4);
numbers.remove(2);
bool contains = numbers.contains(3);

// 映射
Map<string, int> scores = {
    "Alice": 95,
    "Bob": 85,
    "Charlie": 90
};
scores["David"] = 88;
int aliceScore = scores["Alice"];

// 集合
Set<string> names = {"Alice", "Bob", "Charlie"};
names.add("David");
names.remove("Bob");
bool hasAlice = names.contains("Alice");
```

### 5.5 I/O 库

#### 5.5.1 控制台输入输出

```nova
// 输出
print("Hello A");

// 输入
string input = readLine();
print("You entered: " + input);
```

#### 5.5.2 文件 I/O

```nova
// 打开文件
File file = File.open("example.txt", "w");

// 写入文件
file.write("Hello A");

// 关闭文件
file.close();

// 读取文件
File readFile = File.open("example.txt", "r");
string content = readFile.readAll();
readFile.close();
```

### 5.6 加密库

#### 5.6.1 哈希

```nova
// MD5 哈希
string md5Hash = Crypto.md5("Hello A");

// SHA256 哈希
string sha256Hash = Crypto.sha256("Hello A");
```

#### 5.6.2 加密/解密

```nova
// AES 加密
string encrypted = Crypto.aesEncrypt("Hello A", "secretKey");

// AES 解密
string decrypted = Crypto.aesDecrypt(encrypted, "secretKey");
```