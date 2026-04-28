import sys
import os
# 添加项目根目录到路径
sys.path.insert(0, 't:\\A')
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.semantic_analyzer import SemanticAnalyzer

def test_semantic_analyzer_var_declaration():
    """测试语义分析器的变量声明分析"""
    source = "var x = 10;"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    
    assert len(errors) == 0
    print("[PASS] Variable declaration semantic test passed")

def test_semantic_analyzer_function_declaration():
    """测试语义分析器的函数声明分析"""
    source = "function add(int a, int b) { return a + b; }"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    
    assert len(errors) == 0
    print("[PASS] Function declaration semantic test passed")

def test_semantic_analyzer_undefined_variable():
    """测试语义分析器对未定义变量的检测"""
    source = "var x = 10; print(y);"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    
    assert len(errors) > 0
    print(f"Error message: {errors[0]}")
    assert "not declared" in errors[0]
    print("[PASS] Undefined variable semantic test passed")

def test_semantic_analyzer_redeclaration():
    """测试语义分析器对变量重声明的检测"""
    source = "var x = 10; var x = 20;"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    
    assert len(errors) > 0
    assert "Variable x already declared" in errors[0]
    print("[PASS] Variable redeclaration semantic test passed")

def test_semantic_analyzer_function_call():
    """测试语义分析器的函数调用分析"""
    source = "function add(int a, int b) { return a + b; } int result = add(5, 3);"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    
    if errors:
        print(f"Error messages: {errors}")
    assert len(errors) == 0
    print("[PASS] Function call semantic test passed")

def test_semantic_analyzer_if_statement():
    """测试语义分析器的if语句分析"""
    source = "var x = 10; if (x > 5) { print(\"Hello\"); }"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    
    assert len(errors) == 0
    print("[PASS] If statement semantic test passed")

if __name__ == "__main__":
    test_semantic_analyzer_var_declaration()
    test_semantic_analyzer_function_declaration()
    test_semantic_analyzer_undefined_variable()
    test_semantic_analyzer_redeclaration()
    test_semantic_analyzer_function_call()
    test_semantic_analyzer_if_statement()
    print("All semantic analyzer tests passed!")