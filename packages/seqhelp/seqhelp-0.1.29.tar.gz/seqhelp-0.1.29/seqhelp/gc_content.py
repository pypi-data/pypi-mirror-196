import functools
import gzip
import json
from collections import Counter
from pathlib import Path

import numba
import numpy as np
from Bio import SeqIO

from .common import cosine_distance


@functools.cache
def cache_gc_content(
    aid, path: Path, cache_dir: Path = Path("../cache/gc-content")
) -> np.ndarray:
    cache_dir.mkdir(exist_ok=True, parents=True)
    cache_path = (cache_dir / f"{aid}-gc").with_suffix(".json")

    if cache_path.is_file():
        with cache_path.open("r") as f:
            gc = json.load(f)
    else:
        if path.suffix == ".gz":
            with gzip.open(path, "rt") as f:
                records = SeqIO.parse(f, "fasta")
                seq = "".join([str(rec.seq) for rec in records])
        else:
            with path.open("r") as f:
                records = SeqIO.parse(f, "fasta")
                seq = "".join([str(rec.seq) for rec in records])

        gc = Counter(seq)
        with cache_path.open("w") as f:
            json.dump(gc, f)

    gc_ = np.array([gc.get(c, gc.get(c.lower(), 0)) for c in "ACGT"])
    return gc_


@numba.njit
def get_gc_diff(left_gc, right_gc):
    gc_i_a = left_gc / np.sum(left_gc)

    gc_j_a = right_gc / np.sum(right_gc)

    return cosine_distance(gc_i_a, gc_j_a)


class GC:
    """
    Calculate GC distance angular cosine distance
    """

    def __init__(self, path_dict):
        """
        Parameters
        ----------
        path_dict: Dict[str, Path]
            Dictionary for paths, to load sequences when needed.
        """
        self.path_dict = path_dict

    def distance(self, left: str, right: str) -> float:
        left_gc = cache_gc_content(left, self.path_dict[left])
        right_gc = cache_gc_content(right, self.path_dict[right])

        return get_gc_diff(left_gc, right_gc)

    def transform(self, aid: str) -> np.ndarray:
        """Transforms the aid into the corresponding array.

        Parameters
        ----------
        aid: str
            Aid to transform

        Returns
        -------
        np.ndarray
            Array of gc content, in a deterministic order
        """
        gc_array = cache_gc_content(aid, self.path_dict[aid])
        gc_array = gc_array / np.sum(gc_array)
        return gc_array
