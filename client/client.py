# -*- coding: utf-8 -*-
'''
Parser for HTTP library

General
- Take in text input from cURL
- Convert to one string that can be input into HTTP library directly

Specifics
- Must check the command options. Not all should exist, also different for GET and POST
  (E.g.: GET shouldn't take 'd').

HTTP library receives parameters
- (HOST, HTTP_METHOD, PATH, HEADERS: str "k:v" , BODY_DATA, VERBOSE)

TESTING
- In this file's path, enter 'python3 httpc.py get -h hello:world -H ok:lol'
  in the terminal. It should print out the arguments stored.

REQUEST REFERENCE
- httpc (get|post) [-v] (-h "k:v")* [-d inline-data] [-f file] URL
'''
import argparse
from enum import Enum
from urllib.parse import urlparse
from HTTPLibrary import HTTPLibrary

# Enum for HTTP methods
class HTTPMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    DELETE = 'DELETE'

class CustomerApp:

    def __init__(self):
        self.http = HTTPLibrary()
        self.default_url = 'http://localhost:9999'
        self.hostname = ''
        self.full_path = ''
    
    def start(self):
        while loop := self.show_menu(): continue

    def show_menu(self):
        print("Python DB Menu:\n")
        print("  1. Find customer")
        print("  2. Add customer")
        print("  3. Delete customer")
        print("  4. Update customer age")
        print("  5. Update customer address")
        print("  6. Update customer phone")
        print("  7. Print report")
        print("  8. Exit")
        print("\n")

        val = input("Enter a menu number: ")
        while not val.isnumeric() or (val.isnumeric() and (int(val) < 1 or int(val) > 8)):
            print(" -> Invalid menu number. Try again.\n")
            val = input("Enter a menu number: ")
        
        return self.process_action(int(val))
    
    def clean(self, name):
        return name.strip().replace(' ', '%20')
    def reset(self):
        self.hostname = ''
        self.full_path = ''
    
    def process_action(self, val):
        if val == 1:
            name = input("Enter customer name: ")
            if not name:
                print('Please input correct customer name.')
                return
            
            print('')
            url = self.default_url + '/' + self.clean(name)
            self.__validate_URL(url)
            self.http.sendHTTPRequest(self.hostname,HTTPMethod.GET.name,self.full_path)
            self.reset()
        elif val == 2:
            self.reset()
        elif val == 3:
            self.reset()
        elif val == 4:
            self.reset()
        elif val == 5:
            self.reset()
        elif val == 6:
            self.reset()
        elif val == 7:
            url = self.default_url + '/'
            self.__validate_URL(url)
            self.http.sendHTTPRequest(self.hostname,HTTPMethod.GET.name,self.full_path)
            self.reset()
        elif val == 8:
            return False
        
        return True

    # Validates URL in simple manner (checks if has http:// or https:// + a hostname)
    def __validate_URL(self, url):
        result = urlparse(url)
        if all([result.scheme, result.netloc, result.hostname]):
            # Set the hostname and full url path
            self.hostname = result.netloc
            self.full_path = result.path
            if result.params: self.full_path += f';{result.params}'
            if result.query: self.full_path += f'?{result.query}'
            return url
        else:
            raise Exception('Please enter a valid URL.')
    
'''
The program's starting point.
'''
def main():
    print("\n=====[Pan's customer DB program]=====\n")

    app = CustomerApp()
    app.start()

    print('\n===========[END]===========\n')

if __name__ == "__main__":
    main()