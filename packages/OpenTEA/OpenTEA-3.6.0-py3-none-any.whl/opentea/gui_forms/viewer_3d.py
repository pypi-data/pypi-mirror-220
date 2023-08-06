import os
import subprocess
from tkinter import ttk

from loguru import logger
import yaml
from tiny_3d_engine.engine import Engine3D
from tiny_3d_engine.scene3d import load_file_as_scene

from opentea.gui_forms.constants import PARAMS
#from opentea.gui_forms.root_widget import OTRoot
# todo : move this into root module

def add_viewer_3d(otroot):
    title = "3D view"
    view3d_fr = ttk.Frame(otroot.notebook, name=title)
    otroot.notebook.add(view3d_fr, text=title)
    viewer = Viewer3D(
        view3d_fr,
        otroot,
        background=PARAMS["bg_dark"])
    return viewer

class Viewer3D(Engine3D):
    def __init__(self, 
            master, 
            otroot,
            background='black'):
        super().__init__(
            root=master,
            width=1000,
            height=700,
            background=background
        )
        self.otroot = otroot

    def update_view(self, script: str):
        """execute a script for 3d view update"""
        # TODO: clean tmp files

        full_script = os.path.join(PARAMS["calling_dir"], script)
        logger.debug("3D-view : Executing in subprocess ", full_script)

        try:
            scene_file = ".scene_from_gui.geo"
            self.dump(".scene_from_gui")
        except ValueError:
            scene_file = "no_scene"

        dump = yaml.dump(self.otroot.get(), default_flow_style=False)

        with open(".dataset_from_gui.yml", "w") as fout:
            fout.writelines(dump)

        subp = subprocess.run(
            ["python", full_script, ".dataset_from_gui.yml", scene_file],
            # capture_output=True,  # only for python 3.7
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

        if not os.path.exists(".scene_to_gui.geo"):
            logger.debug('No scene: no 3D update.')
            return True

        if subp.returncode == 0:
            new_scene = load_file_as_scene(".scene_to_gui.geo")
            logger.debug("3D update...")
            logger.debug("\n" + subp.stdout.decode("utf-8"))
            self.update(new_scene)
            self.render()
            return True  # success

        else:
            msg_err = "Return code : " + str(subp.returncode)
            msg_err += "\n" + "### STD-OUT / ERR ###" + "\n"
            msg_err += subp.stdout.decode("utf-8")
            logger.warning("3D update failed")
            logger.warning(msg_err)

            return False