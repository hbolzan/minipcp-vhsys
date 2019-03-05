from .vhsys_requests import vhsys_get, vhsys_get_with_params, vhsys_get_since


BASE_ENDPOINT = "produtos"


def produto_by_id(produto_id):
    return vhsys_get(BASE_ENDPOINT + "/{produto_id}".format(produto_id=produto_id))


def produtos_all():
    return vhsys_get(BASE_ENDPOINT, True)


def produto_by_descricao(descricao):
    return vhsys_get_with_params(BASE_ENDPOINT, "desc_produto", descricao)


def produto_by_codigo(codigo):
    return vhsys_get_with_params(BASE_ENDPOINT, "cod_produto", codigo)


# since must be a date formatted as "YYYY-MM-DD"
def produtos_updated_since(since):
    return vhsys_get_since(BASE_ENDPOINT, since, [], True)
