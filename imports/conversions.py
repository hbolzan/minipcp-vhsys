def identity(x):
    return x


def identity_or_none(x):
    return None if not x else x


def tipo_de_pessoa(x):
    return "J" if x == "PJ" else "F"


def cnpj(x, tipo_pessoa):
    return x if tipo_pessoa == "PJ" else None


def cpf(x, tipo_pessoa):
    return None if tipo_pessoa == "PJ" else x


def fn_tipo_de_produto(tipos_mapping, tipo_default):
    return lambda x: tipos_mapping.get(x, tipo_default)


def constantly(x):
    return lambda n: x


def _or(x, y):
    return x or y


def strtimestamp_to_strdate(x):
    return None if not x else x.split(" ")[0]


def seq_generator():
    seq = [0]
    def generator(x):
        seq[0] += 1
        return seq[0]
    return generator


def find_and_get(items, attr, result_attr, convert_before_filter=lambda x: x):
    def _find_and_get(value):
        try:
            x = convert_before_filter(value)
            found = next(filter(lambda i: i.get(attr) == x, items))
            return found.get(result_attr)
        except StopIteration:
            return None
    return _find_and_get
