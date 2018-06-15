from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch
from elasticsearch import exceptions as ESExceptions

class Command(BaseCommand):
	help = 'Purge the Elasticsearch index'

	def handle(self, *args, **options):
		self.stdout.write('Purging the ES')
		es = Elasticsearch([{'host': 'localhost'}])
		try:
			resp = es.indices.delete(index='elixir')
		except ESExceptions.TransportError as TE:
			if TE.status_code == 404:
				do_nothing = True
			else:
				raise TE

		try:
			resp = es.indices.delete(index='domains')
		except ESExceptions.TransportError as TE:
			if TE.status_code == 404:
				do_nothing = True
			else:
				raise TE
