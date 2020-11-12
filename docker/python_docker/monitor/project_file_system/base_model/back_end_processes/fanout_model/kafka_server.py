class KafkaMicroservice:
    root_url = "kafaka_microservice"
    def __init__(self,thread_obj):
        pass
	
    async def create_consumer(self,request):
        user_id = request['user']
        topics = request['topics'].split(',')
#        await kafka_obj.conmuser_consume_msg(self,loop_index,user_id,topics)

    async def send_msg(self,request):
        msg = request['msg']
        topic = request['topic']
        m = kafka_obj.register_producer(msg,topic)
 #       await kafka_obj.producer_send_msg(loop_index,msg,topic)

    async def kafka_stop(self,request):
        kafka_obj.STOP = True
