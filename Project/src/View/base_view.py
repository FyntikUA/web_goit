from abc import ABC, abstractmethod
from tabulate import tabulate
from termcolor import colored
from colorama import Fore

class BaseView(ABC):
    @abstractmethod
    def display_message(self, message):
        """
        Displays a message to the user.
        """
        pass

    @abstractmethod
    def get_input(self, prompt):
        """
        Requests input from the user with a prompt.
        """
        pass

    @abstractmethod
    def display_error(self, message):
        """
        """
        pass

    @abstractmethod
    def display_program_name(self, program_name):
        """
        Displays the name of the program.
        """
        pass

    @abstractmethod
    def display_menu(self, program_name, options):
        """
        Displays a menu with options.
        """
        pass

    @abstractmethod
    def get_confirmation(self, message):
        """
        Requests confirmation from the user (yes/no).
        """
        pass

    @abstractmethod
    def display_note_details(self, note):
        pass

    @abstractmethod
    def display_notes_list(self, notes):
        pass
    
    @abstractmethod
    def display_contacts_list(self, contacts):
        pass

    @abstractmethod
    def format_title(self, text):
        pass

    @abstractmethod
    def format_content(self, text):
        pass
    


class ConsoleView(BaseView):
    def display_message(self, message):
        print(message)

    def get_input(self, prompt):
        return input(prompt)

    def display_program_name(self, program_name):
        length = len(program_name) + 4  # Додати 4 символи для оформлення з обох боків
        line = "-" * length
        centered_program_name = program_name.center(length - 4)  # Вирівнюємо текст по центру, віднімаючи 4 символи з обох боків
        colored_text = colored(centered_program_name, 'cyan')
        print(f"\n{line}\n| {colored_text} |\n{line}")

    def display_menu(self, program_name, options):
        self.display_program_name(program_name)
        # Створення списку варіантів меню для відображення у табличному форматі
        menu_options = [(colored(key, 'cyan'), colored(value, 'yellow')) for key, value in options.items()]
        print(tabulate(menu_options, headers=['Option', 'Description'], tablefmt="pretty", stralign="center", numalign="center"))
        choice = input('Choose an option: ')
        return choice

    def display_error(self, message):
        """
        Displays an error message to the user.
        """
        print(f"\033[91mError: {message}\033[0m")

    def display_note_details(self, note):
        pass

    def display_notes_list(self, notes):
        pass

    def format_title(self, text):
        pass

    def format_content(self, text):
        pass        

    def get_confirmation(self, message):
        response = input(f'{message} (yes/no): ')
        return response.lower() in ['yes']

    def display_contacts_list(self, contacts):
        pass

class NoteConsoleView(ConsoleView):
    def format_title(self, text):
        return f'{Fore.BLUE}{text}{Fore.RESET}'

    def format_content(self, text):
        return f'{Fore.LIGHTWHITE_EX}{text}{Fore.RESET}'

    def display_notes_list(self, notes):
        headers = ['№', 'Title', 'Date', 'Tags',
                   'Content']
        notes_table = [
            [self.format_content(i), self.format_content(note.title[:15] + '...' if len(note.title) > 10 else note.title),
             self.format_content(note.note_date), self.format_content(", ".join(note.tags)),
             self.format_content(note.content)]
            for i, note in enumerate(notes)
        ]
        print(tabulate(notes_table, headers=[self.format_title(header) for header in headers], tablefmt='pretty'))    


class EventConsoleView(ConsoleView):
    def format_title(self, text):
        return f'{Fore.BLUE}{text}{Fore.RESET}'
    
    def format_content(self, text):
        return f'{Fore.LIGHTWHITE_EX}{text}{Fore.RESET}'
    
    def display_event_list(self, events):
        headers = ['№', 'Event', 'Date', 'Tags']
        events_table = [
            [
                self.format_content(i + 1), 
                self.format_content(event.title[:15] + '...' if len(event.title) > 10 else event.title),
                self.format_content(event.date_time), 
                self.format_content(", ".join(event.tags))]
            for i, event in enumerate(events)
        ]
        print(tabulate(events_table, headers=[self.format_title(header) for header in headers], tablefmt='pretty'))   
    
    def display_single_event(self, event):
        headers = ['Event', 'Date', 'Tags']
        events_table = [
            [
                self.format_content(event.title[:15] + '...' if len(event.title) > 10 else event.title),
                self.format_content(event.date_time),
                self.format_content(", ".join(event.tags))
            ]
        ]
        
        print(tabulate(events_table, headers=[self.format_title(header) for header in headers], tablefmt='pretty'))


class ContactConsoleView(ConsoleView):
    def format_title(self, text):
        return f'{Fore.BLUE}{text}{Fore.RESET}'
    
    def format_content(self, text):
        return f'{Fore.LIGHTWHITE_EX}{text}{Fore.RESET}'
    
    def display_contacts_list(self, contacts):
        headers = ['№', 'Name', 'Phones', 'Emails', 'Birthday']
        contacts_table = [
            [
                self.format_content(i + 1), 
                self.format_content(contact.name[:15] + '...' if len(contact.name) > 10 else contact.name),
                self.format_content(", ".join(contact.phones)), 
                self.format_content(contact.email),
                self.format_content(contact.birthday)
            ]
            for i, contact in enumerate(contacts)
        ]
        print(tabulate(contacts_table, headers=[self.format_title(header) for header in headers], tablefmt='pretty'))
    
    def display_single_contact(self, contact):
        headers = ['Name', 'Phones', 'Emails', 'Birthday']
        events_table = [
            [
                self.format_content(contact.name[:15] + '...' if len(contact.name) > 10 else contact.name),
                self.format_content(", ".join(contact.phones)),
                self.format_content(contact.email),
                self.format_content(contact.birthday)
            ]
        ]
        
        print(tabulate(events_table, headers=[self.format_title(header) for header in headers], tablefmt='pretty'))