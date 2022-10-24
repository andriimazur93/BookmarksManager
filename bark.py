import os

import commands


class Option:
    def __init__(self, name, command, prep_call=None, success_message='{result}'):
        self.name = name
        self.command = command
        self.prep_call = prep_call
        self.success_message = success_message

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        success, result = self.command.execute(data)

        formatted_result = ''

        if isinstance(result, list):
            for bookmark in result:
                formatted_result += '\n' + format_bookmark(bookmark)
        else:
            formatted_result = result

        if success:
            print(self.success_message.format(result=formatted_result))

    def __str__(self):
        return self.name


def get_user_input(label, required=True):
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def get_new_bookmark_data():
    return {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False)
    }


def get_bookmark_id_for_deletion():
    return get_user_input('Enter a bookmark ID to delete')


def format_bookmark(bookmark):
    return '\t'.join(
        str(field) if field else ''
        for field in bookmark
    )


def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options


def get_option_choice(options):
    choice = input('Select a command: ')
    while not option_choice_is_valid(choice, options):
        print("Wrong command")
        choice = input('Select a command: ')
    return options[choice.upper()]


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def loop():
    options = {
        'A': Option(
            'Add bookmark',
            commands.AddBookmarkCommand(),
            prep_call=get_new_bookmark_data,
            success_message='Bookmark added!'
            ),
        'B': Option(
            'List bookmarks, order by date',
            commands.ListBookmarksCommand()
            ),
        'T': Option('List bookmarks, order by title',
                    commands.ListBookmarksCommand(order_by='title')
                    ),
        'D': Option('Delete bookmark',
                    commands.DeleteBookmarkCommand(),
                    prep_call=get_bookmark_id_for_deletion,
                    success_message='Bookmark deleted!'
                    ),
        'Q': Option('Quit',
                    commands.QuitCommand()
                    )
    }
    clear_screen()
    print_options(options)
    chosen_option = get_option_choice(options)
    chosen_option.choose()
    _ = input('Press ENTER to return to menu')


if __name__ == "__main__":
    commands.CreateBookmarksTableCommand().execute()
    while True:
        loop()
