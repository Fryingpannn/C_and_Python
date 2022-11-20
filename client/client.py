# -*- coding: utf-8 -*-
'''
Matthew Pan 40135588

Client app for Customer interaction
'''
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
        while self.show_menu(): continue

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
        print()

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
        name = ''
        if val == 1:
            name = self.__input_name()
            print()
            url = self.default_url + '/' + name
            self.__validate_URL(url)
            self.http.sendHTTPRequest(self.hostname,HTTPMethod.GET.name,self.full_path)
            self.reset()
        elif val == 2:
            # Name
            name = self.__input_name()
            # Age (optional)
            age = self.__input_age()
            # Address (optional)
            address = input("Enter customer address: ")
            # Number (optional)
            number = self.__input_phone()
            print()

            data = {
                'name': name,
                'age': age,
                'address': address.strip(),
                'number': number
            }
            url = self.default_url + '/' + name
            self.__validate_URL(url)
            self.http.sendHTTPRequest(self.hostname,HTTPMethod.POST.name, self.full_path, BODY_DATA=data)
            self.reset()
        elif val == 3:
            # Delete customer
            name = self.__input_name()
            url = self.default_url + '/' + name
            self.__validate_URL(url)
            self.http.sendHTTPRequest(self.hostname,HTTPMethod.DELETE.name, self.full_path)    
            self.reset()
        elif val == 4:
            # Update customer age
            name = self.__input_name()
            age = self.__input_age()
            data = { 'age': age }
            url = self.default_url + '/' + name
            self.__validate_URL(url)
            self.http.sendHTTPRequest(self.hostname,HTTPMethod.PATCH.name, self.full_path, BODY_DATA=data)
            self.reset()
        elif val == 5:
            # Update customer address
            name = self.__input_name()
            address = input("Enter customer address: ")
            data = { 'address': address.strip() }
            url = self.default_url + '/' + name
            self.__validate_URL(url)
            self.http.sendHTTPRequest(self.hostname,HTTPMethod.PATCH.name, self.full_path, BODY_DATA=data)
            self.reset()
            self.reset()
        elif val == 6:
            # Update customer phone
            name = self.__input_name()
            number = self.__input_phone()
            data = { 'number': number }
            url = self.default_url + '/' + name
            self.__validate_URL(url)
            self.http.sendHTTPRequest(self.hostname,HTTPMethod.PATCH.name, self.full_path, BODY_DATA=data)
            self.reset()
            self.reset()
            self.reset()
        elif val == 7:
            url = self.default_url + '/'
            self.__validate_URL(url)
            self.http.sendHTTPRequest(self.hostname,HTTPMethod.GET.name,self.full_path)
            self.reset()
        elif val == 8:
            return False
        
        return True
    
    def __input_name(self):
        while True:
            name = input("Enter customer name: ")
            if self.__validate_name(name): break
            print('Please input correct customer name. It should only consist of letters and/or spaces.')

        if not name: raise Exception('Invalid name')
        return self.clean(name)
    
    def __input_age(self):
        age = ''
        while True:
            age = input("Enter customer age: ")
            if age.isnumeric() or age == '': break
            print('Please input correct customer age.')

        return age.strip()
    
    def __input_phone(self):
        # Number (optional)
        number = ''
        while True:
            number = input("Enter customer number: ")
            if self.__validate_nb(number): break
            print('Please input correct customer number.')

        return number.strip()
    
    def __validate_nb(self, nb):
        if nb == '' or all(i.isnumeric() or i.isspace() or i == '-' for i in nb):
            return True
        return False
    
    def __validate_name(self, name):
        if name and all(i.isalpha() or i.isspace() for i in name):
            if all(i.isspace() for i in name): return False
            return True
        return False

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
    print("\n=====[Pan's Customer DB Program]=====\n")

    app = CustomerApp()
    app.start()

    print("\n=========[Good bye!]=========")
    print('===========[END]===========\n')

if __name__ == "__main__":
    main()