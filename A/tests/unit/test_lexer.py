import sys
import os
# 添加项目根目录到路径
sys.path.insert(0, 't:\\A')
from src.lexer.lexer import Lexer, TokenType

def test_lexer_basic():
    """测试词法分析器的基本功能"""
    source = "var x = 10;"
    lexer = Lexer(source)
    
    # 测试变量声明
    token = lexer.get_next_token()
    assert token.type == TokenType.VAR
    assert token.value == "var"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "x"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.ASSIGN
    assert token.value == "="
    
    token = lexer.get_next_token()
    assert token.type == TokenType.INTEGER_LITERAL
    assert token.value == 10
    
    token = lexer.get_next_token()
    assert token.type == TokenType.SEMICOLON
    assert token.value == ";"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.EOF
    print("[PASS] Basic lexer test passed")

def test_lexer_operators():
    """测试词法分析器的操作符识别"""
    source = "a + b - c * d / e % f"
    lexer = Lexer(source)
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "a"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.PLUS
    assert token.value == "+"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "b"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.MINUS
    assert token.value == "-"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "c"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.MULTIPLY
    assert token.value == "*"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "d"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.DIVIDE
    assert token.value == "/"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "e"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.MODULO
    assert token.value == "%"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "f"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.EOF
    print("[PASS] Operators lexer test passed")

def test_lexer_comparison():
    """测试词法分析器的比较操作符识别"""
    source = "a == b != c < d <= e > f >= g"
    lexer = Lexer(source)
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "a"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.EQUAL
    assert token.value == "=="
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "b"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.NOT_EQUAL
    assert token.value == "!="
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "c"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.LESS
    assert token.value == "<"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "d"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.LESS_EQUAL
    assert token.value == "<="
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "e"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.GREATER
    assert token.value == ">"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "f"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.GREATER_EQUAL
    assert token.value == ">="
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "g"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.EOF
    print("[PASS] Comparison operators lexer test passed")

def test_lexer_logical():
    """测试词法分析器的逻辑操作符识别"""
    source = "a && b || c !d"
    lexer = Lexer(source)
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "a"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.AND
    assert token.value == "&&"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "b"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.OR
    assert token.value == "||"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "c"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.NOT
    assert token.value == "!"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IDENTIFIER
    assert token.value == "d"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.EOF
    print("[PASS] Logical operators lexer test passed")

def test_lexer_literals():
    """测试词法分析器的字面量识别"""
    source = '10 3.14 true "hello" \'A\''
    lexer = Lexer(source)
    
    token = lexer.get_next_token()
    assert token.type == TokenType.INTEGER_LITERAL
    assert token.value == 10
    
    token = lexer.get_next_token()
    assert token.type == TokenType.FLOAT_LITERAL
    assert token.value == 3.14
    
    token = lexer.get_next_token()
    assert token.type == TokenType.BOOLEAN_LITERAL
    assert token.value == "true"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.STRING_LITERAL
    assert token.value == "hello"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.CHAR_LITERAL
    assert token.value == "A"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.EOF
    print("[PASS] Literals lexer test passed")

def test_lexer_keywords():
    """测试词法分析器的关键字识别"""
    source = "function if else for while do foreach break continue return"
    lexer = Lexer(source)
    
    token = lexer.get_next_token()
    assert token.type == TokenType.FUNCTION
    assert token.value == "function"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.IF
    assert token.value == "if"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.ELSE
    assert token.value == "else"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.FOR
    assert token.value == "for"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.WHILE
    assert token.value == "while"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.DO
    assert token.value == "do"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.FOREACH
    assert token.value == "foreach"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.BREAK
    assert token.value == "break"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.CONTINUE
    assert token.value == "continue"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.RETURN
    assert token.value == "return"
    
    token = lexer.get_next_token()
    assert token.type == TokenType.EOF
    print("[PASS] Keywords lexer test passed")

if __name__ == "__main__":
    test_lexer_basic()
    test_lexer_operators()
    test_lexer_comparison()
    test_lexer_logical()
    test_lexer_literals()
    test_lexer_keywords()
    print("All lexer tests passed!")