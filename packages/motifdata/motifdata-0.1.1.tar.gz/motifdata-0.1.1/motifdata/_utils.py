import re
import numpy as np
from io import TextIOBase
from ._Motif import Motif

__version_regex = re.compile("^MEME version ([0-9]+)")
__background_regex = re.compile( "^Background letter frequencies(?: \(from (.+)\))?")
__background_sum_error = 0.00001
__pfm_header_regex = re.compile("^letter-probability matrix:(?: alength= ([0-9]+))?(?: w= ([0-9]+))") 

def _parse_version(line: str) -> str:
    match = re.match(__version_regex, line)
    if match:
        return match.group(1)
    else:
        raise RuntimeError("Minimal MEME file missing version string on first line")

def _parse_alphabet(line: str) -> str:
    if line.startswith("ALPHABET "):
        raise NotImplementedError("Alphabet definitions not supported")
    elif line.startswith("ALPHABET= "):
        return line.rstrip()[10:]
    else:
        raise RuntimeError("Unable to parse alphabet line")

def _parse_strands(line: str) -> str:
    strands = line.rstrip()[9:]
    if not ((strands == "+") or (strands == "+ -")):
        raise RuntimeError("Invalid strand specification")
    else:
        return strands

def _parse_background(line: str, handle: TextIOBase) -> str:
    match = re.match(__background_regex, line)
    if match:
        if match.group(1) is not None:
            background_source = match.group(1)
    else:
        raise RuntimeError("Unable to parse background frequency line")

    background = {}
    line = handle.readline()
    while line:
        if (not line.rstrip()) or line.startswith("MOTIF"):
            if (abs(1 - sum(background.values())) <= __background_sum_error):
                return line, background
            else:
                raise RuntimeError("Background frequencies do not sum to 1")
        else:
            line_freqs = line.rstrip().split(" ")
            if len(line_freqs) % 2 != 0:
                raise RuntimeError("Invalid background frequency definition")
            for residue, freq in zip(line_freqs[0::2], line_freqs[1::2]):
                background[residue] = float(freq)
        line = handle.readline()

def _parse_motif(line: str, handle: TextIOBase) -> str:
    
    # parse motif identifier
    line_split = line.rstrip().split(" ")
    if (len(line_split) < 2) or (len(line_split) > 3):
        raise RuntimeError("Invalid motif name line")
    motif_identifier = line_split[1]
    motif_name = line_split[2] if len(line_split) == 3 else None
    
    # parse letter probability matrix header
    line = handle.readline()
    if not line.startswith("letter-probability matrix:"):
        raise RuntimeError(
            "No letter-probability matrix header line in motif entry"
        )
    match = re.match(__pfm_header_regex, line)
    if match:
        motif_alphabet_length = (
            int(match.group(1)) if match.group(1) is not None else None
        )
        motif_length = int(match.group(2)) if match.group(2) is not None else None
    else:
        raise RuntimeError("Unable to parse letter-probability matrix header")
    
    # parse letter probability matrix
    line = handle.readline()
    pfm_rows = []
    while line:
        line_split = line.rstrip().split()
        if motif_alphabet_length is None:
            motif_alphabet_length = len(line_split)
        elif motif_alphabet_length != len(line_split):
            raise RuntimeError(
                "Letter-probability matrix row length doesn't equal alphabet length"
            )
        pfm_row = np.array([float(s) for s in line_split])
        pfm_rows.append(pfm_row)
        line = handle.readline()

        if (line.strip() == "") or line.startswith("MOTIF") or line.startswith("URL"):
            pfm = np.stack(pfm_rows)
            if motif_length is None:
                motif_length = pfm.shape[0]
            elif motif_length != pfm.shape[0]:
                raise RuntimeError(
                    "Provided motif length is not consistent with the letter-probability matrix shape"
                )
            consensus = decode_seq(_token2one_hot(pfm.argmax(axis=1)))
            motif = Motif(
                identifier=motif_identifier,
                pfm=pfm,
                consensus=consensus,
                alphabet_length=motif_alphabet_length,
                length=motif_length,
                name=motif_name
            )
            return motif

DNA = ["A", "C", "G", "T"]
RNA = ["A", "C", "G", "U"]
COMPLEMENT_DNA = {"A": "T", "C": "G", "G": "C", "T": "A"}
COMPLEMENT_RNA = {"A": "U", "C": "G", "G": "C", "U": "A"}

def _get_vocab(vocab):
    if vocab == "DNA":
        return DNA
    elif vocab == "RNA":
        return RNA
    else:
        raise ValueError("Invalid vocab, only DNA or RNA are currently supported")

# exact concise
def _get_index_dict(vocab):
    """
    Returns a dictionary mapping each token to its index in the vocabulary.
    """
    return {i: l for i, l in enumerate(vocab)}

def _token2one_hot(tvec, vocab="DNA", fill_value=None):
    """
    Converts an L-vector of integers in the range [0, D] into an L x D one-hot
    encoding. If fill_value is not None, then the one-hot encoding is filled
    with this value instead of 0.

    Parameters
    ----------
    tvec : np.array
        L-vector of integers in the range [0, D]
    vocab_size : int
        D
    fill_value : float, optional
        Value to fill the one-hot encoding with. If None, then the one-hot
    """
    vocab = _get_vocab(vocab)
    vocab_size = len(vocab)
    arr = np.zeros((vocab_size, len(tvec)))
    tvec_range = np.arange(len(tvec))
    tvec = np.asarray(tvec)
    arr[tvec[tvec >= 0], tvec_range[tvec >= 0]] = 1
    if fill_value is not None:
        arr[:, tvec_range[tvec < 0]] = fill_value
    return arr.astype(np.int8) if fill_value is None else arr.astype(np.float16)

# modified dinuc_shuffle
def _one_hot2token(one_hot, neutral_value=-1, consensus=False):
    """
    Converts a one-hot encoding into a vector of integers in the range [0, D]
    where D is the number of classes in the one-hot encoding.

    Parameters
    ----------
    one_hot : np.array
        L x D one-hot encoding
    neutral_value : int, optional
        Value to use for neutral values.
    
    Returns
    -------
    np.array
        L-vector of integers in the range [0, D]
    """
    if consensus:
        return np.argmax(one_hot, axis=0)
    tokens = np.tile(neutral_value, one_hot.shape[1])  # Vector of all D
    seq_inds, dim_inds = np.where(one_hot.transpose()==1)
    tokens[seq_inds] = dim_inds
    return tokens

def _sequencize(tvec, vocab="DNA", neutral_value=-1, neutral_char="N"):
    """
    Converts a token vector into a sequence of symbols of a vocab.
    """
    vocab = _get_vocab(vocab) 
    index_dict = _get_index_dict(vocab)
    index_dict[neutral_value] = neutral_char
    return "".join([index_dict[i] for i in tvec])

def decode_seq(arr, vocab="DNA", neutral_value=-1, neutral_char="N"):
    """Convert a single one-hot encoded array back to string"""
    return _sequencize(
        tvec=_one_hot2token(arr, neutral_value),
        vocab=vocab,
        neutral_value=neutral_value,
        neutral_char=neutral_char,
    )
