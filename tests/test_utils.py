#!/usr/bin/env python3

__doc__ = """Test utility scripts"""

import pytest

from elastica.utils import isqrt, perm_parity, grouper
from itertools import chain
from numpy.random import randint


def test_isqrt_with_zero():
    assert isqrt(0) == 0


# Splitting tests for small and big
# integers as this should be the common use case
@pytest.mark.parametrize("inp, out", [(1, 1), (4, 2), (9, 3)])
def test_isqrt_small_numbers(inp, out):
    assert isqrt(inp) == out


@pytest.mark.parametrize("inp, out", [(56 ** 2, 56), (98 ** 2, 98)])
def test_isqrt_large_numbers(inp, out):
    assert isqrt(inp) == out


@pytest.mark.parametrize("seq", [list(range(3)), [2, 0, 1], [1, 2, 3]])
def test_perm_parity_correctness_on_even_sequences(seq):
    assert perm_parity(seq) == 1


@pytest.mark.parametrize("seq", [[1, 0, 2], [2, 1, 0], [4, 3, 2, 1]])
def test_perm_parity_correctness_on_odd_sequences(seq):
    assert perm_parity(seq) == -1


@pytest.mark.parametrize("chunksize", [2, 3])
def test_grouper_correctness_for_perfect_sequences(chunksize):
    """ Checks correctness when the length of the sequence is divisible
    by chunksize

    Parameters
    ----------
    chunksize : granularity in which the sequence is grouped

    Returns
    -------

    """
    # length of the sequence
    # max size expected for symplectic algorithms does not exceed five
    seq_len = chunksize * randint(1, 5)
    correct_seq = [None] * seq_len

    # Fill in the sequence with pseudo-random numbers, always of perfect size
    for i_seq in range(seq_len):
        start = randint(1, 10)
        # grouper yields a tuple
        correct_seq[i_seq] = (*range(start, start + chunksize),)

    # We pass the expanded sequence out using chain*
    test_seq = list(grouper(list(chain(*correct_seq)), chunksize))

    assert test_seq == correct_seq


@pytest.mark.parametrize("chunksize", [2, 3])
def test_grouper_correctness_for_imperfect_sequences(chunksize):
    """ Checks correctness when the length of the sequence is NOT divisible
    by chunksize

    Parameters
    ----------
    chunksize : granularity in which the sequence is grouped

    Returns
    -------

    """
    # length of the sequence
    # max size expected for symplectic algorithms does not exceed five
    seq_len = chunksize * randint(1, 5)
    correct_seq = [None] * seq_len

    # Fill in the sequence with pseudo-random numbers, always of perfect size
    # Except the last one where we introduce imperfection
    for i_seq in range(seq_len - 1):
        start = randint(1, 10)
        # grouper yields a tuple
        correct_seq[i_seq] = (*range(start, start + chunksize),)
    # Imperfect sequence not divisivle by chunksize
    correct_seq[-1] = (*range(start, start + chunksize - 1),)

    # We pass the expanded sequence out using chain*
    test_seq = list(grouper(list(chain(*correct_seq)), chunksize))

    assert test_seq == correct_seq
