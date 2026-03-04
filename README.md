# Computação Móvel - TP1: Calculadora Flet

Este repositório contém a implementação de uma calculadora desenvolvida em Python utilizando a biblioteca **Flet**. O projeto evolui de uma calculadora básica para uma versão científica com suporte a expressões complexas e histórico.

---

## Requisitos e Instalação

Antes de correr o programa, certifique-se de que cumpre os seguintes requisitos:

1. **Python:** Versão 3.10 ou superior.
2. **Ambiente Virtual (Recomendado):**
    Para manter as dependências organizadas, crie e ative um ambiente virtual:

    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    ```

3. **Instalação do Flet:**
    Instale a biblioteca Flet (com todas as dependências) via terminal:

    ```bash
    pip install "flet[all]"
    ```

    *Para verificar a instalação:*

    ```bash
    flet --version
    ```

    *Caso precise de atualizar uma versão antiga:*

    ```bash
    pip install "flet[all]" --upgrade
    ```

> **Documentação Oficial:** Se tiver dúvidas durante a instalação, consulte [Installation - Flet](https://docs.flet.dev/getting-started/installation/).

---

## Objetivos do Projeto

### Objetivo 1: Estrutura Base

Implementação da interface gráfica e lógica básica seguindo o tutorial oficial do Flet:
[Flet Calculator Tutorial](https://docs.flet.dev/tutorials/calculator/)

### Objetivo 2: Cálculo de Expressões Numéricas (SymPy)

Nesta fase, o cálculo simples foi melhorado pela biblioteca **SymPy**, permitindo a resolução de expressões matemáticas completas.

**Principais Funcionalidades:**

* **PEMDAS:** O cálculo respeita a ordem correta das operações (Parêntesis > Expoentes > Multiplicação/Divisão > Adição/Subtração).
* **Precisão:** Tratamento correto de números inteiros e decimais (arredondamentos).
* **Input de Texto:** Possibilidade de escrever a equação completa.

**Instalação da dependência:**

Para que este objetivo funcione, é necessário instalar o SymPy:

```bash
pip install sympy
```

> **Documentação Oficial:** Se tiver dúvidas durante a instalação, consulte [SymPy 1.14.0 documentation](https://docs.sympy.org/latest/index.html)

### Objetivo 3: Funcionalidades Extra

De forma a introduzir mais complexidade à calculadora, este requisito visa introduzir as seguintes funcionalidades:

**Potências e Raízes:**

* $\sqrt{x}$ : Raiz Quadrada (<kbd>√</kbd>)
* $x^y$ : Potência (<kbd>^</kbd>)
* $\frac{1}{x}$ : Inversão (<kbd>1/x</kbd>)
* $e^x$ : Exponencial (<kbd>exp</kbd>)

**Trigonometria:**

* $\sin(x)$ : Seno (<kbd>sin</kbd>)
* $\cos(x)$ : Cosseno (<kbd>cos</kbd>)
* $\tan(x)$ : Tangente (<kbd>tan</kbd>)
* $\arcsin(x)$ : Arco-seno (<kbd>asin</kbd>)
* $\arccos(x)$ : Arco-cosseno (<kbd>acos</kbd>)
* $\arctan(x)$ : Arco-tangente (<kbd>atan</kbd>)

**Outros:**

* $\log(x)$ : Logaritmo (<kbd>log</kbd>)
* $n!$ : Fatorial (<kbd>!</kbd>)
* $x \pmod y$ : Módulo / Resto da divisão (<kbd>%</kbd>)
* $r$ : Número aleatório (<kbd>rand</kbd>)

### Execução do programa

```bash
flet run calc.py
```
