import numpy as np
from typing import Optional, Dict, Iterator


class Motif:
    """A class for storing motif information.

    Attributes:
        identifier (str): The identifier for the motif.
        pfm (np.ndarray): The position frequency matrix for the motif.
        consensus (str): The consensus sequence for the motif.
        length (int): The length of the motif.
        alphabet_length (int, optional): The length of the alphabet used to represent the motif. Defaults to None.
        name (str, optional): The name of the motif. Defaults to None.

    Adapted from https://github.com/tobjores/Synthetic-Promoter-Designs-Enabled-by-a-Comprehensive-Analysis-of-Plant-Core-Promoters/blob/main/CNN/CNN_train%2Bevaluate.ipynb
    """

    def __init__(
        self,
        identifier: str,
        pfm: np.ndarray,
        consensus: str,
        length: int,
        alphabet_length: int = None,
        name: Optional[str] = None,
    ):
        self.identifier = identifier
        self.pfm = pfm
        self.consensus = consensus
        self.alphabet_length = alphabet_length
        self.length = length
        self.name = name

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        output = "Motif %s" % self.identifier
        if self.name is not None:
            output += " (%s)" % self.name
        output += " with %d positions" % (
            self.length,
        )
        return output

    def __repr__(self) -> str:
        return self.__str__()

class MotifSet:
    """Stores a set of Motifs.

    Attributes:
        motifs (Dict[str, Motif]): A dictionary of motifs, where the keys are the motif identifiers and the values are Motif objects.
        alphabet (str, optional): The alphabet used to represent the motifs. Defaults to None.
        version (str, optional): The version of the motif set. Defaults to None.
        strands (str, optional): The strands used to represent the motifs. Defaults to None.
        background (str, optional): The background used to represent the motifs. Defaults to None.
        background_source (str, optional): The source of the background used to represent the motifs. Defaults to None.

    Adapted from https://github.com/tobjores/Synthetic-Promoter-Designs-Enabled-by-a-Comprehensive-Analysis-of-Plant-Core-Promoters/blob/main/CNN/CNN_train%2Bevaluate.ipynb
    MEME format: http://meme-suite.org/doc/meme-format.html
    """

    def __init__(
        self,
        motifs: Dict[str, Motif] = {},
        alphabet: Optional[str] = None,
        version: Optional[str] = None,
        strands: Optional[str] = None,
        background: Optional[str] = None,
        background_source: Optional[str] = None,
    ) -> None:
        self.motifs = motifs
        self.alphabet = alphabet
        self.version = version
        self.strands = strands
        self.background = background
        self.background_source = background_source

    def add_motif(self, motif: Motif) -> None:
        """
        Adds a motif to the motif set.

        Args:
            motif (Motif): The motif to add.
        """
        self.motifs[motif.identifier] = motif

    def __str__(self) -> str:
        """
        Returns a string representation of the motif set.

        Returns:
            str: A string representation of the motif set.
        """
        return "MotifSet with %d motifs" % len(self.motifs)

    def __repr__(self) -> str:
        """
        Returns a string representation of the motif set.

        Returns:
            str: A string representation of the motif set.
        """
        return self.__str__()

    def __len__(self) -> int:
        """
        Returns the number of motifs in the motif set.

        Returns:
            int: The number of motifs in the motif set.
        """
        return len(self.motifs)

    def __getitem__(self, key: str) -> Motif:
        """
        Returns the motif with the given identifier.

        Args:
            key (str): The identifier of the motif to retrieve.

        Returns:
            Motif: The motif with the given identifier.

        Raises:
            KeyError: If the motif with the given identifier is not in the motif set.
        """
        return self.motifs[key]

    def __iter__(self) -> Iterator[Motif]:
        """
        Returns an iterator over the motifs in the motif set.

        Returns:
            Iterator[Motif]: An iterator over the motifs in the motif set.
        """
        return iter(self.motifs.values())

    def __contains__(self, key: str) -> bool:
        """
        Returns whether the motif set contains a motif with the given identifier.

        Args:
            key (str): The identifier of the motif to check for.

        Returns:
            bool: Whether the motif set contains a motif with the given identifier.
        """
        return key in self.motifs
    