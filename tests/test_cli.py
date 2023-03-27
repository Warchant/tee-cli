from contextlib import contextmanager
from io import StringIO
import shlex
import sys
from unittest.mock import MagicMock, call, mock_open, patch
import pytest

from tee_cli.__main__ import main


@contextmanager
def mockstdout():
    m = MagicMock(spec=StringIO)
    try:
        old = sys.stdout
        sys.stdout = m
        yield m
    finally:
        sys.stdout = old

@patch("subprocess.Popen")
def test_success(popen: MagicMock):
    p = MagicMock()
    p.wait.return_value = 1
    p.stdout = StringIO("""\
line1
line2
line3
""")
    popen.return_value = p


    with mockstdout() as m:
        with patch("builtins.open", mock_open(read_data="data")) as mf:
            with pytest.raises(SystemExit) as e:
                main(shlex.split("tee-cli -o log make"))
                e.value.code == p.wait.return_value
            mf.assert_called_with("log", "w")

        assert m.write.call_count == 3
        m.write.assert_has_calls([
            call("line1\n"),
            call("line2\n"),
            call("line3\n"),
        ])
        assert m.flush.call_count == 3
