#from db_import.monitor_init_tasks import init_task 

LOAD_BALANCER ={
        "CONTAINER_TYPES":["NGINX"]
        }

NETWORK_INTERFACE ={
        "IN_NET":"127.0.0.1",
        "OUT_NET":"127.0.0.1",
        "MONITOR_NET":"127.0.0.1"
        }

NGINX ={
        "IN_NET":"127.0.0.1", ### input nginx of the container
        "OUT_NET":"127.0.0.1" ### out put nginx of the container
        }
#NETWORK_INTERFACE ={
#        
#        
#            "KAFAKA":{"kafka_br01":"microserver_default"},
#            "CASSANDRA":{"cassandra_br01":"cassandra_bridge"},
#            "REDIS":{"redis_br01":"redis_bridge"},
#            "POSTRGRESQL":{"postgressql_br01":"postgres_bridge"},
#            "FILESERVER":{},
#            #"CONTINER_SUPPER_VISER":"",
#            "MONITOR":"",            
#        
#        }

MONITOR_NETWORK_INTERFACE = {
	"IP_ADDRESS":'10.0.0.4'
}
MONITOR_INITIALIZE_TASKS = "db_json_list"   #was not declared as string, giving error
MONITOR_TEMP_ZIPE_STORE ="temp_zip_file"

MONITOR_TEMP_FOLDER = "temp_extracted_files"

DEFAULT = {
		"CASSANDRA":{"KEY_SPACE":"miworld","IP":NGINX['OUT_NET']},
                "POSTGRESQL":{"USER_ID":"miworld","PASSWORD":"maa@12345","IP":NGINX['OUT_NET'],'DATABASE':'miworld'},#"172.20.0.3","DATABASE":"miworld"},
		"REDIS":{"IP":NGINX['OUT_NET']},#"172.19.0.2"},
		"KAFKA":{"BROKER":['172.18.0.2:9092'],"DEFAULT_TOPICS":["sys"]}#'172.18.0.2:9092'],"DEFAULT_TOPICS":["sys"]}
	 }

NETWORK_CLIENT_TIME_OUT = 60

AUTHENTICAT_MODEL = {
        "TOKEN_AUTHENTICATION":{
            "MANAGER":"token_authentication_manager",
            "DATA_BASE_STRING":{
                "CASSANDRA":DEFAULT["CASSANDRA"],
                "REDIS":DEFAULT["REDIS"]
                }
            }
        }

PERMISSION_MODEL = {
        "PERMISSION":{
            "MANAGER":"permission_manager",
            "DATA_BASE_STRING":
                {
                    "CASSANDRA":DEFAULT["CASSANDRA"],
                    "POSTGRESQL":DEFAULT["POSTGRESQL"],
                    "REDIS":DEFAULT["REDIS"]
                }
            }
        }

MICROSERVICE_API = {
        "MICROSERVICE_SOURCE":{
            "MANAGER":"microservice_manager",
            "DATA_BASE_STRING":{
                "CASSANDRA":{"KEY_SPACE":"miworld","IP":"10.0.0.2"},#NGINX['OUT_NET']},#"10.0.0.2"},
		"POSTGRESQL":{"USER_ID":"miworld","PASSWORD":"maa@12345","IP":"10.0.0.3"}#NGINX['OUT_NET']},#"10.0.0.3"},
                }
            }
        }

KAFKA_META_DATA = {
        "DATA_BASE":"kafaka_meta",
        "DATA_BASE_STRING":{
            "CASSANDRA":DEFAULT["CASSANDRA"],
            "REDIS":DEFAULT["REDIS"],
            "POST_GRES":DEFAULT["POSTGRESQL"]
            }
        }


SYSTEM_STATUS = {
        'is_shutdown':False,
        'is_poweroff':False,
        'is_running':False
        }
