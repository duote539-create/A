# A 语言用户手册

## 1. 简介

A 是一种现代、高效、安全的编程语言，旨在提供简洁易用的语法和强大的功能。本手册将帮助您了解 A 语言的基本语法和使用方法。

## 2. 快速入门

### 2.1 安装

A 语言编译器是用 Python 编写的，因此您需要先安装 Python 3.6 或更高版本。

1. 克隆 A 语言仓库
2. 确保您的系统已安装 Python 3.6+
3. 运行编译器脚本

### 2.2 第一个程序

创建一个名为 `hello.nova` 的文件，内容如下：

```nova
// 打印 Hello, A!
print("Hello, A!");

// 定义一个函数
function add(int a, int b) {
    return a + b;
}

// 调用函数
var result = add(5, 3);
print("5 + 3 =", result);

// 条件语句
if (result > 5) {
    print("Result is greater than 5");
} else {
    print("Result is less than or equal to 5");
}

// 循环语句
for (int i = 0; i < 5; i++) {
    print("i =", i);
}
```

### 2.3 编译和运行

使用 A 编译器将源代码编译为 Python 代码，然后运行生成的 Python 代码：

```bash
# 编译 A 代码
python src/compiler.py hello.nova

# 运行生成的 Python 代码
python output.py
```

## 3. 基本语法

### 3.1 变量声明

A 支持两种变量声明方式：

```nova
// 使用 var 关键字（类型推断）
var x = 10;
var y = 3.14;
var z = true;
var s = "Hello";

// 显式类型声明
int a = 20;
float b = 2.718;
bool c = false;
string d = "World";
char e = 'A';
```

### 3.2 数据类型

A 支持以下数据类型：

- **基本类型**：
  - `int`：整数
  - `float`：浮点数
  - `bool`：布尔值（`true` 或 `false`）
  - `char`：字符
  - `string`：字符串

- **复合类型**：
  - `array`：数组
  - `struct`：结构体
  - `enum`：枚举

- **引用类型**：
  - `class`：类
  - `interface`：接口
  - `function`：函数

### 3.3 操作符

#### 3.3.1 算术操作符

| 操作符 | 描述 | 示例 |
|-------|------|------|
| `+` | 加法 | `a + b` |
| `-` | 减法 | `a - b` |
| `*` | 乘法 | `a * b` |
| `/` | 除法 | `a / b` |
| `%` | 取模 | `a % b` |

#### 3.3.2 比较操作符

| 操作符 | 描述 | 示例 |
|-------|------|------|
| `==` | 等于 | `a == b` |
| `!=` | 不等于 | `a != b` |
| `<` | 小于 | `a < b` |
| `<=` | 小于等于 | `a <= b` |
| `>` | 大于 | `a > b` |
| `>=` | 大于等于 | `a >= b` |

#### 3.3.3 逻辑操作符

| 操作符 | 描述 | 示例 |
|-------|------|------|
| `&&` | 逻辑与 | `a && b` |
| `||` | 逻辑或 | `a || b` |
| `!` | 逻辑非 | `!a` |

#### 3.3.4 赋值操作符

| 操作符 | 描述 | 示例 |
|-------|------|------|
| `=` | 赋值 | `a = b` |
| `+=` | 加法赋值 | `a += b` |
| `-=` | 减法赋值 | `a -= b` |
| `*=` | 乘法赋值 | `a *= b` |
| `/=` | 除法赋值 | `a /= b` |
| `%=` | 取模赋值 | `a %= b` |

### 3.4 控制流

#### 3.4.1 条件语句

```nova
if (condition) {
    // 代码块
} else if (anotherCondition) {
    // 代码块
} else {
    // 代码块
}
```

#### 3.4.2 循环语句

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

#### 3.4.3 跳转语句

```nova
// break 语句（跳出循环）
for (int i = 0; i < 10; i++) {
    if (i == 5) {
        break;
    }
    print(i);
}

// continue 语句（跳过当前循环迭代）
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) {
        continue;
    }
    print(i);
}

// return 语句（从函数返回）
function add(int a, int b) {
    return a + b;
}
```

### 3.5 函数

```nova
// 函数定义
function add(int a, int b) {
    return a + b;
}

// 函数调用
int result = add(5, 3);
print(result);

// 无返回值函数
function greet(string name) {
    print("Hello, ", name);
}

// 调用无返回值函数
greet("A");
```

