import numpy as np
from typing import List, Dict, Union, Optional, Iterator
import Bio
from ._Motif import Motif, MotifSet
from ._utils import _token2one_hot, decode_seq
from ._transform import ppms_to_pwms

def to_biopython(
    motif_set: MotifSet,
    **kwargs
):
    """Convert MotifSet object to list of Bio.motif.Motif objects
    
    Parameters
    ----------
    motif_set : MotifSet
        MotifSet object
    **kwargs
        Additional arguments to pass to Bio.motif.jaspar.Motif constructor
    """
    biopython_motifs = []
    alphabet = motif_set.alphabet
    for motif in motif_set:
        pfm = motif.pfm
        motif_counts = {a: pfm[:, i] for i, a in enumerate(alphabet)}
        biomotif = Bio.motifs.jaspar.Motif(
            motif.identifier,
            motif.name,
            counts=motif_counts,
            alphabet=alphabet,
            **kwargs
        )
        biopython_motifs.append(biomotif)
    return biopython_motifs

def from_biopython(
    biopyhon_motifs: List[Bio.motifs.jaspar.Motif],
    verbose=False
):
    """Convert Bio.motif.Motif objects to MotifSet object

    Parameters
    ----------
    biopyhon_motif : List[Bio.motifs.jaspar.Motif]
        BioPython motif objects in list, can be nested
    verbose : bool, optional
        whether to print out duplicate identifiers that are skipped, by default False
    Returns
    -------
    MotifSet
        MotifSet object
    """
    # flatten list of lists if exists
    if isinstance(biopyhon_motifs[0], list):
        biopyhon_motifs = [item for sublist in biopyhon_motifs for item in sublist]
    motifs = {}
    for biopyhon_motif in biopyhon_motifs:
        norm_cnts = biopyhon_motif.counts.normalize()
        pfm = np.array([list(val) for val in norm_cnts.values()]).T
        curr_motif = Motif(
            identifier=biopyhon_motif.matrix_id,
            pfm=pfm,
            consensus=str(biopyhon_motif.consensus),
            alphabet_length=len(biopyhon_motif.alphabet),
            length=biopyhon_motif.length,
            name=biopyhon_motif.name,
        )
        if curr_motif.identifier in motifs:
            if verbose:
                print(f"Duplicate motif identifier: {curr_motif.name}, skipping")
        else:
            motifs[curr_motif.identifier] = curr_motif
    return MotifSet(motifs=motifs)

def to_pymemesute(
    motif_set: MotifSet,
):
    """TODO: Convert MotifSet object to list of pymemesuite.common.Motif objects
    
    Parameters
    ----------
    motif_set : MotifSet
        MotifSet object
    
    Returns
    -------
    list
        list of pymemesuite.common.Motif objects
    """

    pass

def from_pymemesuite(
    pymemesuite_motifs,
):
    """
    Convert list of pymemesuite.common.Motif objects to MotifSet object

    Parameters
    ----------
    pymemesuite_motifs:
        list, list of pymemesuite.common.Motif objects
    
    Returns
    -------
    MotifSet
    """
    motifs = {}
    for motif in pymemesuite_motifs:
        motif = Motif(
            identifier=motif.accession.decode("utf-8"),
            pfm=np.array(motif.frequencies),
            consensus=motif.consensus,
            name=motif.name.decode("utf-8"),
            length=motif.width
        )
        motifs[motif.identifier] = motif
    return MotifSet(motifs=motifs) 

