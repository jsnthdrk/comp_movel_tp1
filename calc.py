from dataclasses import field
import flet as ft
import sympy as sp
import random
import re # verificar se é pertinente usar esta lib


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
        self.is_scientific = False # controlo para ver se a calculadora está em modo científico ou não
        
        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20
        
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20, weight=ft.FontWeight.BOLD)   
        self.input = ft.TextField(
            value="",
            color=ft.Colors.WHITE,
            text_align=ft.TextAlign.RIGHT, 
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9\+\-\*\/\.\(\)\s]*$"),
            hint_text="Insira a expressão...",
            border=ft.InputBorder.NONE,
            on_submit=self.submit_input
            )
        
        self.mode_button = ft.IconButton(
            icon=ft.Icons.SCIENCE,
            icon_color=ft.Colors.BLUE_200,
            tooltip="Calculadora Científica",
            on_click=self.toggle_mode
        ),
        
        self.row_scientific = ft.Row(visible=False, controls=[
            ExtraActionButton(content="sin(\u0078)", on_click=self.button_clicked),
            ExtraActionButton(content="cos(\u0078)", on_click=self.button_clicked),
            ExtraActionButton(content="tan(\u0078)", on_click=self.button_clicked),
            ExtraActionButton(content="arcsin(\u0078)", on_click=self.button_clicked),
            ExtraActionButton(content="arccos(\u0078)", on_click=self.button_clicked),
            ExtraActionButton(content="arctan(\u0078)", on_click=self.button_clicked),     
        ]
        ),
        
        self.row_scientific_2 = ft.Row(visible=False, controls=[
            ExtraActionButton(content="log(\u0078)", on_click=self.button_clicked),
            ExtraActionButton(content="n!", on_click=self.button_clicked),
            ExtraActionButton(content="%", on_click=self.button_clicked),
            ExtraActionButton(content="rand", on_click=self.button_clicked),
        ]
        ),
        
        self.row_scientific_3 = ft.Row(visible=False, controls=[
            ExtraActionButton(content="\221a(x)", on_click=self.button_clicked), # testar com \u0078 no x
            ExtraActionButton(content="x\u00b2", on_click=self.button_clicked),
            ExtraActionButton(content="\u215fx", on_click=self.button_clicked),
            ExtraActionButton(content="e\u00bx", on_click=self.button_clicked),
        ]
        ),
        
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
            self,result.value = "Error"
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
    
    def toggle_mode(self):
        pass

def main(page: ft.Page):
    page.title = "Calc App"
    # create application instance
    calc = CalculatorApp()

    # add application's root control to the page
    page.add(calc)


ft.run(main)