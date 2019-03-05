from .vhsys_requests import vhsys_get, vhsys_get_with_params, vhsys_get_since


PEDIDOS_BASE_ENDPOINT = "pedidos"
ITENS_BASE_ENDPOINT = "pedidos/{pedido_id}/produtos"
STATUS_EM_ABERTO = "Em Aberto"
STATUS_EM_ANDAMENTO = "Em Andamento"
STATUS_ATENDIDO = "Atendido"
STATUS_CANCELADO = "Cancelado"
DEFAULT_PARAMS = [("status", STATUS_EM_ABERTO)]


# since must be a date formatted as "YYYY-MM-DD"
def pedidos_since(since):
    return vhsys_get_since(PEDIDOS_BASE_ENDPOINT, since, DEFAULT_PARAMS, True)


def pedidos_by_status(status, params=[]):
    return vhsys_get_with_params(PEDIDOS_BASE_ENDPOINT, [("status", status)] + params, True)


def pedidos_all():
    return vhsys_get_with_params(PEDIDOS_BASE_ENDPOINT, DEFAULT_PARAMS, True)


def pedidos_with_items(pedidos):
    if not pedidos:
        return pedidos
    if type(pedidos) == list:
        return [with_items(pedido) for pedido in pedidos]
    return with_items(pedidos)


def with_items(pedido):
    items = pedido_items(pedido.get("id_ped"))
    if not items:
        return pedido
    pedido["items"] = items
    return pedido


def pedido_items(pedido_id):
    return vhsys_get(ITENS_BASE_ENDPOINT.format(pedido_id=pedido_id))
