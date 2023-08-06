from argparse import ArgumentParser


def _get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('-y', '--yeah', help='yeah option')
    parser.add_argument('-m', '--mooo', help='mooo option')
    return parser

def handler(options):
    print(f'handling command for {__file__}')
    print('options', options)


name = 'dummy'
description = 'dummy command'
parser = _get_parser()