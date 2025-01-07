class Parser:
    @staticmethod
    def Parse(path):
        res = {}
        file = open(path, 'r')
        table = file.readlines()
        file.close()
        val_type = 'auto'
        for i in table:
            if i[0] == '#': continue
            if i[0] == ':':
                val_type = i[1:]
                continue

            i = (i[:-1]).strip()

            if i[0] == '[' and i[-1] == ']': continue
            eq_ind = i.find("=")
            if eq_ind == -1: continue
            key = i[:eq_ind]
            

            val = i[eq_ind + 1:]

            try:
                if val_type == 'auto':
                    if val[0] == '"' or val[0] == "'":
                        val = val[1:-1]
                    elif '.' in val:
                        val = float(val)
                    else:
                        val = int(val)
                elif val_type == 'int':
                    val = int(val)
                elif val_type == 'float':
                    val = float(val)
                elif val_type == 'str':
                    val = str(val)
                elif val_type == 'bool':
                    val = bool(val)
                val_type = 'auto'
            except: continue
            
            is_not_array = True
            if eq_ind > 6:
                if key[-2] == '[' and key[-1] == ']':
                    is_not_array = False
                    key = key[:-2]
                    if key in res:
                        res[key].append(val)
                    else:
                        res[key] = [val]

            if is_not_array:
                res[key] = val

        return res
