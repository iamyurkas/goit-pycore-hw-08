from collections import UserDict
import re
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError("Phone number not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days_ahead: int = 7) -> list[dict]:
        birthdays = []
        for user in self.data.values():
            user_birthday = self.__get_user_birthday(user)
            if user_birthday and self.__is_birthday_upcoming(user_birthday, days_ahead):
                birthdays.append(self.__get_user_notification_object(user, user_birthday))
        return birthdays
    
    def __is_birthday_upcoming(self, user_birthday, days_ahead: int=7) -> bool:
        return 0 <= (user_birthday - datetime.now()).days < days_ahead

    def __get_user_birthday(self, user) -> datetime | None:
        if user.birthday is None:
            return None
        
        today = datetime.now()
        birthday = user.birthday.value.replace(year=today.year)
        if birthday < today:
            return birthday.replace(year = today.year + 1)
        return birthday

    def __get_user_notification_object(self, user, user_birthday) -> dict:
        return {
            'name': user.name.value,
            'congratulation_date': self.__get_notification_date(user_birthday).strftime('%Y.%m.%d')
        }

    def __get_notification_date(self, user_birthday) -> datetime:
        notification_date = user_birthday
        if notification_date.weekday() == 5: # Saturday
            notification_date = notification_date + timedelta(days = 2)
        elif notification_date.weekday() == 6: # Sunday
            notification_date = notification_date + timedelta(days = 1)
        return notification_date

