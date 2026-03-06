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
        
        self.width = 400
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
        )
        
        # linhas básicas
        self.row_basic = ft.Row(controls=[
            ExtraActionButton(content="AC", on_click=self.button_clicked),
            ExtraActionButton(content="CE", on_click=self.button_clicked),
            ExtraActionButton(content="%", on_click=self.button_clicked),
            ExtraActionButton(content="\u232b", on_click=self.button_clicked), # backspace
        ]
        )
        
        self.row_basic_2 = ft.Row(controls=[
            DigitButton(content="7", on_click=self.button_clicked),
            DigitButton(content="8", on_click=self.button_clicked),
            DigitButton(content="9", on_click=self.button_clicked),
            ActionButton(content="+", on_click=self.button_clicked),
        ]
        )
        
        self.row_basic_3 = ft.Row(controls=[
            DigitButton(content="4", on_click=self.button_clicked),
            DigitButton(content="5", on_click=self.button_clicked),
            DigitButton(content="6", on_click=self.button_clicked),
            ActionButton(content="-", on_click=self.button_clicked),
        ]
        )
        
        # \u00D7 -> unicode para "*" mas bonito
        self.row_basic_4 = ft.Row(controls=[
            DigitButton(content="1", on_click=self.button_clicked),
            DigitButton(content="2", on_click=self.button_clicked),
            DigitButton(content="3", on_click=self.button_clicked),
            ActionButton(content="\u00d7", on_click=self.button_clicked), # multiplicação
        ]
        )
        
        # \u00F7 -> unicode para "divisao" mas bonito
        self.row_basic_5 = ft.Row(controls=[
            DigitButton(content="0", on_click=self.button_clicked),
            DigitButton(content=".", on_click=self.button_clicked),
            ActionButton(content="\u00f7", on_click=self.button_clicked), # divisão
            ExtraActionButton(content="=", on_click=self.button_clicked),
        ]
        )
        
        # linhas científica
        # \u0078 -> unicode para "x" mas bonito
        self.row_scientific = ft.Row(visible=False, controls=[
            ExtraActionButton(content="sin(\u0078)", on_click=self.button_clicked),
            ExtraActionButton(content="cos(\u0078)", on_click=self.button_clicked),
            ExtraActionButton(content="tan(\u0078)", on_click=self.button_clicked),
            ExtraActionButton(content="n!", on_click=self.button_clicked),
            ExtraActionButton(content="(", on_click=self.button_clicked),
            ExtraActionButton(content=")", on_click=self.button_clicked),
        ]
        )
        
        # \u0078 -> unicode para "x" mas bonito
        self.row_scientific_2 = ft.Row(visible=False, controls=[
            ExtraActionButton(content="arccos(\u0078)", expand=1, on_click=self.button_clicked), 
            ExtraActionButton(content="arcsin(\u0078)", expand=1, on_click=self.button_clicked),
            ExtraActionButton(content="arctan(\u0078)", expand=1, on_click=self.button_clicked),     
            ExtraActionButton(content="log(\u0078)", on_click=self.button_clicked),
        ]
        )
        
        self.row_scientific_3 = ft.Row(visible=False, controls=[
            ExtraActionButton(content="rand", on_click=self.button_clicked),
            ExtraActionButton(content="\221a(x)", on_click=self.button_clicked), # sqrt(x)
            ExtraActionButton(content="x\u00b2", on_click=self.button_clicked), # x^2
            ExtraActionButton(content="\u215fx", on_click=self.button_clicked), # x^(1/2)
            ExtraActionButton(content="e\u00b2", on_click=self.button_clicked) # e^2
        ]
        )
        
        # layout
        self.content = ft.Column(
            controls=[
                ft.Row([self.mode_button], alignment=ft.MainAxisAlignment.START),
                ft.Row([self.input]),
                ft.Row([self.result], alignment=ft.MainAxisAlignment.END),
                ft.Divider(color=ft.Colors.GREY_800),
                
                # modo científico
                self.row_scientific,
                self.row_scientific_2,
                self.row_scientific_3,
                
                # modo básico
                self.row_basic,
                self.row_basic_2,
                self.row_basic_3,
                self.row_basic_4,
                self.row_basic_5
            ]
        )
        
    # refatoração do método de forma a que os novos botões que estão a utilizar unicode sejam processados corretamente (e também mapeados para o modo científico)
    def button_clicked(self, e):
        data = e.control.content
        print(f"Button clicked with data = {data}")
        
        if data == "AC":
            self.input.value = ""
            self.result.value = "0"
            
        elif data == "CE":
            self.input.value = ""
            
        elif data == "\u232b": # backspace
            if len(self.input.value) > 0:
                self.input.value = self.input.value[:-1]
                
        elif data == "=":
            self.calculate_expression()

        # mapeamento dos botões unicode para as expressões corretas para o sympy processar, e também mapeamentos dos botoes do modo cientifico
        elif data == "\u00d7": self.input.value += "*"
        elif data == "\u00f7": self.input.value += "/"
        elif data == "sin(\u0078)": self.input.value += "sin("
        elif data == "cos(\u0078)": self.input.value += "cos("
        elif data == "tan(\u0078)": self.input.value += "tan("
        elif data == "n!":          self.input.value += "factorial("
        elif data == "arccos(\u0078)": self.input.value += "acos("
        elif data == "arcsin(\u0078)": self.input.value += "asin("
        elif data == "arctan(\u0078)": self.input.value += "atan("
        elif data == "log(\u0078)": self.input.value += "log("
        elif data == "\u221a(x)": self.input.value += "sqrt(" # raiz quadrada
        elif data == "x\u00b2": self.input.value += "**2" # x^2
        elif data == "\u215fx": self.input.value += "**(1/2)" # x^(1/2) -> raiz quadrada
        elif data == "e\u00b2": self.input.value += "E**2" # e^2
        
        # nao faz parte do sympy mas é uma função matemática comum, e o sympy consegue processar o random
        elif data == "rand":        self.input.value += str(round(random.random(), 4))
        
        # se nao for mais nada vamos assumir que é alguma outra coisa que passe pelo regex do input filter (1-9,0, +- , etc)            
        else:
            self.input.value += data
        
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
    
    # método para alternar entre os modos básico e científico, tornando as linhas científicas visíveis ou invisíveis conforme o estado atual
    def toggle_mode(self):
        self.is_scientific = not self.is_scientific
        self.row_scientific.visible = self.is_scientific
        self.row_scientific_2.visible = self.is_scientific
        self.row_scientific_3.visible = self.is_scientific
        
        if self.is_scientific:
            self.mode_button.icon = ft.Icons.CALCULATE
            self.tooltip = "Calculadora Básica"
            self.page.window.height = 750
            self.width = 400
        else:
            self.mode_button.icon = ft.Icons.SCIENCE
            self.mode_button.tooltip = "Modo Científico"
            self.page.window.height = 580
            self.width = 400

        self.update()
        self.page.update()

def main(page: ft.Page):
    page.title = "Calc App"
    # create application instance
    calc = CalculatorApp()
    page.window.width = calc.width
    print(f"Page width set to: {page.window.width}")
    page.window.height = calc.height
    print(f"Page height set to: {page.window.height}")
    page.window.resizable = False
    # page.window.center() - RuntimeWarning: Enable tracemalloc to get the object allocation traceback - verificar!

    # add application's root control to the page
    page.add(calc)


ft.run(main)