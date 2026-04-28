import sys
import os
# 添加项目根目录到路径
sys.path.insert(0, 't:\\A')
from src.lexer.lexer import Lexer
from src.parser.parser import Parser

def test_parser_var_declaration():
    """测试语法分析器的变量声明解析"""
    source = "var x = 10;"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    assert len(ast.children) == 1
    assert ast.children[0].type == "VarDeclaration"
    assert ast.children[0].children[0].type == "Identifier"
    assert ast.children[0].children[0].value == "x"
    assert ast.children[0].children[1].type == "Assign"
    assert ast.children[0].children[2].type == "IntegerLiteral"
    assert ast.children[0].children[2].value == 10
    print("[PASS] Variable declaration parser test passed")

def test_parser_function_declaration():
    """测试语法分析器的函数声明解析"""
    source = "function add(int a, int b) { return a + b; }"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    assert len(ast.children) == 1
    assert ast.children[0].type == "FunctionDeclaration"
    assert ast.children[0].children[0].type == "Identifier"
    assert ast.children[0].children[0].value == "add"
    
    # 检查参数列表
    assert ast.children[0].children[1].type == "ParameterList"
    assert len(ast.children[0].children[1].children) == 2
    assert ast.children[0].children[1].children[0].type == "Parameter"
    assert ast.children[0].children[1].children[0].children[0].type == "Type"
    assert ast.children[0].children[1].children[0].children[0].value == "int"
    assert ast.children[0].children[1].children[0].children[1].type == "Identifier"
    assert ast.children[0].children[1].children[0].children[1].value == "a"
    
    # 检查函数体
    assert ast.children[0].children[2].type == "Block"
    assert len(ast.children[0].children[2].children) == 1
    assert ast.children[0].children[2].children[0].type == "ReturnStatement"
    assert ast.children[0].children[2].children[0].children[0].type == "AdditiveExpression"
    print("[PASS] Function declaration parser test passed")

def test_parser_if_statement():
    """测试语法分析器的if语句解析"""
    source = "if (x > 5) { print(\"Hello\"); } else { print(\"World\"); }"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    assert len(ast.children) == 1
    assert ast.children[0].type == "IfStatement"
    assert ast.children[0].children[0].type == "RelationalExpression"
    assert ast.children[0].children[1].type == "Block"
    assert ast.children[0].children[2].type == "Block"
    print("[PASS] If statement parser test passed")

def test_parser_for_statement():
    """测试语法分析器的for语句解析"""
    source = "for (int i = 0; i < 10; i++) { print(i); }"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    assert len(ast.children) == 1
    assert ast.children[0].type == "ForStatement"
    assert ast.children[0].children[0].type == "VarDeclaration"
    assert ast.children[0].children[1].type == "RelationalExpression"
    assert ast.children[0].children[2].type == "UnaryExpression"
    assert ast.children[0].children[3].type == "Block"
    print("[PASS] For statement parser test passed")

def test_parser_while_statement():
    """测试语法分析器的while语句解析"""
    source = "while (x < 10) { x++; }"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    assert len(ast.children) == 1
    assert ast.children[0].type == "WhileStatement"
    assert ast.children[0].children[0].type == "RelationalExpression"
    assert ast.children[0].children[1].type == "Block"
    print("[PASS] While statement parser test passed")

def test_parser_expression():
    """测试语法分析器的表达式解析"""
    source = "var result = a + b * c - d / e;"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    assert len(ast.children) == 1
    assert ast.children[0].type == "VarDeclaration"
    assert ast.children[0].children[2].type == "AdditiveExpression"
    print("[PASS] Expression parser test passed")

if __name__ == "__main__":
    test_parser_var_declaration()
    test_parser_function_declaration()
    test_parser_if_statement()
    test_parser_for_statement()
    test_parser_while_statement()
    test_parser_expression()
    print("All parser tests passed!")