#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from .auth import converse, initiate

parser = ArgumentParser(description='CliAI')

# Subparser for the converse command
converse_parser = parser.subparsers.add_parser(
    'converse', aliases=['chat'], help='Start a conversation with ChatGPT')
converse_parser.add_argument('--api', help='Specify an API')
converse_parser.add_argument('--verbose',
                             '-v',
                             action='store_true',
                             help='Turn on verbose output')
converse_parser.set_defaults(func=converse)


def cli():
    args = parser.parse_args()

    initiate()

    if api_key := args.api:
        initiate(api_key)
    else:
        initiate()

    if args.command == 'converse':
        verbose: bool = args.verbose
        converse(verbose=verbose)
