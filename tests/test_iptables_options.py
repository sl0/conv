import pytest
import sys
from iptables_conv.iptables_converter import my_options, main


def test_01_iptables_converter_option_h(capsys):
    """ check ip6tablesmy_options returns help text
    """
    sys.argv = ['ip6tables-converter', '-h', ]
    with pytest.raises(SystemExit) as execinfo:
        options = my_options()
        print(':' + str(options) + ':')

    out, err = capsys.readouterr()

    assert ': SystemExit' in str(execinfo)

    items = ['Options', 'SOURCEFILE', 'DESTFILE', 'version',
             '--help', '--sloppy', 'Have Fun!', ]

    for item in items:
        assert item in out

    assert len(err) == 0


def test_02_iptables_converter_option_s():
    """ check my_options sloppy and sourcefile name returning
    """
    sys.argv = ['iptab', '-s', 'reference-one', '--sloppy', ]
    options = my_options()

    assert options == {'destfile': None,
                       'sourcefile': 'reference-one',
                       'sloppy': True}


def test_03_iptables_converter_option_d():
    """ check my_options, destfile name returning
    """
    sys.argv = ['ip6tab', '-d', 'one', ]
    options = my_options()

    assert options == {'destfile': 'one',
                       'sourcefile': None,
                       'sloppy': False}


def test_04_iptables_converter_option_sd():
    """ check my_options returns source- and destfile
    """
    sys.argv = ['bla', '-s', 'one', '-d', 'two']
    options = my_options()

    assert options == {'destfile': 'two',
                       'sourcefile': 'one',
                       'sloppy': False}


def test_05_iptables_converter_main_dlft(capsys):
    """ check main behavior on default file not found
    """
    sys.argv = ['ip6tab', ]
    result = main()
    out, err = capsys.readouterr()

    assert 'Errno 2' in err
    assert 'No such file or directory:' in err
    assert 'rules' in err
    assert result == 1


def test_06_iptables_converter_main_ok(capsys):
    """ check main reads a named file
    """
    sys.argv = ['ip6tab', '-s', 'reference-one', ]
    result = main()
    out, err = capsys.readouterr()

    # print(':' + out + ':')
    assert '# generated from: reference-one' in out
    assert result == 0


def test_07_iptables_converter_main_write(capsys):
    """ check main reads and writes w/o error
    """
    sys.argv = ['ip6tab', '-s', 'reference-one', '-d', '/dev/null', ]
    result = main()
    out, err = capsys.readouterr()

    assert len(out) == 0
    assert len(err) == 0
    assert result == 0
