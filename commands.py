import sys
from abc import ABC, abstractmethod
from datetime import datetime

from database import DatabaseManager

db = DatabaseManager('bookmarks.db')


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        pass


class CreateBookmarksTableCommand(Command):
    def execute(self, data=None):
        db.create_table(
            'bookmarks',
            {
                'id': 'integer primary key autoincrement',
                'title': 'text not null',
                'url': 'text not null',
                'notes': 'text',
                'date_added': 'text not null'
            }
        )


class AddBookmarkCommand(Command):
    def execute(self, data):
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added'


class ListBookmarksCommand(Command):
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self, data=None):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand(Command):
    def execute(self, data):
        db.delete('bookmarks', {'id': data})
        return 'Bookmark deleted!'


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()