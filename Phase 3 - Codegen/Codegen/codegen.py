from pprint import pprint


class Codegen:
    def __init__(self):
        self.semantic_errors = []
        self.semantic_stack = []
        self.program_block = []
        self.cur_temp = 1000
        self.temp = {}
        self.cur_mem_addr = 500
        self.func_memory_cur = 2000
        self.memory = {}
        self.break_stack = []
        self.main_access_link = None
        self.fun_declarating = False
        self.arg_declarating = False
        self.declaring_function_body = False
        self.declaring_function_header = False
        self.passing_function_parameters = False
        self.current_function_name = ""
        self.declaring_first_function = True
        self.declaring_main_function = False
        self.declaring_function_parameter = False
        self.hold_first_function_formain = 0
        self.count_pass_params = 0
        self.action_symbols = {
            'pid': self.pid,
            'pnum': self.pnum,  # todo added
            'array_address': self.array_address,
            'assign': self.assign,  # todo added
            'add': self.add,  # todo added
            'mult': self.mult,  # todo added
            'save': self.save,  # todo added
            'jp': self.jp,  # todo added
            'jpf': self.jpf,
            'label': self.label,  # todo added
            'relop': self.relop,  # todo added
            'relop_sign': self.relop_sign,  # todo added
            'sign': self.sign,
            'signed_num': self.signed_num,
            'while': self.whil,
            'pop': self.pop,
            'output': self.output,
            'save_arr': self.save_arr,
            'tmp_save': self.tmp_save,
            'cmp_save': self.cmp_save,
            'jp_break': self.jp_break,
            'jp_switch': self.jp_switch,
            'jpf_switch': self.jpf_switch,
            'function_call': self.function_call,
            'var': self.var,
            'arg': self.arg,
            'fun_declaration': self.fun_declaration,
            'fun_declaration_end': self.fun_declaration_end,
            'param_var': self.param_var,
            'param_arr': self.param_arr,
            'fun_declarated': self.fun_declarated,
            'arg_declaration': self.arg_declaration,
            'return_stmt': self.return_stmt,
        }
        self.arg_actions = ['pid', 'pnum', 'sign', 'relop_sign',
                            'fun_declaration', 'arg_declaration']
        self.symbol_table = {}
        self.temp_args = []
        self.function = None
        self.callers = []
        self.function_arg_number = 0
        self.temp_id = None
        # self.calling_function = []
        self.calling_function = []
        self.is_calling_function = False
        self.called_output = False
        self.return_true = False
        self.return_addr_mem = 3000
        self.we_are_in_while = 0
        self.is_defining_global = False
        self.is_defining_inside_func = False

    def main_switch(self, input_, arg):

        if input_ == "#pid":
            self.pid(arg)
        elif input_ == "#outside_func":
            self.current_function_name = ""
        elif input_ == "#global_id":
            self.is_defining_global = True
        elif input_ == "#pass_by_reference":
            x = self.find_addr()
            top_stack = self.semantic_stack.pop()
            self.add_to_program_block(f'(ASSIGN, #{x}, {top_stack}, )')
            self.semantic_stack.append(x)
        elif input_ == "#push_c":
            self.add_to_program_block('c')
        elif input_ == "#push_b":
            self.add_to_program_block('b')
        elif input_ == "#push_nothing":
            self.return_true = False
            # self.semantic_stack.append("10000")
            # self.add_to_program_block(f'(ASSIGN, #{0}, {10000}, )')
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
            # new_temp = self.get_temp()
            # self.add_to_program_block(f'(ASSIGN, #{t}, {new_temp}, )')
            self.semantic_stack.append('@' + str(t))
        elif input_ == "#assign":
            pprint(self.symbol_table)
            op2 = self.semantic_stack.pop()
            op1 = self.semantic_stack.pop()
            self.add_to_program_block(f'(ASSIGN, {op2}, {op1}, )')
            # self.semantic_stack.append(op1)
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
        elif input_ == "#jpf":
            pb_ind = self.semantic_stack.pop()
            if_exp = self.semantic_stack.pop()
            i = len(self.program_block)
            # print(self.program_block)
            self.program_block[pb_ind] = f'(JPF, {if_exp}, {i}, )'
        elif input_ == "#jpf_save":
            pb_ind = self.semantic_stack.pop()
            if_exp = self.semantic_stack.pop()
            i = len(self.program_block)
            # print(self.program_block)
            self.program_block[pb_ind] = f'(JPF, {if_exp}, {i + 1}, )'
            self.semantic_stack.append(i)
            self.add_to_program_block('')
        elif input_ == "#jp":
            pb_ind = self.semantic_stack.pop()
            i = len(self.program_block)
            self.program_block[pb_ind] = f'(JP, {i}, , )'
        elif input_ == "#label":
            self.we_are_in_while += 1
            # self.break_stack.append('while')  # todo why?????
            pb_ind = len(self.program_block)  # todo: changed  ---->  - 1
            self.semantic_stack.append(pb_ind + 1)

        elif input_ == "#while":
            stack_top = self.semantic_stack.pop()
            stack_top_sub_1 = self.semantic_stack.pop()
            stack_top_sub_2 = self.semantic_stack.pop()
            self.program_block[stack_top] = f'(JPF, {stack_top_sub_1}, {len(self.program_block) + 1}, )'
            # self.add_to_program_block('')
            # corrected jp to JP
            # if self.we_are_in_while > 0:
            #     self.program_block.pop()
            #     self.program_block.pop()
            #     self.add_to_program_block("")
            #     self.add_to_program_block("")
            self.program_block.append(f'(JP, {stack_top_sub_2 - 1}, , )')
            self.we_are_in_while -= 1
            start = stack_top_sub_2 - 1
            end = len(self.program_block) - 1
            for i in range(start, end + 1):
                x = self.program_block[i]
                if x == "c":
                    self.program_block[i] = f'(JP, {start}, , )'
                elif x == "b":
                    self.program_block[i] = f'(JP, {len(self.program_block)}, , )'

            # self.add_to_program_block('')
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
        elif input_ == "#param_function":
            if self.called_output:
                self.output(arg)
            else:
                self.is_calling_function = True
                start_point = self.semantic_stack[-2]
                new_point = start_point + 4
                self.add_to_program_block(f'(ASSIGN, {self.semantic_stack[-1]}, {new_point}, )')
                self.semantic_stack.pop()
                self.semantic_stack.pop()
                self.semantic_stack.append(new_point)
        elif input_ == "#jump_to_function":
            # self.semantic_stack.append(len(self.program_block))
            if not self.called_output and self.is_calling_function:
                hold = self.calling_function[-1]
                y = self.symbol_table[hold]["address"]
                self.add_to_program_block(f'(ASSIGN, #{len(self.program_block) + 2}, {y}, )')
                x = self.symbol_table[hold]
                self.add_to_program_block(f'(JP, {x["PB_address"]}, , )')
                self.is_calling_function = False
                self.calling_function.pop()
        elif input_ == "#return_back":
            # if not self.we_are_in_while:
            # if self.is_calling_function:
            if self.return_true:
                self.return_true = False
                y = self.semantic_stack.pop()
                self.add_to_program_block(f'(ASSIGN, {y}, {self.return_addr_mem}, )')
            hold = ""
            if len(self.calling_function) == 0:
                hold = self.current_function_name
            else:
                hold = self.calling_function[-1]

            x = self.symbol_table[hold]["address"]
            temp_ = self.get_temp()
            self.add_to_program_block(f'(ASSIGN, {x}, {temp_}, )')
            self.add_to_program_block(f'(JP, @{temp_}, , )')
        # TODO
        # elif input_ == "#return_back_definition":

        elif input_ == "#output_call":
            self.output()
        print("####################")
        print("current = " + input_)
        print("block = " + str(self.program_block))
        print("stack = " + str(self.semantic_stack))

    def declare_function(self, next_token):
        if self.declaring_first_function:
            self.hold_first_function_formain = len(self.program_block)
            self.declaring_first_function = False
            self.add_to_program_block('')
        if next_token == "main":
            self.program_block[self.hold_first_function_formain] = (f'(JP, {len(self.program_block)}, , )')
        start_address = self.find_addr()
        self.symbol_table[next_token] = {"type": "function", "address": start_address,
                                         "PB_address": len(self.program_block)}
        self.current_function_name = next_token

    def start_get_paramd(self):
        self.count_pass_params = 0

    def declare_params(self, next_token):
        hold_name = self.current_function_name + " " + next_token
        mem_address = self.find_addr()
        self.symbol_table[hold_name] = {"type": "function_variable", "address": mem_address}  # todo type ???

    def isglobal(self, next_token):
        for key in self.symbol_table:
            string_list = key.split()
            if len(string_list) == 1:
                if string_list[0] == next_token:
                    if self.symbol_table[next_token]["type"] == "function":
                        self.start_get_paramd()
                        self.calling_function.append(next_token)
                    self.semantic_stack.append(self.symbol_table[key]["address"])
                    return True
            # elif len(string_list) > 1:
            #     if string_list[1] == next_token:
            #         if self.symbol_table[next_token]["type"] == "function":
            #             self.start_get_paramd()
            #             self.calling_function = next_token
            #         self.semantic_stack.append(self.symbol_table[key]["address"])
            #         return True
        return False

    def pid(self, next_token):
        # if (self.declaring_function_header):
        #    if (self.declaring_first_function):
        #        self.hold_first_function_formain = len(self.program_block)
        #        self.declaring_first_function = False
        #        self.add_to_program_block('')
        #    if(next_token == "main"):
        #        self.program_block[self.hold_first_function_formain] = (f'(JP, {len(self.program_block)}, , )')
        #    self.symbol_table[next_token] = {"type": "function", "address" : 0 , "PB_address": len(self.program_block)}
        #    self.current_function_name = next_token
        # elif(self.declaring_function_parameter):
        #    hold_name = self.current_function_name + " " + next_token
        #    mem_address = self.find_addr()
        #    self.symbol_table[hold_name] = {"type": "function_variable", "address": mem_address}
        # elif (self.declaring_function_body):
        if next_token == "output":
            self.called_output = True
        else:

            hold_name = self.current_function_name + " " + next_token
            if list(self.symbol_table.keys()).count(hold_name) != 0:
                hold_dict = self.symbol_table[hold_name]
                self.semantic_stack.append(hold_dict["address"])
            elif self.isglobal(next_token):
                pass
            else:
                if self.current_function_name == "":
                    if self.is_defining_global:
                        hold_name = next_token
                        self.is_defining_global = False
                    else:
                        hold_name = "main " + next_token
                mem_address = self.find_addr()
                self.symbol_table[hold_name] = {"type": "function_variable", "address": mem_address}
                hold_dict = self.symbol_table[hold_name]
                self.semantic_stack.append(hold_dict["address"])

    # elif (self.passing_function_parameters):
    # else:

    def find_addr(self):
        t = self.cur_mem_addr
        self.cur_mem_addr += 4
        return t

    def get_temp(self):
        t = self.cur_temp
        self.cur_temp += 4
        return t

    def find_func_addr(self):
        t = self.func_memory_cur
        self.func_memory_cur += 4
        return t

    def generate(self, action_symbol, arg=None):
        # print('==== action sym', action_symbol)
        if not self.main_access_link:
            t = self.get_temp()
            self.main_access_link = t
        # print(f'{action_symbol[1:]}({arg})\r\t\t\t\t\t\t\t\t-> {str(self.semantic_stack)[:-1]}')
        self.action_symbols[action_symbol[1:]](arg)

    #    print(args)
    #    tmp = 0
    #    if len(args) == 3:
    #        void_type = args[0]
    #    else:
    #        tmp = 1
    #    lexeme = args[1 - tmp]
    #    line_no = args[2 - tmp]
    #    self.temp_id = lexeme
    #    if lexeme in self.symbol_table and self.symbol_table[lexeme]['type'] == 'func':
    #        self.callers.append(self.function)
    #        self.calling_function.append(lexeme)
    #        return
    #    if self.fun_declarating:
    #        if lexeme == 'output':
    #            self.calling_function.append(lexeme)
    #            return
    #        for key, value in self.symbol_table[self.function]["args"]:
    #            if key == lexeme:
    #                self.semantic_stack.append(value['addr'])
    #                return
    #        for key, value in self.symbol_table[self.function]["vars"].items():
    #            if key == lexeme:
    #                self.semantic_stack.append(value['addr'])
    #                return
    #        for key, val in self.memory.items():
    #            if key == lexeme:
    #                self.semantic_stack.append(val)
    #                return
    #        if void_type:
    #            err_msg = f"{line_no}: Semantic Error! Illegal type of void for {lexeme}."
    #            self.semantic_errors.append(err_msg)
    #            return
    #        t = self.find_func_addr()
    #        sym = {'addr': t, 'data_type': 'void' if void_type else 'int'}
    #        if self.arg_declarating:
    #            self.temp_args.append([lexeme, sym])
    #        else:
    #            if not 'vars' in self.symbol_table[self.function]:
    #                self.symbol_table[self.function]['vars'] = {}
    #            sym = {lexeme: sym}
    #            self.symbol_table[self.function]['vars'].update(sym)
    #        self.semantic_stack.append(t)
    #    else:
    #        for key, val in self.memory.items():
    #            if key == lexeme:
    #                self.semantic_stack.append(val)
    #                return
    #        if lexeme == 'output':
    #            self.calling_function.append(lexeme)
    #            return
    #        addr = self.find_addr()
    #        self.memory.update({lexeme: addr})
    #        sym = {'addr': addr, 'data_type': 'void' if void_type else 'int', 'args': {}, 'vars': {}}
    #        self.symbol_table.update({lexeme: sym})
    #        self.add_to_program_block(f'(ASSIGN, #0, {addr}, )')
    #        self.semantic_stack.append(addr)

    def add_element_to_arry(self):
        array_element = self.semantic_stack.pop()
        address_to_push = self.semantic_stack.pop()
        self.add_to_program_block(f'(ASSIGN, {array_element}, {address_to_push}, )')
        self.semantic_stack.append(self.find_addr())

    def var(self, args):
        void_type = args[0]
        lexeme = args[1]
        line_no = args[2]
        if void_type:
            err_msg = f"{line_no}: Semantic Error! Illegal type of void for {lexeme}."
            self.semantic_errors.append(err_msg)
            del self.symbol_table[lexeme]
            return
        if self.function:
            self.symbol_table[self.function]['vars'][lexeme].update({'type': 'var'})
        else:
            self.symbol_table[lexeme].update({'type': 'var'})

    def pnum(self, arg):
        num_addr = self.get_temp()
        self.add_to_program_block(f'(ASSIGN, #{arg}, {num_addr}, )')
        self.temp.update({num_addr: arg})
        self.semantic_stack.append(num_addr)

    def array_address(self, arg=None):
        index = self.semantic_stack.pop()
        var_addr = self.semantic_stack.pop()
        t = self.get_temp()
        self.add_to_program_block(f'(MULT, {index}, #4, {t})')
        self.add_to_program_block(f'(ADD, #{var_addr}, {t}, {t})')
        self.semantic_stack.append('@' + str(t))
        # self.temp.update({t: var_addr + 4*int(self.temp[index])})

    def assign(self, arg=None):
        pprint(self.symbol_table)
        op2 = self.semantic_stack.pop()
        op1 = self.semantic_stack.pop()
        self.add_to_program_block(f'(ASSIGN, {op2}, {op1}, )')
        # t = self.get_temp()

    # todo check delete self.semantic_stack.append(op1)
    # self.temp[t] = op1

    def whil(self, arg=None):
        i = len(self.program_block)
        self.program_block[self.semantic_stack[-1]] = f'(JPF, {self.semantic_stack[-2]}, {i + 1}, )'
        self.add_to_program_block(f'(JP, {self.semantic_stack[-3] + 1}, , )')
        # self.add_to_program_block('')
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.break_stack.pop()

    def add(self, arg=None):
        op1 = self.semantic_stack.pop()
        operation = self.semantic_stack.pop()
        op2 = self.semantic_stack.pop()
        t = self.get_temp()
        self.semantic_stack.append(t)
        if operation == '+':
            self.add_to_program_block(f'(ADD, {op1}, {op2}, {t})')
        else:
            self.add_to_program_block(f'(SUB, {op2}, {op1}, {t})')

    def mult(self, arg=None):
        op1 = self.semantic_stack.pop()
        op2 = self.semantic_stack.pop()
        t = self.get_temp()
        self.semantic_stack.append(t)
        self.add_to_program_block(f'(MULT, {op1}, {op2}, {t})')

    def save(self, arg=None):
        pb_ind = len(self.program_block)
        self.semantic_stack.append(pb_ind)
        self.add_to_program_block('')

    def jpf(self, arg=None):  # todo#jpf_save_save
        pb_ind = self.semantic_stack.pop()
        if_exp = self.semantic_stack.pop()
        i = len(self.program_block)
        # print(self.program_block)

        self.program_block[pb_ind] = f'(JPF, {if_exp}, {i}, )'

    # self.semantic_stack.append(i)
    # self.add_to_program_block('')
    def jpf_if(self, arg=None):
        pb_ind = self.semantic_stack.pop()
        if_exp = self.semantic_stack.pop()
        i = len(self.program_block)
        # print(self.program_block)

        self.program_block[pb_ind] = f'(JPF, {if_exp}, {i + 1}, )'
        self.semantic_stack.append(i)

    def jp(self, arg=None):
        pb_ind = self.semantic_stack.pop()
        i = len(self.program_block)
        self.program_block[pb_ind] = f'(JP, {i}, , )'

    def label(self, arg=None):
        self.break_stack.append('while')  # todo why?????
        pb_ind = len(self.program_block) - 1
        self.semantic_stack.append(pb_ind)

    def relop(self, arg=None):
        op_2 = self.semantic_stack.pop()
        operand = self.semantic_stack.pop()
        op_1 = self.semantic_stack.pop()
        t = self.get_temp()
        self.semantic_stack.append(t)
        if operand == '==':
            self.add_to_program_block(f'(EQ, {op_1}, {op_2}, {t})')
        elif operand == '<':
            self.add_to_program_block(f'(LT, {op_1}, {op_2}, {t})')

    def relop_sign(self, arg):
        self.semantic_stack.append(arg)

    def sign(self, arg):
        self.semantic_stack.append(arg)

    def signed_num(self, arg=None):
        n = self.semantic_stack.pop()
        sign = self.semantic_stack.pop()
        if self.temp.__contains__(n):
            number = int(self.temp[n])
            if sign == '-':
                self.pnum(-number)
            else:
                self.pnum(number)
        else:
            if self.fun_declarating:
                for key, value in self.symbol_table[self.function]["args"]:
                    if value['addr'] == n:
                        number = value['addr']
                        t = self.get_temp()
                        self.semantic_stack.append(t)
                        if sign == '-':
                            self.add_to_program_block(f'(MULT, {number}, #-1, {t})')
                        else:
                            self.add_to_program_block(f'(MULT, {number}, #1, {t})')
                        return
                for key, value in self.symbol_table[self.function]["vars"].items():
                    if value['addr'] == n:
                        number = value['addr']
                        t = self.get_temp()
                        self.semantic_stack.append(t)
                        if sign == '-':
                            self.add_to_program_block(f'(MULT, {number}, #-1, {t})')
                        else:
                            self.add_to_program_block(f'(MULT, {number}, #1, {t})')
                        return
                for key, val in self.memory.items():
                    if value['addr'] == n:
                        number = value['addr']
                        t = self.get_temp()
                        self.semantic_stack.append(t)
                        if sign == '-':
                            self.add_to_program_block(f'(MULT, {number}, #-1, {t})')
                        else:
                            self.add_to_program_block(f'(MULT, {number}, #1, {t})')
                        return
            else:
                for key, val in self.memory.items():
                    if val == n:
                        number = val
                        t = self.get_temp()
                        self.semantic_stack.append(t)
                        if sign == '-':
                            self.add_to_program_block(f'(MULT, {number}, #-1, {t})')
                        else:
                            self.add_to_program_block(f'(MULT, {number}, #1, {t})')

    def save_program_block(self):
        with open('output.txt', 'w') as output:
            for i, block in enumerate(self.program_block):
                output.write(f'{i}\t{block}\n')

    def pop(self, arg=None):
        self.semantic_stack.pop()

    def output(self, arg=None):
        if self.called_output:
            to_print = self.semantic_stack.pop()
            self.add_to_program_block(f'(PRINT, {to_print}, , )')
            self.semantic_stack.append(None)
            self.called_output = False

    def save_arr(self, args):
        void_type = args[0]
        lexeme = args[1]
        size = args[2]
        line_no = args[3]
        index = self.semantic_stack.pop()
        if len(self.calling_function) > 0:
            self.symbol_table[self.function]['vars'][lexeme].update({'type': 'arr'})
            for i in range(1, int(self.temp[index])):
                self.add_to_program_block(f'(ASSIGN, #0, {self.func_memory_cur}, )')
                self.func_memory_cur += 4
        else:
            self.symbol_table[lexeme].update({'type': 'arr'})
            for i in range(1, int(self.temp[index])):
                self.add_to_program_block(f'(ASSIGN, #0, {self.cur_mem_addr}, )')
                self.cur_mem_addr += 4
        if void_type:
            err_msg = f"{line_no}: Semantic Error! Illegal type of void for {lexeme}."
            self.semantic_errors.append(err_msg)
            del self.symbol_table[lexeme]
            return

    def tmp_save(self, arg=None):
        self.break_stack.append('switch')
        # print('break stacke now', self.break_stack)
        i = len(self.program_block)
        self.add_to_program_block(f'(JP, {i + 2}, , )')
        self.add_to_program_block('')
        self.semantic_stack.append(i + 1)

    def cmp_save(self, arg=None):
        t = self.get_temp()
        op1 = self.semantic_stack.pop()
        op2 = self.semantic_stack[-1]
        self.add_to_program_block(f'(EQ, {op1}, {op2}, {t})')
        self.semantic_stack.append(t)
        self.add_to_program_block('')
        i = len(self.program_block)
        self.semantic_stack.append(i - 1)

    def jp_break(self, line_no):
        # print('now we are in break ~~~~~~~~', self.break_stack)
        if len(self.break_stack) == 0:
            err_msg = f"{line_no}: Semantic Error! No 'while' or 'switch' found for 'break'"
            self.semantic_errors.append(err_msg)
        break_top = self.break_stack[-1]
        if break_top == 'switch':
            self.add_to_program_block(f'(JP, {self.semantic_stack[-4]}, , )')
        else:  # todo here for break in while loops
            self.add_to_program_block(f'(JP, {self.semantic_stack[-2]}, , )')

    def jpf_switch(self, arg=None):
        ind = self.semantic_stack[-1]
        i = len(self.program_block)
        self.program_block[ind] = f'(JPF, {self.semantic_stack[-2]}, {i} , )'
        self.semantic_stack.pop()
        self.semantic_stack.pop()

    def jp_switch(self, arg=None):
        i = len(self.program_block)
        ind = self.semantic_stack[-2]
        self.program_block[ind] = f'(JP, {i}, , )'
        self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.break_stack.pop()

    def function_call(self, arg):
        # print('~~~~~~', self.calling_function)
        if self.calling_function[-1] == 'output':
            self.output()
            return
        address = self.symbol_table[self.calling_function[-1]]['addr']
        return_address = self.symbol_table[self.calling_function[-1]]['return_address']
        self.add_to_program_block(f'(ASSIGN, #{len(self.program_block) + 2}, {return_address}, )')
        self.add_to_program_block(f'(JP, {address}, , )')
        if self.function_arg_number != len(self.symbol_table[self.calling_function[-1]]['args']):
            err_msg = f"{arg}: semantic error! Mismatch in numbers of arguments of {self.calling_function[-1]}"
            self.semantic_errors.append(err_msg)
            return
        if self.symbol_table[self.calling_function[-1]]['data_type'] == 'void':
            self.semantic_stack.append(None)
        else:
            return_value = self.symbol_table[self.calling_function[-1]]['return_value']
            self.semantic_stack.append(return_value)
        self.function_arg_number = 0
        self.calling_function.pop()
        self.function = self.callers.pop()

    def arg(self, arg=None):
        if not self.function or ((not self.callers or self.callers[-1] != 'main') and self.fun_declarating):
            return
        st = self.symbol_table[self.calling_function[-1]]
        if len(st["args"]) == self.function_arg_number:
            err_msg = f"{arg}: semantic error! Mismatch in numbers of arguments of {self.calling_function[-1]}"
            self.semantic_errors.append(err_msg)
            return
        value_address = self.semantic_stack.pop()
        address = st['args'][self.function_arg_number][1]['addr']
        self.add_to_program_block(f'(ASSIGN, {value_address}, {address}, )')
        self.function_arg_number += 1

    def arg_declaration(self, arg):
        lexeme = arg
        self.arg_declarating = True
        self.fun_declarating = True
        self.function = self.temp_id
        if self.function != 'main':
            self.semantic_stack.append(len(self.program_block))
            self.program_block.append(None)
        t = self.find_func_addr()
        self.symbol_table[self.function].update({'return_value': t})
        t = self.find_func_addr()
        self.symbol_table[self.function].update({'return_address': t})

    def fun_declaration(self, arg):
        lexeme = arg
        if not self.function:
            return
        self.symbol_table[lexeme].update({'type': 'func'})

    def fun_declaration_end(self, arg=None):
        if not self.function:
            return
        self.fun_declarating = False
        address = self.symbol_table[self.function]['return_address']
        self.add_to_program_block(f'(JP, @{address}, , )')
        if self.function != 'main':
            st = self.semantic_stack.pop()
            self.program_block[st] = f'(JP, {len(self.program_block)}, , )'
        self.symbol_table[self.function].update({'type': 'func'})
        self.function = None

    def param_arr(self, arg=None):
        self.temp_args[-1][-1].update({'type': 'arr'})
        if self.arg_declarating:
            self.semantic_stack.pop()

    def param_var(self, arg=None):
        self.temp_args[-1][-1].update({'type': 'var'})
        if self.arg_declarating:
            self.semantic_stack.pop()

    def fun_declarated(self, args):
        if not self.function:
            return
        self.symbol_table[self.function].update({'args': self.temp_args, 'addr': len(self.program_block)})
        self.arg_declarating = False
        self.temp_args = []

    def return_stmt(self, arg=None):
        if self.symbol_table[self.function]['data_type'] == 'void':
            return_address = self.symbol_table[self.function]['return_address']
            self.add_to_program_block(f'(JP, @{return_address}, , )')
            return
        t = self.symbol_table[self.function]['return_value']
        l = self.semantic_stack.pop()
        self.add_to_program_block(f'(ASSIGN, {l}, {t}, )')
        return_address = self.symbol_table[self.function]['return_address']
        self.add_to_program_block(f'(JP, @{return_address}, , )')

    def add_to_program_block(self, str):
        # print('------------------->>', str, 'added.')
        self.program_block.append(str)

# arg type check


# temp_args = [
#     [arg, {'addr': 2, 'data_type': 'void/int', 'type': 'var/arr'}],
#     [arg, {'addr': 2, 'data_type': 'void/int', 'type': 'var/arr'}],
# ]

# test  1: 1 func                            done
# test  2: 1 func                            done
# test  3: switch, 1 func                    done
# test  4: while break, inner func
# test  5: array argument, 1 func
# test  6: 1 func                            done
# test  7: switch, 1 func                    done
# test  8: 1 func, global arr used in func   done
# test  9: inner func, array argument
# test 10: while break, inner func
