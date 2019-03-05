from .vhsys_requests import vhsys_get, vhsys_get_with_params, vhsys_get_since


BASE_ENDPOINT = "clientes"


def cliente_by_id(cliente_id):
    return vhsys_get(BASE_ENDPOINT + "/{cliente_id}".format(cliente_id=cliente_id))


def clientes_all():
    return vhsys_get(BASE_ENDPOINT, True)


def cliente_by_cnpj(cnpj):
    return vhsys_get_with_params(BASE_ENDPOINT, "cnpj_cliente", cnpj)


# since must be a date formatted as "YYYY-MM-DD"
def clientes_updated_since(since):
    return vhsys_get_since(BASE_ENDPOINT, since, [], True)
