import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parser.parser import ASTNode

# 三地址码指令类
class TACInstruction:
    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op  # 操作符
        self.arg1 = arg1  # 第一个操作数
        self.arg2 = arg2  # 第二个操作数
        self.result = result  # 结果
    
    def __str__(self):
        if self.op == 'label':
            return f'{self.result}:'
        elif self.op == 'goto':
            return f'goto {self.result}'
        elif self.op == 'if':
            return f'if {self.arg1} {self.arg2} goto {self.result}'
        elif self.op == 'return':
            return f'return {self.arg1}' if self.arg1 else 'return'
        elif self.op == 'param':
            return f'param {self.arg1}'
        elif self.op == 'call':
            return f'{self.result} = call {self.arg1}, {self.arg2}'
        elif self.op == '=':
            return f'{self.result} = {self.arg1}'
        elif self.op == 'move':
            return f'{self.result} = {self.arg1}'
        else:
            if self.arg2 is not None:
                return f'{self.result} = {self.arg1} {self.op} {self.arg2}'
            else:
                return f'{self.result} = {self.op} {self.arg1}'

# 中间代码生成器类
class IntermediateCodeGenerator:
    def __init__(self):
        self.instructions = []  # 三地址码指令列表
        self.temp_count = 0  # 临时变量计数器
        self.label_count = 0  # 标签计数器
        self.symbol_table = {}  # 符号表，记录变量和它们的地址
    
    def new_temp(self):
        """生成新的临时变量"""
        temp = f't{self.temp_count}'
        self.temp_count += 1
        return temp
    
    def new_label(self):
        """生成新的标签"""
        label = f'L{self.label_count}'
        self.label_count += 1
        return label
    
    def generate(self, ast):
        """生成中间代码"""
        self.visit(ast)
        return self.instructions
    
    def visit(self, node):
        """访问节点"""
        method_name = f'visit_{node.type}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)
    
    def generic_visit(self, node):
        """通用访问方法"""
        for child in node.children:
            self.visit(child)
    
    def visit_Program(self, node):
        """访问程序节点"""
        for child in node.children:
            self.visit(child)
    
    def visit_VarDeclaration(self, node):
        """访问变量声明节点"""
        if node.children[0].type == 'Type':
            # 带类型的变量声明: int i = 0
            var_type = node.children[0].value
            var_name = node.children[1].value
            if len(node.children) > 2 and node.children[2].type == 'Assign':
                # 有初始化值
                expr_result = self.visit(node.children[3])
                # 生成赋值指令
                self.instructions.append(TACInstruction('=', expr_result, None, var_name))
        else:
            # 不带类型的变量声明: var x = 10
            var_name = node.children[0].value
            if len(node.children) > 2 and node.children[1].type == 'Assign':
                # 有初始化值
                expr_result = self.visit(node.children[2])
                # 生成赋值指令
                self.instructions.append(TACInstruction('=', expr_result, None, var_name))
    
    def visit_FunctionDeclaration(self, node):
        """访问函数声明节点"""
        function_name = node.children[0].value
        
        # 生成函数标签
        self.instructions.append(TACInstruction('label', None, None, function_name))
        
        # 处理参数
        params = node.children[1]
        for i, param in enumerate(params.children):
            param_name = param.children[1].value
            # 生成参数赋值指令（假设参数通过寄存器传递）
            self.instructions.append(TACInstruction('move', f'arg{i}', None, param_name))
        
        # 处理函数体
        self.visit(node.children[2])
        
        # 生成函数结束标签
        self.instructions.append(TACInstruction('label', None, None, f'{function_name}_end'))
    
    def visit_Block(self, node):
        """访问块语句节点"""
        for child in node.children:
            self.visit(child)
    
    def visit_ReturnStatement(self, node):
        """访问 return 语句节点"""
        if len(node.children) > 0:
            # 有返回值
            expr_result = self.visit(node.children[0])
            self.instructions.append(TACInstruction('return', expr_result))
        else:
            # 无返回值
            self.instructions.append(TACInstruction('return'))
    
    def visit_ExpressionStatement(self, node):
        """访问表达式语句节点"""
        self.visit(node.children[0])
    
    def visit_FunctionCall(self, node):
        """访问函数调用节点"""
        function_name = node.children[0].value
        args = node.children[1]
        
        # 生成参数传递指令
        arg_count = len(args.children)
        for i, arg in enumerate(args.children):
            arg_result = self.visit(arg)
            self.instructions.append(TACInstruction('param', arg_result))
        
        # 生成调用指令
        result = self.new_temp()
        self.instructions.append(TACInstruction('call', function_name, arg_count, result))
        return result
    
    def visit_IfStatement(self, node):
        """访问 if 语句节点"""
        # 生成条件表达式
        condition_result = self.visit(node.children[0])
        
        # 生成标签
        else_label = self.new_label()
        end_label = self.new_label()
        
        # 生成条件跳转指令
        self.instructions.append(TACInstruction('if', condition_result, 'false', else_label))
        
        # 生成 then 分支
        self.visit(node.children[1])
        self.instructions.append(TACInstruction('goto', None, None, end_label))
        
        # 生成 else 标签
        self.instructions.append(TACInstruction('label', None, None, else_label))
        
        # 生成 else 分支（如果有）
        if len(node.children) > 2:
            self.visit(node.children[2])
        
        # 生成结束标签
        self.instructions.append(TACInstruction('label', None, None, end_label))
    
    def visit_ForStatement(self, node):
        """访问 for 语句节点"""
        # 生成标签
        loop_label = self.new_label()
        end_label = self.new_label()
        
        # 生成初始化部分
        if len(node.children) > 0:
            self.visit(node.children[0])
        
        # 生成循环开始标签
        self.instructions.append(TACInstruction('label', None, None, loop_label))
        
        # 生成条件表达式
        if len(node.children) > 1:
            condition_result = self.visit(node.children[1])
            # 生成条件跳转指令
            self.instructions.append(TACInstruction('if', condition_result, 'false', end_label))
        
        # 生成循环体
        if len(node.children) > 3:
            self.visit(node.children[3])
        
        # 生成更新部分
        if len(node.children) > 2:
            self.visit(node.children[2])
        
        # 生成跳转回循环开始的指令
        self.instructions.append(TACInstruction('goto', None, None, loop_label))
        
        # 生成循环结束标签
        self.instructions.append(TACInstruction('label', None, None, end_label))
    
    def visit_WhileStatement(self, node):
        """访问 while 语句节点"""
        # 生成标签
        loop_label = self.new_label()
        end_label = self.new_label()
        
        # 生成循环开始标签
        self.instructions.append(TACInstruction('label', None, None, loop_label))
        
        # 生成条件表达式
        condition_result = self.visit(node.children[0])
        # 生成条件跳转指令
        self.instructions.append(TACInstruction('if', condition_result, 'false', end_label))
        
        # 生成循环体
        self.visit(node.children[1])
        
        # 生成跳转回循环开始的指令
        self.instructions.append(TACInstruction('goto', None, None, loop_label))
        
        # 生成循环结束标签
        self.instructions.append(TACInstruction('label', None, None, end_label))
    
    def visit_Identifier(self, node):
        """访问标识符节点"""
        return node.value
    
    def visit_IntegerLiteral(self, node):
        """访问整数字面量节点"""
        return node.value
    
    def visit_FloatLiteral(self, node):
        """访问浮点数字面量节点"""
        return node.value
    
    def visit_BooleanLiteral(self, node):
        """访问布尔字面量节点"""
        return node.value
    
    def visit_CharLiteral(self, node):
        """访问字符字面量节点"""
        return f"'{node.value}'"
    
    def visit_StringLiteral(self, node):
        """访问字符串字面量节点"""
        return f'"{node.value}"'
    
    def visit_AdditiveExpression(self, node):
        """访问加法表达式节点"""
        op = node.value
        arg1 = self.visit(node.children[0])
        arg2 = self.visit(node.children[1])
        result = self.new_temp()
        self.instructions.append(TACInstruction(op, arg1, arg2, result))
        return result
    
    def visit_MultiplicativeExpression(self, node):
        """访问乘法表达式节点"""
        op = node.value
        arg1 = self.visit(node.children[0])
        arg2 = self.visit(node.children[1])
        result = self.new_temp()
        self.instructions.append(TACInstruction(op, arg1, arg2, result))
        return result
    
    def visit_RelationalExpression(self, node):
        """访问关系表达式节点"""
        op = node.value
        arg1 = self.visit(node.children[0])
        arg2 = self.visit(node.children[1])
        result = self.new_temp()
        self.instructions.append(TACInstruction(op, arg1, arg2, result))
        return result
    
    def visit_EqualityExpression(self, node):
        """访问相等性表达式节点"""
        op = node.value
        arg1 = self.visit(node.children[0])
        arg2 = self.visit(node.children[1])
        result = self.new_temp()
        self.instructions.append(TACInstruction(op, arg1, arg2, result))
        return result
    
    def visit_LogicalExpression(self, node):
        """访问逻辑表达式节点"""
        op = node.value
        arg1 = self.visit(node.children[0])
        arg2 = self.visit(node.children[1])
        result = self.new_temp()
        self.instructions.append(TACInstruction(op, arg1, arg2, result))
        return result
    
    def visit_UnaryExpression(self, node):
        """访问一元表达式节点"""
        op = node.value
        arg1 = self.visit(node.children[0])
        result = self.new_temp()
        if op in ['++', '--']:
            # 自增和自减操作
            self.instructions.append(TACInstruction('+', arg1, '1', result))
            self.instructions.append(TACInstruction('=', result, None, arg1))
        else:
            self.instructions.append(TACInstruction(op, arg1, None, result))
        return result

# 测试中间代码生成器
def test_intermediate_code_generator():
    from lexer.lexer import Lexer
    from parser.parser import Parser
    
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
    
    generator = IntermediateCodeGenerator()
    instructions = generator.generate(ast)
    
    print('Intermediate code:')
    for instr in instructions:
        print(instr)

if __name__ == '__main__':
    test_intermediate_code_generator()