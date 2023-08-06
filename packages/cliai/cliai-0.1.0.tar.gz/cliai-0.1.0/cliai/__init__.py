#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TODO:
    - Improve using questionary
    - Save Conversations
    - Improve using rich
    - Improve using prompt_toolkit
    - Pre-built prompts
    - Proxy
"""
__version__ = '0.1.0'
__all__ = ['auth', 'config', 'convo', 'cli']

if __name__ == '__main__':
    for module in __all__:
        exec("import {}".format(module))
    cli.cli()
