from pprint import pprint
# Parsa Sharifi 99101762
# Mohammad Javad Maheronnaghsh 99105691
from Scanner import Scanner


class Codegen:
    def __init__(self):
        self.not_to_set_return_type = []
        self.can_get_not_defined = False
        self.can_del_output = False
        self.dirty_bool = False
        self.semantic_stack = [1] * 1000

        self.program_block = []
        self.cur_temp = 1000
        self.temp = {}
        self.cur_mem_addr = 500
        self.current_function_name = ""
        self.declaring_first_function = True
        self.hold_first_function_formain = 0
        self.count_pass_params = 0
        self.symbol_table = {}
        self.calling_function = []
        self.is_calling_function = False
        self.called_output = False
        self.return_true = False
        self.return_addr_mem = 3000
        self.we_are_in_while = 0
        self.is_defining_global = False
        self.is_defining_inside_func = False
        self.all_semantic_errors = []
        self.have_seen_main = False
        self.number_of_params_to_define_func = 0
        self.temp_hold_func_name = {}
        self.temp_hold_func_params = []
        self.hold_name_isglobal = ""
        self.rhs_start = 0
        self.isvoid = True
        self.hold_name_isglobal2 = ""
        self.can_change_get_not_defined_bool = True
    def main_switch(self, input_, arg, scanner):
        print("1" + str(self.symbol_table))
        # print("@@" + str(self.number_of_params_to_define_func))
        # print(self.program_block)
        print(self.all_semantic_errors)
       # print("RHS " + str(self.rhs_start))

        #if(self.dirty_bool == True and input_ != "#rhs_start"):
         #   self.calling_function.pop()


        if input_ == "#pid":
            self.pid(arg, scanner)
        elif input_ == "#false_not_defined":
            self.can_get_not_defined = False
            #self.can_change_get_not_defined_bool = False
        elif input_ == "#true_not_defined":
            #if self.can_change_get_not_defined_bool:
                self.can_get_not_defined = True
            #else:
             #   self.can_change_get_not_defined_bool = True
        elif input_ == "#delivere_to_global2":
            self.hold_name_isglobal2 = self.hold_name_isglobal
        elif input_ == "#has_return":
            self.isvoid = False
        elif input_ == "#rhs_start":
            self.rhs_start += 1
        elif input_ == "#rhs_end":
            self.rhs_start -= 1
        elif input_ == "#assign_param_numbers":
            line_number = scanner.lineNumber
            param_number = self.number_of_params_to_define_func
            params = self.temp_hold_func_params
            detail_func = self.temp_hold_func_name
            name_func = self.current_function_name
            changed_name_func = name_func + str(param_number)
            if changed_name_func in self.symbol_table:
                self.all_semantic_errors.append("#" + str(
                    line_number + 1) + " : Semantic Error! Function '" + name_func + "' has already been defined with this number of arguments.")
                self.not_to_set_return_type.append(changed_name_func)
                for param in params:
                    address_to_reserve = self.find_addr()
                    self.symbol_table[changed_name_func + str(len(self.not_to_set_return_type)) + " " + param] = {"type": "function_variable",
                                                                          "address": address_to_reserve}
                self.current_function_name = changed_name_func + str(len(self.not_to_set_return_type))
                self.not_to_set_return_type.append(changed_name_func + str(len(self.not_to_set_return_type)))
               # to_delete = []
               # for symbol in self.symbol_table.keys():
               #     list_ = symbol.split()
               #     if len(list_) > 1 and list_[0] == changed_name_func:
               #         to_delete.append(symbol)
               # for symbol in to_delete:
               #     del self.symbol_table[symbol]

            else:
                detail_func["param_num"] = len(params)
                self.symbol_table[changed_name_func] = detail_func
                for param in params:
                    address_to_reserve = self.find_addr()
                    self.symbol_table[changed_name_func + " " + param] = {"type": "function_variable",
                                                                      "address": address_to_reserve}
                self.current_function_name = changed_name_func
            self.temp_hold_func_name = {}
            self.temp_hold_func_params = []

            self.number_of_params_to_define_func = 0
            # print("ASSIGN, number_of_params = " + str(self.number_of_params_to_define_func))
        elif input_ == "#chack_for_main_error":
            if not self.have_seen_main:
                line_number = scanner.lineNumber
                self.all_semantic_errors.append(
                    "#" + str(scanner.global_line_number) + " : Semantic Error! main function not found.")
        elif input_ == "#outside_func":
            if not self.current_function_name in self.not_to_set_return_type:
                if self.isvoid:
                    self.symbol_table[self.current_function_name]["return_type"] = "void"
                else:
                    self.symbol_table[self.current_function_name]["return_type"] = "int"
            self.current_function_name = ""
        elif input_ == "#global_id":
            self.is_defining_global = True
        elif input_ == "#pass_by_reference":
            x = self.find_addr()
            top_stack = self.semantic_stack.pop()
            self.add_to_program_block(f'(ASSIGN, #{x}, {top_stack}, )')
            self.semantic_stack.append(x)
        elif input_ == "#push_c":
            if self.we_are_in_while == 0:
                line_number = scanner.lineNumber
                self.all_semantic_errors.append(
                    "#" + str(line_number + 1) + " : Semantic Error! No 'while' found for 'continue'.")
            self.add_to_program_block('c')
        elif input_ == "#push_b":
            if self.we_are_in_while == 0:
                line_number = scanner.lineNumber
                self.all_semantic_errors.append(
                    "#" + str(line_number + 1) + " : Semantic Error! No 'while' found for 'break'.")
            self.add_to_program_block('b')
        elif input_ == "#push_nothing":
            self.return_true = False
        elif input_ == "#push_next":
            self.semantic_stack.append(arg)
        elif input_ == "#prv":
            hold = self.get_temp()
            self.add_to_program_block(f'(ASSIGN, {self.return_addr_mem}, {hold}, )')
            self.semantic_stack.append(hold)
        elif input_ == "#return_enable":
            self.return_true = True
        elif input_ == "#declare_params":
            self.declare_params(arg)
        elif input_ == "#declare_function":
            self.declare_function(arg)
        elif input_ == "#array_address":
            index = self.semantic_stack.pop()
            var_addr = self.semantic_stack.pop()
            t = self.get_temp()
            self.add_to_program_block(f'(MULT, {index}, #4, {t})')
            self.add_to_program_block(f'(ADD, {var_addr}, {t}, {t})')
            self.semantic_stack.append('@' + str(t))
        elif input_ == "#assign":
            pprint(self.symbol_table)
            op2 = self.semantic_stack.pop()
            op1 = self.semantic_stack.pop()
            self.add_to_program_block(f'(ASSIGN, {op2}, {op1}, )')
        elif input_ == "#add_element_to_arry":
            array_element = self.semantic_stack.pop()
            address_to_push = self.semantic_stack.pop()
            self.add_to_program_block(f'(ASSIGN, {array_element}, {address_to_push}, )')
            self.semantic_stack.append(self.find_addr())
        elif input_ == "#pop":
            self.semantic_stack.pop()
        elif input_ == "#save":
            pb_ind = len(self.program_block)
            self.semantic_stack.append(pb_ind)
            self.add_to_program_block('')
        elif input_ == "#jpf" and len(self.all_semantic_errors) == 0:
            pb_ind = self.semantic_stack.pop()
            if_exp = self.semantic_stack.pop()
            i = len(self.program_block)
            self.program_block[pb_ind] = f'(JPF, {if_exp}, {i}, )'
        elif input_ == "#jpf_save" and len(self.all_semantic_errors) == 0:
            pb_ind = self.semantic_stack.pop()
            if_exp = self.semantic_stack.pop()
            i = len(self.program_block)
            self.program_block[pb_ind] = f'(JPF, {if_exp}, {i + 1}, )'
            self.semantic_stack.append(i)
            self.add_to_program_block('')
        elif input_ == "#jp" and len(self.all_semantic_errors) == 0:
            pb_ind = self.semantic_stack.pop()
            i = len(self.program_block)
            self.program_block[pb_ind] = f'(JP, {i}, , )'
        elif input_ == "#label":
            self.we_are_in_while += 1
            pb_ind = len(self.program_block)
            self.semantic_stack.append(pb_ind + 1)

        elif input_ == "#while":
            # stack_top = self.semantic_stack.pop()
            start = 0
            if len(self.all_semantic_errors) == 0:
                stack_top = self.semantic_stack.pop()
                stack_top_sub_1 = self.semantic_stack.pop()
                stack_top_sub_2 = self.semantic_stack.pop()
                self.program_block[stack_top] = f'(JPF, {stack_top_sub_1}, {len(self.program_block) + 1}, )'
                self.program_block.append(f'(JP, {stack_top_sub_2 - 1}, , )')
                start = stack_top_sub_2 - 1
            self.we_are_in_while -= 1

            end = len(self.program_block) - 1
            if len(self.all_semantic_errors) == 0:
                for i in range(start, end + 1):
                    x = self.program_block[i]
                    if x == "c":
                        self.program_block[i] = f'(JP, {start}, , )'
                    elif x == "b":
                        self.program_block[i] = f'(JP, {len(self.program_block)}, , )'

        elif input_ == "#relop":
            op_2 = self.semantic_stack.pop()
            operand = self.semantic_stack.pop()
            op_1 = self.semantic_stack.pop()
            t = self.get_temp()
            self.semantic_stack.append(t)
            if operand == '==':
                self.add_to_program_block(f'(EQ, {op_1}, {op_2}, {t})')
            elif operand == '<':
                self.add_to_program_block(f'(LT, {op_1}, {op_2}, {t})')
        elif input_ == "#relop_sign":
            self.semantic_stack.append(arg)
        elif input_ == "#add":
            op1 = self.semantic_stack.pop()
            operation = self.semantic_stack.pop()
            op2 = self.semantic_stack.pop()
            t = self.get_temp()
            self.semantic_stack.append(t)
            if operation == '+':
                self.add_to_program_block(f'(ADD, {op1}, {op2}, {t})')
            else:
                self.add_to_program_block(f'(SUB, {op2}, {op1}, {t})')
        elif input_ == "#mult":
            op1 = self.semantic_stack.pop()
            op2 = self.semantic_stack.pop()
            t = self.get_temp()
            self.semantic_stack.append(t)
            self.add_to_program_block(f'(MULT, {op1}, {op2}, {t})')
        elif input_ == "#pnum":
            num_addr = self.get_temp()
            self.add_to_program_block(f'(ASSIGN, #{arg}, {num_addr}, )')
            self.temp.update({num_addr: arg})
            self.semantic_stack.append(num_addr)
        elif input_ == "#true_calling_function":
            self.is_calling_function = True
        elif input_ == "#param_function":
            if self.called_output and self.calling_function[-1] == "output":
                self.output(arg)
            else:
                self.number_of_params_to_define_func += 1
                self.is_calling_function = True
                top_of_ss = self.semantic_stack.pop()
                self.temp_hold_func_params.append(top_of_ss)
                # start_point = self.semantic_stack[-2]
                # new_point = start_point + 4
                # self.add_to_program_block(f'(ASSIGN, {self.semantic_stack[-1]}, {new_point}, )')
                # self.semantic_stack.pop()
                # self.semantic_stack.pop()
                # self.semantic_stack.append(new_point)
        elif input_ == "#jump_to_function":
            true_name = ""
            error_bool = False
            if self.called_output and len(self.calling_function) >0 and self.calling_function[-1] == "output":
                if self.can_del_output:
                    self.can_del_output = False
                    self.called_output = False
                    self.number_of_params_to_define_func = 0
                    self.calling_function.pop()
            elif not self.called_output or self.calling_function[-1] != "output":
                param_number = self.number_of_params_to_define_func
                changed_named = self.calling_function[-1] + str(param_number)
                self.calling_function.pop()
                self.calling_function.append(changed_named)
                if len(self.all_semantic_errors) == 0:
                    ss_top = self.semantic_stack.pop()
               # del self.symbol_table[self.current_function_name + " " + self.hold_name_isglobal2]



                if not changed_named in self.symbol_table:  # need keys()?
                    line_number = scanner.lineNumber

                    for x in self.symbol_table.keys():
                        a = x[0:len(x) - 1]
                        b = changed_named[0:len(changed_named) - 1]
                        if x[0:len(x) - 1] == changed_named[0:len(changed_named) - 1]:
                            self.all_semantic_errors.append("#" + str(line_number + 1) + " : Semantic Error!"
                                                            + " Mismatch in numbers of arguments of '" + changed_named[
                                                                                                         0:len(
                                                                                                             changed_named) - 1] + "'.")

                            error_bool = True
                            true_name = x
                            break
                    if not error_bool and self.can_get_not_defined and changed_named[0:len(changed_named) - 1] != "output":
                        #self.can_get_not_defined = False
                        self.all_semantic_errors.append("#" + str(line_number + 1) + " : Semantic Error! '" +
                                                        changed_named[
                                                        0:len(changed_named) - 1] + "' is not defined appropriately.")
                        error_bool = True

                # if not error_bool:
                if true_name != "":
                    changed_named = true_name
                if changed_named in self.symbol_table: #and self.rhs_start > 0:##todo not error_bool was added for test 3 or 10 ?????
                    if self.rhs_start > 0 and self.symbol_table[changed_named]["return_type"] == "void":
                        line_number = scanner.lineNumber
                        self.all_semantic_errors.append(
                            "#" + str(line_number + 1) + " : Semantic Error! Void type in operands.")

                    func = self.symbol_table[changed_named]
                    func_addr = func["address"]
                    for param in self.temp_hold_func_params:
                        func_addr += 4
                        self.add_to_program_block(f'(ASSIGN, {param}, {func_addr}, )')
                    #self.calling_function.append(changed_named)
                    #hold = self.calling_function[-1]
                    hold = changed_named
                    y = self.symbol_table[hold]["address"]
                    self.add_to_program_block(f'(ASSIGN, #{len(self.program_block) + 2}, {y}, )')
                    x = self.symbol_table[hold]
                    self.add_to_program_block(f'(JP, {x["PB_address"]}, , )')
                    self.calling_function.pop()
                self.is_calling_function = False
                self.temp_hold_func_params = []
                self.number_of_params_to_define_func = 0

        elif input_ == "#return_back":
            number_param = self.number_of_params_to_define_func
            if self.isvoid and  not self.current_function_name in self.not_to_set_return_type:
                self.symbol_table[self.current_function_name]["return_type"] = "void"
            if not self.isvoid and  not self.current_function_name in self.not_to_set_return_type:
                self.symbol_table[self.current_function_name]["return_type"] = "int"
            if self.return_true:
                self.return_true = False
                y = self.semantic_stack.pop()
                self.add_to_program_block(f'(ASSIGN, {y}, {self.return_addr_mem}, )')
            hold = ""
            if len(self.calling_function) == 0:
                hold = self.current_function_name
            else:
                hold = self.calling_function[-1]
            if hold in self.symbol_table:
                x = self.symbol_table[hold]["address"]
                temp_ = self.get_temp()
                self.add_to_program_block(f'(ASSIGN, {x}, {temp_}, )')
                self.add_to_program_block(f'(JP, @{temp_}, , )')

        elif input_ == "#output_call":
            self.output()
        print("####################")
        print("current = " + input_)
        # print("block = " + str(self.program_block))
        #print("stack = " + str(self.semantic_stack))
        print("next" , arg)
        #print("calling stack" , self.calling_function)
        #print("errorrrrr  " , self.all_semantic_errors )
    def declare_function(self, next_token):
        self.isvoid = True
        self.number_of_params_to_define_func = 0
        if self.declaring_first_function:
            self.hold_first_function_formain = len(self.program_block)
            self.declaring_first_function = False
            self.add_to_program_block('')
        if next_token == "main":
            self.have_seen_main = True
            if len(self.all_semantic_errors) == 0:
                self.program_block[self.hold_first_function_formain] = (f'(JP, {len(self.program_block)}, , )')
        start_address = self.find_addr()
        self.temp_hold_func_name = {"type": "function", "address": start_address,
                                    "PB_address": len(self.program_block), "param_num": -1}
        # self.symbol_table[next_token] = {"type": "function", "address": start_address,
        #                                  "PB_address": len(self.program_block), "param_num":-1}
        self.current_function_name = next_token

    def start_get_paramd(self):
        self.count_pass_params = 0

    def declare_params(self, next_token):
        self.number_of_params_to_define_func += 1
        # hold_name = self.current_function_name + " " + next_token
        # mem_address = self.find_addr()
        self.temp_hold_func_params.append(next_token)
        # self.symbol_table[hold_name] = {"type": "function_variable", "address": mem_address}  # todo type ???

    def isglobal(self, next_token):
        for key in self.symbol_table:
            string_list = key.split()
            if len(string_list) == 1:
                if string_list[0][0:len(string_list)-2] == next_token:
                    if self.symbol_table[string_list[0]]["type"] == "function":
                        self.start_get_paramd()
                        self.calling_function.append(next_token)
                    self.semantic_stack.append(self.symbol_table[key]["address"])
                    return True
        self.calling_function.append(next_token)
        self.dirty_bool = True
        self.hold_name_isglobal = next_token
        return False

    def pid(self, next_token, scanner):
        if next_token == "output":
            self.called_output = True
            self.rhs_start += 1
            self.calling_function.append("output")
        else:
            hold_name = self.current_function_name + " " + next_token
            if list(self.symbol_table.keys()).count(hold_name) != 0:
                hold_dict = self.symbol_table[hold_name]
                self.semantic_stack.append(hold_dict["address"])
            elif self.isglobal(next_token):
                pass
            else:
                if self.rhs_start > 0 and not self.is_calling_function:  # 26 : Semantic Error! 'c' is not defined appropriately.
                    line_number = scanner.lineNumber
                    line_number += 1
                    flag = False
                    for x in self.symbol_table.keys():
                        if x[0:len(x) - 1] == next_token and self.symbol_table[x]["type"] == "function":
                            flag = True
                    if not flag:
                        self.all_semantic_errors.append("#" + str(
                            line_number) + " : Semantic Error! '" + next_token + "' is not defined appropriately.")
                        self.calling_function.remove(next_token)
                elif self.rhs_start > 0 and self.is_calling_function:
                    line_number = scanner.lineNumber
                    line_number += 1
                    flag = False
                    for x in self.symbol_table.keys():
                        if x[0:len(x) - 1] == next_token and self.symbol_table[x]["type"] != "function":
                            flag = True
                    if not flag:
                        self.all_semantic_errors.append("#" + str(
                            line_number) + " : Semantic Error! '" + next_token + "' is not defined appropriately.")
                if self.current_function_name == "":
                    if self.is_defining_global:
                        hold_name = next_token
                        self.is_defining_global = False
                    else:
                        hold_name = "main0 " + next_token
                mem_address = self.find_addr()
                self.symbol_table[hold_name] = {"type": "function_variable", "address": mem_address}
                hold_dict = self.symbol_table[hold_name]
                self.semantic_stack.append(hold_dict["address"])

    def find_addr(self):
        t = self.cur_mem_addr
        self.cur_mem_addr += 4
        return t

    def get_temp(self):
        t = self.cur_temp
        self.cur_temp += 4
        return t

    def output(self, arg=None):
        if self.called_output:
            self.can_del_output = True
            to_print = self.semantic_stack.pop()
            self.add_to_program_block(f'(PRINT, {to_print}, , )')
            self.rhs_start -= 1
            self.semantic_stack.append(None)
            self.called_output = False
        # else:
        #     self.rhs_start -= 1

    def add_to_program_block(self, str):
        self.program_block.append(str)
