from dataclasses import field

import flet as ft
import sympy as sp


@ft.control
class CalcButton(ft.Button):
    expand: int = field(default_factory=lambda: 1)


@ft.control
class DigitButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.WHITE_24
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.ORANGE
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ExtraActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
    color: ft.Colors = ft.Colors.BLACK


@ft.control
class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()
        self.width = 400
        self.height = 400
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)
        self.input = ft.TextField(
            value="",
            color=ft.Colors.WHITE,
            text_align=ft.TextAlign.RIGHT, 
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9\+\-\*\/\.\(\)\s]*$"),
            hint_text="Insira a expressão...",
            border=ft.InputBorder.NONE,
            on_submit=self.submit_input
            )
        
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[self.input],
                ),
                ft.Row(
                    controls=[self.result],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(content="AC", on_click=self.button_clicked),
                        ActionButton(content="(", on_click=self.button_clicked),
                        ActionButton(content=")", on_click=self.button_clicked),
                        ActionButton(content="/", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="7", on_click=self.button_clicked),
                        DigitButton(content="8", on_click=self.button_clicked),
                        DigitButton(content="9", on_click=self.button_clicked),
                        ActionButton(content="*", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="4", on_click=self.button_clicked),
                        DigitButton(content="5", on_click=self.button_clicked),
                        DigitButton(content="6", on_click=self.button_clicked),
                        ActionButton(content="-", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="1", on_click=self.button_clicked),
                        DigitButton(content="2", on_click=self.button_clicked),
                        DigitButton(content="3", on_click=self.button_clicked),
                        ActionButton(content="+", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            content="0", expand=2, on_click=self.button_clicked
                        ),
                        DigitButton(content=".", on_click=self.button_clicked),
                        ActionButton(content="=", on_click=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.content
        print(f"Button clicked with data = {data}")
        
        if data == "AC":
            self.input.value = ""
            self.result.value = "0"
        
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "+", "-", "*", "/", "(", ")"):
            self.input.value += data
            
        elif data == "=":
            self.calculate_expression()
            
        self.update()
    
    def submit_input(self, e):
        self.calculate_expression()
        self.update()
    
    def calculate_expression(self, e=None):
        try:
            eprx = self.input.value
            if eprx:
                expr = sp.sympify(eprx)
                result = float(expr.evalf())
                
                if result.is_integer():
                    parsed_result = f"{int(result):_}".replace("_", " ")
                    self.result.value = parsed_result
                else:
                    rounded_result = round(result, 8)
                    rounded_parsed_result = f"{rounded_result:_}".replace("_", " ")
                    self.result.value = rounded_parsed_result
            
            self.update()
        
        except Exception as e:
            print("Error: " + str(e))
            self.result.value = "Error"
            self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)

        elif operator == "-":
            return self.format_number(operand1 - operand2)

        elif operator == "*":
            return self.format_number(operand1 * operand2)

        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Calc App"
    # create application instance
    calc = CalculatorApp()
    page.window.width = calc.width + 40
    page.window.height = calc.height + 40
    page.window.resizable = False
    # page.window.center() - RuntimeWarning: Enable tracemalloc to get the object allocation traceback - verificar!

    # add application's root control to the page
    page.add(calc)


ft.run(main)