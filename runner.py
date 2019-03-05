import sys
import datetime
from parse_cli import parse_cli, display_args, validate_args
from minipcp_vhsys import run


def get_args():
    args = parse_cli()
    valid_args = validate_args(args)
    if not valid_args.get("valid"):
        display_error(valid_args)
        sys.exit()
    return fixed_args(args)


def fixed_args(args):
    if not args.all and not args.since and not args.today:
        args.today = True

    if args.today:
        args.since = datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d")
    return args


def display_error(valid_args):
    print("")
    print("ERRO: {}".format(valid_args.get("message")))
    print("")


args = get_args()
if args.verbose:
    display_args(args)
    print("")


run(args)
