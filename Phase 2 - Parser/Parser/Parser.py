class parser:

    def modify_pars_table(self, pars_table):
        pars_table["If_stmt"] = {"if": "if Relational_Expression : Statements Else_block", ";": "SYNCH"}
        pars_table["Else_block"] = {";": "EPSILON", "else": "else : Statements"}
        pars_table["Iteration_stmt"] = {"while": "while ( Relational_Expression ) Statements", ";": "SYNCH"}
        pars_table["Relational_Expression"] = {"ID": "Expression Relop Expression",
                                               "NUM": "Expression Relop Expression", ":": "SYNCH", ")": "SYNCH"}
        pars_table["Relop"] = {"==": "==", "<": "<", "ID": "SYNCH", "NUM": "SYNCH"}
        pars_table["Expression"] = {"ID": "Term Expression_Prime", "NUM": "Term Expression_Prime", "]": "SYNCH",
                                    ";": "SYNCH", ",": "SYNCH", "==": "SYNCH", "<": "SYNCH", ":": "SYNCH", ")": "SYNCH"}
        pars_table["Expression_Prime"] = {";": "EPSILON", "]": "EPSILON", ")": "EPSILON", ",": "EPSILON",
                                          ":": "EPSILON", "==": "EPSILON", "<": "EPSILON",
                                          "+": "+ Term Expression_Prime", "-": "- Term Expression_Prime"}
        pars_table["Term"] = {"ID": "Factor Term_Prime", "NUM": "Factor Term_Prime", "+": "SYNCH", "-": "SYNCH",
                              "]": "SYNCH", ";": "SYNCH", ",": "SYNCH", "==": "SYNCH", "<": "SYNCH", ":": "SYNCH",
                              ")": "SYNCH"}
        pars_table["Term_Prime"] = {";": "EPSILON", "]": "EPSILON", ")": "EPSILON", ",": "EPSILON", ":": "EPSILON",
                                    "==": "EPSILON", "<": "EPSILON", "+": "EPSILON", "-": "EPSILON",
                                    "*": "* Factor Term_Prime"}
        pars_table["Factor"] = {"ID": "Atom Power", "NUM": "Atom Power", "*": "SYNCH", "+": "SYNCH", "-": "SYNCH",
                                "]": "SYNCH", ";": "SYNCH", ",": "SYNCH", "==": "SYNCH", "<": "SYNCH", ":": "SYNCH",
                                ")": "SYNCH"}
        pars_table["Power"] = {";": "Primary", "[": "Primary", "]": "Primary", "(": "Primary", ")": "Primary",
                               ",": "Primary", ":": "Primary", "==": "Primary", "<": "Primary", "+": "Primary",
                               "-": "Primary", "*": "Primary", "**": "** Factor"}
        pars_table["Primary"] = {";": "EPSILON", "[": "[ Expression ] Primary", "]": "EPSILON",
                                 "(": "( Arguments ) Primary", ")": "EPSILON", ",": "EPSILON", ":": "EPSILON",
                                 "==": "EPSILON", "<": "EPSILON", "+": "EPSILON", "-": "EPSILON", "*": "EPSILON"}
        pars_table["Arguments"] = {"ID": "Expression Arguments_Prime", ")": "EPSILON",
                                   "NUM": "Expression Arguments_Prime"}
        pars_table["Arguments_Prime"] = {")": "Epsilon", ",": ", Expression Arguments_Prime"}
        pars_table["Atom"] = {"ID": "ID", "NUM": "NUM", "**": "SYNCH", "[": "SYNCH", "(": "SYNCH", "*": "SYNCH",
                              "+": "SYNCH", "-": "SYNCH", "]": "SYNCH", ";": "SYNCH", ",": "SYNCH", "==": "SYNCH",
                              "<": "SYNCH", ":": "SYNCH", ")": "SYNCH"}

    def __init__(self):
        pars_table = {}

        pars_table["Program"] = {"break": "Statements", "continue": "Statements", "ID": "Statements",
                                 "return": "Statements",
                                 "global": "Statements", "def": "Statements", "if": "Statements", "while": "Statements",
                                 "$": "Statements"}
        self.modify_pars_table(self, pars_table)
