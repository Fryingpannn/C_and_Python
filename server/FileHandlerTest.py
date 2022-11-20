from FileHandler import FileHandler

FileHandler.add_customer('hello', {'name': 'hello', 'age':'5', 'address':'', 'number': ''})
FileHandler.find_customer('matthew pan')
FileHandler.find_customer('Matthew Pan')
FileHandler.delete_customer('john')
FileHandler.update_customer('matthew pan', {'name': 'dathew dan', 'age': '9'})
FileHandler.update_customer('hello', {'age': '10'})