"""
lib/Db4eOSXMRigEditUI/Db4eOSXMRigEditUI.py

This urwid based TUI drops into the db4e-os.py TUI to help the
user reconfigure a local XMRig miner.


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
import urwid

# Where the DB4E modules live
lib_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(lib_dir)

# Import DB4E modules
from Db4eOSDb.Db4eOSDb import Db4eOSDb
from Db4eConfig.Db4eConfig import Db4eConfig
from Db4eOSModel.Db4eOSModel import Db4eOSModel

class Db4eOSXMRigEditUI:
    def __init__(self, parent_tui):
        self.parent_tui = parent_tui
        self.ini = Db4eConfig()
        self.osdb = Db4eOSDb()
        self.model = Db4eOSModel()
        # Most of the initialization is done in set_instance()

    def back_to_main(self, button):
        self.parent_tui.return_to_main()

    def build_p2pool_deployments(self, deployments):
        items = []
        for instance_name, data in sorted(deployments.items()):
            is_selected = (instance_name == self.selected_p2pool)
            radio = urwid.RadioButton(
                self.group,
                data['instance'],
                on_state_change=self.select_p2pool,
                user_data=instance_name,
                state=is_selected
            )
            self.deployment_radios.append(radio)
            items.append(urwid.Columns([
                (20, radio)
            ], dividechars=1))
        return urwid.LineBox(urwid.Padding(urwid.Pile(items), left=2, right=2), title='Select P2Pool daemon', title_align='left', title_attr='title')

    def on_submit(self, button):
        instance = self.instance_edit.edit_text.strip()
        num_threads = self.num_threads_edit.edit_text.strip()

        # Validate input
        try:
            num_threads = int(num_threads)
        except:
            self.results_msg.set_text("The number of threads must be an integer value")
            return
        
        if instance != self.old_instance:
            if self.osdb.get_deployment_by_instance('xmrig', instance):
                self.results_msg.set_text(f"The instance name ({instance}) is already being used. " +
                                        "There can be only one XMRig deployment with that " +
                                        "instance name.")
                return

        # Generate a XMRig configuration file
        conf_dir        = self.ini.config['db4e']['conf_dir']
        tmpl_dir        = self.ini.config['db4e']['template_dir']
        tmpl_vendor_dir = self.ini.config['db4e']['vendor_dir']
        config          = self.ini.config['xmrig']['config']
        version         = self.ini.config['xmrig']['version']
        xmrig_dir = 'xmrig-' + version
        db4e_dir = self.model.get_dir('db4e')
        vendor_dir = self.model.get_dir('vendor')
        tmpl_config = os.path.join(db4e_dir, tmpl_dir, tmpl_vendor_dir, xmrig_dir, conf_dir, config)
        fq_config = os.path.join(vendor_dir, xmrig_dir, conf_dir, instance + '.ini')
        # Make sure the directories exist
        if not os.path.exists(os.path.join(vendor_dir, xmrig_dir)):
            os.mkdir(os.path.join(vendor_dir, xmrig_dir))
        if not os.path.exists(os.path.join(vendor_dir, xmrig_dir, conf_dir)):
            os.mkdir(os.path.join(vendor_dir, xmrig_dir, conf_dir))

        # Delete the old configuration if the instance name has changed
        if instance != self.old_instance:
            old_config = os.path.join(vendor_dir, xmrig_dir, conf_dir, self.old_instance + '.ini')
            if os.path.exists(old_config):
                os.remove(old_config)

        # We need to the upstream P2Pool IP address and stratum port to build the config
        p2pool_rec = self.osdb.get_deployment_by_instance('p2pool', self.selected_p2pool)
        p2pool_id = p2pool_rec['_id']
        url_entry = p2pool_rec['ip_addr'] + ':' + str(p2pool_rec['stratum_port'])
        # Populate the config template placeholders
        placeholders = {
            'MINER_NAME': instance,
            'NUM_THREADS': ','.join(['-1'] * num_threads),
            'URL': url_entry
        }
        with open(tmpl_config, 'r') as f:
            config_contents = f.read()
            for key, val in placeholders.items():
                config_contents = config_contents.replace(f'[[{key}]]', str(val))
        with open(fq_config, 'w') as f:
            f.write(config_contents)

        # Update the deployment record
        update_fields = {
            'config': fq_config,
            'enable': True,
            'instance': instance,
            'num_threads': int(num_threads),
            'p2pool_id': p2pool_id,
        }
        self.osdb.update_deployment_instance('xmrig', instance, update_fields)
        
        # Set the results
        results = f'Re-configured the XMRig miner ({instance}) deployment record. '
        self.results_msg.set_text(results)

        # Remove the submit button
        self.back_button.set_label("Done")
        self.form_buttons.set_focus(0)        
        self.form_buttons.contents = [
            (self.back_button, self.form_buttons.options('given', 8))
        ]

    def select_p2pool(self, radio, new_state, deployment):
        if new_state:
            self.selected_p2pool = deployment

    def reset(self):
        self.old_instance = None
        self.instance_edit = urwid.Edit("XMRig miner name (e.g. sally): ", edit_text='')
        self.num_threads_edit = urwid.Edit("CPU threads: ", edit_text='')
        self.submit_button = urwid.Button(('button', 'Submit'), on_press=self.on_submit)
        self.back_button = urwid.Button(('button', 'Back'), on_press=self.back_to_main)
        self.form_buttons = urwid.Columns([
            (10, self.submit_button),
            (8, self.back_button)
        ], dividechars=1)
        self.selected_p2pool = None
        self.results_msg = urwid.Text('')

    def set_instance(self, instance):
        self.old_instance = instance
        xmrig_rec = self.osdb.get_deployment_by_instance('xmrig', instance)
        instance = xmrig_rec['instance']
        num_threads = xmrig_rec['num_threads']

        # Form elements; edit widgets
        self.instance_edit = urwid.Edit("XMRig miner name (e.g. sally): ", edit_text=instance)
        self.num_threads_edit = urwid.Edit("CPU threads: ", edit_text=str(num_threads))

        # The buttons
        self.submit_button = urwid.Button(('button', 'Submit'), on_press=self.on_submit)
        self.back_button = urwid.Button(('button', 'Back'), on_press=self.back_to_main)

        # The assembled buttons
        self.form_buttons = urwid.Columns([
            (10, self.submit_button),
            (8, self.back_button)
        ], dividechars=1)

        # Setup the reference to the P2Pool instance XMRig will use
        self.selected_p2pool = None
        self.deployment_radios = []
        self.group = []
        p2pool_deployments = {}
        for deployment in self.model.get_deployments_by_component('p2pool'):
            name = deployment['name']
            instance = deployment['instance']
            p2pool_deployments[instance] = { 'name': name, 'instance': instance }
            self.selected_p2pool = instance # Initialize to the last instance
        p2pool_deployments_box = self.build_p2pool_deployments(p2pool_deployments)

        # The assembled form elements and buttons
        self.form_box = urwid.Pile([
            self.instance_edit,
            self.num_threads_edit,
            urwid.Divider(),
            p2pool_deployments_box,
            urwid.Divider(),
            self.form_buttons
        ])

        # Results
        self.results_msg = urwid.Text('')

        # Assembled results
        self.results_box = urwid.Pile([
            urwid.Divider(),
            urwid.LineBox(
                urwid.Padding(
                    self.results_msg,
                    left=2, right=2
                ),
                title="Results", title_align='left', title_attr='title'
            )
        ])

        form_widgets = [
            urwid.Text('XMRig Miner Setup\n\n' +
                'All of the fields below are mandatory. Furthermore ' +
                'the \"miner name\" must be unique within the ' +
                'db4e environment i.e. if you have more than one ' +
                'miner deployed, then each must have their own ' +
                'unique name. The \"CPU threads\" setting determines how ' +
                'many CPU threads to allocate to the miner. It iss recommended ' +
                'that you leave at least one thread free for the OS.\n\n ' +
                'Use the arrow keys or mouse scrollwheel to scroll up and down.'),
            urwid.Divider(),
            urwid.LineBox(
                urwid.Padding(self.form_box, left=2, right=2),
                title='Setup Form', title_align='left', title_attr='title'),
            self.results_box
        ]

        # Wrap in a ListBox to make scrollable
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker(form_widgets))
        self.frame = urwid.LineBox(
            urwid.Padding(listbox, left=2, right=2),
            title='XMRig Miner Setup', title_align='center', title_attr='title'
        )

    def widget(self):
        return self.frame
