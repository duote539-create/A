import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lexer.lexer import Lexer, TokenType

# 抽象语法树节点基类
class ASTNode:
    def __init__(self, type, children=None, value=None, line=None, column=None):
        self.type = type
        self.children = children or []
        self.value = value
        self.line = line
        self.column = column
    
    def add_child(self, child):
        self.children.append(child)
    
    def __str__(self, indent=0):
        prefix = '  ' * indent
        result = f'{prefix}{self.type}'
        if self.value is not None:
            result += f': {self.value}'
        result += '\n'
        for child in self.children:
            result += child.__str__(indent + 1)
        return result

# 语法分析器类
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()
    
    def error(self, message):
        raise Exception(f'Syntax error: {message} at line {self.current_token.line}, column {self.current_token.column}')
    
    def eat(self, token_type):
        """验证当前词法单元类型并前进到下一个"""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Expected {token_type}, got {self.current_token.type}')
    
    def parse(self):
        """解析程序"""
        program = ASTNode('Program')
        while self.current_token.type != TokenType.EOF:
            declaration = self.declaration()
            if declaration:
                program.add_child(declaration)
        return program
    
    def declaration(self):
        """解析声明"""
        if self.current_token.type == TokenType.VAR:
            return self.var_declaration()
        elif self.current_token.type == TokenType.FUNCTION:
            return self.function_declaration()
        elif self.current_token.type == TokenType.CLASS:
            return self.class_declaration()
        elif self.current_token.type == TokenType.STRUCT:
            return self.struct_declaration()
        elif self.current_token.type == TokenType.ENUM:
            return self.enum_declaration()
        elif self.current_token.type == TokenType.IMPORT:
            return self.import_declaration()
        elif self.current_token.type == TokenType.EXPORT:
            return self.export_declaration()
        elif self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.CHAR, TokenType.STRING]:
            # 带类型的变量声明
            return self.typed_var_declaration()
        else:
            return self.statement()
    
    def var_declaration(self):
        """解析变量声明"""
        node = ASTNode('VarDeclaration', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.VAR)
        
        # 标识符
        if self.current_token.type == TokenType.IDENTIFIER:
            node.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
            self.eat(TokenType.IDENTIFIER)
        else:
            self.error('Expected identifier')
        
        # 赋值
        if self.current_token.type == TokenType.ASSIGN:
            node.add_child(ASTNode('Assign', value='=', line=self.current_token.line, column=self.current_token.column))
            self.eat(TokenType.ASSIGN)
            node.add_child(self.expression())
        
        self.eat(TokenType.SEMICOLON)
        return node
    
    def typed_var_declaration(self):
        """解析带类型的变量声明"""
        node = ASTNode('VarDeclaration', line=self.current_token.line, column=self.current_token.column)
        
        # 类型
        node.add_child(ASTNode('Type', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
        self.eat(self.current_token.type)
        
        # 标识符
        if self.current_token.type == TokenType.IDENTIFIER:
            node.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
            self.eat(TokenType.IDENTIFIER)
        else:
            self.error('Expected identifier')
        
        # 赋值
        if self.current_token.type == TokenType.ASSIGN:
            node.add_child(ASTNode('Assign', value='=', line=self.current_token.line, column=self.current_token.column))
            self.eat(TokenType.ASSIGN)
            node.add_child(self.expression())
        
        self.eat(TokenType.SEMICOLON)
        return node
    
    def function_declaration(self):
        """解析函数声明"""
        node = ASTNode('FunctionDeclaration', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.FUNCTION)
        
        # 函数名
        if self.current_token.type == TokenType.IDENTIFIER:
            node.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
            self.eat(TokenType.IDENTIFIER)
        else:
            self.error('Expected function name')
        
        # 参数列表
        self.eat(TokenType.LPAREN)
        params = ASTNode('ParameterList')
        if self.current_token.type != TokenType.RPAREN:
            params.add_child(self.parameter())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.add_child(self.parameter())
        node.add_child(params)
        self.eat(TokenType.RPAREN)
        
        # 函数体
        self.eat(TokenType.LBRACE)
        body = ASTNode('Block')
        while self.current_token.type != TokenType.RBRACE:
            body.add_child(self.declaration())
        node.add_child(body)
        self.eat(TokenType.RBRACE)
        
        return node
    
    def parameter(self):
        """解析函数参数"""
        node = ASTNode('Parameter')
        # 参数类型
        if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.CHAR, TokenType.STRING]:
            node.add_child(ASTNode('Type', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
            self.eat(self.current_token.type)
        else:
            self.error('Expected parameter type')
        
        # 参数名
        if self.current_token.type == TokenType.IDENTIFIER:
            node.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
            self.eat(TokenType.IDENTIFIER)
        else:
            self.error('Expected parameter name')
        
        return node
    
    def class_declaration(self):
        """解析类声明"""
        node = ASTNode('ClassDeclaration', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.CLASS)
        
        # 类名
        if self.current_token.type == TokenType.IDENTIFIER:
            node.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
            self.eat(TokenType.IDENTIFIER)
        else:
            self.error('Expected class name')
        
        # 类体
        self.eat(TokenType.LBRACE)
        body = ASTNode('ClassBody')
        while self.current_token.type != TokenType.RBRACE:
            body.add_child(self.declaration())
        node.add_child(body)
        self.eat(TokenType.RBRACE)
        
        return node
    
    def struct_declaration(self):
        """解析结构体声明"""
        node = ASTNode('StructDeclaration', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.STRUCT)
        
        # 结构体名
        if self.current_token.type == TokenType.IDENTIFIER:
            node.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
            self.eat(TokenType.IDENTIFIER)
        else:
            self.error('Expected struct name')
        
        # 结构体体
        self.eat(TokenType.LBRACE)
        body = ASTNode('StructBody')
        while self.current_token.type != TokenType.RBRACE:
            # 成员变量
            if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.BOOL, TokenType.CHAR, TokenType.STRING]:
                member = ASTNode('MemberVariable')
                member.add_child(ASTNode('Type', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
                self.eat(self.current_token.type)
                if self.current_token.type == TokenType.IDENTIFIER:
                    member.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
                    self.eat(TokenType.IDENTIFIER)
                else:
                    self.error('Expected member name')
                self.eat(TokenType.SEMICOLON)
                body.add_child(member)
            else:
                self.error('Expected member variable declaration')
        node.add_child(body)
        self.eat(TokenType.RBRACE)
        
        return node
    
    def enum_declaration(self):
        """解析枚举声明"""
        node = ASTNode('EnumDeclaration', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.ENUM)
        
        # 枚举名
        if self.current_token.type == TokenType.IDENTIFIER:
            node.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
            self.eat(TokenType.IDENTIFIER)
        else:
            self.error('Expected enum name')
        
        # 枚举值
        self.eat(TokenType.LBRACE)
        values = ASTNode('EnumValues')
        if self.current_token.type == TokenType.IDENTIFIER:
            values.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
            self.eat(TokenType.IDENTIFIER)
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                if self.current_token.type == TokenType.IDENTIFIER:
                    values.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
                    self.eat(TokenType.IDENTIFIER)
                else:
                    self.error('Expected enum value')
        node.add_child(values)
        self.eat(TokenType.RBRACE)
        
        return node
    
    def import_declaration(self):
        """解析导入声明"""
        node = ASTNode('ImportDeclaration', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.IMPORT)
        
        # 模块名
        if self.current_token.type == TokenType.STRING_LITERAL:
            node.add_child(ASTNode('StringLiteral', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
            self.eat(TokenType.STRING_LITERAL)
        else:
            self.error('Expected module path')
        
        self.eat(TokenType.SEMICOLON)
        return node
    
    def export_declaration(self):
        """解析导出声明"""
        node = ASTNode('ExportDeclaration', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.EXPORT)
        
        # 导出的声明
        declaration = self.declaration()
        node.add_child(declaration)
        
        return node
    
    def statement(self):
        """解析语句"""
        if self.current_token.type == TokenType.IF:
            return self.if_statement()
        elif self.current_token.type == TokenType.FOR:
            return self.for_statement()
        elif self.current_token.type == TokenType.WHILE:
            return self.while_statement()
        elif self.current_token.type == TokenType.DO:
            return self.do_while_statement()
        elif self.current_token.type == TokenType.FOREACH:
            return self.foreach_statement()
        elif self.current_token.type == TokenType.RETURN:
            return self.return_statement()
        elif self.current_token.type == TokenType.BREAK:
            return self.break_statement()
        elif self.current_token.type == TokenType.CONTINUE:
            return self.continue_statement()
        elif self.current_token.type == TokenType.TRY:
            return self.try_catch_statement()
        elif self.current_token.type == TokenType.LBRACE:
            return self.block_statement()
        else:
            return self.expression_statement()
    
    def if_statement(self):
        """解析if语句"""
        node = ASTNode('IfStatement', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.IF)
        
        # 条件表达式
        self.eat(TokenType.LPAREN)
        node.add_child(self.expression())
        self.eat(TokenType.RPAREN)
        
        # then分支
        node.add_child(self.statement())
        
        # else分支
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            node.add_child(self.statement())
        
        return node
    
    def for_statement(self):
        """解析for语句"""
        node = ASTNode('ForStatement', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.FOR)
        
        # 初始化、条件、更新
        self.eat(TokenType.LPAREN)
        if self.current_token.type != TokenType.SEMICOLON:
            # 处理变量声明
            if self.current_token.type == TokenType.INT:
                # 变量声明
                var_node = ASTNode('VarDeclaration')
                var_node.add_child(ASTNode('Type', value='int'))
                self.eat(TokenType.INT)
                if self.current_token.type == TokenType.IDENTIFIER:
                    var_node.add_child(ASTNode('Identifier', value=self.current_token.value))
                    self.eat(TokenType.IDENTIFIER)
                    if self.current_token.type == TokenType.ASSIGN:
                        var_node.add_child(ASTNode('Assign', value='='))
                        self.eat(TokenType.ASSIGN)
                        var_node.add_child(self.expression())
                    node.add_child(var_node)
                else:
                    self.error('Expected identifier')
            else:
                node.add_child(self.expression())
        self.eat(TokenType.SEMICOLON)
        if self.current_token.type != TokenType.SEMICOLON:
            node.add_child(self.expression())
        self.eat(TokenType.SEMICOLON)
        if self.current_token.type != TokenType.RPAREN:
            node.add_child(self.expression())
        self.eat(TokenType.RPAREN)
        
        # 循环体
        node.add_child(self.statement())
        
        return node
    
    def while_statement(self):
        """解析while语句"""
        node = ASTNode('WhileStatement', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.WHILE)
        
        # 条件表达式
        self.eat(TokenType.LPAREN)
        node.add_child(self.expression())
        self.eat(TokenType.RPAREN)
        
        # 循环体
        node.add_child(self.statement())
        
        return node
    
    def do_while_statement(self):
        """解析do-while语句"""
        node = ASTNode('DoWhileStatement', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.DO)
        
        # 循环体
        node.add_child(self.statement())
        
        # 条件表达式
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        node.add_child(self.expression())
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMICOLON)
        
        return node
    
    def foreach_statement(self):
        """解析foreach语句"""
        node = ASTNode('ForEachStatement', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.FOREACH)
        
        # 变量声明
        self.eat(TokenType.LPAREN)
        if self.current_token.type == TokenType.VAR:
            node.add_child(self.var_declaration())
        else:
            self.error('Expected var declaration')
        
        # in关键字
        if self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == 'in':
            self.eat(TokenType.IDENTIFIER)
        else:
            self.error('Expected \'in\'')
        
        # 集合表达式
        node.add_child(self.expression())
        self.eat(TokenType.RPAREN)
        
        # 循环体
        node.add_child(self.statement())
        
        return node
    
    def return_statement(self):
        """解析return语句"""
        node = ASTNode('ReturnStatement', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.RETURN)
        
        # 返回表达式
        if self.current_token.type != TokenType.SEMICOLON:
            node.add_child(self.expression())
        
        self.eat(TokenType.SEMICOLON)
        return node
    
    def break_statement(self):
        """解析break语句"""
        node = ASTNode('BreakStatement', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.BREAK)
        self.eat(TokenType.SEMICOLON)
        return node
    
    def continue_statement(self):
        """解析continue语句"""
        node = ASTNode('ContinueStatement', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.CONTINUE)
        self.eat(TokenType.SEMICOLON)
        return node
    
    def try_catch_statement(self):
        """解析try-catch语句"""
        node = ASTNode('TryCatchStatement', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.TRY)
        
        # try块
        self.eat(TokenType.LBRACE)
        try_block = ASTNode('Block')
        while self.current_token.type != TokenType.RBRACE:
            try_block.add_child(self.declaration())
        node.add_child(try_block)
        self.eat(TokenType.RBRACE)
        
        # catch块
        if self.current_token.type == TokenType.CATCH:
            self.eat(TokenType.CATCH)
            self.eat(TokenType.LPAREN)
            # 异常参数
            if self.current_token.type == TokenType.IDENTIFIER:
                node.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
                self.eat(TokenType.IDENTIFIER)
            else:
                self.error('Expected exception parameter')
            self.eat(TokenType.RPAREN)
            
            # catch块体
            self.eat(TokenType.LBRACE)
            catch_block = ASTNode('Block')
            while self.current_token.type != TokenType.RBRACE:
                catch_block.add_child(self.declaration())
            node.add_child(catch_block)
            self.eat(TokenType.RBRACE)
        
        return node
    
    def block_statement(self):
        """解析块语句"""
        node = ASTNode('Block', line=self.current_token.line, column=self.current_token.column)
        self.eat(TokenType.LBRACE)
        while self.current_token.type != TokenType.RBRACE:
            node.add_child(self.declaration())
        self.eat(TokenType.RBRACE)
        return node
    
    def expression_statement(self):
        """解析表达式语句"""
        node = ASTNode('ExpressionStatement', line=self.current_token.line, column=self.current_token.column)
        node.add_child(self.expression())
        self.eat(TokenType.SEMICOLON)
        return node
    
    def expression(self):
        """解析表达式"""
        return self.assignment_expression()
    
    def assignment_expression(self):
        """解析赋值表达式"""
        left = self.logical_or_expression()
        
        if self.current_token.type == TokenType.ASSIGN:
            node = ASTNode('AssignmentExpression', value='=', line=self.current_token.line, column=self.current_token.column)
            node.add_child(left)
            self.eat(TokenType.ASSIGN)
            node.add_child(self.assignment_expression())
            return node
        elif self.current_token.type in [TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, TokenType.MULTIPLY_ASSIGN, TokenType.DIVIDE_ASSIGN, TokenType.MODULO_ASSIGN]:
            node = ASTNode('AssignmentExpression', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            node.add_child(left)
            self.eat(self.current_token.type)
            node.add_child(self.assignment_expression())
            return node
        else:
            return left
    
    def logical_or_expression(self):
        """解析逻辑或表达式"""
        left = self.logical_and_expression()
        
        while self.current_token.type == TokenType.OR:
            node = ASTNode('LogicalExpression', value='||', line=self.current_token.line, column=self.current_token.column)
            node.add_child(left)
            self.eat(TokenType.OR)
            node.add_child(self.logical_and_expression())
            left = node
        
        return left
    
    def logical_and_expression(self):
        """解析逻辑与表达式"""
        left = self.equality_expression()
        
        while self.current_token.type == TokenType.AND:
            node = ASTNode('LogicalExpression', value='&&', line=self.current_token.line, column=self.current_token.column)
            node.add_child(left)
            self.eat(TokenType.AND)
            node.add_child(self.equality_expression())
            left = node
        
        return left
    
    def equality_expression(self):
        """解析相等性表达式"""
        left = self.relational_expression()
        
        while self.current_token.type in [TokenType.EQUAL, TokenType.NOT_EQUAL]:
            node = ASTNode('EqualityExpression', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            node.add_child(left)
            self.eat(self.current_token.type)
            node.add_child(self.relational_expression())
            left = node
        
        return left
    
    def relational_expression(self):
        """解析关系表达式"""
        left = self.additive_expression()
        
        while self.current_token.type in [TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL]:
            node = ASTNode('RelationalExpression', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            node.add_child(left)
            self.eat(self.current_token.type)
            node.add_child(self.additive_expression())
            left = node
        
        return left
    
    def additive_expression(self):
        """解析加法表达式"""
        left = self.multiplicative_expression()
        
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            node = ASTNode('AdditiveExpression', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            node.add_child(left)
            self.eat(self.current_token.type)
            node.add_child(self.multiplicative_expression())
            left = node
        
        return left
    
    def multiplicative_expression(self):
        """解析乘法表达式"""
        left = self.unary_expression()
        
        while self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            node = ASTNode('MultiplicativeExpression', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            node.add_child(left)
            self.eat(self.current_token.type)
            node.add_child(self.unary_expression())
            left = node
        
        return left
    
    def unary_expression(self):
        """解析一元表达式"""
        if self.current_token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.NOT]:
            node = ASTNode('UnaryExpression', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            self.eat(self.current_token.type)
            node.add_child(self.unary_expression())
            return node
        else:
            # 处理自增和自减操作符
            expr = self.primary_expression()
            if self.current_token.type == TokenType.PLUS and self.peek() == TokenType.PLUS:
                node = ASTNode('UnaryExpression', value='++', line=self.current_token.line, column=self.current_token.column)
                node.add_child(expr)
                self.eat(TokenType.PLUS)
                self.eat(TokenType.PLUS)
                return node
            elif self.current_token.type == TokenType.MINUS and self.peek() == TokenType.MINUS:
                node = ASTNode('UnaryExpression', value='--', line=self.current_token.line, column=self.current_token.column)
                node.add_child(expr)
                self.eat(TokenType.MINUS)
                self.eat(TokenType.MINUS)
                return node
            return expr
    
    def peek(self):
        """查看下一个词法单元，但不前进"""
        from lexer.lexer import Lexer
        # 保存当前状态
        current_pos = self.lexer.position
        current_char = self.lexer.current_char
        current_line = self.lexer.line
        current_column = self.lexer.column
        
        # 获取下一个词法单元
        next_token = self.lexer.get_next_token()
        
        # 恢复状态
        self.lexer.position = current_pos
        self.lexer.current_char = current_char
        self.lexer.line = current_line
        self.lexer.column = current_column
        
        return next_token.type if next_token else None
    
    def primary_expression(self):
        """解析基本表达式"""
        if self.current_token.type == TokenType.INTEGER_LITERAL:
            node = ASTNode('IntegerLiteral', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            self.eat(TokenType.INTEGER_LITERAL)
            return node
        elif self.current_token.type == TokenType.FLOAT_LITERAL:
            node = ASTNode('FloatLiteral', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            self.eat(TokenType.FLOAT_LITERAL)
            return node
        elif self.current_token.type == TokenType.BOOLEAN_LITERAL:
            node = ASTNode('BooleanLiteral', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            self.eat(TokenType.BOOLEAN_LITERAL)
            return node
        elif self.current_token.type == TokenType.CHAR_LITERAL:
            node = ASTNode('CharLiteral', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            self.eat(TokenType.CHAR_LITERAL)
            return node
        elif self.current_token.type == TokenType.STRING_LITERAL:
            node = ASTNode('StringLiteral', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            self.eat(TokenType.STRING_LITERAL)
            return node
        elif self.current_token.type == TokenType.IDENTIFIER:
            node = ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
            self.eat(TokenType.IDENTIFIER)
            
            # 函数调用
            if self.current_token.type == TokenType.LPAREN:
                call_node = ASTNode('FunctionCall', line=node.line, column=node.column)
                call_node.add_child(node)
                self.eat(TokenType.LPAREN)
                args = ASTNode('ArgumentList')
                if self.current_token.type != TokenType.RPAREN:
                    args.add_child(self.expression())
                    while self.current_token.type == TokenType.COMMA:
                        self.eat(TokenType.COMMA)
                        args.add_child(self.expression())
                call_node.add_child(args)
                self.eat(TokenType.RPAREN)
                return call_node
            
            # 成员访问
            elif self.current_token.type == TokenType.DOT:
                member_node = ASTNode('MemberAccess', line=node.line, column=node.column)
                member_node.add_child(node)
                self.eat(TokenType.DOT)
                if self.current_token.type == TokenType.IDENTIFIER:
                    member_node.add_child(ASTNode('Identifier', value=self.current_token.value, line=self.current_token.line, column=self.current_token.column))
                    self.eat(TokenType.IDENTIFIER)
                else:
                    self.error('Expected member name')
                return member_node
            
            # 数组访问
            elif self.current_token.type == TokenType.LBRACKET:
                array_node = ASTNode('ArrayAccess', line=node.line, column=node.column)
                array_node.add_child(node)
                self.eat(TokenType.LBRACKET)
                array_node.add_child(self.expression())
                self.eat(TokenType.RBRACKET)
                return array_node
            
            return node
        elif self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.expression()
            self.eat(TokenType.RPAREN)
            return expr
        else:
            self.error('Expected primary expression')

# 测试语法分析器
def test_parser():
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
    print(ast)

if __name__ == '__main__':
    test_parser()