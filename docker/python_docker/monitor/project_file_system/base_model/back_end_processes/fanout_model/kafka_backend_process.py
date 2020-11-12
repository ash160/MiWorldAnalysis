from base_model.config import DEFAULT,NETWORK_INTERFACE
from base_model.common_models.common_api_lib import GenClass,BackendProcess
#from base_model.config import NETWORK_INTERFACE
#from base_model.common_models.common_api_lib import BackendProcess
from base_model.meta_model.container_db import MicroserviceResource
from base_model.back_end_processes.fanout_model.kafka_db import KafkaMsgMeta
from base_model.UserTopicsList.DB_client import UserTopicsListDB_client
#import threading
import ujson
class ProducerConsumerModel(BackendProcess):
    MAXIMUM_PRODUCER = 3
    MINIMUM_PRODUCER  = 1
    MAXIMUM_CONSUMER = 3
    MINIMUM_CONSUMER = 0
    #user_request_url = []
    #request_list = []
    STOP = False


    loop_list = []
    consumer_list = [] ### It will be 1d arry of [user id] ####

    producer_list = {} ### It is a 2d array[loop][producer] of producer object for each loop ####
    number_of_producer = {} ### It is a 1d array of int for count value of producer for each loop ####
    number_of_consumer = {} ### It is a 1d array of int for count value of comsumer for each loop ####

    #user_consumer = [] #### It is a array of  dic {user_id:consumer} #######
    server_name = DEFAULT['KAFKA']["BROKER"]#'localhost:9092'  #### default server. I will change it later ####
    default_topic =DEFAULT['KAFKA']['DEFAULT_TOPICS'] #KAFKA_MODEL["DEFAULT_TOPICS"]
    rule_fun_type = {'system':'*','user':'msg','kafka_admin':'msg'}
    fun_list = ['producer_send_msg','conmuser_consume_msg']
    kafka_fun_list ={'kafka':{'ProducerConsumerModel':'subscribe_topics'},{'ProducerConsumerModel':'unsubscribe_topics'}} #{} ### {'sub_topic':..,'fun':..} {'namespace':{'class':{'function':function_pointer}}}
    #allow_fun = ['*']


    def __init__(self,thread_obj,loop_index):
        self.thread_obj = thread_obj
        self.loop_list = thread_obj.loop_list
        self.ragister_loop(loop_index)
        self.user_topics_client = UserTopicsListDB_client(thread_obj,loop_index)


    def ragister_loop(self,loop_index): ##### Initialize everyone #####
        self.producer_list[loop_index]=[] ##### {[],[],[],.....}
        self.number_of_producer[loop_index]=0 ##### {0,0,0,....}
        self.number_of_consumer[loop_index]=0
        #self.user_consumer.append({})   #### [{},{},{},.......]


    def create_consumer(self,loop_index,user_id, topic_list = None):
        #### This function will create a consumer for each user process ####
        loop = self.loop_list[loop_index]
        consumer_obj = None
        if self.number_of_consumer[loop_index] <=self.MAXIMUM_CONSUMER:
            if topic_list is None:
                consumer_obj = AIOKafkaConsumer(self.default_topic,loop=loop, bootstrap_servers=self.server_name,group_id=user_id)

            else:
                consumer_obj = AIOKafkaConsumer(topic_list,loop=loop, bootstrap_servers=self.server_name,group_id=user_id)

            #self.user_consumer[loop_index][user_id] = consumer_obj
            self.number_of_consumer[loop_index] += 1
            return consumer_obj
        else:
            return False
    def register_producer(msg,topic):

        request_json_meta_data = {"servic":"kafka","service_type":"producer","msg": msg, "topic": topic}

        return request_json_meta_data
    def register_consumer(user_id,topics):
        request_json_meta_data = {"servic":"kafka","service_type":"consumer","topics": topics,"user_id":user_id}

        return request_json_meta_data




    #async def kafka_service(self,loop_index,task):
    #    if coro_worker_manager.corouting_mager_obj.corouting_work_list[user_id][task_id]["status"]  !="DONE":
    #        task = coro_worker_manager.corouting_mager_obj.corouting_work_list[user_id][task_id]
    #
    #        if task["service_type"] == "producer":
    #            await self.producer_send_msg(loop_index,task["msg"],task["topic"])
    #        if task["service_type"] == "consumer":
    #            await self.conmuser_consume_msg(loop_index,task["user_id"],task["topics"])

