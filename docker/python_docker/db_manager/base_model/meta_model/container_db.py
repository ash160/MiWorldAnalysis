import uuid
from cassandra.cqlengine import columns,connection
from datetime import datetime
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.connection import setup
#from base_model import config
from base_model.config import MICROSERVICE_API


#### Container type to nginx mapper ###########
ContanerTypeToNginxMapping = {     
    'MANAGER':{'IN_NET':'','OUT_NET':'15.0.0.2','url_type':'mn_con'},
    'UI':{'IN_NET':'','OUT_NET':'','url_type':'ui_con'}
}


class KafkaMsgMeta(Model):
    kafka_broker_cluster = columns.Text(primary_key=True, required = True) ## cluster name by str like DEFULT 
    fun_name_list = columns.Text(required = True) ## json array {namespace:{'class_name':[funtion_name]}}
    kafka_broker_list = columns.Text() ## json array
    name_space = columns.Text(partition_key=True,required=True) ### json array [name_space]
    


class ServerInfo(Model):
    container_name = columns.Text(required=True,primary_key=True)
    containerip = columns.Text()
    no_of_threads = columns.Integer()
    master_port = columns.Text()

#class ThreadInfo(Model):
#    thread_url = columns.Text()
#    container_name = columns.Text(required=True,partition_key=True)
#    thread_port = columns.Text(required=True,partition_key = True)
#
#class ContainerUrlMapping(Model):
#    container_name = columns.Text(required=True,partition_key = True)
#    namespace = columns.Text(required=True,partition_key=True)


class UrlTypeProtocalMapping(Model): ## bridge information should be exist befor service has been created.
    url_type = columns.Text(primary_key=True) ### ui
    protocal = columns.Text()                 ### http

class UrlMethodMapping(Model): ### may not require
    url_type = columns.Text()
    method = columns.Text() ### not require
    url = columns.Text(primary_key = True)

class ContainerIso(Model):
    container_type = columns.Text(primary_key=True, max_length=255)
    container_iso  = columns.Text(max_length=255)
    container_dir = columns.Text()

class NetworkInterface(Model):
    netmask = columns.Integer()
    base_ip = columns.Text(max_length=255)
    inter_face_type = columns.Text(max_length=255) ### UI_INNET, UI_OUTNET, MANAGER_INNET, MAN_OUT, MONITOR_NET,
    inter_face_code = columns.Text(max_length=255, primary_key = True) # bridge name
    inter_face_name = columns.Text(max_length=255)

#class Naginx(Model):
#    name = columns.Text() ### ui
#    url_type = columns.Text()

class ContainerObject(Model):
    container_name = columns.Text(primary_key= True)
    container_type = columns.Text(max_length=255,partition_key=True)
    status = columns.Text(max_length = 255) ####  running, not_running, stop

class ContainerObjectNetworking(Model):
    ip_address = columns.Text(primary_key=True, max_length=50)
    container_type = columns.Text(partition_key=True,max_length=255)
    container_name = columns.Text(required= True,partition_key=True)
    master_ip_address = columns.Text() ## X
    inter_face_code = columns.Text(max_length=255) ### inter_face_type

class ContainerNetworking(Model):
    container_type = columns.Text(max_length=255,partition_key=True)
    inter_face_type = columns.Text(max_length=255,partition_key = True)

class MicroserviceResource(Model):
    namespace = columns.Text(required=True,primary_key=True)
    source_url = columns.Text()
    sub_url = columns.Text() ###  ['/create','/update','/delete','/list','/retrieve']
    source_code = columns.Text(required=True)
    created_by = columns.Text(required=True)
    created_at = columns.Text(required=False)
    time_stamp = columns.Float(required=True)
    import_parameters = columns.Text() ### import parameter list {"namespace":["model",.....]}###
    microservice_class_name = columns.Text()
    is_core = columns.Boolean(default=True,partition_key=True) 
    
    #level = columns.Text() ### lvl_0 for system restart, lvl_1_1 for supervisor restart, lvl_1_2 for monitor restart, lvl_2 for supervisor microservice restart
    container_type = columns.Text()
    

setup([MICROSERVICE_API["MICROSERVICE_SOURCE"]["DATA_BASE_STRING"]["CASSANDRA"]["IP"]], MICROSERVICE_API["MICROSERVICE_SOURCE"]["DATA_BASE_STRING"]["CASSANDRA"]["KEY_SPACE"], retry_connect=True)
sync_table(ContainerNetworking)
sync_table(ContainerObject)
sync_table(ContainerObjectNetworking)
sync_table(NetworkInterface)
sync_table(ContainerIso)
sync_table(UrlTypeProtocalMapping)
sync_table(UrlMethodMapping)
sync_table(ServerInfo)
sync_table(MicroserviceResource)
