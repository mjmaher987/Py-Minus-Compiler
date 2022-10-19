from anytree import Node, RenderTree

import codegen
from Scanner import *

#Parsa Sharifi 99101762
#Mohammad Javad Maheronnaghsh 99105691
class Lexer:
    def __init__(self):
        # self.CodeGenerator =
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
        self.pars_table = {"Program": {"break": "Statements #chack_for_main_error", "continue": "Statements #chack_for_main_error", "ID": "Statements #chack_for_main_error",
                                       "return": "Statements #chack_for_main_error",
                                       "global": "Statements #chack_for_main_error", "def": "Statements #chack_for_main_error", "if": "Statements #chack_for_main_error",
                                       "while": "Statements #chack_for_main_error",
                                       "$": "Statements #chack_for_main_error"},
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
                           "Simple_stmt": {"break": "#push_b break", "continue": "#push_c continue", "ID": "Assignment_Call",
                                           "return": "Return_stmt",
                                           "global": "Global_stmt", ";": "SYNCH"},
                           "Compound_stmt": {"def": "Function_def", "if": "If_stmt", "while": "Iteration_stmt",
                                             ";": "SYNCH"},
                           "Assignment_Call": {"ID": "#pid ID B", ";": "SYNCH"},
                           "B": {"=": "= #false_not_defined #rhs_start C #true_not_defined #rhs_end", "(": "( #rhs_start #delivere_to_global2 Arguments #rhs_end ) "
                                                                      "#output_call", ";": "SYNCH",
                                 "[": "[ Expression #array_address ] = #false_not_defined #rhs_start C #true_not_defined #rhs_end"},
                           "C": {"ID": "Expression #assign", "[": "[ #pass_by_reference Expression #add_element_to_arry List_Rest #pop ]", "NUM": "Expression #assign",#todo check assign #add_element_to_memory
                                 ";": "SYNCH"},
                           "List_Rest": {"]": "EPSILON", ",": ", Expression #add_element_to_arry List_Rest"},
                           "Return_stmt": {"return": "return #rhs_start #return_enable Return_Value #rhs_end #return_back", ";": "SYNCH"},
                           "Return_Value": {";": "#push_nothing EPSILON", "ID": "#has_return Expression", "NUM": "#has_return Expression"},
                           "Global_stmt": {"global": "global #global_id #pid ID", ";": "SYNCH"},#global id
                           "Function_def": {"def": "def #declare_function ID ( Params #assign_param_numbers ) : Statements #return_back #outside_func", ";": "SYNCH"},#todo id for function
                           "Params": {"ID": "#declare_params ID Params_Prime", ")": "EPSILON"},
                           "Params_Prime": {")": "EPSILON", ",": ", #declare_params ID Params_Prime"},
                           "If_stmt": {"if": "if Relational_Expression #save : Statements Else_block", ";": "SYNCH"},
                           "Else_block": {";": "EPSILON #jpf", "else": "else #jpf_save : Statements #jp"},
                           "Iteration_stmt": {"while": "while #label ( Relational_Expression ) #save Statements #while", ";": "SYNCH"},#todo check save and label for while
                           "Relational_Expression": {"ID": "#rhs_start Expression Relop Expression #rhs_end #relop",#todo check relop and next 2 lines!!!!!
                                                     "NUM": "#rhs_start Expression Relop Expression #rhs_end #relop", ":": "SYNCH", ")": "SYNCH"},
                           "Relop": {"==": "#relop_sign ==", "<": "#relop_sign <", "ID": "SYNCH", "NUM": "SYNCH"},
                           "Expression": {"ID": "Term Expression_Prime", "NUM": "Term Expression_Prime", "]": "SYNCH",
                                          ";": "SYNCH", ",": "SYNCH", "==": "SYNCH", "<": "SYNCH", ":": "SYNCH",
                                          ")": "SYNCH"},
                           "Expression_Prime": {";": "EPSILON", "]": "EPSILON", ")": "EPSILON", ",": "EPSILON",
                                                ":": "EPSILON", "==": "EPSILON", "<": "EPSILON",
                                                "+": "#push_next + Term #add Expression_Prime", "-": "#push_next - Term #add Expression_Prime"},#todo check add and sub
                           "Term": {"ID": "Factor Term_Prime", "NUM": "Factor Term_Prime", "+": "SYNCH", "-": "SYNCH",
                                    "]": "SYNCH", ";": "SYNCH", ",": "SYNCH", "==": "SYNCH", "<": "SYNCH", ":": "SYNCH",
                                    ")": "SYNCH"},
                           "Term_Prime": {";": "EPSILON", "]": "EPSILON", ")": "EPSILON", ",": "EPSILON",
                                          ":": "EPSILON",
                                          "==": "EPSILON", "<": "EPSILON", "+": "EPSILON", "-": "EPSILON",
                                          "*": "* Factor #mult Term_Prime"},#todo check mult
                           "Factor": {"ID": "Atom Power", "NUM": "Atom Power", "*": "SYNCH", "+": "SYNCH", "-": "SYNCH",
                                      "]": "SYNCH", ";": "SYNCH", ",": "SYNCH", "==": "SYNCH", "<": "SYNCH",
                                      ":": "SYNCH",
                                      ")": "SYNCH"},
                           "Power": {";": "Primary", "[": "Primary", "]": "Primary", "(": "Primary", ")": "Primary",
                                     ",": "Primary", ":": "Primary", "==": "Primary", "<": "Primary", "+": "Primary",
                                     "-": "Primary", "*": "Primary", "**": "** Factor"},
                           "Primary": {";": "EPSILON", "[": "[ Expression #array_address ] Primary", "]": "EPSILON",
                                       "(": "( #rhs_start #delivere_to_global2 Arguments #rhs_end #prv ) Primary", ")": "EPSILON", ",": "EPSILON", ":": "EPSILON",
                                       "==": "EPSILON", "<": "EPSILON", "+": "EPSILON", "-": "EPSILON", "*": "EPSILON"},
                           "Arguments": {"ID": "Expression #param_function Arguments_Prime #rhs_end #jump_to_function #rhs_start", ")": "#true_calling_function #rhs_end #jump_to_function #rhs_start EPSILON",
                                         "NUM": "Expression #param_function Arguments_Prime #rhs_end #jump_to_function #rhs_start"},
                           "Arguments_Prime": {")": "EPSILON", ",": ", #delivere_to_global2 Expression #param_function Arguments_Prime"},
                           "Atom": {"ID": "#pid ID", "NUM": "#pnum NUM", "**": "SYNCH", "[": "SYNCH", "(": "SYNCH", "*": "SYNCH",#todo added pnum
                                    "+": "SYNCH", "-": "SYNCH", "]": "SYNCH", ";": "SYNCH", ",": "SYNCH", "==": "SYNCH",
                                    "<": "SYNCH", ":": "SYNCH", ")": "SYNCH"}}

    def start_process(self):
        global next_token
        stack = ["$", "Program"]
        program = Node("Program")
        father_stack = [program]  # TODO
        can_get_next_token = True
        token_cuple = None
        finish = False
        while True:
            # if len(stack) == 1:
            #    stack.append("Program")
            # else:
            # if len(stack) == 0:
            #    break
            # else:
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
                    elif token_cuple[0] == "ID" and token_cuple[1] == "global":
                        token_cuple = ("KEYWORD", token_cuple[1])
                        next_token = token_cuple[1]
                    elif token_cuple[0] == "NUMBER":
                        token_cuple = ("NUM", token_cuple[1])
                        next_token = token_cuple[0]
                    else:
                        next_token = token_cuple[1]
            # else:
            #    can_get_next_token = True
            top = stack[-1]
            # if next_token == "$":
            #    break
            # if top == "Statement" or top == "Statements":
                # print(top + "  " + next_token)
            # print(list(self.pars_table[top].keys()))
            # print(type(self.pars_table[top]))
            # z = list(self.pars_table[top].keys()).count(next_token)
            #TODO
            #check for #
            # if top.startswith("#"):
            #     # codegenerator.main_switch(top, token_cuple[1])
            #     # stack.pop()
            #     # top = stack[-1]
            # print("$$" + str(stack))
            while top.startswith("#"):


                codegenerator.main_switch(top, token_cuple[1], self.scanner)
                stack.pop()

                father_stack.pop()
                top = stack[-1]
           # print("token", token_cuple[1])
            #print("compiler stack" , stack)
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
                # +" on line " + str(self.scanner.lineNumber)
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
                # for i in range(len(all_to_push)):
                #    father_stack.append(hold_node)
                # for i in range(len(all_to_push)):
                #    father_stack.append(Node(all_to_push[i], father_stack[-1]))

                all_to_push.reverse()
                for i in range(len(all_to_push)):
                    if all_to_push[i] == "EPSILON":
                        Node("epsilon", hold_node)
                    else:
                        stack.append(all_to_push[i])
                        father_stack.append(hold_node)
                # print(RenderTree(program).by_attr("foo"))
            #     print(stack)
            # print(self.all_errors)
        x = ""
        counter1 = 0
        for pre, _, node in RenderTree(program):
            counter1 += 1
            x += "%s%s" % (pre, node.name)
            if counter1 <= len(program.descendants):
                x += "\n"
        codegen_output = ""
        count = 0
        for t in codegenerator.program_block:
            if count <= len(codegenerator.program_block) - 3:
                codegen_output += str(count)
                codegen_output += "\t"
                codegen_output += t
                codegen_output += "\n"
            count += 1
        #remove duplicate errors
        codegenerator.all_semantic_errors = list(dict.fromkeys(codegenerator.all_semantic_errors))
        with open('output.txt', 'w', encoding="utf-8") as f:
            if len(codegenerator.all_semantic_errors) == 0:
                f.write(codegen_output)
            else:
                f.write("The output code has not been generated.")
        with open('semantic_errors.txt', 'w', encoding="utf-8") as f:
            to_write_string = ""
            for error in codegenerator.all_semantic_errors:
                to_write_string += error
                to_write_string += "\n"
            if to_write_string == "":
                f.write("The input program is semantically correct.")
            else:
                f.write(to_write_string[0:-1])
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


        # print(stack)
        self.scanner.checkUnclosedComment()
        self.scanner.save()

        # print("asd")


if __name__ == '__main__':
    global codegenerator
    codegenerator = codegen.Codegen()
    x = Lexer()


    # x.start_process()
