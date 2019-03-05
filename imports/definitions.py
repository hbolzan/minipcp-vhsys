from imports import mappings
from db.db import exec_sql_with_result
from vhsys import vhsys_clientes, vhsys_produtos
from vhsys.vhsys_pedidos import pedidos_all, pedidos_since, pedidos_by_status, pedidos_with_items


SOURCE_TYPE__ALL = "all"
SOURCE_TYPE__SINCE = "since"
SOURCE_TYPE__BY_ID = "by_id"


def clientes(source_type, source_param=None):
    return {
        "source": {
            SOURCE_TYPE__ALL: vhsys_clientes.clientes_all,
            SOURCE_TYPE__SINCE: lambda: vhsys_clientes.clientes_updated_since(source_param),
            SOURCE_TYPE__BY_ID: lambda: vhsys_clientes.cliente_by_id(source_param),
        }.get(source_type),
        "target": "view_vhsys_nfe_clientes",
        "check_attrs": ["id", "id_cliente"],
        "mapping": mappings.clientes(),
        "description": "clientes",
    }


def produtos(source_type, source_param=None):
    return {
        "source": {
            SOURCE_TYPE__ALL: vhsys_produtos.produtos_all,
            SOURCE_TYPE__SINCE: lambda: vhsys_produtos.produtos_updated_since(source_param),
            SOURCE_TYPE__BY_ID: lambda: vhsys_produtos.produto_by_id(source_param),
        }.get(source_type),
        "target": "produtos",
        "check_attrs": ["codigonfe", "id_produto"],
        "check_transform_fn": str,
        "mapping": mappings.produtos(),
        "description": "produtos",
    }


def pedidos(source_type, source_param=None):
    return {
        "source": {
            SOURCE_TYPE__ALL: lambda: pedidos_with_items(pedidos_all()),
            SOURCE_TYPE__SINCE: lambda: pedidos_with_items(pedidos_since(source_param)),
            # SOURCE_TYPE__BY_ID: lambda: vhsys_pedidos.pedido_by_id(source_param),
        }.get(source_type),
        "target": "vendas_pedidos",
        "check_attrs": ["id", "id_ped"],
        "abort_update_condition": ["situacao", lambda s: s != "A"],
        "mapping": mappings.pedidos(),
        "description": "pedidos de venda",
        "children_defs": [{"def_fn": pedidos_itens, "def_args": ["id_ped", "items", all_minipcp_produtos()]}]
    }


def pedidos_itens(id_pedido, pedido_items, minipcp_produtos):
    return {
        "source": lambda: pedido_items,
        "target": "vendas_pedidos_itens",
        "mapping": mappings.pedidos_itens(minipcp_produtos),
        "description": "itens de pedido de venda",
        "init_statement": "delete from vendas_pedidos_itens where pedido = {};".format(id_pedido),
    }


def all_minipcp_produtos():
    produtos = [None]
    def _all_minipcp_produtos(db_conn, *args, **kwargs):
        if produtos[0] is None:
            produtos[0] = exec_sql_with_result(db_conn, "select * from produtos order by tipo, codigo")
        return produtos[0]
    return _all_minipcp_produtos
