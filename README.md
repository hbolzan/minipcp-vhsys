# Integração MiniPCP - VHSYS

## Pré requisitos

### MiniPCP Versão 7.1.1.2704 ou posterior

A integração depende de uma view específica de clientes que foi adicionada nesta versão

http://minipcp.download/instalacao/minipcp_r/2017/minipcpPG7112704update.exe


### Python 3.7

baixe e instale um dos seguintes pacotes

* Windows 32 bits: https://www.python.org/ftp/python/3.7.2/python-3.7.2.exe
* Windows 64 bits: https://www.python.org/ftp/python/3.7.2/python-3.7.2-amd64.exe

## Instalação

* Crie uma pasta e copie nela os arquivos do projeto
* Pela linha de comando, entre na pasta do projeto e rode
```
# pip install -r requirements.txt
```
* Copie o arquivo `local_settings.sample` para `local_settings.py`
* Altere o arquivo `local_settings.py` e preencha 
** os tokens VHSYS 
** a senha do banco de dados
** o host do banco de dados se não for `localhost`
* Verifique se as configurações do arquivo `settings.py` precisam ser alteradas

## Como usar

O módulo de integração MiniPCP - VHSYS roda a partir da linha de comando como um script python e aceite diversos parâmetros. Para exibir as informações de ajuda, digite no prompt de comando:
```
python runner.py -h
```

```
usage: runner.py [-h] [-V] [-a] [-t] [-s SINCE] [-v] [-d]

Integração MiniPCP - VHSYS

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -a, --all             Importar todos os produtos, clientes e pedidos em
                        aberto
  -t, --today           Importar todos os dados incluídos ou alterados hoje
  -s SINCE, --since SINCE
                        Importar todos os dados incluídos ou alterados desde a
                        data (no formato YYYY-MM-DD)
  -v, --verbose         Executa em modo verboso
  -d, --dry-run         Somente exibição dos comandos SQL que serão executados

```

## Observações
* Caso nenhum parâmetro seja informado, será usada opção `--today` que corresponde a usar `--since` com a data de hoje.
* Para exibir os comandos que serão aplicados no banco, sem executá-los de fato, utilize a opção `--dry-run`
* Sempre que um registro for importado novamente, os dados correspondentes no MiniPCP serão atualizados, exceto pedidos de venda que não estiverem mais na situação 'Aguardando liberação'.
