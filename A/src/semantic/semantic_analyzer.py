import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parser.parser import ASTNode

# 符号表类
class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}
    
    def put(self, name, symbol):
        """添加符号"""
        self.symbols[name] = symbol
    
    def get(self, name):
        """获取符号"""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None
    
    def has(self, name):
        """检查符号是否存在"""
        if name in self.symbols:
            return True
        elif self.parent:
            return self.parent.has(name)
        else:
            return False
    
    def enter_scope(self):
        """进入新作用域"""
        return SymbolTable(self)
    
    def exit_scope(self):
        """退出当前作用域"""
        return self.parent

# 符号类
class Symbol:
    def __init__(self, name, type, kind):
        self.name = name
        self.type = type
        self.kind = kind  # var, function, class, struct, enum

# 类型系统
class TypeSystem:
    @staticmethod
    def is_compatible(type1, type2):
        """检查类型是否兼容"""
        if type1 == type2:
            return True
        # 这里可以添加类型转换规则
        return False
    
    @staticmethod
    def get_type(node):
        """获取表达式的类型"""
        if node.type == 'IntegerLiteral':
            return 'int'
        elif node.type == 'FloatLiteral':
            return 'float'
        elif node.type == 'BooleanLiteral':
            return 'bool'
        elif node.type == 'CharLiteral':
            return 'char'
        elif node.type == 'StringLiteral':
            return 'string'
        elif node.type == 'Identifier':
            # 需要从符号表中获取类型
            return None
        elif node.type == 'FunctionCall':
            # 需要从符号表中获取函数返回类型
            return None
        elif node.type == 'AdditiveExpression':
            # 假设两个操作数类型相同
            return TypeSystem.get_type(node.children[0])
        elif node.type == 'MultiplicativeExpression':
            # 假设两个操作数类型相同
            return TypeSystem.get_type(node.children[0])
        elif node.type == 'RelationalExpression':
            return 'bool'
        elif node.type == 'EqualityExpression':
            return 'bool'
        elif node.type == 'LogicalExpression':
            return 'bool'
        elif node.type == 'UnaryExpression':
            return TypeSystem.get_type(node.children[0])
        else:
            return None

