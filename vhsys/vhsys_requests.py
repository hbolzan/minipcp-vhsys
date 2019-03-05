import json
import urllib
import urllib.request
from settings import VHSYS_API_BASE_URL
from local_settings import VHSYS_ACCESS_TOKEN, VHSYS_SECRET_TOKEN

"""
curl -X GET \
    https://{api_address}/v2/pedidos/:id_ped \
    -H 'access-token: SEU (Access-Token) DE ACESSO ' \
    -H 'secret-access-token: SEU (Secret-Access-Token) DE ACESSO' \
    -H 'cache-control: no-cache' \
    -H 'content-type: application/json' \
"""


def vhsys_get_since(endpoint, since, additional_params=[], expect_list=False):
    "since must be a date formatted as YYYY-MM-DD"
    return vhsys_get_with_params(
        endpoint,
        [("data_modificacao", since)] + additional_params,
        expect_list
    )


def vhsys_get_with_params(endpoint, params, expect_list=False):
    """
    params must be an array of tuples with key, value pairs as in
    [("status", "Em Aberto"), ("since", "2019-03-01")]
    """
    url_query = "&".join(["{}={}".format(k, str(v).replace(" ", "%20")) for k, v in params])
    return vhsys_get(
        endpoint + "?{}".format(url_query),
        expect_list=expect_list
    )


def vhsys_get(endpoint, expect_list=False):
    response = vhsys_request(endpoint)
    if not response or len(response["data"]) == 0:
        return False
    if not expect_list:
        if len(response["data"]) == 1:
            return response["data"][0]
    return response["data"]


def vhsys_request(endpoint):
    req = urllib.request.Request(url=vhsys_url(endpoint), headers=vhsys_headers())
    try:
        with urllib.request.urlopen(req) as response:
            result = response.read()
    except urllib.request.HTTPError:
        return False
    return json.loads(result)


def vhsys_url(endpoint):
    return "{base_url}/{endpoint}".format(base_url=VHSYS_API_BASE_URL, endpoint=endpoint)


def vhsys_headers():
    return {
        "access-token": VHSYS_ACCESS_TOKEN,
        "secret-access-token": VHSYS_SECRET_TOKEN,
        "cache-control": "no-cache",
        "content-type": "application/json",
    }
