import graphviz
from triplalex import lexer
import triplayacc
from instruction import print_prog,write_tramCode_to_file

# Test for Lexer
def tokens_to_string(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
        lexer.input(code)

        # Token ausgeben
        for token in lexer:
            print(token)
    print('\n')

def build_ast(file_path):
    source = "\n".join(open(file_path).readlines())
    return triplayacc.parser.parse(source)  # ,debug=True)

# Test for Parser
def ast_to_string(ast):
    print("AST:")
    print(ast, '\n')

def program_to_string(path):
    try:
        # Datei öffnen und Inhalt zeilenweise lesen
        with open(path, 'r') as datei:
            zeilen = datei.readlines()

        # Zeilennummern hinzufügen und Inhalt mit Zeilennummern zusammenstellen
        ausgabe = "Current Program - " + path + '\n'
        for nummer, zeile in enumerate(zeilen, start=1):
            ausgabe += f"{nummer}:\t {zeile}"

        return ausgabe

    except FileNotFoundError:
        return f"Die Datei '{path}' wurde nicht gefunden."

def generate_parse_tree_dot_file(ast, file_path, extensive):
    parse_tree = graphviz.Digraph('parse_tree', comment='Parse-Tree for' + file_path)
    ast.to_dot(parse_tree, extensive)
    #print(parse_tree.source)
    # Exportiere den parse_tree in DOT-Format und speichern Sie es in einer Datei
    parse_tree_file_path = "parse_tree.dot"
    with open(parse_tree_file_path, 'w') as dot_file:
        dot_file.write(parse_tree.source)


if __name__ == '__main__':
    # Path to .tripla-File
    file_path = "triplaprograms/code_Uebung04.tripla"
    ast = build_ast(file_path)

    # Print program to console
    print(program_to_string(file_path) + '\n')

    # Identified Tokens by Lexer to String
    #tokens_to_string(file_path)

    # AST by Parser to String
    ast_to_string(ast)

    # Generate .dot-File with Parse-Tree
    #generate_parse_tree_dot_file(ast, file_path, extensive=False)

    # Compile TRIPLA to TRAM Code
    tram_code = ast.to_code()
    write_tramCode_to_file(tram_code)
    print_prog(tram_code)