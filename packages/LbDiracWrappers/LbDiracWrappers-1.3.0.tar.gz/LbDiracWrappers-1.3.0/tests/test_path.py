###############################################################################
# (c) Copyright 2023 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import pytest

from LbDiracWrappers import get_default_path


def test_plain():
    assert "/bin" in get_default_path()


@pytest.mark.parametrize(
    "bash_output,expected_path",
    [
        ["", None],
        ["\n\n\n", None],
        ["PATH=abc\n", "abc"],
        ["PATH=abc", "abc"],
        ["abc\nPATH=abc\ndef", "abc"],
        ["PATHabc\ndefs\n\nss", None],
    ],
)
def test_monkeypatched(monkeypatch, bash_output, expected_path):
    monkeypatch.setattr("subprocess.check_output", lambda *x, **y: bash_output)
    assert get_default_path() == expected_path
