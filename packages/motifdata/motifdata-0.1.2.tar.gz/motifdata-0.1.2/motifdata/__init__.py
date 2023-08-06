try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

package_name = "motifdata"
__version__ = importlib_metadata.version(package_name)

from Bio import motifs
from Bio.motifs import jaspar
from ._Motif import Motif, MotifSet
from ._io import (
    read_meme,
    read_homer,
    read_motifs,
    load_jaspar,
    read_h5,
    write_meme,
    write_homer,
    write_h5
)

from ._convert import (
    to_biopython,
    from_biopython,
    from_pymemesuite,
    to_kernel,
    from_kernel
)