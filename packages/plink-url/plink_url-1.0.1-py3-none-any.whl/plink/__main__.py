import argparse
import pkg_resources
from analyser import Analyser
from options import Options
from termcolor import colored

def print_splash_screen(verbose):
    logo = '''
       _ _       _    
      | (_)     | |   
 _ __ | |_ _ __ | | __
| '_ \| | | '_ \| |/ /
| |_) | | | | | |   < 
| .__/|_|_|_| |_|_|\_\ 
| |                   
|_|                   
    '''
    print(colored(logo, "magenta"))
    if verbose:
        print(colored("plink v" + pkg_resources.get_distribution('plink-url').version, "cyan"))

def initialise(arguments):
    return Options(whitelist=arguments.whitelist, depth=arguments.depth, blacklist=arguments.blacklist, start_url=arguments.start_url, verbose=arguments.verbose)

def main():
    #Retrieve, validate and parse arguments from CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("start_url", type=str, help="Initial URL to analyse")
    parser.add_argument("--whitelist", "-w", help="Domains to analyse. Can only be provided if blacklist is missing", nargs="*")
    parser.add_argument("--blacklist", "-b", help="Domains to skip, Can only be provided if whitelist is missing", nargs="*")
    parser.add_argument("--depth", "-d", type=int, help="Number of analysis cycles", const=3, default=3, nargs="?")
    parser.add_argument("--verbose", "-v", action="store_true", help="Give more output (including potential errors, and a list of individual URL scans)")
    args = parser.parse_args()

    #Both whitelist and blacklist cannot be specified
    if args.whitelist is not None and args.blacklist is not None:
        parser.error("Either provide a whitelist, or a blacklist, you cannot specify both")

    print_splash_screen(args.verbose)

    options = initialise(args)
    a = Analyser(options)
    a.analyse()

if __name__ == '__main__':
    main()