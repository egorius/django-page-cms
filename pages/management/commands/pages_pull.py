from django.core.management.base import BaseCommand, CommandError
import requests
import os
from pages.management.utils import APICommand

class Command(APICommand):
    help = 'Pull data from a Django Page CMS API'

    def handle(self, *args, **options):
        self.parse_options(options)

        self.cprint("Fetching page data on " + self.host)
        self.host = self.host + '?format=json'

        page_list = requests.get(self.host, auth=self.auth)
        if page_list.status_code != 200:
            raise ValueError(page_list.status_code)
        json = page_list.text
        
        if not os.path.exists(os.path.dirname(self.filename)):
            os.makedirs(os.path.dirname(self.filename))
        with open(self.filename, "w") as f:
            f.write(json)
        self.cprint(self.filename + " written to disk")
