class GenClass:
    allow_function =['*']
    backend_func = None
    function_dict= {}
    network_interface = ""
    url_type = 'ui'
    thread_manager_obj = None
    loop_index = None
    
    def __init__(self,thread_manager_obj=None,loop_index=None):
        #print('haiigen')
        if thread_manager_obj is not None and loop_index is not None:
            self.thread_manager_obj = thread_manager_obj
            self.loop_index = loop_index

    def create_router(self):
        r = router()
        temp_url = []
        
        if self.allow_function[0] =='*':
            for x in self.function_dict:
                if len(self.function_dict[x]) ==2:
                    temp_url.append([x,self.function_dict[x][1],getattr(self,self.function_dict[x][0]),'json',4]) #### security layer 4 for all layer security, json type is default data type
                else:
                    temp_url.append([x,self.function_dict[x][1],getattr(self,self.function_dict[x][0]),self.function_dict[x][2],self.function_dict[x][3]])


        else:
            for x in self.allow_function:
                if len(self.function_dict[x]) ==2:
                    temp_url.append([x,self.function_dict[x][1],getattr(self,self.function_dict[x][0]),'json',4]) 
                else:
                    temp_url.append([x,self.function_dict[x][1],getattr(self,self.function_dict[x][0]),self.function_dict[x][2],self.function_dict[x][3]])

        r.urls = temp_url
        return r


class router:
    """ router class """
    urls = [] ### [regx, [method,rout_function]|router ] {name:\d+}
    dict_url ={}
    buffer_size = 1000000000000
    #__call=False

    #def __init__(selfs):
     #   self.urls = urls
      #  self.get_urls()
       # __call=True

    def get_urls(self,sep='/'):
        actual_url = []
        #if self.__call:
         #   return copy.deepcopy(self.urls)
        u = self.urls
        for x in u:
            if len(x) == 2:
                if type(x[1]) is router:
                    temp_urls = x[1].get_urls() ### Get all url of the model
                    for y in range(len(temp_urls)):
                        temp_urls[y][0] = sep.join([x[0],temp_urls[y][0]]) ### Get url from map root
                    actual_url = actual_url + temp_urls
                else:
                    return False
            else:
                actual_url.append(x)
        self.urls = actual_url
        #print(self.urls)
        return actual_url

    def create_dict(self):
        """Converts url list into dictionary"""

        temp_urls = self.urls
        dict_url = {}
        for x in temp_urls:
            dict_url[x[0]] = {"method":x[1],"callback":x[2],"addition_parameters":[x[3],x[4]]}
        self.dict_url = dict_url
    
    def get_urls_list(self):
        urls = self.urls
        url_list = []
        for x in urls:
            url_list.append(x)
        
        return  url_list

class BackendProcess:
    fun_list = None
    allow_fun = ['*']

    def get_services(self):
        tmp={}
        if self.allow_fun[0]=='*':
            for x in self.fun_list:
                tmp[x]=getattr(self,x)
        return tmp	


def get_ip(request):
        client_address = None
        try:
            # case server 200.000.02.001
            client_address = request.META["HTTP_X_FORWARDED_FOR"]
        except:
            # case localhost ou 127.0.0.1
            client_address = request.META["REMOTE_ADDR"]
        return client_address

