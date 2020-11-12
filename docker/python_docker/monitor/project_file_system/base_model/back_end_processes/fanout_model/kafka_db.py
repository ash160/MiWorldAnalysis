#from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
from base_model.common_models.common_api_lib import GenClass
from base_model.config import KAFKA_META_DATA

#### Loop is BigBoss for every where ############
#### kafka manager manager producer and consumer object life cycle ###
#### It is responcibale for data streaming to users.
#### The producer object is created and mainted for each loop.
####When an user want to send a massage he/she could take the produced object to send the data.#####
#### It create equal amount of consumer for each user for each loop ####
#### consumer object is created when user login and destroyed after user logout ###

#from support.socket_manager import socket_manager_obj
#from django_db import models
 
import uuid
#from cassandra.cqlengine import columns
from cassandra.cqlengine import columns,connection
from datetime import datetime
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.connection import setup
import ujson

class KafkaMsgMeta(Model):
    kafka_broker_cluster = columns.Text(partition_key = True, required = True) ## cluster name by str like DEFULT 
    fun_name_list = columns.Text(partition_key = True, required = True) ## json array {namespace:[funtion_name]}
    kafka_broker_list = columns.Text(partition_key = True, required = True) ## json array
    name_space_list = columns.Text(required=True) ### json array [name_space]
    extra_info = columns.Text()

#setup([KAFKA_META_DATA['DATA_BASE_STRING']['CASSANDRA']['IP']],KAFKA_META_DATA['DATA_BASE_STRING']['CASSANDRA']['KEY_SPACE'] , retry_connect=True)
sync_table(KafkaMsgMeta)

#communication_methods = {'RR':{'subcribe':None,'logout':None},'OO':{'post_like':'post_like','story_like':'story_like','notification':'notifications'},'OM':{'post','story'}}##communication_db.objects.get.all()


class  KafkaMetadataService(GenClass):
    allow_function =['*']
    network_interface = None
    function_dict= {
            '/list':['list','get'],
            '/create':['create','post'],
            '/retrieve':['retrieve','get'],
            '/update':['update','put'],
            '/delete_kafka_broker_cluster':['delete_kafka_broker_cluster','put'],
            #  'partial_update':['','put']
            }
    

    async def list(self,request):
        data = KafkaMsgMeta.objects.all()
        data_list = []
        for x in data:
            data_list.append(dict(x))
        return ujson.dumps(data_list)
    async def retrieve(self,request): ## retrive by kafaka clust 
        pk = request['pk']
        data = KafkaMsgMeta.objects.get(kafka_brocker_cluster = pk)

        return ujson.data(dict(data))

        

    async def create(self,request):
        data =request.data
      #  
      #          'kafka_broker_cluster':request['broker_cluster'],
      #          'kafaka_broker_list':request['kafaka_broker_list'], ### kafka broker list of json objects
      #          'name_space_list':request['name_space_list'], 
      #          'fun_name_list':request['fun_name_list'], ### {nanmespace:[function_name] }
      #          'extra_info':request['extra_infor']
      #          }
        KafkaMsgMeta(**data).save()
        return 'creatred'

    async def update(self,request):
        data = request.data
       # {
       #         'kafka_broker_cluster':request['broker_cluster'],
       #         'kafaka_broker_list':request['kafaka_broker_list'], ### kafka broker list of json objects
       #         'name_space_list':request['name_space_list'], 
       #         'fun_name_list':request['fun_name_list'], ### {namespace:[function_name]}
       #         'extra_info':request['extra_infor']
       #         }
        KafkaMsgMeta(**data).save()
        return 'Updated'
#
#        
#
    async def delete_kafka_broker_cluster(self,request):
        cluster_name = request['cluster_name']
        #broker = request['brocker']        
        rs= KafkaMsgMeta(kafka_broker_cluster = cluster_name).delete()
        return 'kafaka cluster is deleted successfully.'
# 

#class  kafka_metadata_service(CassandraManager):
#    keyspace =KafkaMsgMeta
