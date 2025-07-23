
#from integration.loghandler import Loghandler

types = {'int': int, 'float': float, 'string': str, 'str': str, 'bool': bool, 'enum' : None, 'dict' : None, 'array': None}
default = {'int': 0, 'float': 0.0, 'string': '', 'str': '', 'bool': False, 'enum' : ["(Not Set)"], 'dict' : {}, 'array': []}

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

    exprno = 0
    key = None
    val = None
    typeof = default_type
    func = types[default_type]
    bottomclamp = None
    topclamp = None

    size_bottomclamp = None
    size_topclamp = None
    array_typeof = None

    l = len(context) + 1

    i = 0
    while i < l:
        if i + 1 != l:
            p = context[i]

            if nest_level > 0:
                match p: # nested table/array
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
            elif is_string > 0: # string and no nested tables
                match p:
                    case '"':
                        if is_string == 1:
                            is_string = 0
                        elif nest_level == 0:
                            expr += '"'
                    case "'":
                        if is_string == 2:
                            is_string = 0
                        elif nest_level == 0:
                            expr += "'"
                    case _:
                        expr += p
            else: #nothing of above, plain expression and no nested tables
                match p:
                    case ':':
                        analyze = 1
                    case ',':
                        analyze = 2
                    case '"':
                        is_string = 1
                    case "'":
                        is_string = 2
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
                        if expr != '': #array declaration are only allowed to start from the first symbol of expression, otherwise it is something like "int[]"
                            expr += '['
                        else:
                            if not is_expr_table:
                                intable_start = i + 1
                                is_expr_array = True
                            if is_expr_array:
                                nest_level += 1
                    case ']':
                        if is_expr_array:
                            if parse_array:
                                table.append("error: unexpected ']'")
                            else:
                                table["error"] = "unexpected ']'"
                            return table
                    case _:
                        expr += p
        else:
            analyze = 2
        
        i += 1
        

        if analyze > 0:
            findarr = expr.find('[')
            #print(expr) print token
            if not expr:
                pass
            elif exprno == 0 and not parse_array:
                key = expr
            elif is_expr_table:
                is_expr_table = False
                typeof = 'dict'
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

            elif expr[0] == '(' and not parse_array: # expression is the bottom range llimit
                bottomclamp = expr[1:]
            elif expr[-1] == ')' and not parse_array: # expression is the top range llimit
                topclamp = expr[:-1]
            elif expr in types or expr[:findarr] in types: # expression is a type specification

                if findarr != -1: # an array
                    array_typeof = expr[:findarr]
                    if expr[-1] != ']':
                        size_bottomclamp = expr[findarr + 1:]
                    typeof = 'array'
                    func = types[array_typeof]
                    if val is None:
                        val = []
                    else:
                        val = [val]
                else: # not an array
                    typeof = expr
                    if expr == 'enum' or expr == 'array':
                        if val is None:
                            val = []
                        else:
                            val = [val]

            elif expr[-1] == ']':
                size_topclamp = int(expr[:-1])
            else: # expression is a value
                if typeof == 'array':
                    if func is not None:
                        try:
                            val.append(func(expr))
                        except Exception as ex:
                            val.append(default[array_typeof])
                            val.append(f"error: {ex}")
                elif typeof == 'enum':
                    val.append(expr)
                else:
                    val = expr



            if analyze == 2:

                if exprno > 0 or parse_array:
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
                                constrains[path + ':' + key] = (bottomclamp, topclamp)
                        elif val is None:
                            val = default[typeof]
                    except Exception as ex:
                        if parse_array:
                            table.apend(f"error: {ex}")
                        else:
                            table['error'] = ex
                        return table

                    if parse_array:
                        table.append(val)
                    else:
                        table[key] = val


                exprno = 0
                key = None
                val = None
                typeof = default_type
                func = types[default_type]
                bottomclamp = None
                topclamp = None

                size_bottomclamp = None
                size_topclamp = None
                array_typeof = None
            else:
                exprno += 1
            
            analyze = 0
            expr = ''
                


    return table

def ParseConfig(content):
    table = {}
    text = content.replace('\n', '').replace('\t', '').replace(' ', '')

    if len(text) == 0: return {"error": "missing config."}

    if text[0] + text[-1] == '{}': text = text[1:-1]

    if text[-1] == ',': return {"error": "Expected '}' at the end of the table, got ',' instead."}

    table = smartParseTable(text, '')


    return table

#test
#print(ParseConfig("{a : 3 : int, b : 6, info : {c : int : 5, b : enum : hello : bye}, c : int[] : [2, 4, 3, 5]}"))
