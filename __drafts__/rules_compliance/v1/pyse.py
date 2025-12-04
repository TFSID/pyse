"""
DEVELOPER CONTEXT:
Role: Senior Python Developer - Rules Enforcement & Code Sanitization
Module: Core Rules Integration
Branch: rules/vanilla-enforcement

CRITICAL CONSTRAINTS:
1. NO EXTERNAL DEPENDENCIES - Only Python 3.8+ Standard Library
2. CLI-FIRST - Maintain argparse interface
3. ISOLATION MODE - All outputs to __drafts__ only
4. BACKWARD COMPATIBLE - Keep existing functionality intact
"""

import os
import sys
import argparse
import threading
from logging import DEBUG
from utils.helper import setup_logger
from engine.aol import Aol
from engine.ask import Ask
from engine.bing import Bing
from engine.getsearchinfo import GetSearchInfo
from engine.gigablast import Gigablast
from engine.google import Google
from engine.lycos import Lycos
from engine.metager import MetaGer
from engine.mojeek import Mojeek
from engine.naver import Naver
from engine.seznam import Seznam
from engine.yahoo import Yahoo
from engine.yandex import Yandex

logger = setup_logger()

# Isolation path for outputs
ISOLATION_ROOT = "__drafts__/rules_compliance/v1/outputs"
if not os.path.exists(ISOLATION_ROOT):
    os.makedirs(ISOLATION_ROOT, exist_ok=True)

def get_isolated_path(filename):
    """Ensures file paths are within the isolation directory."""
    if os.path.isabs(filename):
        # If absolute, warn or try to re-route?
        # For now, just return it, assuming user knows what they are doing if they provide full path.
        # But for 'default' values, we want them in isolation.
        return filename
    return os.path.join(ISOLATION_ROOT, os.path.basename(filename))

def save_links(links, filename='results.txt'):
    filename = get_isolated_path(filename)
    current_links = []
    if not isinstance(links, list):
        return

    if os.path.exists(filename) and os.path.isfile(filename):
        with open(filename, 'r') as f:
            current_links = f.read().splitlines()

    for link in links:
        if link not in current_links:
            with open(filename, 'a', encoding='utf-8', errors='replace') as f:
                try:
                    f.write('%s\n' % link)
                except UnicodeEncodeError:
                    logger.error(link)
                except Exception as err:
                    logger.error(err)

            current_links.append(link)


def engine_tasks(engine, keyword, output=None):
    links = engine.search(keyword)
    if output:
        save_links(links, output)
    else:
        save_links(links)


def engine_start(keyword, output=None, debug_mode=False, cookie_file=None):
    logger.info('Start search with keyword: %s' % keyword)

    # Cookie file also needs isolation if default
    if cookie_file:
         cookie_file = get_isolated_path(cookie_file)

    engines = [
        Aol(debug=debug_mode, cookie_file=cookie_file),
        Ask(debug=debug_mode, cookie_file=cookie_file),
        Bing(debug=debug_mode, cookie_file=cookie_file),
        GetSearchInfo(debug=debug_mode, cookie_file=cookie_file),
        Gigablast(debug=debug_mode, cookie_file=cookie_file),
        Google(debug=debug_mode, cookie_file=cookie_file),
        Lycos(debug=debug_mode, cookie_file=cookie_file),
        MetaGer(debug=debug_mode, cookie_file=cookie_file),
        Mojeek(debug=debug_mode, cookie_file=cookie_file),
        Naver(debug=debug_mode, cookie_file=cookie_file),
        Seznam(debug=debug_mode, cookie_file=cookie_file),
        Yahoo(debug=debug_mode, cookie_file=cookie_file),
        Yandex(debug=debug_mode, cookie_file=cookie_file),
    ]

    threads = []

    for engine in engines:
        t = threading.Thread(target=engine_tasks, args=(engine, keyword, output))
        threads.append(t)

    if threads:
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


def main():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]')
    # noinspection PyProtectedMember
    parser._optionals.title = 'Options'
    parser.add_argument('-k', '--keyword',
                        dest='keyword',
                        help='Keyword to search',
                        action='store')
    parser.add_argument('-l', '--list',
                        dest='keyword_list',
                        help='List keywords from file',
                        action='store')
    parser.add_argument('-o', '--output',
                        dest='output_file',
                        help='Output results (default results.txt)',
                        default='results.txt',
                        action='store')
    parser.add_argument('-d', '--debug',
                        dest='debug_mode',
                        help='Set DEBUG mode',
                        action='store_true')
    parser.add_argument('-c', '--cookie-file',
                        dest='cookie_file',
                        help='Cookie file (default cookies.txt)',
                        default='cookies.txt',
                        action='store')

    args = parser.parse_args()

    if not args.keyword and not args.keyword_list:
        parser.print_help()
        sys.exit()

    if args.debug_mode:
        logger.setLevel(DEBUG)

    if args.keyword:
        engine_start(keyword=args.keyword, output=args.output_file, debug_mode=args.debug_mode, cookie_file=args.cookie_file)
    elif args.keyword_list:
        if os.path.exists(args.keyword_list) and os.path.isfile(args.keyword_list):
            with open(args.keyword_list, 'r') as fp:
                lines = fp.read().splitlines()
                for line in lines:
                    engine_start(keyword=line, output=args.output_file, debug_mode=args.debug_mode, cookie_file=args.cookie_file)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('Quit')