### 3.6 结构体和类

#### 3.6.1 结构体

```nova
// 结构体定义
struct Point {
    int x;
    int y;
}

// 结构体实例化
Point p = Point(10, 20);

// 访问结构体成员
print("x =", p.x);
print("y =", p.y);
```

#### 3.6.2 类

```nova
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
        print("Hello, my name is ", name);
    }
}

// 类实例化
Person person = Person("Alice", 30);

// 调用方法
person.sayHello();
```

### 3.7 数组

```nova
// 数组声明
int[] numbers = [1, 2, 3, 4, 5];
string[] names = ["Alice", "Bob", "Charlie"];

// 数组访问
int first = numbers[0];
string last = names[names.length - 1];

// 数组长度
int length = numbers.length;

// 遍历数组
for (int i = 0; i < numbers.length; i++) {
    print(numbers[i]);
}

// foreach 遍历
foreach (var number in numbers) {
    print(number);
}
```

### 3.8 枚举

```nova
// 枚举定义
enum Color {
    RED,
    GREEN,
    BLUE
}

// 枚举使用
Color c = Color.RED;

// 枚举比较
if (c == Color.RED) {
    print("Color is red");
}
```

## 4. 标准库

### 4.1 基础库

#### 4.1.1 字符串处理

```nova
// 字符串长度
int length = len("Hello");

// 字符串连接
string combined = "Hello" + " " + "World";

// 字符串分割
string[] parts = split("a,b,c", ",");

// 字符串查找
int index = find("Hello World", "World");

// 字符串替换
string replaced = replace("Hello World", "World", "A");

// 转换为小写
string lower = lower("HELLO");

// 转换为大写
string upper = upper("hello");

// 去除首尾空白
string trimmed = trim("  Hello  ");
```

#### 4.1.2 数学运算

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

// 向下取整
int floor = Math.floor(3.7);

// 向上取整
int ceil = Math.ceil(3.2);

// 四舍五入
int round = Math.round(3.5);
```

#### 4.1.3 输入输出

```nova
// 输出
print("Hello, A!");
print("The answer is", 42);

// 输入
string name = input("Enter your name: ");
print("Hello, ", name);
```

#### 4.1.4 时间函数

```nova
// 获取当前时间
float now = Time.now();

// 睡眠
Time.sleep(1.0); // 睡眠 1 秒

// 格式化时间
string time = Time.strftime("%Y-%m-%d %H:%M:%S");
```

#### 4.1.5 操作系统函数

```nova
// 获取当前工作目录
string cwd = OS.getcwd();

// 更改工作目录
OS.chdir("/path/to/directory");

// 列出目录内容
string[] files = OS.listdir(".");

// 创建目录
OS.mkdir("new_directory");

// 删除文件
OS.remove("file.txt");

// 重命名文件
OS.rename("old.txt", "new.txt");
```

### 4.2 网络库

#### 4.2.1 HTTP 客户端

```nova
// 发送 GET 请求
HttpResponse response = Http.get("https://api.example.com/data");
string body = response.body;
int statusCode = response.statusCode;

// 发送 POST 请求
HttpResponse postResponse = Http.post("https://api.example.com/data", "{\"name\": \"A\"}");
```

#### 4.2.2 TCP 通信

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
client.connect();
client.send("A");
string response = client.receive();
client.close();
print(response);
```

### 4.3 并发库

#### 4.3.1 线程

```nova
// 创建线程
Thread thread = Thread(() => {
    for (int i = 0; i < 10; i++) {
        print("Thread: ", i);
        Thread.sleep(100);
    }
});

// 启动线程
thread.start();

// 等待线程完成
thread.join();
```

#### 4.3.2 锁

```nova
// 创建锁
Lock lock = Lock();
int counter = 0;

// 使用锁
void increment() {
    with (lock) {
        counter++;
    }
}
```

#### 4.3.3 通道

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
    print("Received: ", value);
}
```

### 4.4 集合库

#### 4.4.1 列表

```nova
// 创建列表
List<int> numbers = [1, 2, 3];

// 添加元素
numbers.add(4);

// 移除元素
numbers.remove(2);

// 检查元素是否存在
bool contains = numbers.contains(3);

// 获取列表长度
int length = numbers.length;
```

#### 4.4.2 映射

```nova
// 创建映射
Map<string, int> scores = {
    "Alice": 95,
    "Bob": 85,
    "Charlie": 90
};

