# comp_movel_tp1 - calculadora

este trabalho visa criar e implementar uma calculadora em FLET, cuja versão base será usada através do seguinte link: https://docs.flet.dev/tutorials/calculator/

## requisitos para correr o programa

1. deverá, primeiro, confirmar se possui Python 3.10 ou uma versão mais recente 
2. instalar a biblioteca flet no seu terminal com o seguinte comando: 'pip install 'flet[all]'
3. ou, alternativamente, se esitver a usar uma venv (virtual environment):
'python -m venv .venv  
source .venv/bin/activate
pip install 'flet[all]'
4. se preferir, confirme a sua instalação com o comando: 'flet doctor' ou 'flet --version'
5. se por acaso possuir uma versão de Flet mais antiga, pode usar o seguinte comando para atualizar a biblioteca para a versão mais recente:
'pip install 'flet[all]' --upgrade'
6. caso alguma dúvida surja que impacte a instalação do Flet para poder utilizar a aplicação, pode consultar os seguintes links:
https://docs.flet.dev/
https://docs.flet.dev/getting-started/installation/

### objetivo 1
este objetivo visa implementar a funcionalidade de resolução de equações utilizando a biblioteca "SymPy" -> https://docs.sympy.org/latest/index.html

assim, podemos implementar a resolução de equações (como por exemplo, casos notáveis), seguindo a prioridade de cálculo PEMDAS (Parenthesis > Exponents > Multiplication & Division > Addition & Subtraction), que, implementa a ordem de operações que aprendemos e usamos hoje em dia em equações mais "básicas", ou seja, numa calculadora científica.

ou seja, prioritizamos parentesis, seguidos por expoentes, depois decidimos entre multiplicação OU divisão, e, por fim, entre adição OU subtração.

1. para tal, torna-se uma depedência do nosso projeto, e, temos que instalar:
'pip install sympy'
2. isto, depois, irá ser refletido no desenvolvimento do projeto, de forma a possibilitar a elaboração de equações, com arredondamentos precisos, e, para tal, irá ser possível ESCREVER na calculadora a equação.
