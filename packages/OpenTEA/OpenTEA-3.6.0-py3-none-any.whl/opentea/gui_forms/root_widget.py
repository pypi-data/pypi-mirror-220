"""
The root widget
===============

The root widget is the fisrt called by otinker.
It corresponds to the firts node ot the SCHEMA.

At the root widget, the whole window is created.
The root host the main Tab-notebook,
and if necessary the wiew 3D tab.

Tabs callbacks:
===============

As tabs callbacks can change any part of the memory,
These callbacks are passed down to the root widget,
trigerring two subprocesses.

Execute:
--------

Execute is about memory modification.
The callback associated shows the following singature:

nested object > callback > nested object

Update_3d_view:
---------------

Update_3d_view is about 3D feedback.
The callback associated shows the following singature:

nested object, 3D scene > callback > 3D scene

"""

from __future__ import annotations
import abc
from copy import deepcopy
from tkinter import ttk

import yaml


from opentea.gui_forms.constants import (
    PARAMS,
    load_icons,
    set_system,
    config_style,
)


from opentea.gui_forms.node_widgets import (
    OTNodeWidget,
    OTTabWidget,
)
from opentea.gui_forms.menus import DefaultMenubar

from opentea.gui_forms.soundboard import play_door
from opentea.gui_forms.viewer_3d import add_viewer_3d
from opentea.gui_forms.viewer_2d import add_viewer_2d



class OTRoot:

    def __init__(self, schema, tksession, style, data_file, tab_3d=False, tab_2d=False):

        # TODO: clear tmp_dir and delete at the end (.tmp?)
        # Compatibility with OOTTeeWidget
        self.name="root"
        self.my_root_tab_widget = None # See OTTreeElement to undestand this one (ADN)
        self.schema = schema
        self.tksession = tksession
        #########
        
        # ADN : Todo, remove this horror! 
        self._status_temp = 0
        self._status_invalid=0 # Due to _update_parent_status()
        self.status = 0
        #ADN :  another horrible quirk    
        self._data_file=None #private storage of datafile for property self.datafile
        
        # Configuration of appearance
        self.global_config(style)
        self.set_menubar()
        play_door()
        #===========================

        
        self.root_tab = RootTabWidget(self.schema, self, data_file)
        
        self.data_file=data_file 
            #! By this setter, the title is updated, and self.root_tab.data_file too!
        
        if tab_3d:
            self.root_tab.view3d = add_viewer_3d(self)
        if tab_2d:
            self.root_tab.view2d = add_viewer_2d(self)

    @property
    def title(self):
        """Make the title dynamic at the top of the window"""
        return f"{self.schema.get('title', '')} - {self.data_file}"

    def _set_title(self):
        """Update the window title, itself automatically updated"""
        self.tksession.title(self.title)

    @property
    def properties(self):
        # TODO: check if this is required
        return self.schema.get('properties', {})


    # We have a data file prop/setter 
    # to update the window and forms on change of the datafile
    @property
    def data_file(self):
        return self._data_file

    @data_file.setter
    def data_file(self, path):
        self._data_file = path
        self.root_tab.data_file = path 
        self._set_title()    

    def global_config(self, style):
        """Main configurations for root widget"""
        self.icons = load_icons()
        set_system()
        config_style(style)
        self.tksession.columnconfigure(0, weight=1)
        self.tksession.rowconfigure(0, weight=1)

        self.frame = ttk.Frame(self.tksession, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky="news")

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", padx=2, pady=3, expand=True)

        self._set_title()
    
    def set_menubar(self):
        """Start the menubar on the top of the screen"""
        self._menubar = DefaultMenubar(self)
        self._menubar.activate()
        #self._menubars = [self._menubar]
        
    def mainloop(self):
        """Start the mainloop
        
         usefull when testing to NOT start the mainloop
        """
        self.tksession.mainloop()

    def get(self):
        """How Opentea Save the project"""
        return self.root_tab.get()
    
    def save_project(self):
        """How Opentea Save the project"""
        self.root_tab.save_project()




    def load_project(self, data_file):
        """How Opentea load the project"""
        self.root_tab.load_project(data_file)

    def add_child(self, child:RootTabWidget):
        """Necessary to behave llike an OTTreeElement
        
        Called when creating the child RootTabWidget
        
        Because "
        When you create the element, it adds itself to its parent familly
        self.children[child.name] = child"

        """
        pass
        # indeed no need to update this
        # ADN : really I hate when OO forces you to add void methods
        #  to make it work 
        #self.root_tab = child

