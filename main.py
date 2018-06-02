import os
import sys
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor

loader = DataLoader()


inventory = InventoryManager(loader=loader, sources='/home/labicsc02-65961/Documentos/Asinble-server/Inventory/inventory')
variable_manager = VariableManager(loader=loader, inventory=inventory)

peticion = 'eliminarCarpeta'
nombre_path = '/home/labicsc02-65961/Documentos/carpeta'
# si lo que se quiere trabajar es un archivo se debe especificar el nombre del file y la extension del file


if(peticion == 'eliminarCarpeta'):
    playbook_path = '/home/labicsc02-65961/Documentos/Asinble-server/Playbooks/playbook_eliminarCarpeta.yml'

elif(peticion == 'eliminarArchivo'):
    playbook_path = '/home/labicsc02-65961/Documentos/Asinble-server/Playbooks/playbook_eliminarFile.yml'

elif(peticion == 'crearArchivoTXT'):
    playbook_path = '/home/labicsc02-65961/Documentos/Asinble-server/Playbooks/playbook_crearArchivoTXT.yml'

elif(peticion == 'crearCarpeta'):
    playbook_path = '/home/labicsc02-65961/Documentos/Asinble-server/Playbooks/playbook_crearCarpeta.yml'


if not os.path.exists(playbook_path):
    print('[INFO] The playbook does not exist')
    sys.exit()

Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax',
                                 'connection','module_path', 'forks', 'remote_user',
                                 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                                 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check','diff'])

options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False,
                  connection='ssh', module_path=None, forks=100, remote_user='labicsc02-65961',
                  private_key_file='/home/labicsc02-65961/.ssh/id_rsa', ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None,
                  scp_extra_args=None, become=True, become_method='sudo',
                become_user='root', verbosity=None, check=False, diff=False)

variable_manager.extra_vars = {'hosts': 'all', 'path': nombre_path } # This can accomodate various other command line arguments.`

passwords = dict(vault_pass='adminlabicssc2018')

pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)

results = pbex.run()