from time import sleep

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command that waits for database to be available"""

    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                connection.ensure_connection()
                db_conn = True
            except OperationalError as e:  # pragma: no cover
                self.stdout.write(f'Database unavailable, waiting 1 second... {e}')
                sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
