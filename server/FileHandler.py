import os
import shutil
import mimetypes
from pathlib import Path
from Modules.FileLock import FileLock

class FileHandler:

    def __init__(self, verbose=False):
        # when in debug mode, use 'server/data.txt' instead
        self.defaultDirectory = 'data.txt'
        '''
        {Name : [Age, Address, Number]}
        '''
        self.verbose = verbose
        self.database = {}
        self.count = 0
        self.read_database()

    def read_database(self):
        file_path = self.defaultDirectory
        if not Path(file_path).exists() or not Path(file_path).is_file():
            raise Exception('Cannot read from database. Incorrect path or "data.txt" does not exist.')
        
        self.count = 0
        with open(file_path) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                
                self.count += 1
                customer = line.split('|')
                name, age, address, number = customer
                if all(i == '' or i.isspace() for i in name): continue
                if number == '\n': number = ''
                self.database[name.strip()] = [age.strip(), address.strip(), number.strip()]
        
        if self.verbose: print('[In memory DB begin]:\n', self.database)

    def print_database(self):
        file_path = self.defaultDirectory
        try:
            self.save_database()
            if not Path(file_path).exists() or not Path(file_path).is_file():
                return {
                    'statusCode': 404,
                    'data': 'Database does not exist.'
                }
                
            with open(file_path) as f: 
                file_data = f.read()

            if self.verbose: print('[Printing Database]:\n', file_data)
            CONTENT_TYPE = 'Content-Type: ' + mimetypes.guess_type(file_path)[0] 
            CONTENT_DISPOSITION = 'Content-Disposition: attachment; filename="' + self.defaultDirectory + '"'

            return {
                'data': file_data,
                'statusCode': 200,
                'headers': [CONTENT_TYPE, CONTENT_DISPOSITION]
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'data': f'Error getting file content: {e}'
            }

    def find_customer(self, name):
        if name not in self.database:
            return {
                'statusCode': 404,
                'data': f'Customer not found: {name}'
            }
        
        data = '|'.join([name] + self.database[name])
        if self.verbose: print('[Find customer]:\n', name)
        return {
            'statusCode': 201,
            'data': data
        }

    def add_customer(self, name, customer):
        customer_name, age, address, number = customer.values()
        if name in self.database:
            return {
                'statusCode': 400,
                'data': f'Customer already exists: {name}'
            }
        
        self.count += 1
        self.database[name] = [str(age),address,number]
        if self.verbose: print('[Add customer]: ', name)
        self.save_database()
        return {
                'statusCode': 201,
                'data': f'Customer added: {name}'
            }
    
    def delete_customer(self, name):
        if name not in self.database:
            return {
                'statusCode': 404,
                'data': f'Customer does not exists: {name}'
            }
        
        self.count -= 1
        if self.verbose: print('[Delete customer]:\n', name)
        del self.database[name]
        self.save_database()
        return {
            'statusCode': 201,
            'data': f'Customer deleted: {name}'
        }
    
    def update_customer(self, name, customer):
        if name not in self.database:
            return {
                'statusCode': 404,
                'data': f'Customer does not exists: {name}'
            }
        
        if self.verbose: print('[Updating customer]: ', name)

        curr_customer = self.database[name]
        if 'name' in customer:
            del self.database[name]
            name = customer['name']
        if 'age' in customer: curr_customer[0] = customer['age']
        if 'address' in customer: curr_customer[1] = customer['address']
        if 'number' in customer: curr_customer[2] = customer['number']
        self.database[name] = curr_customer

        self.save_database()
        return {
                'statusCode': 201,
                'data': f'Customer updated: {name}'
            }

    def save_database(self):
        filename = self.defaultDirectory

        filecontent = []
        for name,value in self.database.items():
            if name: filecontent.append([name] + value)
        filecontent.sort()
        filecontent = '\n'.join('|'.join(customer) for customer in filecontent)
        if self.verbose: print('[Printing save database]:\n', filecontent)

        # Locking the file to perform the write operation
        with FileLock(filename):
            try:
                f = open(filename, "w")
                f.write(filecontent)
                f.close()
                return {
                    'data': 'Successfully wrote file content.',
                    'statusCode': 200
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'data': f'Error getting file content: {e}'
                }