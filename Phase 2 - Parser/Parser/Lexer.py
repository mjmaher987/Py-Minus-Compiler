from anytree import Node, RenderTree
from Scanner import *


class Lexer:
    def __init__(self):
        self.scanner = Scanner()
        self.pars_table = {}
        self.fill_pars_table()
        self.all_errors = []
        self.all_terminals = ["break", "continue", "return", "while", "$", "EPSILON", ";", "global", "def", "if",
                              "else", "while", "=", "(", ")", "[", "]", ",", ":", "==", "<",
                              "+", "-", "*", "**", "ID"]  # TODO
        self.tree_nodes = []
        self.start_process()

    def fill_pars_table(self):
        self.pars_table = {"Program": {"break": "Statements", "continue": "Statements", "ID": "Statements",
                                       "return": "Statements",
                                       "global": "Statements", "def": "Statements", "if": "Statements",
                                       "while": "Statements",
                                       "$": "Statements"},
                           "Statements": {";": "EPSILON", "break": "Statement ; Statements",
                                          "continue": "Statement ; Statements",
                                          "ID": "Statement ; Statements", "return": "Statement ; Statements",
                                          "global": "Statement ; Statements", "def": "Statement ; Statements",
                                          "if": "Statement ; Statements", "else": "EPSILON",
                                          "while": "Statement ; Statements",
                                          "$": "EPSILON"},
                           "Statement": {"break": "Simple_stmt", "continue": "Simple_stmt", "ID": "Simple_stmt",
                                         "return": "Simple_stmt", "global": "Simple_stmt", "def": "Compound_stmt",
                                         "if": "Compound_stmt", "while": "Compound_stmt", ";": "SYNCH"},
                           "Simple_stmt": {"break": "break", "continue": "continue", "ID": "Assignment_Call",
                                           "return": "Return_stmt",
                                           "global": "Global_stmt", ";": "SYNCH"},
                           "Compound_stmt": {"def": "Function_def", "if": "If_stmt", "while": "Iteration_stmt",
                                             ";": "SYNCH"},
                           "Assignment_Call": {"ID": "ID B", ";": "SYNCH"},
                           "B": {"=": "= C", "(": "( Arguments )", ";": "SYNCH", "[": "[ Expression ] = C"},
                           "C": {"ID": "Expression", "[": "[ Expression List_Rest ]", "NUM": "Expression",
                                 ";": "SYNCH"},
                           "List_Rest": {"]": "EPSILON", ",": ", Expression List_Rest"},
                           "Return_stmt": {"return": "return Return_Value", ";": "SYNCH"},
                           "Return_Value": {";": "EPSILON", "ID": "Expression", "NUM": "Expression"},
                           "Global_stmt": {"global": "global ID", ";": "SYNCH"},
                           "Function_def": {"def": "def ID ( Params ) : Statements", ";": "SYNCH"},
                           "Params": {"ID": "ID Params_Prime", ")": "EPSILON"},
                           "Params_Prime": {")": "EPSILON", ",": ", ID Params_Prime"},
                           "If_stmt": {"if": "if Relational_Expression : Statements Else_block", ";": "SYNCH"},
                           "Else_block": {";": "EPSILON", "else": "else : Statements"},
                           "Iteration_stmt": {"while": "while ( Relational_Expression ) Statements", ";": "SYNCH"},
                           "Relational_Expression": {"ID": "Expression Relop Expression",
                                                     "NUM": "Expression Relop Expression", ":": "SYNCH", ")": "SYNCH"},
                           "Relop": {"==": "==", "<": "<", "ID": "SYNCH", "NUM": "SYNCH"},
                           "Expression": {"ID": "Term Expression_Prime", "NUM": "Term Expression_Prime", "]": "SYNCH",
                                          ";": "SYNCH", ",": "SYNCH", "==": "SYNCH", "<": "SYNCH", ":": "SYNCH",
                                          ")": "SYNCH"},
                           "Expression_Prime": {";": "EPSILON", "]": "EPSILON", ")": "EPSILON", ",": "EPSILON",
                                                ":": "EPSILON", "==": "EPSILON", "<": "EPSILON",
                                                "+": "+ Term Expression_Prime", "-": "- Term Expression_Prime"},
                           "Term": {"ID": "Factor Term_Prime", "NUM": "Factor Term_Prime", "+": "SYNCH", "-": "SYNCH",
                                    "]": "SYNCH", ";": "SYNCH", ",": "SYNCH", "==": "SYNCH", "<": "SYNCH", ":": "SYNCH",
                                    ")": "SYNCH"},
                           "Term_Prime": {";": "EPSILON", "]": "EPSILON", ")": "EPSILON", ",": "EPSILON",
                                          ":": "EPSILON",
                                          "==": "EPSILON", "<": "EPSILON", "+": "EPSILON", "-": "EPSILON",
                                          "*": "* Factor Term_Prime"},
                           "Factor": {"ID": "Atom Power", "NUM": "Atom Power", "*": "SYNCH", "+": "SYNCH", "-": "SYNCH",
                                      "]": "SYNCH", ";": "SYNCH", ",": "SYNCH", "==": "SYNCH", "<": "SYNCH",
                                      ":": "SYNCH",
                                      ")": "SYNCH"},
                           "Power": {";": "Primary", "[": "Primary", "]": "Primary", "(": "Primary", ")": "Primary",
                                     ",": "Primary", ":": "Primary", "==": "Primary", "<": "Primary", "+": "Primary",
                                     "-": "Primary", "*": "Primary", "**": "** Factor"},
                           "Primary": {";": "EPSILON", "[": "[ Expression ] Primary", "]": "EPSILON",
                                       "(": "( Arguments ) Primary", ")": "EPSILON", ",": "EPSILON", ":": "EPSILON",
                                       "==": "EPSILON", "<": "EPSILON", "+": "EPSILON", "-": "EPSILON", "*": "EPSILON"},
                           "Arguments": {"ID": "Expression Arguments_Prime", ")": "EPSILON",
                                         "NUM": "Expression Arguments_Prime"},
                           "Arguments_Prime": {")": "EPSILON", ",": ", Expression Arguments_Prime"},
                           "Atom": {"ID": "ID", "NUM": "NUM", "**": "SYNCH", "[": "SYNCH", "(": "SYNCH", "*": "SYNCH",
                                    "+": "SYNCH", "-": "SYNCH", "]": "SYNCH", ";": "SYNCH", ",": "SYNCH", "==": "SYNCH",
                                    "<": "SYNCH", ":": "SYNCH", ")": "SYNCH"}}

    def start_process(self):
        stack = ["$", "Program"]
        program = Node("Program")
        father_stack = [program]  # TODO
        can_get_next_token = True
        token_cuple = None
        finish = False
        while True:
            if len(stack) == 0:
                break
            if self.scanner.bool_continue_get_next == False:
                next_token = "$"
            elif can_get_next_token:

                self.scanner.get_next_token()
                if finish:
                    break
                if self.scanner.lineNumber >= len(self.scanner.allTokens):
                    finish = True
                    next_token = "$"
                else:
                    token_cuple = self.scanner.allTokens[self.scanner.lineNumber][-1]
                    if token_cuple[0] == "ID" and token_cuple[1] != "global":
                        next_token = token_cuple[0]
                    elif token_cuple[0] == "NUMBER":
                        token_cuple = ("NUM", token_cuple[1])
                        next_token = token_cuple[0]
                    else:
                        next_token = token_cuple[1]

            top = stack[-1]

            if list(self.pars_table.keys()).count(top) != 0 and list(self.pars_table[top].keys()).count(
                    next_token) == 0:
                if next_token == "$":
                    self.all_errors.append((self.scanner.lineNumber, " : syntax error, Unexpected EOF"))
                    break
                if self.scanner.counter == 0:
                    self.all_errors.append((self.scanner.lineNumber, " : syntax error, illegal " + next_token))
                    can_get_next_token = True
                else:
                    self.all_errors.append((self.scanner.lineNumber + 1, " : syntax error, illegal " + next_token))
                    can_get_next_token = True
            elif list(self.pars_table.keys()).count(top) != 0 and self.pars_table[top][next_token] == "SYNCH":
                stack.pop()
                father_stack.pop()
                if self.scanner.counter == 0:
                    self.all_errors.append((self.scanner.lineNumber, " : " + "syntax error, missing " + top))
                else:
                    self.all_errors.append((self.scanner.lineNumber + 1, " : " + "syntax error, missing " + top))
                can_get_next_token = False
            elif list(self.pars_table.keys()).count(top) != 0 and self.pars_table[top][next_token] == "EPSILON":
                hold_NT = stack.pop()
                hold_father = Node(hold_NT, father_stack.pop())
                Node("epsilon", hold_father)
                can_get_next_token = False
            elif list(self.pars_table.keys()).count(top) == 0 and top != next_token:
                stack.pop()
                father_stack.pop()
                if self.scanner.counter == 0:
                    self.all_errors.append((self.scanner.lineNumber, " : " + "syntax error, missing " + top))
                else:
                    self.all_errors.append((self.scanner.lineNumber + 1, " : " + "syntax error, missing " + top))
                can_get_next_token = False
            elif top == next_token:
                if (next_token == "$"):
                    stack.pop()
                    Node("$", program)
                    break
                else:
                    stack.pop()
                    hold_node = father_stack.pop()
                    Node("(" + token_cuple[0] + ", " + token_cuple[1] + ")", hold_node)
                    can_get_next_token = True
            else:
                can_get_next_token = False
                x = stack.pop()
                if x != "Program":
                    string_ = str(self.pars_table[top][next_token])
                    all_to_push = string_.split(" ")
                    hold_node = father_stack.pop()
                    hold_node = Node(x, hold_node)
                else:
                    string_ = str(self.pars_table[top][next_token])
                    all_to_push = string_.split(" ")
                    hold_node = program

                all_to_push.reverse()
                for i in range(len(all_to_push)):
                    if all_to_push[i] == "EPSILON":
                        Node("epsilon", hold_node)
                    else:
                        stack.append(all_to_push[i])
                        father_stack.append(hold_node)

        x = ""
        counter1 = 0
        for pre, _, node in RenderTree(program):
            counter1 += 1
            x += "%s%s" % (pre, node.name)
            if counter1 <= len(program.descendants):
                x += "\n"
        with open('parse_tree.txt', 'w', encoding="utf-8") as f:
            f.write(x)
        with open('syntax_errors.txt', 'w', encoding="utf-8") as f:
            if len(self.all_errors) == 0:
                f.write("There is no syntax error.")
            else:
                y = ""
                counter = 0
                for i in self.all_errors:
                    counter += 1
                    y += "#"
                    y += str(i[0])
                    y += i[1]
                    if counter <= len(self.all_errors):
                        y += "\n"
                f.write(y)


        self.scanner.checkUnclosedComment()
        self.scanner.save()


if __name__ == '__main__':
    x = Lexer()
