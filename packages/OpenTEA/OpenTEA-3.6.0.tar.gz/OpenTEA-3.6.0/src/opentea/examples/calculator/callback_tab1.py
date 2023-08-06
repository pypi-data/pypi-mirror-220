"""Module for the first tab."""

from opentea.noob.noob import nob_get, nob_set
from opentea.process_utils import process_tab


def process_controle_existif(nob_in):
    """Update the list of dimensions."""
    nob_out = nob_in.copy()

    # update dimensions
   # ndim = nob_get(nob_in, "ndim_choice")
   # if ndim == "two":
   #     nob_set(nob_out, ["x", "y"], "req_ndim")
   # else:
   #     nob_set(nob_out, ["x", "y", "z"], "req_ndim")

    # update patches
    npatch = nob_get(nob_in, "npatches")

    list_patches = ["a1","a2","a3"]
    if npatch == 1:
        list_patches = ["p1","p2","p3","p4",]
    if npatch == 2:
        list_patches = ["p1","p3","p2","p4",]
    if npatch == 3:
        list_patches = ["p1","p2","p3"]
    if npatch == 4:
        list_patches = ["p2","p3","p4"]

    nob_set(nob_out, list_patches, "list_patches")

    return nob_out


if __name__ == "__main__":
    process_tab(process_controle_existif)
