"""
lib/Mining/Db4eOSModel.py

This is the db4e-os model, which is part of db4e-os MVC pattern.
"""


"""
  This file is part of *db4e*, the *Database 4 Everything* project
  <https://github.com/NadimGhaznavi/db4e>, developed independently
  by Nadim-Daniel Ghaznavi. Copyright (c) 2024-2025 NadimGhaznavi
  <https://github.com/NadimGhaznavi/db4e>.
 
  This program is free software: you can redistribute it and/or 
  modify it under the terms of the GNU General Public License as 
  published by the Free Software Foundation, version 3.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License for more details.

  You should have received a copy (LICENSE.txt) of the GNU General 
  Public License along with this program. If not, see 
  <http://www.gnu.org/licenses/>.
"""

# Import supporting modules
import urwid
import os, sys

# Where the DB4E modules live
lib_dir = os.path.dirname(__file__) + "/../lib/"
# Import DB4E modules
db4e_dirs = [
  lib_dir + 'Infrastructure',
  lib_dir + 'Mining'
]
for db4e_dir in db4e_dirs:
  sys.path.append(db4e_dir)

from Db4eOS.Db4eOS import Db4eOS
from Db4eOSDb.Db4eOSDb import Db4eOSDb

# The five core component types managed by db4e-os.
DB4E_CORE = ['db4e', 'p2pool', 'xmrig', 'monerod', 'repo']

# Dummy model for status reporting and probing
class Db4eOSModel:
    def __init__(self):
        # ['db4e', 'p2pool', 'xmrig', 'monerod', 'repo']
        self.deployments = DB4E_CORE
        self._os = Db4eOS()
        self._db = Db4eOSDb()

    def get_db4e_deployment(self):
        db4e_rec = self._db.get_db4e_deployment()
        db4e = {
            'name': db4e_rec['name'],
            'status': db4e_rec['status']
        }
        return db4e
    
    def get_db4e_status(self):
        return self._os.get_db4e_service_status()

    def get_repo_deployment(self):
        repo_rec = self._db.get_repo_deployment()
        repo = {
            'name': repo_rec['name'],
            'status': repo_rec['status']
        }
        return repo
    
    def get_repo_dir(self):
        repo_rec = self._db.get_repo_deployment()
        return repo_rec['install_dir']

    def get_monerod_deployments(self):
        deployments = {}
        for deployment in self._db.get_monerod_deployments():
            name = deployment['name']
            status = deployment['status']
            instance = deployment['instance']
            deployments[instance] = { 'name': name, 'status': status, 'instance': instance }
        return deployments
        
    def get_monerod_deployment(self, instance):
        return self._db.get_deployment_by_instance('monerod', instance)

    def get_p2pool_deployments(self):
        deployments = {}
        for deployment in self._db.get_p2pool_deployments():
            name = deployment['name']
            status = deployment['status']
            instance = deployment['instance']
            deployments[instance] = { 'name': name, 'status': status, 'instance': instance }
        return deployments

    def get_p2pool_deployment(self, instance):
        return self._db.get_deployment_by_instance('p2pool', instance)

    def get_xmrig_deployments(self):
        deployments = {}
        for deployment in self._db.get_xmrig_deployments():
            name = deployment['name']
            status = deployment['status']
            instance = deployment['instance']
            deployments[instance] = { 'name': name, 'status': status, 'instance': instance }
        return deployments
    
    def update_db4e(self, update_fields):
        self._db.update_db4e(update_fields)

    def update_repo(self, update_fields):
        self._db.update_repo(update_fields)

    def update_monerod(self, update_fields, instance):
        self._db.update_monerod(update_fields, instance)

    def update_p2pool(self, update_fields, instance):
        self._db.update_p2pool(update_fields, instance)

    def update_xmrig(self, update_fields, instance):
        self._db.update_xmrig(update_fields, instance)