import re

# 词法单元类型定义
class TokenType:
    # 关键字
    VAR = 'VAR'
    INT = 'INT'
    FLOAT = 'FLOAT'
    BOOL = 'BOOL'
    CHAR = 'CHAR'
    STRING = 'STRING'
    ARRAY = 'ARRAY'
    STRUCT = 'STRUCT'
    CLASS = 'CLASS'
    INTERFACE = 'INTERFACE'
    ENUM = 'ENUM'
    FUNCTION = 'FUNCTION'
    RETURN = 'RETURN'
    IF = 'IF'
    ELSE = 'ELSE'
    FOR = 'FOR'
    WHILE = 'WHILE'
    DO = 'DO'
    FOREACH = 'FOREACH'
    BREAK = 'BREAK'
    CONTINUE = 'CONTINUE'
    TRY = 'TRY'
    CATCH = 'CATCH'
    THROW = 'THROW'
    IMPORT = 'IMPORT'
    EXPORT = 'EXPORT'
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'
    PROTECTED = 'PROTECTED'
    STATIC = 'STATIC'
    CONST = 'CONST'
    LET = 'LET'
    ASYNC = 'ASYNC'
    AWAIT = 'AWAIT'
    GO = 'GO'
    CHANNEL = 'CHANNEL'
    
    # 操作符
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    MODULO = 'MODULO'
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    ASSIGN = 'ASSIGN'
    PLUS_ASSIGN = 'PLUS_ASSIGN'
    MINUS_ASSIGN = 'MINUS_ASSIGN'
    MULTIPLY_ASSIGN = 'MULTIPLY_ASSIGN'
    DIVIDE_ASSIGN = 'DIVIDE_ASSIGN'
    MODULO_ASSIGN = 'MODULO_ASSIGN'
    
    # 标点符号
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'
    SEMICOLON = 'SEMICOLON'
    COMMA = 'COMMA'
    DOT = 'DOT'
    COLON = 'COLON'
    QUESTION = 'QUESTION'
    
    # 字面量
    INTEGER_LITERAL = 'INTEGER_LITERAL'
    FLOAT_LITERAL = 'FLOAT_LITERAL'
    BOOLEAN_LITERAL = 'BOOLEAN_LITERAL'
    CHAR_LITERAL = 'CHAR_LITERAL'
    STRING_LITERAL = 'STRING_LITERAL'
    
    # 标识符
    IDENTIFIER = 'IDENTIFIER'
    
    # 结束符
    EOF = 'EOF'

# 关键字映射
keywords = {
    'var': TokenType.VAR,
    'int': TokenType.INT,
    'float': TokenType.FLOAT,
    'bool': TokenType.BOOL,
    'char': TokenType.CHAR,
    'string': TokenType.STRING,
    'array': TokenType.ARRAY,
    'struct': TokenType.STRUCT,
    'class': TokenType.CLASS,
    'interface': TokenType.INTERFACE,
    'enum': TokenType.ENUM,
    'function': TokenType.FUNCTION,
    'return': TokenType.RETURN,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'for': TokenType.FOR,
    'while': TokenType.WHILE,
    'do': TokenType.DO,
    'foreach': TokenType.FOREACH,
    'break': TokenType.BREAK,
    'continue': TokenType.CONTINUE,
    'try': TokenType.TRY,
    'catch': TokenType.CATCH,
    'throw': TokenType.THROW,
    'import': TokenType.IMPORT,
    'export': TokenType.EXPORT,
    'public': TokenType.PUBLIC,
    'private': TokenType.PRIVATE,
    'protected': TokenType.PROTECTED,
    'static': TokenType.STATIC,
    'const': TokenType.CONST,
    'let': TokenType.LET,
    'async': TokenType.ASYNC,
    'await': TokenType.AWAIT,
    'go': TokenType.GO,
    'channel': TokenType.CHANNEL,
    'true': TokenType.BOOLEAN_LITERAL,
    'false': TokenType.BOOLEAN_LITERAL
}

# 词法单元类
class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        return f'Token({self.type}, "{self.value}", {self.line}, {self.column})'