#            if task["service_type"]=="consumer_del":
 #               await self.consumer_del(loop_index,user_id)



    async def subscribe_topics(self,user_id,consumer_obj,msg):
        #### This function will update user topics list ####
        #cache_manager.cache_manager_obj.create("user_topic_list",topics_list,user_id)
        topics_list = await self.user_topics_client.retrive({'user':user_id})
        topic = msg['topic']
        topic_list.append(topic)
        consumer_obj.subscribe(topic_list)
    async def unsubscribe_topics(self,user_id,consumer_obj,msg):
        topics_list = await self.user_topics_client.retrive({'user':user_id})
        topic = msg['topic']
        topic_list.remove(topic)
        consumer_obj.subscribe(topic_list)

    def assing_producer(self,loop_index):
        if not self.producer_list[loop_index] == []:
            return self.producer_list[loop_index].pop()
        elif self.number_of_producer[loop_index] < self.MAXIMUM_PRODUCER:
            temp_producer = AIOKafkaProducer(loop=self.loop_list[loop_index], bootstrap_servers=self.server_name)
            self.number_of_producer[loop_index] += 1
            return temp_producer
        else:
            return False

    async def send_msg(self,msg,topic):

        producer_obj = self.assing_producer(self.loop_index)
        if not producer_obj:
            return False
        await producer_obj.start()
        try:
            await producer_obj.send_and_wait(topic, str.encode(msg))
        finally:
            # Wait for all pending messages to be delivered or expire.

            await producer_obj.stop()
            self.producer_list[self.loop_index].append(producer_obj)


    async def producer_send_msg(self,loop_index,task): ######### by corouting
        if self.STOP:
            self.thread_obj.corouting_mager.add_pending_task_list(task_meta)
            return False
        msg=task['msg']
        topic = task['topic']
        producer_obj = self.assing_producer(loop_index)
        if not producer_obj:
            return False
        await producer_obj.start()
        try:
            await producer_obj.send_and_wait(topic, str.encode(msg))
        finally:
            # Wait for all pending messages to be delivered or expire.

            await producer_obj.stop()
            self.producer_list[loop_index].append(producer_obj)


    async def kafaka_stoping(self):
        self.STOP = True




    async def conmuser_consume_msg(self,loop_index,task):
        user_id=task['user_id']
        topics = task['topics']
        self.consumer_list.append(user_id)
        consumer_obj =self.create_consumer(loop_index,user_id,topics)#self.assing_consumer(user_id,loop_index,topics)
        if not consumer_obj:
            return False
        await consumer_obj.start()
        try:
            async for msg in consumer_obj:
                if self.kafka_fun_list[msg['namespace']]['class']['function'](user_id,consumer_obj,msg) is False:
                    break
                if self.STOP:
                    break

        finally:
            await consumer_obj.stop()
           # await consumer_obj.close()
            self.number_of_consumer[loop_index] -=1
            del consumer_obj

    async def consumer_del(user_id,consumer_obj,msg):
        if user_id == msg['user_id']:
            self.consumer_list.remove(user_id)
            return False


    #user_list = []






class KafkaBackendProcessSuport(GenClass):
    kafka_backend_class = ProducerConsumerModel
    kafka_backend_process_obj = None
    backend_func = None
    allow_function =['*']
    function_dict= {
            'consumer_delete':['init_consumer_delete','socket'],
            'create_consumer':['init_create_consumer','socket'],
            'add_kafka_funcs_of_namespace':['add_kafka_funcs_of_namespace','socket'],
            'delete_kafka_funcs':['delete_kafka_funcs','socket'],
            'update_kafka_funcs':['update_kafka_funcs','socket'],
            'init_kafka_backend_services':['init_kafka_backend_services','socket']

            }

    def __init__(self,thread_obj,loop_index):
        #print("Haii")
        self.thread_obj = thread_obj
        self.kafka_backend_process_obj = self.kafka_backend_class(thread_obj)
        self.backend_func = self.kafka_backend_process_obj.distribut_users

    async def send_msg(self,request):
        data = request.data
        msg = data['msg']
        topic = data['topic']
        await self.kafka_backend_process_obj.send_msg(msg,topic)


    async def init_consumer_delete(self,request):
        data = request.data
        msg = {'sub_topic':{'fun_type':'system','fun':'consumer_del'},'user_id':data['user_id']}
        topic = 'system'
        task_meta = self.kafka_backend_process_obj.register_producer(msg,topic)
        self.thread_obj.coroutin_manager.add_pending_task_list(task_meta)

    async def init_create_consumer(self,request):
        data = request.data
        user_id = data['user_id']
        topics = data['topics']
        task_meta = self.kafka_backend_process_obj.register_consumer(user_id,topics)
        self.thread_obj.coroutin_manager.add_pending_task_list(task_meta)

    async def add_kafka_funcs_of_namespace(self,request):
        data = request.data
        self.add_kafka_function(data)


    def add_kafka_function(data):
        sub_topic = data['namespace']
        functions = data['functions']
        function_list = ujson.loads(functions.split)


        for x in function_list:
            tmp_namespace = getattr(import_manager_obj,sub_topic)
            self.kafka_backend_process_obj.kafka_fun_list[sub_topic] ={sub_topic+"."+x:getattr(tmp_namespace,x)}



    async def delete_kafka_funcs(self,request):
        data = request.data
        sub_topic = data['namespace']
        functions = data['functions']
        function_list = ujson.loads(functions)
        for x in function_list:
            #tmp_namespace = getattr(import_manager_obj,namespace)
            del self.kafka_backend_process_obj.kafka_fun_list[sub_topic][sub_topic+"."+x]

    async def update_kafka_funcs(self,request):
        data = request.data
        self.add_kafka_function(data)

    async def init_kafka_backend_services(self,request):
        broker_cluster = self.kafka_backend_class.broker_cluster
        kafka_cluster_info = KafkaMsgMeta.objects().get(kafka_broker_cluster=broker_cluster)
        fun_name_list =ujson.loads(kafka_cluster_info.fun_name_list) ## json array {namespace:[funtion_name]}
        kafka_broker_list =kafka_cluster_info.kafka_broker_list ## json array
        name_space_list = ujson.loads(kafka_cluster_info.name_space_list) ### json array [name_space]
        for x in name_space_list:
            data={}
            data['namespace'] = x
            data['functions'] = ujson.dumps(fun_name_list[x])
            self.add_kafka_function(data)
