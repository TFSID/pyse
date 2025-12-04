import os
import sys
import argparse
import threading
import importlib
import pkgutil
import inspect
from logging import DEBUG
from utils.helper import setup_logger
import engine

logger = setup_logger()


def save_links(links, filename='results.txt'):
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


def load_engines(debug_mode=False):
    """
    Dynamically load all engines from the engine directory.
    """
    engines = []
    package_path = engine.__path__
    prefix = engine.__name__ + "."

    for _, name, _ in pkgutil.iter_modules(package_path, prefix):
        try:
            module = importlib.import_module(name)
            # Find classes in the module
            for member_name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    # Check if the class is defined in this module (not imported)
                    if obj.__module__ == name:
                        # Assumption: The class name corresponds to the engine name
                        # and it has a 'search' method.
                        if hasattr(obj, 'search'):
                            try:
                                instance = obj(debug=debug_mode)
                                engines.append(instance)
                            except Exception as e:
                                logger.error(f"Failed to instantiate engine {member_name} from {name}: {e}")
        except Exception as e:
            logger.error(f"Failed to load module {name}: {e}")

    return engines


def engine_start(keyword, output=None, debug_mode=False):
    logger.info('Start search with keyword: %s' % keyword)

    engines = load_engines(debug_mode)

    if not engines:
        logger.error("No engines loaded.")
        return

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

    args = parser.parse_args()

    if not args.keyword and not args.keyword_list:
        parser.print_help()
        sys.exit()

    if args.debug_mode:
        logger.setLevel(DEBUG)

    if args.keyword:
        engine_start(keyword=args.keyword, output=args.output_file, debug_mode=args.debug_mode)
    elif args.keyword_list:
        if os.path.exists(args.keyword_list) and os.path.isfile(args.keyword_list):
            with open(args.keyword_list, 'r') as fp:
                lines = fp.read().splitlines()
                for line in lines:
                    engine_start(keyword=line, output=args.output_file, debug_mode=args.debug_mode)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('Quit')