def from_kernel(
    kernel: np.ndarray,
    identifiers: List[str] = None,
    names: List[str] = None,
    alphabet: str = "ACGT",
    bg: Optional[Dict[str, float]] = None,
    strands: str = "+ -",
):
    """Convert array of motif weights to MotifSet object
    
    Parameters
    ----------
    kernel : np.ndarray
        array of motif weights, shape (n_filters, n_channels, len_filter)
    identifiers : List[str], optional
        list of motif identifiers, by default None
    names : List[str], optional
        list of motif names, by default None
    alphabet : str, optional
        alphabet of motifs, by default "ACGT"
    bg : Optional[Dict[str, float]], optional
        background distribution of motifs, by default None
    strands : str, optional
        strands of motifs, by default "+ -"
    
    Returns
    -------
    MotifSet
        MotifSet object
    """
    n_filters, n_channels, len_filter = kernel.shape
    identifiers = identifiers or [f"filter_{i}" for i in range(n_filters)]
    names = names or [f"filter_{i}" for i in range(n_filters)]
    motifs = {}
    for i in range(n_filters):
        name = names[i]
        pfm = kernel[i].T
        consensus = decode_seq(_token2one_hot(pfm.argmax(axis=1)))
        motifs[name] = Motif(
            identifier=identifiers[i],
            name=names[i],
            pfm=pfm,
            consensus=consensus,
            length=len_filter,
            alphabet_length=len(alphabet)
        )
    return MotifSet(
        motifs=motifs,
        alphabet=alphabet,
        version="5",
        background=bg,
        strands=strands
    )

def to_kernel(
    motif_set,
    kernel= None,
    convert_to_pwm=True,
    divide_by_bg=False,
    motif_align="center",
    kernel_align="center"
):
    """Convert MotifSet object to a torch Tensor
    
    TODO make this return just a numpy array, so we can avoid torch altogether. init function can handle that
    
    This is often useful for initializing the weights of a convolutional layer with motifs.
    
    Parameters
    ----------
    motif_set : md.MotifSet
        The motif set to convert to a tensor
    tensor : torch.Tensor, optional
        A tensor to convert to a kernel, by default None
    size : tuple, optional
        The size of the kernel to initialize, by default None
    convert_to_pwm : bool, optional
        Whether to convert the motifs to PWMs, by default True
    motif_align : str, optional
        If the motif is longer than the kernel, what part of the motif to take
        (left, center, right), by default "center". If the motif length is odd
        the extra base will right aligned.
    kernel_align : str, optional
        If the kernel is longer than the motif, what part of the kernel to take
        (left, center, right), by default "center". If the kernel length is odd
        the extra base will right aligned.
    """

    # Check if torch is installed
    try:
        import torch
    except ImportError:
        raise ImportError("Please install PyTorch to use this function (pip install torch))")

    # Check if kernel is a tensor with 3 dimensions
    if len(kernel.shape) != 3:
        raise RuntimeError("Kernel matrix size must be a tuple of length 3")

    # Get the dimensions of the kernel
    N, A, L = kernel.shape
    
    # 
    motifs = motif_set.motifs
    for i, motif_id in enumerate(motifs):
        motif = motifs[motif_id]
        curr_kernel = motif.pfm
        if convert_to_pwm:
            curr_kernel = ppms_to_pwms(curr_kernel)
        if divide_by_bg:
            curr_kernel = curr_kernel / 0.25
        if len(curr_kernel) > L:
            if motif_align == "left":
                curr_kernel = curr_kernel[:L, :]
            elif motif_align == "center":
                start = (len(curr_kernel) - L) // 2
                curr_kernel = curr_kernel[start : start + L, :]
            elif motif_align == "right":
                curr_kernel = curr_kernel[-L:, :]
            kernel[i, :, :] = torch.tensor(curr_kernel, dtype=torch.float32).transpose(0, 1)
        else:
            if kernel_align == "left":
                kernel[i, :, : len(curr_kernel)] = torch.tensor(curr_kernel, dtype=torch.float32).transpose(0, 1)
            elif kernel_align == "center":
                start = (L - len(curr_kernel)) // 2
                kernel[i, :, start : start + len(curr_kernel)] = torch.tensor(curr_kernel, dtype=torch.float32).transpose(0, 1)
            elif kernel_align == "right":
                kernel[i, :, -len(curr_kernel) :] = torch.tensor(curr_kernel, dtype=torch.float32).transpose(0, 1)
    return kernel

