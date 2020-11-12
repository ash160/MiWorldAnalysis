from base_model.suport_thread.import_model import import_manager_obj
from base_model.config import SYSTEM_STATUS

while SYSTEM_STATUS['is_shutdown'] is not True:
    import_manager_obj.add_namespace('root_models.container_manage')
    container_manager_obj = import_manager_obj.root_models.container_manage.container_suppervisor(import_manager_obj)
    container_manager_obj.supervisor_run()
    

SYSTEM_STATUS['is_poweroff']=True
