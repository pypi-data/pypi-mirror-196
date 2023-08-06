#!/usr/bin/env python3
# coding: utf-8
# SPDX-License-Identifier: MIT
"""Testing MAC addresses."""
import pytest
import letterbomb

TEST_MAC = "ECC40DFB90B9"
DOLPHIN_MAC = "0017AB999999"
BAD_MAC = "000000000000"


def test_bad_length():
    with pytest.raises(letterbomb.BadLengthMACError) as e:
        letterbomb.write(f"{TEST_MAC}FF", "U", False)
    assert not isinstance(e, letterbomb.BadLengthMACError)


def test_dolphin_mac():
    with pytest.raises(letterbomb.EmulatedMACError) as e:
        letterbomb.write(DOLPHIN_MAC, "U", False)
    assert not isinstance(e, letterbomb.EmulatedMACError)


def test_invalid_mac():
    with pytest.raises(letterbomb.InvalidMACError) as e:
        letterbomb.write(BAD_MAC, "U", False)
    assert not isinstance(e, letterbomb.InvalidMACError)


def test_ok_mac():
    assert letterbomb.write(TEST_MAC, "U", False)
