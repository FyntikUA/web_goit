from View.base_view import ContactConsoleView
from tools.common import CommandHandler, handle_error, clear_console
import json, re


class Contact:
    """
    Represents a contact with name, email, phones, address, birthday, etc.

    Attributes:
        name (str): The name of the contact.
        email (str): The email address of the contact.
        phones (list): List of phone numbers of the contact.
        address (str): The address of the contact.
        birthday (str): The birthday of the contact.
    """
    def __init__(self, name, email=None, phones=None, address=None, birthday=None):
        """
        Initializes a Contact object with the provided information.

        Args:
            name (str): The name of the contact.
            email (str): The email address of the contact.
            phones (list): List of phone numbers of the contact.
            address (str): The address of the contact.
            birthday (str): The birthday of the contact.
        """
        self.name = name
        self.email = email
        self.phones = phones if phones else []
        self.address = address
        self.birthday = birthday

    def __str__(self):
        """
        Returns a string representation of the contact.

        Returns:
            str: A string containing the name, email, phones, address, and birthday of the contact.
        """
        return f"Name: {self.name}\nEmail: {self.email}\nPhones: {', '.join(self.phones)}\n" \
               f"Address: {self.address}\nBirthday: {self.birthday}"


class ContactManager:
    """
    Manages contacts, including loading, saving, adding, searching, editing, deleting,
    and displaying all contacts.

    Attributes:
        file_path (str): The file path to store contacts.
        contacts (list): A list of Contact objects representing the contacts.
        view: The view object for input/output.
    """
    def __init__(self, file_path, view):
        """
        Initializes a ContactManager object with the provided file path and view.

        Args:
            file_path (str): The file path to store contacts.
            view: The view object for input/output.
        """
        self.file_path = file_path
        self.contacts = self.load_contacts()
        self.view = view

    def load_contacts(self):
        """
        Loads contacts from a JSON file.

        Returns:
            list: A list of Contact objects representing the loaded contacts.
        """
        try:
            with open(self.file_path, 'r') as file:
                contacts_data = json.load(file)
                contacts = [Contact(**contact_data) for contact_data in contacts_data]
                return contacts
        except FileNotFoundError:
            return []

    def save_contacts(self):
        """
        Saves contacts to a JSON file.
        """
        contacts_data = [contact.__dict__ for contact in self.contacts]
        with open(self.file_path, 'w') as file:
            json.dump(contacts_data, file, indent=4)

    @handle_error
    def add_contact(self):
        name = self.view.get_input('Enter contact name: ')
        email = self.view.get_input('Enter contact email: ')
        while not self.validate_email(email):
            email = self.view.get_input('Invalid email format. Please enter a valid email: ')

        phones_input = self.view.get_input('Enter contact phones (comma-separated): ')
        phones = phones_input.split(',')
        for phone in phones:
            while not self.validate_phone(phone.strip()):
                phone = self.view.get_input(f'Invalid phone number format ({phone}). Please enter a valid phone number: ')

        address = self.view.get_input('Enter contact address: ')
        birthday = self.view.get_input('Enter contact birthday (YYYY-MM-DD): ')
        while not self.validate_birthday(birthday):
            birthday = self.view.get_input('Invalid birthday format. Please enter a valid birthday (YYYY-MM-DD): ')

        contact = Contact(name, email, phones, address, birthday)
        self.contacts.append(contact)
        self.save_contacts()
        self.view.display_message('Contact added successfully.')

    @handle_error
    def search_contact(self):
        """
        Searches for a contact based on the given query.
        """
        query = self.view.get_input('Enter search query: ')
        results = [contact for contact in self.contacts if query in contact.name
                   or query in contact.email or query in contact.phones
                   or query in contact.address or query in contact.birthday]
        if results:
            self.view.display_message('Search results:')
            for result in results:
                self.view.display_single_contact(result)
        else:
            self.view.display_error('No contacts found matching the query.')

    @handle_error
    def edit_contact(self):
        name_to_edit = self.view.get_input('Enter the name of the contact you want to edit: ')
        for contact in self.contacts:
            if contact.name == name_to_edit:
                self.view.display_message(str(contact))
                email = self.view.get_input('Enter the new email for the contact: ')
                while not self.validate_email(email):
                    email = self.view.get_input('Invalid email format. Please enter a valid email: ')

                phones_input = self.view.get_input('Enter the new phones for the contact (comma-separated): ')
                phones = phones_input.split(',')
                for phone in phones:
                    while not self.validate_phone(phone.strip()):
                        phone = self.view.get_input(f'Invalid phone number format ({phone}). Please enter a valid phone number: ')

                address = self.view.get_input('Enter the new address for the contact: ')
                birthday = self.view.get_input('Enter the new birthday for the contact (YYYY-MM-DD): ')
                while not self.validate_birthday(birthday):
                    birthday = self.view.get_input('Invalid birthday format. Please enter a valid birthday (YYYY-MM-DD): ')

                contact.email = email
                contact.phones = phones
                contact.address = address
                contact.birthday = birthday
                self.save_contacts()
                self.view.display_message('Contact successfully edited. Updated details:')
                self.view.display_contact_search(contact)
                return
        self.view.display_error('Contact not found.')

    @handle_error
    def delete_contact(self):
        name_to_delete = self.view.get_input('Enter the name of the contact you want to delete: ')
        for contact in self.contacts:
            if contact.name == name_to_delete:
                self.contacts.remove(contact)
                self.save_contacts()
                self.view.display_message('Contact successfully deleted.')
                return
        self.view.display_error('Contact not found.')

    def display_all_contacts(self):
        if not self.contacts:
            self.view.display_error('No contacts found.')
            return
        self.view.display_message('All contacts:')
        self.view.display_contacts_list(self.contacts)


    def validate_email(self, email):
        """
        Перевіряє правильність формату електронної пошти.
        """
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email)

    def validate_phone(self, phone):
        """
        Перевіряє правильність формату номера телефону.
        """
        phone_regex = r'^\d{10}$'  # Перевірка для формату 10 цифр
        return re.match(phone_regex, phone)

    def validate_birthday(self, birthday):
        """
        Перевіряє правильність формату дня народження.
        """
        birthday_regex = r'^\d{4}-\d{2}-\d{2}$'  # Перевірка для формату YYYY-MM-DD
        return re.match(birthday_regex, birthday)



