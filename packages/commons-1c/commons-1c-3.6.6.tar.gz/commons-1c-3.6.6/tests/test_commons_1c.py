# -*- coding: utf-8 -*-
import re
from pathlib import Path

import pytest

from commons_1c.platform_ import get_last_1c_exe_file_fullpath
from commons_1c.version import get_version_as_number, get_version_as_parts


def test_get_version_as_number():
    assert get_version_as_number('') == 0
    assert get_version_as_number('foo') == 0
    assert get_version_as_number('1') == 1000000000000
    assert get_version_as_number('1.1') == 1000100000000
    assert get_version_as_number('1.1.1') == 1000100010000
    assert get_version_as_number('1.1.1.1') == 1000100010001


def test_get_version_as_parts():
    assert get_version_as_parts('') == []
    assert get_version_as_parts('foo') == []
    assert get_version_as_parts('1') == ['1']
    assert get_version_as_parts('1.1') == ['1', '1']
    assert get_version_as_parts('1.1.1') == ['1', '1', '1']
    assert get_version_as_parts('1.1.1.1') == ['1', '1', '1', '1']


def test_get_last_1c_exe_file_fullpath_1():
    file_fullpath = get_last_1c_exe_file_fullpath()
    assert isinstance(file_fullpath, Path)
    assert re.match(r'(?i)c:\\Program Files \(x86\)\\1cv8\\\d+\.\d+\.\d+\.\d+\\bin\\1cv8\.exe', str(file_fullpath))


def test_get_last_1c_exe_file_fullpath_2() -> None:
    with pytest.raises(Exception) as e:
        get_last_1c_exe_file_fullpath(config_file='bla.cfg')
        assert re.match(r'1CEStart.cfg file does not exist', str(e))
