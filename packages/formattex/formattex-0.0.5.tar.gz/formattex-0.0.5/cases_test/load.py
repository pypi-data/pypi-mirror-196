from TexSoup import TexSoup

from formattex.intermediate_repr import cleanup_expressions

def get_expressions(code):
    soup = TexSoup(code)
    return [node.expr for node in soup.all]


with open("input1.tex") as file:
    code = file.read()

expressions = get_expressions(code)

expressions = cleanup_expressions(expressions)


