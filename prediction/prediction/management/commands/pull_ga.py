from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('test_int', nargs='+', type=int)
        
    def handle(self, *args, **options):
        print('\nhello world this is now working right ******\n')


            