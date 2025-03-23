from address_book import AddressBook, Record
import pickle
import os

SAVE_PATH = "address_book.pkl"


def save_address_book(book, filename=SAVE_PATH):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_address_book(filename=SAVE_PATH):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return AddressBook()

address_book = load_address_book()

def main():
    print("Welcome to the assistant bot!")

    commands = {
        "hello": greet,
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "close": goodbye,
        "exit": goodbye,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
    }

    while True:
        user_input = input("Enter a command: ")
        try:
            cmd, *args = parse_input(user_input)
            if cmd in commands:
                try:
                    print(commands[cmd](*args))
                    if cmd in {"exit", "close"}:
                        break
                except TypeError:
                    print(f"Invalid arguments for command '{cmd}'.")
            else:
                print("Invalid command. Available commands:", ", ".join(commands.keys()))
        except Exception as e:
            print(f"Error: {e}")

def input_error(default_message="An error occurred."):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, IndexError, KeyError) as e:
                return str(e) or default_message
        return wrapper
    return decorator

def parse_input(user_input):
    parts = user_input.strip().split()
    return parts if parts else [""]

@input_error("Usage: add <name> <phone>")
def add_contact(name, phone):
    if address_book.find(name):
        return f"Contact '{name}' already exists."

    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return f"Contact '{name}' added."

@input_error("Usage: change <name> <phone>")
def change_contact(name, phone):
    record = address_book.find(name)
    if not record:
        return f"Contact '{name}' not found."

    if record.phones:
        record.edit_phone(record.phones[0].value, phone)
    else:
        record.add_phone(phone)
    return f"Contact '{name}' updated."

@input_error("Usage: phone <name>")
def show_phone(name):
    record = address_book.find(name)
    if not record:
        return f"Contact '{name}' not found."

    if record.phones:
        return record.phones[0].value
    return f"Contact '{name}' has no phone numbers."

@input_error("Uase: <name> <birthday>")
def add_birthday(*args):
    name, birthday = args
    record = address_book.find(name)
    if record is None:
        return "Contact not found."
    else:
        record.add_birthday(birthday)
        return "Birthday added."

def show_birthday(name):
    record = address_book.find(name)
    if record is None:
        return "Contact not found."
    else:
        return f"{record.birthday.value.strftime("%d.%m.%Y")}"
    
def birthdays():
    if not address_book.data:
        return "No contacts found."
    return "\n".join([f"{contact["name"]} - {contact["congratulation_date"]}" for contact in address_book.get_upcoming_birthdays()])

def show_all():
    if not address_book.data:
        return "No contacts found."
    return "\n".join([f"{contact.name} - {contact.phones[0].value} - {contact.birthday.value.strftime('%d.%m.%Y') if contact.birthday else 'Birthday not set'}" for contact in address_book.values()])

def greet():
    return "How can I help you?"

def goodbye():
    save_address_book(address_book)
    return "Goodbye! Address book saved."

if __name__ == "__main__":
    main()
