from tkinter import ttk
from tiny_2d_engine.main import Acquisition2D
#from opentea.gui_forms.root_widget import OTRoot
# todo : move this into root module


def add_viewer_2d(otroot):
    """Injection of a viewer 2D to opentea"""
    title = "2D dialog"
    view2d_fr = ttk.Frame(otroot.notebook, name=title)
    otroot.notebook.add(view2d_fr, text=title)
    viewer = Viewer2D(
        view2d_fr,
        otroot,
    )
    return viewer


class Viewer2D(Acquisition2D):
    def __init__(self, master, otroot):
        super().__init__(master, standalone=True)
        self.pack( side="top")
        self.otroot = otroot

    def get(self):
        print("get trigerred")
        return self.acq_canvas.as_dict()

    def set(self, data: dict):
        print("set trigerred")
        self.acq_canvas.load_dict(data)
