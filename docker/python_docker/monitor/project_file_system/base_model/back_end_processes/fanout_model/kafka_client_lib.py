#from base_model.common_models.common_api_lib import GenClass

#class KafakaServerClient(GenClass):
#    function_dict ={"subscribe":["post","subscribe"]}
#    async def subscribe(self,request):
#        topic = request['topic']
#        msg = {'fun_name':'subscribe','fun_type':'system','topic':topic}
#        m = kafka_obj.register_producer(msg,topic)
#        await kafka_obj.producer_send_msg(loop_index,m,topic)
#        return 'msg send successfully '
##async def send_msg(self,request):






class KafkaServerClient:
    method = 'post'
    sockect_obj = None
    db = None
    loop_index = None
    data_type = ['*'] ## for all '*' or ['cassandra','redis','postgresql']
    #db_interface_list = {} ## {'db_type':['db_type':interface]}
    url_header = NGINX['KAFKA']
    out_net = NETWORK_INTERFACE['OUT_NET']


    def __init__(self,thread_manager_obj,loop_index):
        self.loop_index = loop_index
        self.socket_obj = thread_manager_obj.socket_obj
        self.thread_manager_obj = thread_manager_obj



        async def send_msg(self,user,msg):
            data = {'user':user,'msg':msg} ### {'namespace':'','class':'','func':'','msg':'90890890'}
            return await self.socket_obj.send_single_request(self.loop_index,self.out_net,self.method, "json", self.url_header+"/Kafka/"+"/send_msg/", data)




        async def init_consumer_delete(self,user):
            data = {'user':user}
            return await self.socket_obj.send_single_request(self.loop_index,self.out_net,self.method, "json", self.url_header+"/Kafka/"+"/init_consumer_delete/",{'user':user})



        async def init_create_consumer(self,user):
            data = {'user':user}
            return await self.socket_obj.send_single_request(self.loop_index,self.out_net,self.method, "json", self.url_header+"/Kafka/"+"/init_create_consumer/",{'user':user})
