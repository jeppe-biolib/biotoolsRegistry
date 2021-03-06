from django.conf import settings as app_settings
from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch
from elixir.models import *
from elixir.serializers import *
import random, time
from multiprocessing import Pool, cpu_count
from rest_framework.renderers import JSONRenderer

def parallel_function(x):
	resource = ResourceSerializer(Resource.objects.get(id=x[0]), many=False).data
	return JSONRenderer().render(resource)

def parallel_function_v2(x):
	resource = LegacyResourceSerializer(Resource.objects.get(id=x[0]), many=False).data
	return JSONRenderer().render(resource)

class Command(BaseCommand):
	help = 'Regenerate the Elasticsearch index'

	def handle(self, *args, **options):
		self.stdout.write('Regenerating the ES')
		es = Elasticsearch(app_settings.ELASTIC_SEARCH_URLS)
		resourceList = Resource.objects.filter(visibility=1)
		self.stdout.write('--------------------\nid\t:\tname\n--------------------')
		# if sending with curl you need to wrap the object below -> {"mappings": object}
		mapping_subdomains = {
			"subdomains": {
				"properties": {
					"domain": {
						"type": "string",
						"fields": {
							"raw": {
								"type": "string",
								"index": "not_analyzed"
							}
						}
					},
					"resources": {
						"properties": {
							"biotoolsID": {
								"type": "string",
								"fields": {
									"raw": {
										"type": "string",
										"index": "not_analyzed"
									}
								}
							},
							"versionId": {
								"type": "string",
								"fields": {
									"raw": {
										"type": "string",
										"index": "not_analyzed"
									}
								}
							}
						}
					}
				}
			}
		}
	
		es.indices.create('elixir', ignore=400)
		es.indices.create('elixir_v2', ignore=400)
		time.sleep(3)

		# ADD SETTINGS
		settings = {
			"analysis": {
				"analyzer": {
					"not_analyzed_case_insensitive":{
						"tokenizer":"keyword",
						"filter":"lowercase"
					}
				}
			},
			"index": {
				"max_result_window": 50000
			}
		}
		es.indices.close (index='elixir')
		es.indices.close (index='elixir_v2')
		es.indices.put_settings (index='elixir', body=settings)
		es.indices.put_settings (index='elixir_v2', body=settings)
		es.indices.open (index='elixir')
		es.indices.open (index='elixir_v2')

		# ADD MAPPING
		mapping = {
			"tool" : {
				"properties" : {
					"collectionID" : {
						"type" : "text",
						"analyzer": "not_analyzed_case_insensitive",
						"fielddata": True,
						"fields": {
							"raw": { 
								"type":  "keyword"
							}
						}
					},
					"description" : {
						"type" : "text",
						"analyzer": "english",
						"fielddata": True
					},
					"homepage" : {
						"type" : "text",
						"analyzer": "not_analyzed_case_insensitive",
						"fielddata": True
					},
					"name" : {
						"type" : "text",
						"analyzer": "not_analyzed_case_insensitive",
						"fielddata": True,
						"fields": {
							"raw": { 
								"type":  "keyword"
							}
						}
					},
					"topic" : {
						"properties" : {
							"term" : {
								"type" : "text",
								"analyzer": "english",
								"fielddata": True,
								"fields": {
									"raw": { 
										"type":  "keyword"
									}
								}
							}
						}
					},
					"function": {
						"properties": {
							"note": {
								"type": "text",
								"analyzer": "english",
								"fielddata": True
							},
							"cmd": {
								"type": "text",
								"analyzer": "english",
								"fielddata": True
							},
							"input": {
								"properties": {
									"data": {
										"properties": {
											"term": {
												"type": "text",
												"analyzer": "english",
												"fielddata": True,
												"fields": {
													"raw": { 
														"type" : "text",
														"analyzer": "not_analyzed_case_insensitive",
														"fielddata": True
													},
													"keyword": {
				                		"type": "keyword"
				              		}
												}
											}
										}
									},
									"format": {
										"properties": {
											"term": {
												"type": "text",
												"analyzer": "english",
												"fielddata": True,
												"fields": {
													"raw": { 
														"type" : "text",
														"analyzer": "not_analyzed_case_insensitive",
														"fielddata": True
													},
													"keyword": {
				                		"type": "keyword"
				              		}
												}
											}
										}
									}
								}
							},
							"output": {
								"properties": {
									"data": {
										"properties": {
											"term": {
												"type": "text",
												"analyzer": "english",
												"fielddata": True,
												"fields": {
													"raw": { 
														"type" : "text",
														"analyzer": "not_analyzed_case_insensitive",
														"fielddata": True
													},
													"keyword": {
				                		"type": "keyword"
				              		}
												}
											}
										}
									},
									"format": {
										"properties": {
											"term": {
												"type": "text",
												"analyzer": "english",
												"fielddata": True,
												"fields": {
													"raw": { 
														"type" : "text",
														"analyzer": "not_analyzed_case_insensitive",
														"fielddata": True
													},
													"keyword": {
				                		"type": "keyword"
				              		}
												}
											}
										}
									}
								}
							},
							"operation": {
								"properties": {
									"term": {
										"type": "text",
										"analyzer": "english",
										"fielddata": True,
										"fields": {
											"raw": { 
												"type":  "keyword"
											}
										}
									}
								}
							}
						}
					},
					# "contact" : {
					# 	"properties" : {
					# 		"name" : {
					# 			"type" : "text",
					# 			"analyzer": "english",
					# 			"fielddata": True
					# 		}
					# 	}
					# },
					# Maybe add other fields here like credit orcidid, credit elixirPlatform , elixirNode
					"credit" : {
						"properties" : {
							"note" : {
								"type" : "text",
								"analyzer": "english",
								"fielddata": True
							},
							"name" : {
								"type" : "text",
								"analyzer": "english",
								"fielddata": True,
								"fields": {
									"raw": { 
										"type" : "text",
										"analyzer": "not_analyzed_case_insensitive",
										"fielddata": True
									},
									"keyword": {
                		"type": "keyword"
              		}
								}
							}
						}
					},
					"documentation" : {
						"properties" : {
							"note" : {
								"type" : "text",
								"analyzer": "english",
								"fielddata": True
							}
						}
					},
					"biotoolsID" : {
						"type" : "text",
						"analyzer": "not_analyzed_case_insensitive",
						"fielddata": True
					},
					"id" : {
						"type" : "text",
						"analyzer": "not_analyzed_case_insensitive",
						"fielddata": True
					},
					"language" : {
						"type" : "text",
						"fielddata": True,
						"analyzer": "not_analyzed_case_insensitive",
						"fields": {
							"raw": { 
								"type":  "keyword"
							}
						}
					},
					"license" : {
						"type" : "text",
						"analyzer": "not_analyzed_case_insensitive",
						"fielddata": True,
						"fields": {
							"raw": { 
								"type":  "keyword"
							}
						}
					},
					"operatingSystem" : {
						"type" : "text",
						"analyzer": "not_analyzed_case_insensitive",
						"fielddata": True
					},
					# "otherID" : {
					# 	"properties" : {
					# 		"value" : {
					# 			"type" : "text",
					# 			"analyzer": "not_analyzed_case_insensitive",
					# 			"fielddata": True
					# 		},
					# 		"type" : {
					# 			"type" : "text",
					# 			"analyzer": "not_analyzed_case_insensitive",
					# 			"fielddata": True
					# 		},
					# 		"version" : {
					# 			"type" : "text",
					# 			"analyzer": "not_analyzed_case_insensitive",
					# 			"fielddata": True
					# 		}
					# 	}
					# },
					"toolType" : {
						"type" : "text",
						"analyzer": "not_analyzed_case_insensitive",
						"fielddata": True,
						"fields": {
							"raw": { 
								"type":  "keyword"
							}
						}
					},
					"version" : {
						"type" : "text",
						"analyzer": "not_analyzed_case_insensitive",
						"fielddata": True
					},
					# "version" : {
					# 	"properties" : {
					# 		"version" : {
					# 			"type" : "text",
					# 			"analyzer": "english",
					# 			"fielddata": True
					# 		}
					# 	}
					# },
					"versionId" : {
						"type" : "text",
						"fielddata": True,
						"analyzer": "not_analyzed_case_insensitive"
					},
					"maturity" : {
						"type" : "text",
						"fielddata": True,
						"analyzer": "not_analyzed_case_insensitive"
					},
					"cost" : {
						"type" : "text",
						"fielddata": True,
						"analyzer": "not_analyzed_case_insensitive",
						"fields": {
							"raw": { 
								"type":  "keyword"
							}
						}
					},
					"owner" : {
						"type" : "text",
						"fielddata": True,
						"analyzer": "not_analyzed_case_insensitive"
					}
				}
			}
		}
		es.indices.put_mapping(index='elixir', doc_type='tool', body=mapping)
		es.indices.put_mapping(index='elixir_v2', doc_type='tool', body=mapping)

		es.indices.create('domains')
		es.indices.put_mapping(index='domains', doc_type='subdomains', body=mapping_subdomains)

		rl_id = Resource.objects.filter(visibility=1).values_list('id')
		pool = Pool(processes=cpu_count())

		# schema 2.0
		res_v2 = pool.map_async(parallel_function_v2, rl_id)
		results_v2 = res_v2.get(timeout=10000)
		for el in results_v2:
			es.index(index='elixir_v2', doc_type='tool', body=el)

		# schema 3.0
		res = pool.map_async(parallel_function, rl_id)
		results = res.get(timeout=10000)
		for el in results:
			es.index(index='elixir', doc_type='tool', body=el)


		# for resourceItem in resourceList:
		# 	resource = ResourceSerializer(resourceItem, many=False).data
		# 	self.stdout.write('%s\t:\t%s' % (resource['id'], resource['name']))
		# 	es.index(index='elixir', doc_type='tool', body=resource)

		# this is not really correct because the there are multiple versions to a resource
		# should probably be the same for domain resource , or just remove version and versionId
		for domain in Domain.objects.all():
			es.index(index='domains', doc_type='subdomains', body={'domain':domain.name, 'title': domain.title, 'sub_title': domain.sub_title, 'description': domain.description, 'resources': map(lambda x: {'biotoolsID': x.biotoolsID, 'versionId': x.versionId, 'name': x.name, 'version': x.version}, domain.domainresource_set.all())})
			self.stdout.write('%s'%(domain.name))


		# for domain in Domain.objects.all():
		# 	es.index(index='domains', doc_type='subdomains', body={'domain':domain.name, 'title': domain.title, 'sub_title': domain.sub_title, 'description': domain.description, 'resources': map(lambda x: {'biotoolsID': x.biotoolsID, 'versionId': x.versionId, 'name': x.name}, domain.domainresource_set.all())})
		# 	self.stdout.write('%s'%(domain.name))
