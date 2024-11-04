class Parser:
    @staticmethod
    def Parse(path):
        res = {}
        file = open(path, 'r')
        table = file.readlines()
        file.close()
        for i in table:
            i = (i[:-1]).strip()

            eq_ind = i.find("=")
            if eq_ind == -1: continue
            key = i[:eq_ind]
            

            val = i[eq_ind + 1:]

            if val[0] == '"' or val[0] == "'":
                val = val[1:-1]
            elif '.' in val:
                val = float(val)
            else:
                val = int(val)
            
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