# 词法分析器类
class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[self.position] if self.position < len(self.source) else None
    
    def advance(self):
        """前进到下一个字符"""
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
        self.current_char = self.source[self.position] if self.position < len(self.source) else None
    
    def skip_whitespace(self):
        """跳过空白字符"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        """跳过注释"""
        # 单行注释
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            return True
        # 多行注释
        elif self.current_char == '/' and self.peek() == '*':
            self.advance()  # 跳过 /
            self.advance()  # 跳过 *
            while self.current_char is not None:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  # 跳过 *
                    self.advance()  # 跳过 /
                    return True
                self.advance()
            return True
        return False
    
    def peek(self):
        """查看下一个字符，但不前进"""
        peek_pos = self.position + 1
        return self.source[peek_pos] if peek_pos < len(self.source) else None
    
    def get_number(self):
        """获取数字字面量"""
        number = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            number += self.current_char
            self.advance()
        
        if '.' in number:
            return Token(TokenType.FLOAT_LITERAL, float(number), self.line, self.column - len(number))
        else:
            return Token(TokenType.INTEGER_LITERAL, int(number), self.line, self.column - len(number))
    
    def get_string(self):
        """获取字符串字面量"""
        string = ''
        self.advance()  # 跳过引号
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':  # 转义字符
                self.advance()
                if self.current_char == 'n':
                    string += '\n'
                elif self.current_char == 't':
                    string += '\t'
                elif self.current_char == '"':
                    string += '"'
                elif self.current_char == '\\':
                    string += '\\'
                else:
                    string += self.current_char
            else:
                string += self.current_char
            self.advance()
        self.advance()  # 跳过结束引号
        return Token(TokenType.STRING_LITERAL, string, self.line, self.column - len(string) - 2)
    
    def get_char(self):
        """获取字符字面量"""
        char = ''
        self.advance()  # 跳过单引号
        if self.current_char == '\\':  # 转义字符
            self.advance()
            if self.current_char == 'n':
                char = '\n'
            elif self.current_char == 't':
                char = '\t'
            elif self.current_char == "'":
                char = "'"
            elif self.current_char == '\\':
                char = '\\'
            else:
                char = self.current_char
        else:
            char = self.current_char
        self.advance()  # 跳过字符
        self.advance()  # 跳过结束单引号
        return Token(TokenType.CHAR_LITERAL, char, self.line, self.column - len(char) - 2)
    
    def get_identifier(self):
        """获取标识符或关键字"""
        identifier = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()
        
        if identifier in keywords:
            return Token(keywords[identifier], identifier, self.line, self.column - len(identifier))
        else:
            return Token(TokenType.IDENTIFIER, identifier, self.line, self.column - len(identifier))
    
    def get_next_token(self):
        """获取下一个词法单元"""
        while self.current_char is not None:
            # 跳过空白字符
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # 跳过注释
            if self.skip_comment():
                continue
            
            # 数字
            if self.current_char.isdigit():
                return self.get_number()
            
            # 字符串
            if self.current_char == '"':
                return self.get_string()
            
            # 字符
            if self.current_char == "'":
                return self.get_char()
            
            # 标识符或关键字
            if self.current_char.isalpha() or self.current_char == '_':
                return self.get_identifier()
            
            # 操作符和标点符号
            if self.current_char == '+':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.PLUS_ASSIGN, '+=', self.line, self.column - 2)
                return Token(TokenType.PLUS, '+', self.line, self.column - 1)
            
            if self.current_char == '-':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.MINUS_ASSIGN, '-=', self.line, self.column - 2)
                return Token(TokenType.MINUS, '-', self.line, self.column - 1)
            
            if self.current_char == '*':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.MULTIPLY_ASSIGN, '*=', self.line, self.column - 2)
                return Token(TokenType.MULTIPLY, '*', self.line, self.column - 1)
            
            if self.current_char == '/':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.DIVIDE_ASSIGN, '/=', self.line, self.column - 2)
                return Token(TokenType.DIVIDE, '/', self.line, self.column - 1)
            
            if self.current_char == '%':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.MODULO_ASSIGN, '%=', self.line, self.column - 2)
                return Token(TokenType.MODULO, '%', self.line, self.column - 1)
            
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQUAL, '==', self.line, self.column - 2)
                return Token(TokenType.ASSIGN, '=', self.line, self.column - 1)
            
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NOT_EQUAL, '!=', self.line, self.column - 2)
                return Token(TokenType.NOT, '!', self.line, self.column - 1)
            
            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LESS_EQUAL, '<=', self.line, self.column - 2)
                return Token(TokenType.LESS, '<', self.line, self.column - 1)
            
            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GREATER_EQUAL, '>=', self.line, self.column - 2)
                return Token(TokenType.GREATER, '>', self.line, self.column - 1)
            
            if self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    return Token(TokenType.AND, '&&', self.line, self.column - 2)
                return Token(TokenType.AND, '&', self.line, self.column - 1)
            
            if self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    return Token(TokenType.OR, '||', self.line, self.column - 2)
                return Token(TokenType.OR, '|', self.line, self.column - 1)
            
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.line, self.column - 1)
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.line, self.column - 1)
            
            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{', self.line, self.column - 1)
            
            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}', self.line, self.column - 1)
            
            if self.current_char == '[':
                self.advance()
                return Token(TokenType.LBRACKET, '[', self.line, self.column - 1)
            
            if self.current_char == ']':
                self.advance()
                return Token(TokenType.RBRACKET, ']', self.line, self.column - 1)
            
            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMICOLON, ';', self.line, self.column - 1)
            
            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',', self.line, self.column - 1)
            
            if self.current_char == '.':
                self.advance()
                return Token(TokenType.DOT, '.', self.line, self.column - 1)
            
            if self.current_char == ':':
                self.advance()
                return Token(TokenType.COLON, ':', self.line, self.column - 1)
            
            if self.current_char == '?':
                self.advance()
                return Token(TokenType.QUESTION, '?', self.line, self.column - 1)
            
            # 未知字符
            raise Exception(f'Unknown character: {self.current_char} at line {self.line}, column {self.column}')
        
        # 结束符
        return Token(TokenType.EOF, None, self.line, self.column)

# 测试词法分析器
def test_lexer():
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
    token = lexer.get_next_token()
    while token.type != TokenType.EOF:
        print(token)
        token = lexer.get_next_token()

if __name__ == '__main__':
    test_lexer()