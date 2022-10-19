# Mohammad Javad Maheronnaghsh 99105691
# Parsa Sharifi 99101762


def read_input_file_function(lines):
    input_file = open("input.txt", "r")

    while True:
        line = input_file.readline()
        if line == '':
            break
        line = line.replace("\n", "")

        lines.append(line)


class Scanner:
    def __init__(self):
        self.bool_continue_get_next = True
        self.lines = []
        read_input_file_function(self.lines)
        self.allTokens = []
        for i in range(len(self.lines)):
            array = []
            self.allTokens.append(array)
        self.allErrors = []
        for i in range(len(self.lines)):
            self.allErrors.append([])
        self.allKeyword = ["break", "continue", "def", "else", "if", "return", "while"]
        self.allId = []
        self.allSymbols = [";", ":", ",", "[", "]", "(", ")", "+", "-", "*", "=", "<", "==", "**"]
        # self.allComments = {}
       # self.counter_for_phase3 = 0

        self.severalLineComment = False
        self.oneLineComment = False
        self.found_id_error = False
        self.found_number_error = False
        self.counter = 0
        self.lineNumber = 0
        self.scannedUntilNow = ""
        self.start_unclosed_comment = 0

    def get_next_token(self):
        if self.lineNumber >= len(self.lines):
            self.bool_continue_get_next = False
            #return tuple("$" , "$")
            return
        elif self.counter >= len(self.lines[self.lineNumber]):
            self.found_number_error = False
            self.found_id_error = False
            if self.oneLineComment:
                # self.allComments[self.lineNumber + 1] = self.scannedUntilNow
                self.oneLineComment = False
            # multiline comment TODO
            self.scannedUntilNow = ""
            self.lineNumber += 1
            self.counter = 0
            if self.lineNumber >= len(self.lines):
                self.bool_continue_get_next = False
                #return tuple("$", "$")
                return
        bool_continue = True
        while bool_continue:
            is_end = True
            while is_end:

                if self.lineNumber >= len(self.lines):
                    self.bool_continue_get_next = False
                    #return tuple("$", "$")
                    return
                if self.counter >= len(self.lines[self.lineNumber]):
                    self.found_number_error = False
                    self.found_id_error = False
                    self.oneLineComment = False
                    self.counter = 0
                    self.lineNumber += 1
                else:
                    is_end = False

            now_character = self.lines[self.lineNumber][self.counter]
            bool_end_of_line = True
            lookahead_character = ""
            if self.counter < len(self.lines[self.lineNumber]) - 1:
                lookahead_character = self.lines[self.lineNumber][self.counter + 1]
                bool_end_of_line = False
            if self.severalLineComment:
                if now_character == "*" and lookahead_character == "/":
                    self.severalLineComment = False
                    self.scannedUntilNow = ""
                    self.counter += 1
                else:
                    self.scannedUntilNow += now_character
            elif now_character == "#" or self.oneLineComment:
                self.oneLineComment = True
                pass


            elif (not self.severalLineComment) and now_character == "*" and lookahead_character == "/":
                self.counter += 1
                tuple_ = ("*/", "Unmatched comment")
                self.allErrors[self.lineNumber].append(tuple_)
            ## if we are at the end of the line
            elif now_character == "/" and lookahead_character == "*":
                self.severalLineComment = True
                self.start_unclosed_comment = self.lineNumber
                self.counter += 1
            elif bool_end_of_line:

                self.scannedUntilNow += now_character
                if self.found_id_error:
                    # new added
                    tuple_ = (self.scannedUntilNow, "Invalid input")
                    self.allErrors[self.lineNumber].append(tuple_)
                    self.scannedUntilNow = ""
                    self.found_id_error = False
                elif self.found_number_error:
                    tuple_ = (self.scannedUntilNow, "Invalid number")
                    self.allErrors[self.lineNumber].append(tuple_)
                    self.scannedUntilNow = ""
                    self.found_number_error = False
                elif self.scannedUntilNow == " " or self.scannedUntilNow == '\t' or \
                        self.scannedUntilNow == '\n' or self.scannedUntilNow == '\r' or \
                        self.scannedUntilNow == '\v' or self.scannedUntilNow == "\f":
                    self.scannedUntilNow = ""
                elif self.scannedUntilNow in self.allKeyword:
                    tuple_ = ("KEYWORD", self.scannedUntilNow)
                    self.allTokens[self.lineNumber].append(tuple_)
                    bool_continue = False
                    self.scannedUntilNow = ""
                    #return tuple_
                elif self.scannedUntilNow in self.allId:
                    tuple_ = ("ID", self.scannedUntilNow)
                    self.allTokens[self.lineNumber].append(tuple_)
                    bool_continue = False
                    self.scannedUntilNow = ""
                   # return tuple_
                elif self.scannedUntilNow in self.allSymbols:
                    tuple_ = ("SYMBOL", self.scannedUntilNow)
                    self.allTokens[self.lineNumber].append(tuple_)
                    bool_continue = False
                    self.scannedUntilNow = ""
                    #return tuple_
                elif self.scannedUntilNow.isnumeric():
                    tuple_ = ("NUMBER", self.scannedUntilNow)
                    self.allTokens[self.lineNumber].append(tuple_)
                    bool_continue = False
                    self.scannedUntilNow = ""
                   # return tuple_
                elif 48 <= ord(now_character) <= 57:
                    if 65 <= ord(self.scannedUntilNow[0]) <= 90 or 97 <= ord(self.scannedUntilNow[0]) <= 122:
                        self.allId.append(self.scannedUntilNow)
                        tuple_ = ("ID", self.scannedUntilNow)
                        self.allTokens[self.lineNumber].append(tuple_)
                        bool_continue = False
                        self.scannedUntilNow = ""
                       # return tuple_
                    else:
                        tuple_ = (self.scannedUntilNow, "Invalid number")
                        self.allErrors[self.lineNumber].append(tuple_)
                        self.lineNumber += 1
                        self.counter = 0
                        self.scannedUntilNow = ""
                        self.found_number_error = False
                        self.found_id_error = False
                        self.oneLineComment = False
                elif 65 <= ord(self.scannedUntilNow[0]) <= 90 or 97 <= ord(self.scannedUntilNow[0]) <= 122:
                    # new added
                    self.allId.append(self.scannedUntilNow)
                    tuple_ = ("ID", self.scannedUntilNow)
                    self.allTokens[self.lineNumber].append(tuple_)
                    bool_continue = False
                    self.scannedUntilNow = ""
                    #return tuple_
                else:
                    tuple_ = (self.scannedUntilNow, "Invalid input")
                    self.allErrors[self.lineNumber].append(tuple_)
                    self.lineNumber += 1
                    self.counter = 0
                    self.scannedUntilNow = ""
                    self.found_number_error = False
                    self.found_id_error = False
                    self.oneLineComment = False
            ## if we are in the middle of the line
            else:
                self.scannedUntilNow += now_character
                if self.scannedUntilNow == " " or self.scannedUntilNow == '\t' or \
                        self.scannedUntilNow == '\n' or self.scannedUntilNow == '\r' or \
                        self.scannedUntilNow == '\v' or self.scannedUntilNow == "\f":
                    self.scannedUntilNow = ""
                    pass
                elif self.scannedUntilNow.isnumeric():
                    if lookahead_character == " " or lookahead_character == '\t' or \
                            lookahead_character == '\n' or lookahead_character == '\r' or \
                            lookahead_character == '\v' or lookahead_character == "\f":
                        tuple_ = ("NUMBER", self.scannedUntilNow)
                        self.allTokens[self.lineNumber].append(tuple_)
                        bool_continue = False
                        self.scannedUntilNow = ""
                        #return tuple_
                    elif 48 <= ord(lookahead_character) <= 57 or lookahead_character == ".":
                        pass
                    elif (
                            lookahead_character in self.allSymbols) or lookahead_character == '/' or lookahead_character == "#":
                        tuple_ = ("NUMBER", self.scannedUntilNow)
                        self.allTokens[self.lineNumber].append(tuple_)
                        bool_continue = False
                        self.scannedUntilNow = ""
                       # return tuple_
                    # elif 65 <= ord(lookahead_character) <= 90 or 97 <= ord(lookahead_character) <= 122:
                    # new added
                    else:
                        self.found_number_error = True

                elif self.scannedUntilNow in self.allSymbols:
                    if self.scannedUntilNow == "*" or self.scannedUntilNow == "=":
                        if lookahead_character == self.scannedUntilNow:
                            pass
                        elif 65 <= ord(lookahead_character) <= 90 or 97 <= ord(lookahead_character) <= 122 or 48 <= ord(
                                lookahead_character) <= 57 \
                                or lookahead_character == " " or lookahead_character == '\t' or \
                                lookahead_character == '\n' or lookahead_character == '\r' or \
                                lookahead_character == '\v' or lookahead_character == "\f" \
                                or lookahead_character in self.allSymbols or lookahead_character == "#":
                            tuple_ = ("SYMBOL", self.scannedUntilNow)
                            self.allTokens[self.lineNumber].append(tuple_)
                            bool_continue = False
                            self.scannedUntilNow = ""
                           # return tuple_
                    else:
                        tuple_ = ("SYMBOL", self.scannedUntilNow)
                        self.allTokens[self.lineNumber].append(tuple_)
                        bool_continue = False
                        self.scannedUntilNow = ""
                       # return tuple_
                elif self.scannedUntilNow in self.allKeyword:
                    if lookahead_character == " " or lookahead_character == '\t' or \
                            lookahead_character == '\n' or lookahead_character == '\r' or \
                            lookahead_character == '\v' or lookahead_character == "\f" \
                            or lookahead_character in self.allSymbols or lookahead_character == '/':
                        tuple_ = ("KEYWORD", self.scannedUntilNow)
                        self.allTokens[self.lineNumber].append(tuple_)
                        bool_continue = False
                        self.scannedUntilNow = ""
                        #return tuple_
                elif 65 <= ord(self.scannedUntilNow[0]) <= 90 or 97 <= ord(self.scannedUntilNow[0]) <= 122:
                    if self.found_id_error:
                        # if lookahead_character == " " or lookahead_character == '\t' or \
                        #         lookahead_character == '\n' or lookahead_character == '\r' or \
                        #         lookahead_character == '\v' or lookahead_character == "\f" \
                        #         or lookahead_character in self.allSymbols \
                        #         or 65 <= ord(lookahead_character) <= 122 or 48 <= ord(lookahead_character) <= 57:
                        tuple_ = (self.scannedUntilNow, "Invalid input")
                        self.allErrors[self.lineNumber].append(tuple_)
                        self.scannedUntilNow = ""
                        self.found_id_error = False
                        # else:
                        #     pass
                    else:
                        if lookahead_character == " " or lookahead_character == '\t' or \
                                lookahead_character == '\n' or lookahead_character == '\r' or \
                                lookahead_character == '\v' or lookahead_character == "\f" \
                                or lookahead_character in self.allSymbols or lookahead_character == "#":
                            self.allId.append(self.scannedUntilNow)
                            tuple_ = ("ID", self.scannedUntilNow)
                            self.allTokens[self.lineNumber].append(tuple_)
                            bool_continue = False
                            self.scannedUntilNow = ""
                          #  return tuple_
                        elif 65 <= ord(lookahead_character) <= 90 or 97 <= ord(lookahead_character) <= 122 or 48 <= ord(
                                lookahead_character) <= 57:
                            pass
                        else:
                            self.found_id_error = True
                elif 48 <= ord(self.scannedUntilNow[0]) <= 57:
                    if self.found_number_error:
                        # if 65 <= ord(lookahead_character) <= 90 or 97 <= ord(lookahead_character) <= 122 or 48 <= ord(
                        #         lookahead_character) <= 57 \
                        #         or lookahead_character == " " or lookahead_character == '\t' or \
                        #         lookahead_character == '\n' or lookahead_character == '\r' or \
                        #         lookahead_character == '\v' or lookahead_character == "\f" \
                        #         or lookahead_character in self.allSymbols or lookahead_character == "#":
                        tuple_ = (self.scannedUntilNow, "Invalid number")
                        self.allErrors[self.lineNumber].append(tuple_)
                        self.scannedUntilNow = ""
                        self.found_number_error = False
                        # else:
                        #     pass
                    else:
                        if lookahead_character == " " or lookahead_character == '\t' or \
                                lookahead_character == '\n' or lookahead_character == '\r' or \
                                lookahead_character == '\v' or lookahead_character == "\f" \
                                or lookahead_character in self.allSymbols:
                            tuple_ = ("NUMBER", self.scannedUntilNow)
                            self.allTokens[self.lineNumber].append(tuple_)
                            bool_continue = False
                            self.scannedUntilNow = ""
                           # return tuple_
                        elif 48 <= ord(lookahead_character) <= 57:
                            pass
                        else:
                            self.found_number_error = True
                # definitely error
                else:
                    # if 65 <= ord(lookahead_character) <= 90 or 97 <= ord(lookahead_character) <= 122 or 48 <= ord(lookahead_character) <= 57 \
                    #         or lookahead_character == " " or lookahead_character == '\t' or \
                    #         lookahead_character == '\n' or lookahead_character == '\r' or \
                    #         lookahead_character == '\v' or lookahead_character == "\f" \
                    #         or lookahead_character in self.allSymbols or lookahead_character == "#":
                    tuple_ = (self.scannedUntilNow, "Invalid input")
                    self.allErrors[self.lineNumber].append(tuple_)
                    self.scannedUntilNow = ""
            self.counter += 1

    def save(self):
        ## save symbol table
        allId_unique = []
        for i in self.allId:
            if i not in allId_unique:
                allId_unique.append(i)
        allId_unique = self.allKeyword + allId_unique
        with open('symbol_table.txt', "w+") as f:
            last_answer = ""
            for i in range(len(allId_unique)):
                last_answer += str(i + 1)
                last_answer += "."
                last_answer += "\t"
                last_answer += allId_unique[i]
                last_answer += "\n"

            f.write(last_answer)

        ## save errors

        with open('lexical_errors.txt', "w+") as f:
            answer_error = ""
            for i in range(len(self.allErrors)):
                if len(self.allErrors[i]) != 0:
                    answer_error += str(i + 1)
                    answer_error += "."
                    answer_error += "\t"
                    for j in range(len(self.allErrors[i])):
                        answer_error += "("
                        # x = str(self.allErrors[i][j][0]).replace("'", "")
                        x = str(self.allErrors[i][j][0])
                        answer_error += x
                        answer_error += ", "
                        # y = str(self.allErrors[i][j][1]).replace("'", "")
                        y = str(self.allErrors[i][j][1])
                        answer_error += y
                        if j == len(self.allErrors[i]) - 1:
                            answer_error += ")"
                        else:
                            answer_error += ") "
                    answer_error += "\n"
            if answer_error == "":
                answer_error = "There is no lexical error."
            f.write(answer_error)

        ## save tokens

        with open('tokens.txt', "w+") as f:
            answer_ = ""
            for i in range(len(self.allTokens)):
                if len(self.allTokens[i]) != 0:
                    answer_ += str(i + 1)
                    answer_ += "."
                    answer_ += "\t"
                    for j in range(len(self.allTokens[i])):
                        answer_ += "("
                        # x = str(self.allTokens[i][j][0]).replace("'", "")
                        x = str(self.allTokens[i][j][0])
                        answer_ += x
                        answer_ += ", "
                        # y = str(self.allTokens[i][j][1]).replace("'", "")
                        y = str(self.allTokens[i][j][1])
                        answer_ += y
                        if j == len(self.allTokens[i]) - 1:
                            answer_ += ")"
                        else:
                            answer_ += ") "
                    answer_ += "\n"
            f.write(answer_)

    def checkUnclosedComment(self):
        if self.severalLineComment:
            str = self.scannedUntilNow[:min(8, len(self.scannedUntilNow))]
            if len(self.scannedUntilNow) > 8:
                str += "..."
            tuple_ = ("/*" + str, "Unclosed comment")
            self.allErrors[self.start_unclosed_comment].append(tuple_)


#x = Scanner()
#while bool_continue_get_next:
#    x.get_next_token()
#x.checkUnclosedComment()
#x.save()