# 语义分析器类
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        # 初始化标准库函数
        self.init_stdlib()
    
    def init_stdlib(self):
        """初始化标准库函数"""
        # 添加 print 函数
        self.symbol_table.put('print', Symbol('print', 'void', 'function'))
    
    def error(self, message, line, column):
        """记录错误"""
        self.errors.append(f'Error at line {line}, column {column}: {message}')
    
    def analyze(self, ast):
        """分析抽象语法树"""
        self.visit(ast)
        return self.errors
    
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
        # 处理不同形式的变量声明
        if node.children[0].type == 'Type':
            # 带类型的变量声明: int i = 0
            var_type = node.children[0].value
            identifier = node.children[1]
            var_name = identifier.value
        else:
            # 不带类型的变量声明: var x = 10
            identifier = node.children[0]
            var_name = identifier.value
            var_type = None
            # 类型推断
            if len(node.children) > 2:
                expr_type = TypeSystem.get_type(node.children[2])
                var_type = expr_type
        
        # 检查变量是否已声明
        if self.symbol_table.has(var_name):
            self.error(f'Variable {var_name} already declared', identifier.line, identifier.column)
        
        # 添加到符号表
        if var_type:
            self.symbol_table.put(var_name, Symbol(var_name, var_type, 'var'))
        else:
            self.error(f'Cannot infer type for variable {var_name}', identifier.line, identifier.column)
    
    def visit_FunctionDeclaration(self, node):
        """访问函数声明节点"""
        function_name = node.children[0].value
        
        # 检查函数是否已声明
        if self.symbol_table.has(function_name):
            self.error(f'Function {function_name} already declared', node.children[0].line, node.children[0].column)
        
        # 进入函数作用域
        self.symbol_table = self.symbol_table.enter_scope()
        
        # 处理参数
        params = node.children[1]
        param_types = []
        for param in params.children:
            param_name = param.children[1].value
            param_type = param.children[0].value
            # 检查参数是否已声明
            if self.symbol_table.has(param_name):
                self.error(f'Parameter {param_name} already declared', param.children[1].line, param.children[1].column)
            # 添加到符号表
            self.symbol_table.put(param_name, Symbol(param_name, param_type, 'var'))
            param_types.append(param_type)
        
        # 处理函数体
        self.visit(node.children[2])
        
        # 退出函数作用域
        self.symbol_table = self.symbol_table.exit_scope()
        
        # 添加函数到符号表
        self.symbol_table.put(function_name, Symbol(function_name, 'int', 'function'))  # 暂时假设返回类型为 int
    
    def visit_Identifier(self, node):
        """访问标识符节点"""
        var_name = node.value
        # 检查变量是否已声明
        if not self.symbol_table.has(var_name):
            self.error(f'Variable {var_name} not declared', node.line, node.column)
    
    def visit_FunctionCall(self, node):
        """访问函数调用节点"""
        function_name = node.children[0].value
        # 检查函数是否已声明
        if not self.symbol_table.has(function_name):
            self.error(f'Function {function_name} not declared', node.children[0].line, node.children[0].column)
        else:
            # 检查参数数量（暂时简单检查）
            function_symbol = self.symbol_table.get(function_name)
            # 检查参数中的标识符
            if len(node.children) > 1:
                args = node.children[1]
                for arg in args.children:
                    self.visit(arg)
    
    def visit_IfStatement(self, node):
        """访问 if 语句节点"""
        # 检查条件表达式类型是否为 bool
        condition_type = TypeSystem.get_type(node.children[0])
        if condition_type != 'bool':
            self.error(f'Condition must be of type bool, got {condition_type}', node.children[0].line, node.children[0].column)
        
        # 访问 then 分支
        self.visit(node.children[1])
        
        # 访问 else 分支（如果有）
        if len(node.children) > 2:
            self.visit(node.children[2])
    
    def visit_ForStatement(self, node):
        """访问 for 语句节点"""
        # 进入循环作用域
        self.symbol_table = self.symbol_table.enter_scope()
        
        # 访问初始化部分
        if len(node.children) > 0:
            self.visit(node.children[0])
        
        # 检查条件表达式类型是否为 bool
        if len(node.children) > 1:
            # 暂时跳过类型检查，因为变量可能在初始化部分刚刚声明
            # condition_type = TypeSystem.get_type(node.children[1])
            # if condition_type != 'bool':
            #     self.error(f'Condition must be of type bool, got {condition_type}', node.children[1].line, node.children[1].column)
            pass
        
        # 访问更新部分
        if len(node.children) > 2:
            self.visit(node.children[2])
        
        # 访问循环体
        if len(node.children) > 3:
            self.visit(node.children[3])
        
        # 退出循环作用域
        self.symbol_table = self.symbol_table.exit_scope()
    
    def visit_WhileStatement(self, node):
        """访问 while 语句节点"""
        # 检查条件表达式类型是否为 bool
        condition_type = TypeSystem.get_type(node.children[0])
        if condition_type != 'bool':
            self.error(f'Condition must be of type bool, got {condition_type}', node.children[0].line, node.children[0].column)
        
        # 访问循环体
        self.visit(node.children[1])
    
    def visit_ReturnStatement(self, node):
        """访问 return 语句节点"""
        # 这里可以添加返回值类型检查
        if len(node.children) > 0:
            self.visit(node.children[0])
    
    def visit_Block(self, node):
        """访问块语句节点"""
        # 进入块作用域
        self.symbol_table = self.symbol_table.enter_scope()
        
        # 访问块内语句
        for child in node.children:
            self.visit(child)
        
        # 退出块作用域
        self.symbol_table = self.symbol_table.exit_scope()

# 测试语义分析器
def test_semantic_analyzer():
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
    
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    
    if errors:
        print('Semantic errors:')
        for error in errors:
            print(error)
    else:
        print('No semantic errors found.')

if __name__ == '__main__':
    test_semantic_analyzer()