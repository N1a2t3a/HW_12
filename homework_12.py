import json
from collections import UserDict
from datetime import datetime

class Phone:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, number):
        if not isinstance(number, str):
            raise ValueError("Phone number must be a string")

        # Перевірка на коректність введеного номера телефону
        if not number.isdigit():
            raise ValueError("Phone number can only contain digits")

        self._value = number

class Birthday:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, date):
        if not isinstance(date, datetime):
            raise ValueError("Birthday must be a datetime object")

        # Перевірка на коректність введеного дня народження
        if date > datetime.now():
            raise ValueError("Birthday cannot be in the future")

        self._value = date

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def matches_criteria(self, criteria):
        if self.name.matches_criteria(criteria):
            return True
        if self.phone and self.phone.matches_criteria(criteria):
            return True
        if self.birthday and self.birthday.matches_criteria(criteria):
            return True
        return False

    def days_to_birthday(self):
        if self.birthday and self.birthday.value is not None:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)

            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)

            days_left = (next_birthday - today).days
            return days_left
        return None

class Field:
    def __init__(self, value):
        self.value = value

    def matches_criteria(self, criteria):
        return str(self.value).lower() == str(criteria).lower()

class Name(Field):
    pass

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search(self, criteria):
        results = []
        for record in self.data.values():
            if record.matches_criteria(criteria):
                results.append(record)
        return results

    def iterator(self, n):
        if n <= 0:
            raise ValueError("Invalid iterator step size")

        start = 0
        while start < len(self.data):
            yield list(self.data.values())[start:start+n]
            start += n

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Invalid input. Please enter name and phone number separated by a space."

    return inner

address_book = AddressBook()

@input_error
def add_contact(contact_info):
    name, phone = contact_info.split(' ')
    name_field = Name(name)
    phone_field = Phone(phone)
    record = Record(name_field, phone_field)
    address_book.add_record(record)
    return "Contact added successfully."

@input_error
def change_phone(contact_info):
    name, phone = contact_info.split(' ')
    record = address_book.data.get(name)
    if record:
        record.phone.value = phone
        return "Phone number updated successfully."
    else:
        raise KeyError

@input_error
def show_phone(name):
    record = address_book.data.get(name)
    if record:
        return record.phone.value
    else:
        raise KeyError

def show_all_contacts():
    if len(address_book.data) == 0:
        return "No contacts found."
    else:
        return "\n".join([f"{name}: {record.phone.value}" for name, record in address_book.data.items()])

# Функція збереження адресної книги на диск
def save_address_book_to_disk(address_book, filename):
    with open(filename, 'w') as file:
        data = []
        for record in address_book.values():
            data.append({
                'name': record.name.value,
                'phone': record.phone.value if record.phone else None,
                'birthday': record.birthday.value.isoformat() if record.birthday else None
            })
        json.dump(data, file)

# Функція завантаження адресної книги з диска
def load_address_book_from_disk(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        address_book = AddressBook()
        for item in data:
            name = item['name']
            phone = item['phone']
            birthday = item['birthday'] if item['birthday'] else None
            if birthday:
                birthday = Birthday(datetime.fromisoformat(birthday))
            record = Record(Name(name), Phone(phone) if phone else None, birthday)
            address_book.add_record(record)
        return address_book

address_book = load_address_book_from_disk("address_book.json")

def command_parser(command):
    command = command.strip()

    if command == "hello":
        return "How can I help you?"
    elif command.startswith("add"):
        contact_info = command[4:]
        return add_contact(contact_info)
    elif command.startswith("change"):
        contact_info = command[7:]
        return change_phone(contact_info)
    elif command.startswith("phone"):
        name = command[6:]
        return show_phone(name)
    elif command == "show all":
        return show_all_contacts()
    else:
        return "Invalid command. Please try again."

def process_command(command):
    if command in ["good bye", "close", "exit"]:
        print("Good bye!")
        return False

    result = command_parser(command)
    print(result)
    return True

def main():
    print("How can I help you?")
    while True:
        command = input("> ")
        if not process_command(command):
            # Збереження адресної книги на диск перед виходом
            save_address_book_to_disk(address_book, "address_book.json")
            break

if __name__ == "__main__":
    main()

# Додавання контактів в адресну книгу
add_contact("John Doe 1234567890")  
add_contact("Jane Smith 9876543210")  
add_contact("Alice Johnson 1112223333")  


change_phone("Jane Smith 5555555555")  


print(show_phone("John Doe"))  
print(show_phone("Jane Smith"))  
print(show_phone("Alice Johnson"))  


all_contacts = show_all_contacts()
print(all_contacts)