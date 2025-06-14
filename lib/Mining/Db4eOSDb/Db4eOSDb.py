"""
lib/Mining/Db4eOSDb/Db4eOSDb.py

This module is part of the Data Abstraction Layer. All *db4e* 
deployment operations that result in a database operation go through 
this module. This module, in turn, communicates with the Db4eDb 
module to access MongoDB.
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


# Supporting modules
import os, sys
from datetime import datetime, timezone
from copy import deepcopy

# Where the DB4E modules live
lib_dir = os.path.dirname(__file__) + "/../../"
# Import DB4E modules
db4e_dirs = [
    lib_dir + 'Infrastructure',
    lib_dir + 'Mining'
]
for db4e_dir in db4e_dirs:
    sys.path.append(db4e_dir)

from Db4eDb.Db4eDb import Db4eDb 
from Db4eLogger.Db4eLogger import Db4eLogger

DB4E_RECORD = {
    'component': 'db4e',
    'name': 'db4e service',
    'version': '0.15.0-beta',
    'status': 'stopped',
    'install_dir': None,
    }

REPO_RECORD = {  
    'component': 'repo',
    'name': 'Website repo',
    'status': 'not_installed',
    'install_dir': None,
    'github_user': None,
    'github_repo': None,
    'install_dir': None,
    }

MONEROD_RECORD_REMOTE = {
    'component': 'monerod',
    'instance': None,
    'ip_addr': None,
    'name': 'Monero daemon',
    'remote': True,
    'rpc_bind_port': 18081,
    'status': 'not_installed',
    'zmq_pub_port': 18083,
    }


MONEROD_RECORD = {
    'component': 'monerod',
    'config': 'monerod.ini',
    'data_dir': None,
    'name': 'Monero daemon',
    'in_peers': 16,
    'instance': None,
    'ip_addr': None,
    'log_level': 0,
    'log_name': 'monerod.log',
    'max_log_files': 5,
    'max_log_size': 100000,
    'out_peers': 16,
    'p2p_bind_port': 18080,
    'priority_node_1': 'p2pmd.xmrvsbeast.com',
    'priority_node_2': 'nodes.hashvault.pro',
    'priority_port_1': 18080,
    'priority_port_2': 18080,
    'remote': False,
    'rpc_bind_port': 18081,
    'show_time_stats': 1,
    'status': 'not_installed',
    'version': '0.18.4.0',
    'zmq_pub_port': 18083,
    'zmq_rpc_port': 18082,
    }

P2POOL_RECORD_REMOTE = {
    'component': 'p2pool',
    'instance': None,
    'ip_addr': None,
    'monerod_id': None,
    'name': 'P2Pool daemon',
    'status': 'not_installed',
    'stratum_port': 3333,
    }

P2POOL_RECORD = {
    'component': 'p2pool',
    'conf_dir': 'conf',
    'config': 'p2pool.ini',
    'instance': None,
    'in_peers': 16,
    'ip_addr': None,
    'log_level': 1,
    'log_dir': 'logs',
    'monerod_id': None,
    'name': 'P2Pool daemon',
    'out_peers': 16,
    'p2p_port': 37889,
    'status': 'not_installed',
    'stratum_port': 3333,
    'version': '4.7',
    'wallet': None,
    }

XMRIG_RECORD = {
    'component': 'xmrig',
    'config': None,
    'instance': None,
    'name': 'XMRig miner',
    'num_threads': None,
    'p2pool_id': None,
    'status': 'not_installed',
    }

class Db4eOSDb:
  
    def __init__(self):
        self._db = Db4eDb()
        self.log = Db4eLogger('Db4eOSDb')
        self._col = self._db.get_collection(self._db._depl_collection)
        db4e_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        self._db4e_dir = db4e_dir
        self.init_deployments()

    def init_deployments(self):
        # Make sure we have a 'db4e' and 'repo' deployment records.
        self.ensure_record('db4e', DB4E_RECORD)
        self.ensure_record('repo', REPO_RECORD)

    def ensure_record(self, component, record_template):
        rec = self.get_deployment_by_component(component)
        if not rec:
            self.add_deployment(deepcopy(record_template))

    def add_deployment(self, jdoc):
        jdoc['doc_type'] = 'deployment'
        jdoc['updated'] = datetime.now(timezone.utc)
        self._db.insert_one(self._col, jdoc)

    def new_deployment(self, component, update_fields):
        if component == 'monerod':
            if update_fields['remote']:
                new_rec = deepcopy(MONEROD_RECORD_REMOTE)
                new_rec.update(update_fields)
                self.add_deployment(new_rec)
        elif component == 'p2pool':
            if update_fields['remote']:
                new_rec = deepcopy(P2POOL_RECORD_REMOTE)
                new_rec.update(update_fields)
                self.add_deployment(new_rec)

    def get_db4e_dir(self):
        return self._db4e_dir
    
    def get_deployment_by_component(self, component, tmpl_flag=None):
        if tmpl_flag:
            doc = self._db.find_one(self._col, {'doc_type': 'template', 'component': component})
        else:        
            doc = self._db.find_one(self._col, {'doc_type': 'deployment', 'component': component})
        return doc

    def get_deployments_by_component(self, component):
        # Return a cursor
        docs = self._db.find_many(self._col, {'doc_type': 'deployment', 'component': component})
        return docs or []
    
    def get_deployment_by_instance(self, component, instance):
        return self._db.find_one(
            self._col, {'doc_type': 'deployment', 'component': component, 'instance': instance})
    
    def get_db4e_deployment(self):
        # Return the db4e deployment doc
        return self.get_deployment_by_component('db4e')
    
    def get_repo_deployment(self):
        # Return the repo deployment doc
        return self.get_deployment_by_component('repo')

    def get_monerod_deployments(self):
        # Return the Monero daemon deployment docs
        return self.get_deployments_by_component('monerod')

    def get_p2pool_deployments(self):
        # Return the P2Pool deployment docs
        return self.get_deployments_by_component('p2pool')

    def get_repo_dir(self):
        depl = self.get_repo_deployment()
        return depl['install_dir']
    
    def get_tmpl(self, component, remote=None):
        if component == 'monerod':
            if remote:
                return deepcopy(MONEROD_RECORD_REMOTE)
            else:
                return deepcopy(MONEROD_RECORD)
        elif component == 'p2pool':
            if remote:
                return deepcopy(P2POOL_RECORD_REMOTE)
            else:
                return deepcopy(P2POOL_RECORD)
        elif component == 'xmrig':
            return deepcopy(XMRIG_RECORD)

    def get_xmrig_deployments(self):
        # Return the xmrig deployment docs
        return self.get_deployments_by_component('xmrig')
    
    def get_xmrig_tmpl(self):
        return self._db.find_one(self._col, {'doc_type': 'template', 'component': 'xmrig'})

    def update_deployment(self, component, update_fields, instance=None):
        update_fields['updated'] = datetime.now(timezone.utc)
        # Update an existing instance's deployment
        if instance and update_fields['doc_type'] == 'deployment':
            return self._db.update_one(
                {'doc_type': 'deployment', 'component': component, 'instance': instance},
                {'$set': update_fields})

        # Create a new instance deployment
        if instance and update_fields['doc_type'] == 'template':
            if component == 'monerod':
                new_rec = deepcopy(MONEROD_RECORD)
                new_rec.update(update_fields)
                new_rec['updated'] = datetime.now(timezone.utc)
                new_rec['doc_type'] = 'deployment'
                return self._db.insert_one(self._col, new_rec)
            elif component == 'p2pool':
                new_rec = deepcopy(P2POOL_RECORD)
                new_rec.update(update_fields)
                new_rec['updated'] = datetime.now(timezone.utc)
                new_rec['doc_type'] = 'deployment'
                return self._db.insert_one(self._col, new_rec)
            elif component == 'xmrig':
                new_rec = deepcopy(XMRIG_RECORD)
                new_rec.update(update_fields)
                new_rec['updated'] = datetime.now(timezone.utc)
                new_rec['doc_type'] = 'deployment'
                return self._db.insert_one(self._col, new_rec)

        # An update of a 'db4e' or 'repo' deployment record.            
        return self._db.update_one(
            self._col, {'doc_type': 'deployment', 'component': component},
            {'$set': update_fields}
        )
    
    def update_deployment_instance(self, component, instance, update_fields):
        update_fields['updated'] = datetime.now(timezone.utc)
        return self._db.update_one(
            self._col,
            {'doc_type': 'deployment', 'component': component, 'instance': instance },
            {'$set': update_fields }
        )
    
    def update_db4e(self, update_fields):
        return self.update_deployment('db4e', update_fields)
    
    def update_repo(self, update_fields):
        return self.update_deployment('repo', update_fields)
    
    def update_monerod(self, update_fields, instance):
        return self.update_deployment_instance('monerod', instance, update_fields)

    def update_p2pool(self, update_fields, instance):
        return self.update_deployment_instance('p2pool', instance, update_fields)

    def update_xmrig(self, update_fields, instance):
        return self.update_deployment_instance('xmrig', instance, update_fields)