class RootTabWidget(OTNodeWidget, metaclass=abc.ABCMeta):
    def __init__(self, schema: dict, parent: OTRoot, datafile: str=None):
        self.title = 'RootTabWidget'
        self.data_file=datafile
        self.view3d = None
        self.view2d = None

        super().__init__(schema, parent, 'RootTabWidget')
        
        
        self.my_root_tab_widget = self
        self._config_frame()

        # specific attributes to handle dependents
        self._global_dependents = dict()
        self._dependents = self._global_dependents
        self._xor_dependents = dict()
        self._xor_level = 0
        self._dependent_names = set()

        self._initialize_tabs()

    #########################################
    # Dependencies with nested XOR
    # Lots to unpack and comment
    def prepare_to_receive_xor_dependents(self):
        self._xor_level += 1
        self._dependents = self._xor_dependents

    def assign_xor_dependents(self):
        self._xor_level -= 1

        if self._xor_level == 0:
            self.assign_dependents()
            self._dependents = self._global_dependents

    def add_dependency(self, master_name, slave):
        """Include a reactive dependency of one widget to the other
        
        If node1 have an ot_require for node2, 
        node1 slave is added to node2 slave list, and node2 is the master.
        """
        slaves_list = self._dependents.get(master_name, [])

        self._dependents[master_name] = slaves_list

        self._dependent_names.add(slave.name)

        # TODO : ADN to me this is not used at all!
        slaves_list.append(slave)

    def assign_dependents(self):
        # find by name and add dependency
        for master_name, slaves in self._dependents.items():
            master = self.get_child_by_name(master_name)
            if master is None:
                msg=f"Dependency error, -{master_name}- was not found in your Schema"
                raise RuntimeError(msg)
            master.add_dependents(slaves)

        # reset dependents
        self._dependents.clear()
    ############################################



    ############################
    # ADN NEEDED TO REDEFINE 
    # @property
    # def status(self):
    #     return self._get_status()

    # @status.setter
    # def status(self, status):
    #     if status == self._status:
    #         return
    #     self._status = status
    ###################################

    def _config_frame(self):
        """Configuration of the present widget"""
        self.frame = ttk.Frame(self.parent.frame)
        self.parent.notebook.add(self.frame, text=self.title)
        self.notebook = ttk.Notebook(self.frame, name="tab_nb")
        self.notebook.pack(fill="both", padx=2, pady=3, expand=True)

    def _initialize_tabs(self):
        """Addition of child tabs"""
        for tab_name, tab_obj in self.properties.items():
            OTTabWidget(tab_obj, self, tab_name)  # goes to children when creating tab

       
        self.assign_dependents()

        # set saved state
        self.load_project(self.data_file)
        
        # validate
        self.validate()

    def load_project(self, path:str=None):
        if path is None:
            return
        with open(path, 'r') as file:
            state = yaml.load(file, Loader=yaml.SafeLoader)
        self.set(state)
    
    def save_project(self):
        if self.data_file is None:
            raise NotImplementedError
        state = self.get()
        with open(self.data_file, 'w') as file:
            yaml.dump(state, file, Dumper=yaml.SafeDumper)

    def _get_validated(self):
        return {tab.name: tab.status for tab in self.children.values()}

    def get(self)-> dict:
        """Add the metavidget setter to the basic get"""
        data_ = super().get()
        if self.view2d is not None:
            data_.update({
                "v2d_dataslot" : self.view2d.get()
            })
        return data_

    def set(self, data):
        """Add the metavidget setter to the basic set"""

        data_ = deepcopy(data)
        v2d_data = None
        if "v2d_dataslot" in data_:
            v2d_data = deepcopy(data_["v2d_dataslot"])
            del data_["v2d_dataslot"]
        
        super().set(data_)

        if self.view2d is not None:
            self.view2d.set(v2d_data)