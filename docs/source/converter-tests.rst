==========================
iptables-converter - tests
==========================

Untested software, that means software which isn't accompanied by automated
functional tests, is assumed to be broken by design. As iptables-converter is
written in python, use of the popular unittests is done for your convienience.
The unittests were developed and run by nose, which later have been replaced
by pytest. The advantages of pytest over nose are much simpler tests and less
overhead. So all newer testcases are written for pytest and thus rely on the
plain python assert statement.

Two testclasses are build: Chains_Test and Tables_Test accordingly to the
two classes from which the iptables-converter module and script is build from.

Basic usage
-----------

Lets see, how to run the tests within the source-tree by just calling
pytest::


    $ pytest
    ========================== test session starts ==========================
    platform linux -- Python 3.6.6, pytest-3.2.3, py-1.4.34, pluggy-0.4.0
    rootdir: /home/hans/devel/conv, inifile:
    plugins: cov-2.5.1
    collected 37 items

    tests/test_iptables_converter.py ............................
    tests/test_iptables_options.py .........

    ======================= 37 passed in 0.05 seconds =======================
    $

All tests passed. Fine.

Verbose usage
-------------

If you want to see more, just add a **-v** to
the commandline::


    $ pytest -v
    ================================ test session starts =================================
    platform linux -- Python 3.6.6, pytest-3.2.3, py-1.4.34, pluggy-0.4.0 -- /home/hans/wb/bin/python3.6
    cachedir: .cache
    rootdir: /home/hans/devel/conv, inifile:
    plugins: cov-2.5.1
    collected 37 items

    tests/test_iptables_converter.py::Chains_Test::test_01_create_a_chain_object PASSED
    tests/test_iptables_converter.py::Chains_Test::test_02_prove_policies PASSED
    tests/test_iptables_converter.py::Chains_Test::test_03_tables_names PASSED
    tests/test_iptables_converter.py::Chains_Test::test_04_flush PASSED
    tests/test_iptables_converter.py::Chains_Test::test_05_new_chain PASSED
    tests/test_iptables_converter.py::Chains_Test::test_06_new_existing_chain_fails PASSED
    tests/test_iptables_converter.py::Chains_Test::test_07_insert_rule_fail PASSED
    tests/test_iptables_converter.py::Chains_Test::test_08_insert_rule_fail PASSED
    tests/test_iptables_converter.py::Chains_Test::test_09_insert_rule_works PASSED
    tests/test_iptables_converter.py::Chains_Test::test_10_append_rule PASSED
    tests/test_iptables_converter.py::Chains_Test::test_11_remove_predef_chain PASSED
    tests/test_iptables_converter.py::Chains_Test::test_12_remove_chain PASSED
    tests/test_iptables_converter.py::Chains_Test::test_13_illegal_command PASSED
    tests/test_iptables_converter.py::Tables_Test::test_01_create_a_tables_object PASSED
    tests/test_iptables_converter.py::Tables_Test::test_02_nat_prerouting PASSED
    tests/test_iptables_converter.py::Tables_Test::test_03_mangle_table PASSED
    tests/test_iptables_converter.py::Tables_Test::test_04_raw_table PASSED
    tests/test_iptables_converter.py::Tables_Test::test_05_not_existing_chain PASSED
    tests/test_iptables_converter.py::Tables_Test::test_06_read_not_existing_file PASSED
    tests/test_iptables_converter.py::Tables_Test::test_07_read_empty_file PASSED
    tests/test_iptables_converter.py::Tables_Test::test_08_reference_one PASSED
    tests/test_iptables_converter.py::Tables_Test::test_09_shell_variables PASSED
    tests/test_iptables_converter.py::Tables_Test::test_10_shell_functions PASSED
    tests/test_iptables_converter.py::Tables_Test::test_11_reference_sloppy_one PASSED
    tests/test_iptables_converter.py::Tables_Test::test_12_create_a_tables6_object PASSED
    tests/test_iptables_converter.py::Tables_Test::test_13_re6ference_one PASSED
    tests/test_iptables_converter.py::Tables_Test::test_14_re6ference_sloppy_one PASSED
    tests/test_iptables_converter.py::test_15_tables_printout PASSED
    tests/test_iptables_options.py::test_01_iptables_converter_option_h PASSED
    tests/test_iptables_options.py::test_02_iptables_converter_option_s PASSED
    tests/test_iptables_options.py::test_03_iptables_converter_option_d PASSED
    tests/test_iptables_options.py::test_04_iptables_converter_option_sd PASSED
    tests/test_iptables_options.py::test_05_iptables_converter_main_dlft PASSED
    tests/test_iptables_options.py::test_06_iptables_converter_main_ok PASSED
    tests/test_iptables_options.py::test_07_iptables_converter_main_write PASSED
    tests/test_iptables_options.py::test_08_iptables_converter_option_dest_file PASSED
    tests/test_iptables_options.py::test_09_iptables_converter_option_source_file PASSED

    ============================= 37 passed in 0.06 seconds ==============================
    $


Code coverage
-------------

If you want to get to know something about the test-coverage, just
give pytest a try::

    $ pytest --cov=iptables_conv --cov-report=term-missing
    =============================== test session starts ================================
    platform linux -- Python 3.6.6, pytest-3.2.3, py-1.4.34, pluggy-0.4.0
    rootdir: /home/hans/devel/conv, inifile:
    plugins: cov-2.5.1
    collected 37 items

    tests/test_iptables_converter.py ............................
    tests/test_iptables_options.py .........

    ----------- coverage: platform linux, python 3.6.6-final-0 -----------
    Name                                  Stmts   Miss  Cover   Missing
    -------------------------------------------------------------------
    iptables_conv/__init__.py                 8      0   100%
    iptables_conv/iptables_converter.py     230      7    97%   28-29, 72, 129-131, 314
    -------------------------------------------------------------------
    TOTAL                                   238      7    97%


    ============================ 37 passed in 0.10 seconds =============================
    $

If you like to have a look into the sources, you will find the
tests directory. Therein all the tests reside. I hope they are
self explaining.

testrunner
----------

To simply run the tests, **setup.py** has a test target::

    $ python setup.py test
       ...
    $

This runs flake8 and pytest.
If you prefer less typing::

    $ pytest
       ...
    $

Or, possibly the best way of doing is the following super power.

Check tests, syntax and style
-----------------------------

For your convenience, a **tox.ini** is prepared.
Give tox a try to check altogether in one single run:

    - python2.7
    - python3.5
    - python3.6
    - flake8
    - docs

