import os

from django.core.management.commands import startapp

MANAGEMENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Command(startapp.Command):
    def handle_template(self, template, subdir):
        if template is None:
            self.stdout.write('Using custom template.')
            template = os.path.join(MANAGEMENT_DIR, 'templates', 'app_template.zip')

        return super().handle_template(template, subdir)
