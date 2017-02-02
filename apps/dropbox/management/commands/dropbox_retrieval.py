"""
Examine existing PredictDataset objects.

- Retrieve files from confirmed dropbox links

"""

import logging
LOGGER = logging.getLogger('apps.dropbox')

from django.core.management.base import BaseCommand, CommandError

from apps.predict.models import PredictDataset
from apps.dropbox.models import DropboxFile

class RetrievalError(IOError):
    pass

class Command(BaseCommand):
    help = """Regular run of new dropbox links:

      manage.py dropbox_retrieval

    """
    def handle(self, **options):
        CONFIRMED = PredictDataset.STATUS['DATASET_CONFIRMED']
        for dataset in PredictDataset.objects.filter(status=CONFIRMED):
            print " * Looking at dataset: %s" % str(dataset)
            dataset.set_status('FILE_RETRIEVAL_STARTED')
            try:
                for d_file in DropboxFile.objects.filter(retrieval_start__isnull=True):
                    print "  + Downloading: %s" % d_file.url
                    d_file.download_now()
                    if d_file.retrieval_error:
                        raise RetrievalError(d_file.retrieval_error)
            except Exception as err:
                print "  XXX Failed: %s" % str(err)
                dataset.set_status('FILE_RETRIEVAL_FAILED')
            else:
                dataset.set_status('FILE_RETRIEVAL_SUCCESS')

