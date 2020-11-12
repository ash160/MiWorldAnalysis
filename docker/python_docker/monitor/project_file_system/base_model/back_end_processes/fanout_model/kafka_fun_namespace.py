class KafkaFuncClass:
    service_func_list = []

    def generate_sevice_fun(self):
        class_name = type(self).__name__+'.{}'
        func_list_dic = {}
        for x in self.service_func_list:
            func_list_dic[class_name.format(x)] = getattr(self,x)

        return func_list_dic

    def __init__(thread_obj):
        self.thread_obj = thread_obj
