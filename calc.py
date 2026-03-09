from dataclasses import field
import json
import flet as ft
import sympy as sp
import random
from datetime import datetime as dt
import duckdb
import os

class HistoryItem:
    def __init__(self, index, expression, result):
        self.index = index
        self.expression = expression
        self.result = result
        self.timestamp = dt.now().strftime("%H:%M:%S")
    
    # client storage
    def to_dict(self):
        return {
            "index": self.index,
            "expression": self.expression,
            "result": self.result,
            "timestamp": self.timestamp
        }
    
    # duckdb storage
    def to_tuple(self):
        return (self.index, self.expression, self.result, self.timestamp)
    
    # debug: assim podemos mostrar na consola o nosso objeto
    def __str__(self):
        return f"\nID: {self.index}\nExpression: {self.expression}\nResult: {self.result}\nTimestamp: {self.timestamp}\n----"

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
        
        # setup das vars para o historico
        self.history_data = [] # HistoryItem.object
        self.history_counter = 0 # HistoryItem.index
        self.last_expression = "" # HistoryItem.expression
        
        # nome ficheiro parquet
        self.db_file = "history.parquet"
        
        # duckdb init -> tabela staging
        self.conn = duckdb.connect(":memory:")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS history_staging (
                index INTEGER,
                expression VARCHAR,
                result VARCHAR,
                timestamp VARCHAR
            )                  
        """)
        
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
            icon_color=ft.Colors.WHITE,
            tooltip="Modo Científico",
            on_click=self.toggle_mode
        )
        
        self.history_button = ft.IconButton(
            icon=ft.Icons.HISTORY,
            icon_color=ft.Colors.WHITE,
            tooltip="Histórico de Cálculos",
            on_click=self.toggle_history_view
        )
        
        # linhas básicas
        self.row_basic = ft.Row(controls=[
            ExtraActionButton(content="AC", expand=True,on_click=self.button_clicked),
            ExtraActionButton(content="CE", expand=True, on_click=self.button_clicked),
            ExtraActionButton(content="%", expand=True, on_click=self.button_clicked),
            ExtraActionButton(content="\u232b", expand=True, on_click=self.button_clicked), # backspace
        ])
        
        self.row_basic_2 = ft.Row(controls=[
            DigitButton(content="7", expand=True, on_click=self.button_clicked),
            DigitButton(content="8", expand=True, on_click=self.button_clicked),
            DigitButton(content="9", expand=True, on_click=self.button_clicked),
            ActionButton(content="+", expand=True, on_click=self.button_clicked),
        ]
        )
        
        self.row_basic_3 = ft.Row(controls=[
            DigitButton(content="4", expand=True, on_click=self.button_clicked),
            DigitButton(content="5", expand=True, on_click=self.button_clicked),
            DigitButton(content="6", expand=True, on_click=self.button_clicked),
            ActionButton(content="-", expand=True, on_click=self.button_clicked),
        ]
        )
        
        # \u00D7 -> unicode para "*" mas bonito
        self.row_basic_4 = ft.Row(controls=[
            DigitButton(content="1", expand=True, on_click=self.button_clicked),
            DigitButton(content="2", expand=True, on_click=self.button_clicked),
            DigitButton(content="3", expand=True, on_click=self.button_clicked),
            ActionButton(content="\u00d7", expand=True, on_click=self.button_clicked), # multiplicação
        ]
        )
        
        # \u00F7 -> unicode para "divisao" mas bonito
        self.row_basic_5 = ft.Row(controls=[
            DigitButton(content="0", expand=True, on_click=self.button_clicked),
            DigitButton(content=".", expand=True, on_click=self.button_clicked),
            ActionButton(content="\u00f7", expand=True, on_click=self.button_clicked), # divisão
            ExtraActionButton(content="=", expand=True, on_click=self.button_clicked),
        ]
        )
        
        # linhas científica
        # \u0078 -> unicode para "x" mas bonito
        self.row_scientific = ft.Row(visible=False, controls=[
            ExtraActionButton(content="sin(\u0078)", expand=True, on_click=self.button_clicked),
            ExtraActionButton(content="cos(\u0078)", expand=True, on_click=self.button_clicked),
            ExtraActionButton(content="tan(\u0078)", expand=True, on_click=self.button_clicked),
            ExtraActionButton(content="n!", expand=True, on_click=self.button_clicked),
            ExtraActionButton(content="(", expand=True, on_click=self.button_clicked),
            ExtraActionButton(content=")", on_click=self.button_clicked),
        ]
        )
        
        # \u0078 -> unicode para "x" mas bonito
        self.row_scientific_2 = ft.Row(visible=False, controls=[
            ExtraActionButton(content="arccos(\u0078)", expand=True, on_click=self.button_clicked), 
            ExtraActionButton(content="arcsin(\u0078)", expand=True, on_click=self.button_clicked),
            ExtraActionButton(content="arctan(\u0078)", expand=True, on_click=self.button_clicked),     
            ExtraActionButton(content="log(\u0078)", expand=True, on_click=self.button_clicked),
        ]
        )
        
        self.row_scientific_3 = ft.Row(visible=False, controls=[
            ExtraActionButton(content="rand", expand=True, on_click=self.button_clicked),
            ExtraActionButton(content="\u221a(x)", expand=True, on_click=self.button_clicked), # sqrt(x)
            ExtraActionButton(content="x\u00b2", expand=True, on_click=self.button_clicked), # x^2
            ExtraActionButton(content="\u215fx", expand=True, on_click=self.button_clicked),  # x^(1/2)
            ExtraActionButton(content="e\u00b2", expand=True, on_click=self.button_clicked) # e^2
        ]
        )
        
        # layout dos botoes (agrupados)
        self.buttons_layout = ft.Column(
            controls=[
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
                
        # layout do historico
        self.history_list_view = ft.ListView(
            expand=True, 
            spacing=10, 
            padding=10, 
        )
        
        # container para o historico
        self.history_container = ft.Container(
            content=self.history_list_view,
            visible=False,
            bgcolor=ft.Colors.GREY_900,
            border_radius=10,
            padding=5,
            expand=True,
            height=220
        )
        
        # layout principal da app
        self.content = ft.Column(
            controls=[
                ft.Row([self.mode_button, self.history_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([self.input], alignment=ft.MainAxisAlignment.END), # agora fica sempre alinhado à direita (fim do container)
                ft.Row([self.result], alignment=ft.MainAxisAlignment.END),
                ft.Divider(color=ft.Colors.GREY_800),
                
                # area dinamica
                ft.Container(
                    content=ft.Stack(
                        controls=[
                            self.buttons_layout,
                            self.history_container
                        ]
                    ),
                    expand=True # ocupar todo os espaço disponivel
                )
            ]
        )
        
    # refatoração do método de forma a que os novos botões que estão a utilizar unicode sejam processados corretamente (e também mapeados para o modo científico)
    def button_clicked(self, e):
        data = e.control.content
        print(f"Button clicked with data = {data}") # debug
        
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
        elif data == "rand": self.input.value += str(round(random.random(), 4))
        
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
                if eprx == self.last_expression: # ver se a expressão já foi calculada, se sim, só da output no resultado
                    return
                
                eprx = sp.sympify(eprx)
                result = float(eprx.evalf())
                
                text_result = ""
                if result.is_integer():
                    parsed_result = f"{int(result):_}".replace("_", " ")
                    text_result = parsed_result
                    self.result.value = parsed_result
                else:
                    rounded_result = round(result, 8)
                    rounded_parsed_result = f"{rounded_result:_}".replace("_", " ")
                    text_result = rounded_parsed_result
                    self.result.value = rounded_parsed_result
                
                self.add_to_history(self.input.value, text_result)
                self.last_expression = self.input.value
                print(f"Calculated result: {self.result.value}") # debug
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
    
    # método para alternar entre os modos básico e científico, tornando as linhas científicas visíveis ou invisíveis conforme o estado atual
    def toggle_mode(self):
        self.is_scientific = not self.is_scientific
        self.row_scientific.visible = self.is_scientific
        self.row_scientific_2.visible = self.is_scientific
        self.row_scientific_3.visible = self.is_scientific
        
        if self.is_scientific == False: # normalmente faria sentido usar o default do "if" is true, mas como a variavel é predefina para false, a logica estava trocada :)
            self.mode_button.icon = ft.Icons.SCIENCE
            self.mode_button.tooltip = "Modo Básico"
            self.height = 450 # altura do container diminui para acomodar os botões básicos
            self.page.window.height = self.height # largura da janela fica proporcional ao contai
            self.width = 350 # largura do container diminui para acomodar os botões básicos
            self.page.window.width = self.width # altura da janela fica proporcional ao container
            self.history_container.height = 220 # votlar à altura inicial
        else:
            self.mode_button.icon = ft.Icons.CALCULATE
            self.mode_button.tooltip = "Modo Científico"
            self.height = 570 # altura do container aumenta para acomodar os novos botões
            self.page.window.height = self.height # largura da janela fica proporcional ao container
            self.width = 650 # largura do container aumenta para acomodar os novos botões
            self.page.window.width = self.width # altura da janela fica proporcional ao container
            self.history_container.height = 340 # altura nova para acomodar a janela

        self.update()
        self.page.update()
    
    # método para adicionar o ultimo calculo efetuado e resultado obtido no historico
    # se o numero de calculos armazenados, apaga o mais antigo
    def add_to_history(self, expression, result):
        self.history_counter += 1
        
        item = HistoryItem(self.history_counter, expression, result)
        self.history_data.insert(0, item)
        if len(self.history_data) > 10:
            deleted_item = self.history_data.pop()
            print(f"----\nLimite de itens alcançado, removido: {deleted_item}\n")
        
        print(f"----\nItem Adicionado: {item}") # debug
        self.render_history()
        
        if self.page:
            self.page.run_task(self.save_history) # persistencia
                
    # método para apagar um item do historico (expressão e resultado) do historico
    def delete_from_history(self, item_object):
        if item_object in self.history_data:
            self.history_data.remove(item_object)
            self.render_history()
            if self.page: 
                self.page.run_task(self.save_history) # persistencia
            self.update()
            print(f"----\nItem Apagado: {item_object}") # debug
    
    # método para copiar o resultado da iteração do histórico para a clipboard
    async def copy_result(self, text_result):
        await ft.Clipboard().set(text_result)
        self.page.show_dialog(ft.SnackBar(ft.Text('Texto copiado!')))
        print(f"----\nResultado Copiado: {text_result}") # debug
    
    # método para termos o "render" gráfico, isto é para definir a nossa nova janela overlay
    def render_history(self):
        self.history_list_view.controls.clear()

        
        for item in self.history_data:
            async def copy_handler(e, result=item.result):
                await self.copy_result(result)
            # render do botao copiar
            copy_button = ft.IconButton(
                icon=ft.Icons.COPY,
                icon_size=20,
                tooltip="Copiar Resultado",
                on_click=copy_handler
            )
            # render do botao apagar
            delete_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color=ft.Colors.RED,
                icon_size=20,
                tooltip="Apagar Cálculo",
                on_click=lambda e, obj=item: self.delete_from_history(obj)
            )

            header_row = ft.Row(
                controls=[
                    ft.Text(f"id:{item.index}", size=12,color=ft.Colors.GREY_500),
                    ft.Text(f"{item.timestamp}", size=12,color=ft.Colors.GREY_500),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            
            # render do "corpo" de cada item do historico
            content_col = ft.Column(
                controls=[
                    header_row,
                    ft.Text(f"{item.expression}", size=14, color=ft.Colors.WHITE_70),
                    ft.Row(
                        controls=[
                            ft.Text(f"= {item.result}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_200, expand=True),
                            copy_button,
                            delete_button
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ],
                spacing=2
            )
            # render do container do cartao (controlos)
            card = ft.Container(
                content=content_col,
                bgcolor=ft.Colors.WHITE_10,
                border_radius=8,
                padding=10,
            )
            
            self.history_list_view.controls.append(card)
    
    # método para alternar entre mostrar a nossa janela de histórico e a calculadora atual
    def toggle_history_view(self, e):
        is_showing_history = self.history_container.visible
        
        if is_showing_history: # ocultar o historico
            self.history_container.visible = False
            self.buttons_layout.visible = True
            self.history_button.icon = ft.Icons.HISTORY
        else: # mostrar o historico
            self.history_container.visible = True
            self.buttons_layout.visible = False
            self.render_history()
        
        self.update()
                    
    # método para carregar histórico nas duas soluções de armazenamento
    async def load_history(self):
        self.history_data.clear()
        self.history_counter = 0
        loaded_from_parquet = False

        # tentar por parquet se o mesmo tiver operacional
        if os.path.exists(self.db_file):
            try:
                result = duckdb.sql(f"""
                    SELECT * FROM read_parquet('{self.db_file}')
                    ORDER BY index DESC
                """).fetchall()

                for row in result:
                    item = HistoryItem(int(row[0]), str(row[1]), str(row[2]))
                    item.timestamp = str(row[3])
                    self.history_data.append(item)
                    if item.index > self.history_counter:
                        self.history_counter = item.index

                loaded_from_parquet = True
                print(f"Histórico carregado do Parquet: {len(self.history_data)} itens")
            except Exception as e:
                print(f"Erro ao ler Parquet: {e}")

        # tentar por shared preferences se o parquet nao funcionar
        if not loaded_from_parquet:
            try:
                prefs = ft.SharedPreferences()
                data_json = await prefs.get("calc_history")
                if data_json:
                    data = json.loads(data_json) # serialização por json
                    if isinstance(data, list):
                        for d in data:
                            item = HistoryItem(
                                d.get("index", 0),
                                d.get("expression", ""),
                                d.get("result", "")
                            )
                            item.timestamp = d.get("timestamp", dt.now().strftime("%H:%M:%S"))
                            self.history_data.append(item)
                            if item.index > self.history_counter:
                                self.history_counter = item.index
                        print(f"Histórico carregado do SharedPreferences: {len(self.history_data)} itens")
                        # sincronizar calculos guardados na client storage para a nossa base de dados
                        await self.save_history()
            except Exception as e:
                print(f"Erro ao ler SharedPreferences: {e}")

        if not self.history_data:
            print("Nenhum histórico anterior encontrado.")

        await self.debug_storage()
        self.render_history()
        self.update()
        
    # método de sincronização nas duas soluções de armazenamento
    async def save_history(self):
        try:
            # Save to SharedPreferences as JSON string
            prefs = ft.SharedPreferences()
            data_dicts = [item.to_dict() for item in self.history_data]
            data_json = json.dumps(data_dicts)
            await prefs.set("calc_history", data_json)

            # Save to DuckDB Parquet
            if self.history_data:
                tuples = [item.to_tuple() for item in self.history_data]
                self.conn.execute("DELETE FROM history_staging")
                self.conn.executemany("INSERT INTO history_staging VALUES (?, ?, ?, ?)", tuples)
                self.conn.execute(f"""
                    COPY history_staging TO '{self.db_file}' 
                    (FORMAT 'parquet', OVERWRITE true)
                """)
            else:  # se o meu historico tiver vazio, vamos remover o ficheiro
                if os.path.exists(self.db_file):
                    os.remove(self.db_file)

            print(f"Histórico sincronizado com sucesso no SharedPreferences e Parquet: {len(self.history_data)} itens")
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")     
                 
    async def debug_storage(self):
        print("\n=== STORAGE DEBUG ===")

        # debug parquet
        try:
            if os.path.exists(self.db_file):
                result = duckdb.sql(f"SELECT * FROM read_parquet('{self.db_file}')").fetchall()
                print(f"Parquet contents ({len(result)} rows):")
                for row in result:
                    print(row)
            else:
                print("Parquet file does not exist.")
        except Exception as e:
            print(f"Error reading Parquet: {e}")

        # debug sharedpreferences
        try:
            prefs = ft.SharedPreferences()
            data_json = await prefs.get("calc_history")
            if data_json:
                data = json.loads(data_json)
                print(f"SharedPreferences contents ({len(data)} items):")
                for item in data:
                    print(item)
            else:
                print("SharedPreferences: no data found.")
        except Exception as e:
            print(f"Error reading SharedPreferences: {e}")

        print("=== END DEBUG ===\n")

async def main(page: ft.Page):
    page.title = "Calc App"
    page.bgcolor = ft.Colors.BLACK
    page.window.resizable = False
    page.window.height = 450 # altura inicial da janela, que é a mesma do container em modo básico
    page.window.width = 350 # largura inicial da janela, que é a mesma do container em modo básico
    # create application instance
    calc = CalculatorApp()
    # add application's root control to the page
    page.add(calc)
    await calc.load_history() # load no startup

ft.run(main)