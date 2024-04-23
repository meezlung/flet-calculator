import flet as ft
from decimal import Decimal, getcontext
import math

def main(page: ft.Page):
    page.title = "Mislang's Calculator"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    text_result_box: list[str] = []
    result: ft.Text = ft.Text(value="0", size=20)
    controls: set[str] = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "/", "*", ".", "^", "%", "(", ")", "!")

    def update_text_result_box(data: str) -> None:
        nonlocal text_result_box

        text_result_box.append(data)
        result.value = ''.join(text_result_box)
        page.update()


    def on_keyboard(event: ft.KeyboardEvent) -> None:
        nonlocal text_result_box

        if event.ctrl and event.key == "Backspace":
            text_result_box = []
            result.value = "0"
            page.update()
        
        elif event.key == "Backspace":
            if text_result_box:
                text_result_box.pop()
                result.value = ''.join(text_result_box)
                page.update()
            else:
                result.value = "0"
                page.update()

        elif event.shift and event.key == "=":
            update_text_result_box(data="+")

        elif event.shift and event.key == "8":
            update_text_result_box(data="×")

        elif event.key == "-":
            update_text_result_box(data="−")

        elif event.key == "/":
            update_text_result_box(data="÷")
            
        elif event.shift and event.key == "5":
            update_text_result_box(data="%")

        elif event.shift and event.key == "6":
            update_text_result_box(data="^")

        elif event.shift and event.key == "9":
            update_text_result_box(data="(")

        elif event.shift and event.key == "0":
            update_text_result_box(data=")")

        elif event.key == "Enter":
            if text_result_box:
                result.value = str(evaluate_expression(text_result_box)) # TODO: Implement a solver function for text_result_box
            else:
                result.value = "0"
            text_result_box = []
            page.update()

        elif event.key in controls:
            update_text_result_box(event.key)

        print(text_result_box)

    
    def button_clicked(event) -> None:
        nonlocal text_result_box
        
        data: str = event.control.data
        if data == "CE":
            text_result_box = []
            result.value = "0"
            page.update()

        elif data == "=":
            if text_result_box:
                result.value = str(evaluate_expression(text_result_box)) # TODO: Implement a solver function for text_result_box
            else:
                result.value = "0"
            text_result_box = []
            
            page.update()

        else:
            update_text_result_box(data)

        print(text_result_box)

    def evaluate_expression(expression):
        getcontext().prec = 20  # Set precision to handle large numbers
        
        def precedence(op):
            if op in {'+', '-'}:
                return 1
            elif op in {'×', '÷'}:
                return 2
            elif op in {'^', 'sqrt', 'ln', 'logn', '%', '!'}:
                return 3
            return 0

        def apply_operation(operands, operators):
            while len(operators) > 0 and len(operands) > 1:
                op = operators.pop()
                if op == '!':
                    a = operands.pop()
                    operands.append(factorial(a))
                elif op == '%':
                    a = operands.pop()
                    operands.append(a / 100)
                elif op == 'ln':
                    a = operands.pop()
                    if a <= 0:
                        return None  # ln(x) where x <= 0 is undefined
                    operands.append(math.log(a))
                elif op == 'logn':
                    b = operands.pop()
                    a = operands.pop()
                    if a <= 0 or b <= 0 or a == 1:
                        return None  # logn(x, base) where x <= 0, base <= 0, or x == 1 is undefined
                    operands.append(math.log(a, b))
                elif op == 'sqrt':
                    a = operands.pop()
                    if a < 0:
                        return None  # Square root of a negative number is undefined
                    operands.append(math.sqrt(a))
                elif op == '^':
                    b = operands.pop()
                    a = operands.pop()
                    operands.append(a ** b)
                else:
                    b = operands.pop()
                    a = operands.pop()
                    if op == '+':
                        operands.append(a + b)
                    elif op == '-':
                        operands.append(a - b)
                    elif op == '×':
                        operands.append(a * b)
                    elif op == '÷':
                        if b == 0:
                            return None  # Division by zero is undefined
                        operands.append(a / b)

        def factorial(n):
            if n == 0:
                return 1
            else:
                return n * factorial(n - 1)

        # Tokenize the input expression properly
        def tokenize_expression(expression):
            tokens = []
            current_token = ''
            for char in expression:
                if char.isdigit() or char == '.':
                    current_token += char
                elif char in {'+', '-', '×', '÷', '^', '(', ')', '!', '%'}:
                    if current_token:
                        tokens.append(current_token)
                        current_token = ''
                    tokens.append(char)
                elif char.isalpha():  # Function names like ln, logn, sqrt
                    current_token += char
            if current_token:
                tokens.append(current_token)
            return tokens

        # Parse the tokens and evaluate the expression
        def parse_and_evaluate(tokens):
            operands = []
            operators = []

            for token in tokens:
                if token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit()):
                    operands.append(Decimal(token))
                elif token in {'+', '-', '×', '÷', '^', '!', '%', 'ln', 'logn', 'sqrt'}:
                    apply_operation(operands, operators)
                    operators.append(token)
                elif token == '(':
                    operators.append(token)
                elif token == ')':
                    while operators[-1] != '(':
                        apply_operation(operands, operators)
                    operators.pop()  # Discard the opening parenthesis

            apply_operation(operands, operators)

            return operands[0] if operands else None

        # Tokenize the input expression and evaluate it
        tokens = tokenize_expression(expression)
        result = parse_and_evaluate(tokens)
        return result
    
    page.on_keyboard_event = on_keyboard

    page.add(
        ft.Container(
            alignment=ft.alignment.center,
            width=500,
            bgcolor=ft.colors.BLACK12,
            border_radius=ft.border_radius.all(20),
            padding=30,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[result], alignment="end"),
                    
                    ft.Row(controls=[
                                    ft.ElevatedButton(text="x!", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="!"),
                                    ft.ElevatedButton(text="(", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="("),
                                    ft.ElevatedButton(text=")", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data=")"),
                                    ft.ElevatedButton(text="%", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="%"),
                                    ft.ElevatedButton(text="CE", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="CE")
                                    ], alignment="center"),

                    ft.Row(controls=[
                                    ft.ElevatedButton(text="ln", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="ln"),
                                    ft.ElevatedButton(text="7", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="7"),
                                    ft.ElevatedButton(text="8", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="8"),
                                    ft.ElevatedButton(text="9", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="9"),
                                    ft.ElevatedButton(text="÷", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="÷")
                                    ], alignment="center"),

                    ft.Row(controls=[
                                    ft.ElevatedButton(text="log", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="log"),
                                    ft.ElevatedButton(text="4", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="4"),
                                    ft.ElevatedButton(text="5", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="5"),
                                    ft.ElevatedButton(text="6", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="6"),
                                    ft.ElevatedButton(text="×", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="×")
                                    ], alignment="center"),

                    ft.Row(controls=[
                                    ft.ElevatedButton(text="√", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="√"),
                                    ft.ElevatedButton(text="1", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="1"),
                                    ft.ElevatedButton(text="2", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="2"),
                                    ft.ElevatedButton(text="3", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="3"),
                                    ft.ElevatedButton(text="−", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="−")
                                    ], alignment="center"),

                    ft.Row(controls=[
                                    ft.ElevatedButton(text="x^y", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="^"),
                                    ft.ElevatedButton(text="0", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="0"),
                                    ft.ElevatedButton(text=".", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="."),
                                    ft.ElevatedButton(text="=", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="="),
                                    ft.ElevatedButton(text="+", width=80, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_clicked, data="+")
                                    ], alignment="center"),
                ]
            )
        )
    )


ft.app(main)
