import sys
import importlib
import ujson
import uuid
from base_model.meta_model.container_db import MicroserviceResource
import os
import pathlib
import time

root_path = 'import_folder'

class ImportManager:
    
    name_space_list = {} ### {namespace:{filename:str,is_imported:bool[True:False]}
    root_folder = root_path
    addition_info = {} ### {namespace:{}} This will containg addition infomation except source code + namespace from the data base
    
    def __init__(self):
        self.name_space_list['config'] = {'filename':'../config'}
        p = pathlib.Path(self.root_folder)
        self.config = importlib.import_module('base_model.config')
        if not p.exists():
            os.makedirs(self.root_folder)

        #self.config = config

    class Comm:
        pass


    def add_namespace(self,name_space):
        """Namespace face and add to local data structure"""
        #print(name_space)
        data=None
        temp_str =""
        try:
            self.name_space_list[name_space]
        except:
           
            #temp_str = ""
            data = MicroserviceResource.objects().filter(namespace = name_space).allow_filtering().first()
#MicroserviceResource.objects.get(namespace = name_space)
            #print(data)
            import_parameter = ujson.loads(data.import_parameters)#['model']
                        #print(type(import_parameter))
            #print(import_parameter)
            if import_parameter !={}:
                #print(import_parameter)

                for x in import_parameter:

                    if 'sys' not in import_parameter[x]:
                #        continue
                        try:
                            self.name_space_list[x]
                        except:
                #            pass
                           
                            self.add_namespace(x)
                        finally:
                ###        pass
                            temp_str+='from base_model.suport_thread.import_model import import_manager_obj\n'
                            if len(import_parameter[x])>1:
                                for y in import_parameter[x][0].split(','):
                                    temp_str +=y+" = import_manager_obj."+x+"."+y+"\n"
                            else:
                                temp_str+='import '+x+'\n'
                    else:
                        #try:
                    ##        #self.name_space_list[x]
                    ##    #except:
                        if len(import_parameter[x])>1:
                            temp_str +="from "+x+" import "+import_parameter[x][0]+"\n"
                        else:
                            temp_str+='import '+x+'\n'

                    ##        #pass
                    #    
                    #    #    return False

                    #    #self.add_namespace(x,import_parameter[x],'system')
                        #temp_str +="from "+x+" import ("
                        
            #print(temp_str)
            #   pass
            #for y in import_parameter[x]["model"]:
            #    temp_str +=y+" = import_manager_obj."+x+"."+y+"\n"
            source_code  = temp_str + data.source_code
            self.addition_info[name_space] ={}
            self.addition_info[name_space]['source_url'] = data.source_url
            self.addition_info[name_space]['sub_url'] = data.sub_url
            self.addition_info[name_space]['created_by'] = data.created_by
            self.addition_info[name_space]['created_at'] = data.created_at
            self.addition_info[name_space]['time_stamp'] = data.time_stamp
            self.addition_info[name_space]['import_parameters'] = data.import_parameters 
            #print(source_code)
            #
            snp = name_space.split('.')
            file_name = ""
            ch = self
            if len(snp)>1:

                #print(snp)
                sdir = self.root_folder+'/'+'/'.join(snp[:len(snp)-1])
                #print(sdir)
                if not pathlib.Path(sdir).exists():
                    
                    os.makedirs(sdir)
                tf = self.root_folder+'.'+name_space
                #print(tf)

                file_name = sdir+'/'+snp[len(snp)-1]+'.py'
                #print(file_name)    
                for x in range(len(snp)-1):
                #   
                    try:
                        getattr(ch,snp[x])
                #        
                    except:
                        temp = self.Comm()
                #        print(snp[x])
                        setattr(ch,snp[x],temp)
                    ch = getattr(ch,snp[x])
                #file_name = self.root_folder+'/'+file_name

                self.name_space_list[name_space] = file_name
                f = open(file_name,'w+')
                f.write(source_code)
                f.close()
                #print(tf)
                ##
                ##print(name_space)
                #m = input('haii try')
                time.sleep(1/(10**2))
                temp = importlib.import_module(tf)
                #m = input('haii try')
                setattr(ch,snp[-1],temp)

            else:
                tf = self.root_folder+'.'+name_space
                file_name = name_space+'.py'
                file_name = self.root_folder+'/'+file_name
                self.name_space_list[name_space] = file_name
#                print(file_name)
                f = open(file_name,'w+')
                f.write(source_code)
                f.close()
                #print(tf)

                #temp = importlib.import_module(tf)
                #setattr(ch,name_space,temp)

        
        finally:
            pass
            

    def walk(self,path): 
        ''' This is the walk function it tarvel from top of the path to end. path is the namespace like "a.b.c.d" it will return d object.'''
        array_str = path.split('.')
        temp_obj = getattr(self,array_str[0])
        array_str = array_str[1:]
        for x in array_str:
            temp_obj = getattr(temp_obj,x)

        return temp_obj

    def update_namespace(self,namespace):
        del self.name_space_list[namespace]
        self.add_namespace(namespace)
       
       
    def delete_namespace(self,namespace):
        snp = namespace.split('.')
        
        ch  = self
        #print(getattr(ch,snp[0]))

        for x in range(len(snp)-1):
            ch = getattr(ch,snp[x])
        m = getattr(ch,snp[len(snp)-1])
        del m

       
    def list(self):
        return self.name_space_list
   
   
###will be moved to common_api

    def reset(self):
        m = list(self.name_space_list.keys())
        m.remove('config')
        for x in m:
            self.update_namespace(x)

        
    def preprocess_source_code(self,namespace):
        """This function get the actual source code and compile the code"""
        try:
            self.name_space_list[namespace]
        except:
            self.add_namespace(namespace)
                 

import_manager_obj = ImportManager()