// 添加元素
scores["David"] = 88;

// 获取元素
int aliceScore = scores["Alice"];

// 检查键是否存在
bool hasAlice = scores.containsKey("Alice");
```

#### 4.4.3 集合

```nova
// 创建集合
Set<string> names = {"Alice", "Bob", "Charlie"};

// 添加元素
names.add("David");

// 移除元素
names.remove("Bob");

// 检查元素是否存在
bool hasAlice = names.contains("Alice");
```

## 5. 高级特性

### 5.1 异常处理

```nova
try {
    // 可能抛出异常的代码
    int result = 10 / 0;
} catch (e) {
    // 异常处理代码
    print("Error: ", e);
}
```

### 5.2 异步编程

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

### 5.3 泛型

```nova
// 泛型函数
function<T> max(T a, T b) {
    return a > b ? a : b;
}

// 调用泛型函数
int maxInt = max(10, 20);
float maxFloat = max(3.14, 2.718);

// 泛型类
class Box<T> {
    T value;
    
    Box(T v) {
        value = v;
    }
    
    T get() {
        return value;
    }
}

// 使用泛型类
Box<int> intBox = Box<int>(42);
int value = intBox.get();
```

### 5.4 模块系统

```nova
// 导入模块
import "math";
import "network";

// 使用模块中的函数
float pi = math.PI;
HttpResponse response = network.Http.get("https://api.example.com");

// 导出模块
export function add(int a, int b) {
    return a + b;
}
```

## 6. 最佳实践

### 6.1 代码风格

- 使用 4 个空格进行缩进
- 变量和函数名使用 snake_case
- 类名使用 PascalCase
- 常量使用全大写
- 每行不超过 80 个字符
- 为函数和复杂代码添加注释

### 6.2 性能优化

- 使用适当的数据结构
- 避免不必要的计算
- 使用并发处理耗时操作
- 优化循环和递归
- 合理使用缓存

### 6.3 安全性

- 验证用户输入
- 避免使用不安全的操作
- 正确处理异常
- 保护敏感数据
- 遵循最小权限原则

## 7. 常见问题

### 7.1 语法错误

**问题**：`Syntax error: Expected primary expression`
**解决方案**：检查代码的语法结构，确保符合 A 语言的语法规则。

### 7.2 语义错误

**问题**：`Variable x not declared`
**解决方案**：在使用变量前先声明它。

**问题**：`Variable x already declared`
**解决方案**：移除重复的变量声明。

### 7.3 运行时错误

**问题**：`Division by zero`
**解决方案**：在进行除法操作前检查除数是否为零。

**问题**：`Index out of bounds`
**解决方案**：在访问数组元素前检查索引是否在有效范围内。

## 8. 示例程序

### 8.1 计算器

```nova
// 简单计算器
function add(int a, int b) {
    return a + b;
}

function subtract(int a, int b) {
    return a - b;
}

function multiply(int a, int b) {
    return a * b;
}

function divide(int a, int b) {
    if (b == 0) {
        print("Error: Division by zero");
        return 0;
    }
    return a / b;
}

// 测试计算器
print("5 + 3 =", add(5, 3));
print("5 - 3 =", subtract(5, 3));
print("5 * 3 =", multiply(5, 3));
print("5 / 3 =", divide(5, 3));
print("5 / 0 =", divide(5, 0));
```

### 8.2 斐波那契数列

```nova
// 斐波那契数列
function fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// 测试斐波那契数列
for (int i = 0; i < 10; i++) {
    print("fibonacci(", i, ") =", fibonacci(i));
}
```

### 8.3 简单服务器

```nova
// 简单 TCP 服务器
TcpServer server = TcpServer(8080);
print("Server started on port 8080");

server.listen((client) => {
    string message = client.read();
    print("Received: ", message);
    client.write("Echo: " + message);
    client.close();
});
```

## 9. 总结

A 是一种现代、高效、安全的编程语言，提供了简洁易用的语法和强大的功能。本手册介绍了 A 语言的基本语法、数据类型、控制流、函数、结构体、类、数组、枚举等特性，以及标准库的使用方法。

通过学习本手册，您应该能够编写基本的 A 程序，并使用其标准库进行各种操作。如果您有任何问题或建议，请参考 A 语言的官方文档或社区资源。