#from integration.loghandler import Loghandler


def bool(n):
    if n == True: return True
    if n == False: return False
    if type(n) is str:
        n_lc = n.lower()
        if n_lc == 'true': return True
        if n_lc == 'false': return False
    return n

types = {'integer': int, 'int': int, 'float': float, 'string': str, 'str': str, 'boolean': bool, 'bool': bool, 'dictionary': None, 'dict' : None, 'array': None}
default = {'integer': 0, 'int': 0, 'float': 0.0, 'string': '', 'str': '', 'boolean': False, 'bool': False, 'dictionary': {}, 'dict' : {}, 'array': []}

constrains = {}
array_constrains = {}
 

def smartParseTable(context, path, parse_array = False, default_type = 'str'):
    #print(context)

    table = {}
    if parse_array:
        table = []
    expr = ''
    analyze = 0

    is_string = 0

    nest_level = 0
    intable_start = 0
    intable_end = 0
    is_expr_table = False
    is_expr_array = False
    is_expr_string = False

    allow_key_not_first = False

    exprno = 0
    key = None
    val = None
    func = None
    typeof = 'str'
    if default_type == 'str' or default_type in types:
        typeof = default_type
        func = types[default_type]
    else:
        default_type = 'str'
    bottomclamp = None
    topclamp = None

    size_bottomclamp = None
    size_topclamp = None
    array_typeof = default_type

    l = len(context) + 1
    i = 0
    if context[0] == '{':
        i += 1
        l -= 1

    while i < l:
        if i + 1 != l:
            p = context[i]

            if is_string > 0: # String
                match p:
                    case '"': # "
                        if is_string == 1:
                            is_string = 0
                        elif nest_level == 0:
                            expr += '"'
                    case "'": # '
                        if is_string == 2:
                            is_string = 0
                        elif nest_level == 0:
                            expr += "'"
                    case _:
                        expr += p
            elif nest_level > 0: # Nested table/array
                match p:
                    case '{':
                        if is_expr_table:
                            nest_level += 1
                    case '}':
                        if is_expr_table:
                            nest_level -= 1
                            if nest_level == 0:
                                expr = context[intable_start:i]
                    case '[':
                        if is_expr_array:
                            nest_level += 1
                    case ']':
                        if is_expr_array:
                            nest_level -= 1
                            if nest_level == 0:
                                expr = context[intable_start:i]
            else: # Nothing of above, plain expression and no nested tables
                match p:
                    case ':':
                        analyze = 1 # Analyze 1: expression end
                    case ',':
                        analyze = 2 # Analyze 2: declaration end
                    case '"':
                        is_string = 1
                        is_expr_string = True
                    case "'":
                        is_string = 2
                        is_expr_string = True
                    case '{':
                        if not is_expr_array:
                            intable_start = i + 1
                            is_expr_table = True
                        if is_expr_table:
                            nest_level += 1
                    case '}':
                        if parse_array:
                            table.append("error: unexpected '}'")
                        else:
                            table["error"] = "unexpected '}'"
                        return table
                    case '[':
                        if expr != '': # If the first expression symbol is not '[', it will be interpreted as a type specification like 'int[]'
                            expr += '['
                        else:
                            if not is_expr_table:
                                intable_start = i + 1
                                is_expr_array = True
                            if is_expr_array:
                                nest_level += 1
                    case ']':
                        if '[' not in expr: #and not parse_array:
                            if parse_array:
                                table.append("error: unexpected ']'")
                            else:
                                table["error"] = "unexpected ']'"
                            return table
                    case ' ':
                        pass
                    case _:
                        expr += p
        else:
            analyze = 2 # Analyze 2: declaration end
        
        i += 1
        
        if analyze > 0:
            findarr = expr.find('[')

            # Allow skipping tokens until the expression is nothing else but a key.
            # Key condition is located in the very end,
            # which means that everything that is not normal text quoteless value
            # will hijack all branching from it.
            if key is None: 
                allow_key_not_first = True


            if not expr:
                pass
            elif is_expr_string:
                is_expr_string = False
                val = expr
            elif is_expr_table:
                if key is None:
                    allow_key_not_first = True

                is_expr_table = False
                typeof = 'dict'
                # TODO: We may omit first key check when we convert this into a serializer
                if not key and not parse_array:
                    table["error"] = "table key omitted"
                    return table
                else:
                    val = smartParseTable(expr, f"{path}:{key}")

            elif is_expr_array:
                is_expr_array = False
                if not key and not parse_array:
                    table["error"] = "array key omitted"
                    return table
                else:
                    intable = smartParseTable(expr, f"{path}:{key}", parse_array = True, default_type = array_typeof)
                    if typeof == 'array':
                        val += intable
                    else:
                        typeof = 'array'
                        val = intable
            elif expr[0] == '(' and not parse_array: # Expression is the bottom range llimit
                bottomclamp = expr[1:]
            elif expr[-1] == ')' and not parse_array: # Expression is the top range llimit
                topclamp = expr[:-1]
            elif expr in types or expr[:findarr] in types: # Expression is a type specification

                if findarr != -1: # Is an array
                    array_typeof = expr[:findarr]
                    if expr[-1] != ']':
                        size_bottomclamp = expr[findarr + 1:]
                    typeof = 'array'
                    func = types[array_typeof]
                    if val is None:
                        val = []
                    elif type(val) is not list:
                        val = [val]
                else: # Is not an array
                    typeof = expr
                    if expr == 'array':
                        if val is None:
                            val = []
                        elif type(val) is list or type(val) is dict:
                            val = [val]
                        else:
                            val = [[val]]

            elif expr[-1] == ']':
                size_topclamp = int(expr[:-1])
            elif (exprno == 0 or allow_key_not_first) and not parse_array: # Expression is a key
                key = expr
                allow_key_not_first = False
            else: # Expression is a value
                if typeof == 'array':
                    if func is not None:
                        try:
                            val.append(func(expr))
                        except Exception as ex:
                            val.append(default[array_typeof])
                            val.append(f"{type(ex).__name__}({ex})")
                else:
                    val = expr


            if analyze == 2:

                if key and exprno > 0 or parse_array:
                    try:
                        func = types[typeof]
                        if func is not None:

                            if val is None:
                                val = default[typeof]
                            else:
                                val = func(val)
                            
                            if not parse_array:
                                if bottomclamp:
                                    bottomclamp = func(bottomclamp)
                                if topclamp:
                                    topclamp = func(topclamp)

                                #print(topclamp, bottomclamp)
                                constrains[path + ':' + key] = (bottomclamp, topclamp)
                        elif val is None:
                            val = default[typeof]
                    except Exception as ex:
                        if parse_array:
                            table.append(f"{type(ex).__name__}({ex})")
                        else:
                            table[type(ex).__name__] = str(ex)
                        return table

                    if parse_array:
                        table.append(val)
                    else:
                        table[key] = val

            elif key is None:
                table["Error"] = f"missing key for value."
                return table


                exprno = 0
                key = None
                val = None
                typeof = default_type
                func = types[default_type]
                bottomclamp = None
                topclamp = None

                size_bottomclamp = None
                size_topclamp = None
                if not parse_array:
                    array_typeof = 'str'
            else:
                exprno += 1
            
            analyze = 0
            expr = ''
                


    return table

def ParseConfig(content):
    table = {}
    text = content.replace('\n', '').replace('\t', '').strip()

    ln = len(text)

    if ln < 2: return {"error": "missing config."}

    if text[0] == '{':
        if text[-1] != '}':
            return {"error": "Expected '}' at the end of the config."}

    table = smartParseTable(text, '')

    return table

#test
print(ParseConfig("{a : 3 : int, b : 6, 'tricks' : extrastr, [1, 2] : int[] : [3, 4] : wtf, info : {c : int : 5, b : string[] : hello : bye, ambig : \"string\"}, c : int[] : [2, 4, 3, 5]}"))
