import sys
from abc import ABC, abstractmethod
from datetime import datetime

from persistance import BookmarkDatabase

persistance = BookmarkDatabase()


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        pass


class AddBookmarkCommand(Command):
    def execute(self, data):
        data['date_added'] = datetime.utcnow().isoformat()
        persistance.create(data)
        return True, None


class ListBookmarksCommand(Command):
    def __init__(self, order_by='date_added'):
        self.order_by = order_by

    def execute(self, data=None):
        return True, persistance.list(order_by=self.order_by)


class DeleteBookmarkCommand(Command):
    def execute(self, data):
        persistance.delete(data)
        return True, None


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()