class ContactCommandHandler(CommandHandler):
    """
    Handles commands for contact management, such as adding, searching, editing, deleting,
    and displaying all contacts.

    Attributes:
        manager: The ContactManager object to perform contact-related operations.
        view: The view object for input/output.
    """
    def __init__(self, manager, view):
        """
        Initializes a ContactCommandHandler object with the provided ContactManager object and view.

        Args:
            manager: The ContactManager object to perform contact-related operations.
            view: The view object for input/output.
        """
        self.manager = manager
        commands = {
            '1': ('Add contact', manager.add_contact),
            '2': ('Search contact', manager.search_contact),
            '3': ('Edit contact', manager.edit_contact),
            '4': ('Delete contact', manager.delete_contact),
            '5': ('Display all contacts', manager.display_all_contacts),
            '0': ('Return to main menu', self.return_to_main_menu)
        }
        super().__init__(commands, view)

    def handle_command(self, choice):
        """
        Handles the selected command.

        Args:
            choice (str): The user's choice of command.
        """
        command = self.commands.get(choice)
        if command:
            command[1]()
        else:
            self.view.display_error('Invalid choice. Please select a valid option.')

    def return_to_main_menu(self):
        """
        Returns to the main menu.
        """
        pass


def run_contact_manager():
    """
    Runs the contact manager program.
    """
    program_name = 'Contact Manager V0.1'
    file_path = 'contacts.json'
    view = ContactConsoleView()
    manager = ContactManager(file_path, view)
    command_handler = ContactCommandHandler(manager, view)

    while True:
        options = {
            '1': 'Add contact',
            '2': 'Search contact',
            '3': 'Edit contact',
            '4': 'Delete contact',
            '5': 'Display all contacts',
            '0': 'Return to main menu'
        }
        choice = view.display_menu(program_name, options)
        if choice == '0':
            return
        else:
            command_handler.handle_command(choice)


if __name__ == '__main__':
    clear_console()
    run_contact_manager()
