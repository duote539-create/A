import sys
import os
# 添加项目根目录到路径
sys.path.insert(0, 't:\\A')
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.codegen.intermediate_code_generator import IntermediateCodeGenerator

def test_intermediate_code_generator_var_declaration():
    """测试中间代码生成器的变量声明生成"""
    source = "var x = 10;"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    generator = IntermediateCodeGenerator()
    instructions = generator.generate(ast)
    
    assert len(instructions) > 0
    assert instructions[0].op == "="
    assert instructions[0].result == "x"
    assert instructions[0].arg1 == 10
    print("[PASS] Variable declaration intermediate code test passed")

def test_intermediate_code_generator_function_declaration():
    """测试中间代码生成器的函数声明生成"""
    source = "function add(int a, int b) { return a + b; }"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    generator = IntermediateCodeGenerator()
    instructions = generator.generate(ast)
    
    assert len(instructions) > 0
    # 查找函数标签
    found = False
    for instr in instructions:
        if instr.op == "label" and instr.result == "add":
            found = True
            break
    assert found
    print("[PASS] Function declaration intermediate code test passed")

def test_intermediate_code_generator_if_statement():
    """测试中间代码生成器的if语句生成"""
    source = "if (x > 5) { print(\"Hello\"); } else { print(\"World\"); }"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    generator = IntermediateCodeGenerator()
    instructions = generator.generate(ast)
    
    assert len(instructions) > 0
    # 查找条件跳转指令
    found = False
    for instr in instructions:
        if instr.op == "if":
            found = True
            break
    assert found
    print("[PASS] If statement intermediate code test passed")

def test_intermediate_code_generator_for_statement():
    """测试中间代码生成器的for语句生成"""
    source = "for (int i = 0; i < 10; i++) { print(i); }"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    generator = IntermediateCodeGenerator()
    instructions = generator.generate(ast)
    
    assert len(instructions) > 0
    # 查找循环标签
    found = False
    for instr in instructions:
        if instr.op == "label" and instr.result.startswith("L"):
            found = True
            break
    assert found
    print("[PASS] For statement intermediate code test passed")

def test_intermediate_code_generator_expression():
    """测试中间代码生成器的表达式生成"""
    source = "var result = a + b * c;"
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()
    
    generator = IntermediateCodeGenerator()
    instructions = generator.generate(ast)
    
    assert len(instructions) > 0
    # 查找乘法指令
    found = False
    for instr in instructions:
        if instr.op == "*":
            found = True
            break
    assert found
    print("[PASS] Expression intermediate code test passed")

if __name__ == "__main__":
    test_intermediate_code_generator_var_declaration()
    test_intermediate_code_generator_function_declaration()
    test_intermediate_code_generator_if_statement()
    test_intermediate_code_generator_for_statement()
    test_intermediate_code_generator_expression()
    print("All intermediate code generator tests passed!")