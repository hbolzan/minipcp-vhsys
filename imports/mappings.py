from imports import conversions
from settings import DEFAULT_PRODUTO_TIPO, PRODUTOS_TIPOS, DEFAULT_PRODUTO_UNIDADE


def clientes():
    return {
        "id": ["id_cliente", conversions.identity],
        "tipo_de_pessoa": ["tipo_pessoa", conversions.tipo_de_pessoa],
        "cnpj": ["cnpj_cliente", conversions.cnpj, ["tipo_pessoa"]],
        "cpf": ["cnpj_cliente", conversions.cpf, ["tipo_pessoa"]],
        "inscricao_estadual": ["insc_estadual", conversions.identity],
        "apelido": ["fantasia_cliente", conversions.with_max_length(50)],
        "razaosocial": ["razao_cliente", conversions.with_max_length(100)],
        "pode_alterar_precos": [None, conversions.constantly("S")],
        "pais": [None, conversions.constantly(1058)],
    }


def produtos():
    return {
        "tipo": [None, conversions.fn_tipo_de_produto(PRODUTOS_TIPOS, DEFAULT_PRODUTO_TIPO)],
        "codigo": ["cod_produto", lambda x, y: str(conversions._or(x, y)), ["id_produto"]],
        "codigoean": ["codigo_barra_produto", conversions.identity],
        "codigonfe": ["id_produto", str],
        "descricao": ["desc_produto", conversions.with_max_length(50)],
        "situacao": [None, conversions.constantly("A")],
        "estoque": [None, conversions.constantly("S")],
        "unidade": [None, conversions.constantly(DEFAULT_PRODUTO_UNIDADE)],
        "custopadrao": ["valor_custo_produto", conversions.identity],
        "precovenda": ["valor_produto", conversions.identity],
    }


def pedidos():
    return {
        "id": ["id_ped", conversions.identity],
        "numero": ["id_ped", str],
        "tipo": [None, conversions.constantly("P")],
        "situacao": [None, conversions.constantly("A")],
        "data_pedido": ["data_pedido", conversions.identity_or_none],
        "data_entrada": ["data_cad_pedido", conversions.strtimestamp_to_strdate],
        "prazo": ["prazo_entrega", conversions.identity_or_none],
        "cliente": ["id_cliente", conversions.identity],
        "condpg": [None, conversions.constantly("0")],
        "observacoes": ["obs_pedido", conversions.identity],
    }


def pedidos_itens(minipcp_produtos):
    return {
        "pedido": ["id_pedido", conversions.identity],
        "item": [None, conversions.seq_generator()],
        "tipo": ["id_produto", conversions.find_and_get(minipcp_produtos, "codigonfe", "tipo", str)],
        "produto": ["id_produto", conversions.find_and_get(minipcp_produtos, "codigonfe", "codigo", str)],
        "quantidade": ["qtde_produto", float],
        "precounitariocheio": ["valor_unit_produto", float],
        "precounitario": ["valor_unit_produto", float],
        "descontototal": ["valor_desconto", float],
        "observacoes": ["info_adicional", conversions.identity],
    }
