'''
Server file.

usage: httpfs [-v] [-p PORT] [-d PATH-TO-DIR]
-v Prints debugging messages.
-p Specifies the port number that the server will listen and serve at.
Default is 8080.
-d Specifies the directory that the server will use to read/write requested
files. Default is the current directory when launching the application.
'''
import argparse
from HTTPServerLibrary import HTTPServerLibrary

def validate_port(port, parser):
    if not port.isnumeric() or len(port) > 5:
        parser.error("Please input a valid port number.")
    
    return int(port)

def validate_directory(directory, parser):
    return directory

def main():
    print("\n=====[Pan's Server]=====\n")

    parser = argparse.ArgumentParser(add_help=False)

    # When storing arguments, can use parameters to perform extra parsing
    parser.add_argument('-help', action='help', help='Show this help message and exit')
    parser.add_argument('-v', dest='verbose', help='Verbose mode. Display more information for a given request.',
                        default=False, action='store_true')
    parser.add_argument('-p', dest='port', help='Specifies the port number that the server will listen and serve at. Default is 8080.',
                        type=lambda port: validate_port(port,parser), default='9999')
    parser.add_argument('-d', dest='directory', help='Specifies the directory that the server will use to read/write requested\
                        files. Default is the current directory when launching the application.', type=lambda dir: validate_directory(dir, parser))
    # All arguments will be stored here
    parsed_args = parser.parse_args()

    http = HTTPServerLibrary()
    port = 9999
    directory = 'database.txt'
    verbose = False
    if parsed_args.port: port = parsed_args.port
    if parsed_args.directory: directory = parsed_args.directory
    if parsed_args.verbose: verbose = parsed_args.verbose

    http.startServer(port, directory, verbose)

    print('\n===========[END]==========\n')

if __name__ == "__main__":
    main()