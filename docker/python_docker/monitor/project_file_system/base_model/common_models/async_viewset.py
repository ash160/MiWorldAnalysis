#import uuid

#import datetime

#from db_manager_viewset import cassandra_manager_obj, cache_manager_obj
#from cache_manager import cache_manager_obj
#from cassandra_manager import cassandra_manager
#from post_gras_manager import post_gras_manager
from common_api_lib import router,GenClass
from db_manager_client import DBClient
from base_model.permission_model.permission_checker import ParmissionChecker

import datetime

from serializers import Serializer

class ViewSetMaster(GenClass):
    permission_class = ParmissionChacker
    lookup_field ='user'
    loop_index = None
    pk = 'pk'
    serializer_class = None #Serializer
    require_user_mapping = False
    user_fild = None
    model_name = ""
    tmp_cache=None
    db_manager_class = None #DB_client
    db_manager_client = None
    allow_function =['*']
    permission_list = ['read','write','edit','delete']
    function_dict= {
            'list':['list','get'],
            'create':['create','post'],
            'retrive':['retrive','get'],
            'update':['update','put'],
            'destroy':['destroy','post'],
            'partial_update':['partial_update','put']
            }


    def id_generetor(user):
        return user+str(datetime.datetime.timestamp())

    def __init__(self,thread_manager_obj,loop_index):
        self.permission_obj = self.permission_class(thread_manager_obj,loop_index)
        self.thread_manager_obj = thread_manager_obj
        self.loop_index = loop_index
        self.db_manager_client = self.db_manager_class(thread_manager_obj,loop_index)
        #self.permission_mape

    async def list(self, request):

        if await self.permission_obj.has_permission(request.user, self.model_name,'read'):
            data = await self.db_manager_client.list(request)
            return data,200
        else:
            return "Invalid Authorization",400


    async def create(self,request):
        user = request.user

        if await self.permission_obj.has_permission(user, self.model_name,'write'):
            id = self.id_generetor(user)
            data = request.data
            data[self.pk] = id
            serializer_data = self.serializer_class(data=data)
            if serializer_data.is_valid():

                self.permission_obj.assing_permission(user,self.model,id,'*','*',True)
                rs = await self.db_manager_client.create(request['data'])
                return (request.data, 201)
            else:
                return  (request.data, 406)

        else:
            return "Invalid Authorization",400


    async def retrive(request, pk=None):
        if self.permission_obj.has_permission(request.user, self.model_name,'read'):
            if pk is not None:
                if self.permission_obj.has_object_permission(request.user, pk,'read'):
                    data = await self.db_manager_client.retrive(request,pk)
                    return data,201
                else:
                    return 'Invalid Authorization for the item',400
        else:
            return "Invalid Authorization",400

    async def update(self,request, pk=None):
        if self.permission_obj.has_permission(request.user, self.model_name,'edit'):
            if pk is None:
                return  (request.data, 400)
            else:
                if self.permission_obj.has_object_permission(request.user, pk,'edit'):
                    data = request.data
                    serializer_data = self.serializer_class(data=data)
                    if serializer_data.is_valid():
                        rs = await self.db_manager_client.update(request,pk)
                        return (rs, 201)
                else:
                    return "Invalid Authorization for the item",400
                else:
                    return (rs, 406)

        else:
            return "Invalid Authorization",400

    async def partial_update(self,request, pk=None):
        return await self.update(request,pk)

    async def destroy(request, pk=None):
        if self.permission_obj.has_permission(request.user, self.model_name,'delete'):
            if self.permission_obj.has_object_permission(request.user, pk,'delete'):
                if pk is None:
                    return  (request.data, 400)
                else:
                    rs = self.db_manager_client.destroy(request,pk)
                    res1 = rs['row_effected']
                    if res1 > 0:
                        return (request.data, 201)
                    else:
                        return (request.data, 406)

            else:
                return "Invalid Authorization for the item",400

        else:
            return "Invalid Authorization",400

   # def create_router():
   #     r = router()
   #     temp_url = []
   #     for x in self.function_dict:
   #         temp_url.append(self.function_dict[x][0],self.function_dict[x][1],getattr(self,x))
   #     r.urls = temp_url
   #     return r
