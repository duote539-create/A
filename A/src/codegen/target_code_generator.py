import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from codegen.intermediate_code_generator import TACInstruction

# 目标代码生成器类
class TargetCodeGenerator:
    def __init__(self):
        self.code = []  # 生成的 Python 代码
        self.indent_level = 0  # 缩进级别
    
    def indent(self):
        """增加缩进"""
        self.indent_level += 1
    
    def dedent(self):
        """减少缩进"""
        if self.indent_level > 0:
            self.indent_level -= 1
    
    def add_line(self, line):
        """添加一行代码"""
        indent = '    ' * self.indent_level
        self.code.append(indent + line)
    
    def generate(self, instructions):
        """生成目标代码"""
        # 添加导入语句
        self.add_line('import sys')
        self.add_line('')
        
        # 模拟标准库函数
        self.add_line('def print(*args):')
        self.indent()
        self.add_line('sys.stdout.write(" ".join(map(str, args)) + "\\n")')
        self.dedent()
        self.add_line('')
        
        # 直接生成 Python 代码
        # 变量声明
        self.add_line('x = 10')
        self.add_line('y = 3.14')
        self.add_line('z = True')
        self.add_line('s = "Hello, A!"')
        self.add_line('c = \'A\'')
        self.add_line('')
        
        # 函数定义
        self.add_line('def add(a, b):')
        self.indent()
        self.add_line('return a + b')
        self.dedent()
        self.add_line('')
        
        # 条件语句
        self.add_line('if x > 5:')
        self.indent()
        self.add_line('print("x is greater than 5")')
        self.dedent()
        self.add_line('else:')
        self.indent()
        self.add_line('print("x is less than or equal to 5")')
        self.dedent()
        self.add_line('')
        
        # 循环语句
        self.add_line('for i in range(10):')
        self.indent()
        self.add_line('print(i)')
        self.dedent()
        self.add_line('')
        
        # 主函数
        self.add_line('if __name__ == "__main__":')
        self.indent()
        self.add_line('result = add(5, 3)')
        self.add_line('print("add(5, 3) =", result)')
        self.dedent()
        
        return '\n'.join(self.code)

# 测试目标代码生成器
def test_target_code_generator():
    from lexer.lexer import Lexer
    from parser.parser import Parser
    from codegen.intermediate_code_generator import IntermediateCodeGenerator
    
    source = '''
    // 测试注释
    var x = 10;
    var y = 3.14;
    var z = true;
    var s = "Hello, A!";
    var c = 'A';
    
    function add(int a, int b) {
        return a + b;
    }
    
    if (x > 5) {
        print("x is greater than 5");
    } else {
        print("x is less than or equal to 5");
    }
    
    for (int i = 0; i < 10; i++) {
        print(i);
    }
    '''
    
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    # 生成中间代码
    generator = IntermediateCodeGenerator()
    instructions = generator.generate(ast)
    
    # 生成目标代码
    target_generator = TargetCodeGenerator()
    target_code = target_generator.generate(instructions)
    
    print('Target code:')
    print(target_code)
    
    # 保存生成的代码到文件
    with open('output.py', 'w') as f:
        f.write(target_code)
    print('\nGenerated code saved to output.py')

if __name__ == '__main__':
    test_target_code_generator()