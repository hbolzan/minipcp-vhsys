import datetime
import argparse


def init_parser():
    parser = argparse.ArgumentParser(description="Integração MiniPCP - VHSYS")
    parser.add_argument("-V", "--version", action="version", version="%(prog)s 0.1")
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        default=False,
        help="Importar todos os produtos, clientes e pedidos em aberto"
    )
    parser.add_argument(
        "-t", "--today",
        action="store_true",
        default=False,
        help="Importar todos os dados incluídos ou alterados hoje"
    )
    parser.add_argument(
        "-s", "--since",
        action="store",
        help="Importar todos os dados incluídos ou alterados desde a data (no formato YYYY-MM-DD)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Executa em modo verboso"
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        default=False,
        help="Somente exibição dos comandos SQL que serão executados"
    )
    return parser


def parse_cli():
    parser = init_parser()
    return parser.parse_args()


def validate_cli_args(args):
    # if args.all and ()
    pass


def display_args(args):
    print("all....: {}".format(args.all))
    print("today..: {}".format(args.today))
    print("since..: {}".format(args.since))
    print("verbose: {}".format(args.verbose))
    print("dry-run: {}".format(args.dry_run))


def validate_args(args):
    if args.all and (args.today or args.since):
        return validation_status(False, "--all não pode ser usado em conjunto com --today ou --since")
    if args.today and args.since:
        return validation_status(False, "--today não pode ser usado em conjunto com --since")
    if args.since and not valid_date(args.since):
        return validation_status(
            False,
            "{} não é uma data váilda para --since. A data deve estar no formato YYYY-MM-DD. Exemplo: 2019-01-31".format(args.since)
        )
    return validation_status(True, "OK")


def valid_date(date_str):
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validation_status(valid, msg):
    return {
        "valid": valid,
        "message": msg
    }
