import functools
import gzip
import itertools
import json
from collections import defaultdict
from pathlib import Path
from typing import Final, Iterable

import numpy as np
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from tqdm import tqdm

from . import gc_content
from .common import cosine_distance

DINUCLEOTIDE_TUPLES: Final = set((n1, n2) for n1 in "ACGT" for n2 in "ACGT")
DINUCLEOTIDES: Final = [f"{n1}{n2}" for (n1, n2) in DINUCLEOTIDE_TUPLES]


def _dinucleotide_generator(record: SeqRecord) -> Iterable[tuple[str, str]]:
    return itertools.pairwise(record.seq)


@functools.cache
def cache_dinucleotides(
    aid, path: Path, cache_dir: Path = Path("../cache/dinucleotides")
):
    cache_dir.mkdir(exist_ok=True, parents=True)
    cache_path = (cache_dir / f"{aid}-dinucleotides").with_suffix(".json")

    if cache_path.is_file():
        with cache_path.open("r") as f:
            dinucleotides_ = json.load(f)
    else:
        if path.suffix == ".gz":
            with gzip.open(path, "rt") as f:
                records = SeqIO.parse(f, "fasta")
                dinucleotides_ = _count_dinucleotides(records)
        else:
            with path.open("r") as f:
                records = SeqIO.parse(f, "fasta")
                dinucleotides_ = _count_dinucleotides(records)

        with cache_path.open("w") as f:
            json.dump(dinucleotides_, f)

    return dinucleotides_


def _count_dinucleotides(records):
    dinucleotides__ = defaultdict(int)
    for rec in tqdm(
        records,
        desc="Iterating records to calculate dinucleotides",
        position=3,
        leave=False,
    ):
        for din in tqdm(
            _dinucleotide_generator(rec),
            desc=f"Iterating dinucleotides in record {rec.id}",
            position=4,
            leave=False,
            total=len(rec.seq) - 1,
        ):
            dinucleotides__[din] += 1
    dinucleotides_ = {
        f"{din[0]}{din[1]}": dinucleotides__[din] for din in DINUCLEOTIDE_TUPLES
    }
    return dinucleotides_


def dinucleotide_odds_ratio_cosine_distance(
    left_dinucleotides, left_gc, right_dinucleotides, right_gc
):
    left_odds_ratios = np.array(
        [
            left_dinucleotides[din]
            / (
                left_gc[_nucleotide_to_index(din[0])]
                * left_gc[_nucleotide_to_index(din[1])]
            )
            for din in DINUCLEOTIDES
        ]
    )
    left_odds_ratios = np.nan_to_num(left_odds_ratios, copy=False)
    right_odds_ratios = np.array(
        [
            right_dinucleotides[din]
            / (
                right_gc[_nucleotide_to_index(din[0])]
                * right_gc[_nucleotide_to_index(din[1])]
            )
            for din in DINUCLEOTIDES
        ]
    )
    right_odds_ratios = np.nan_to_num(right_odds_ratios, copy=False)

    return cosine_distance(left_odds_ratios, right_odds_ratios)


class Dinucleotides:
    """Calculate cosine similarity between dinucleotide odds ratios

    Dinucleotide odds ratio is as defined by Karlin and Burge in https://doi.org/10.1016/S0168-9525(00)89076-9
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
        left_gc = gc_content.cache_gc_content(left, self.path_dict[left])
        left_dinucleotides = cache_dinucleotides(left, self.path_dict[left])
        right_gc = gc_content.cache_gc_content(right, self.path_dict[right])
        right_dinucleotides = cache_dinucleotides(right, self.path_dict[right])

        return dinucleotide_odds_ratio_cosine_distance(
            left_dinucleotides, left_gc, right_dinucleotides, right_gc
        )

    def transform(self, aid: str) -> np.ndarray:
        """Transforms the aid into the corresponding array.

        Parameters
        ----------
        aid: str
            Aid to transform

        Returns
        -------
        np.ndarray
            Array of dinucleotide odds ratios, in a deterministic order
        """
        gc = gc_content.cache_gc_content(aid, self.path_dict[aid])
        dinucleotides_ = cache_dinucleotides(aid, self.path_dict[aid])
        transform_ = np.array(
            [
                dinucleotides_[din]
                / (gc[_nucleotide_to_index(din[0])] * gc[_nucleotide_to_index(din[1])])
                for din in DINUCLEOTIDES
            ]
        )
        transform_ = np.nan_to_num(transform_, copy=False)
        return transform_


def _nucleotide_to_index(nucleotide: str) -> int:
    if nucleotide == "A":
        return 0
    elif nucleotide == "C":
        return 1
    elif nucleotide == "G":
        return 2
    else:
        return 3
