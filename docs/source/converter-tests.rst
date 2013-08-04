==========================
iptables-converter - tests
==========================

Untested software, that means software which isn't accompanied by automated 
functional tests, is assumed to be broken by design. As iptables-converter is 
written in python, use of the popular unittests is done for your convienience. 

Two testclasses are build: Chains_Test and Tables_Test accordingly to the
two classes from which the iptables-converter script is build from.

Runing the tests with nosetests::

   nosetests  --with-coverage
   ....................
   Name                 Stmts   Miss  Cover   Missing
   --------------------------------------------------
   iptables_converter     174     14    92%   226-239, 243-244
   ----------------------------------------------------------------------
   Ran 20 tests in 0.038s
   
   OK

The untested lines are the following::

   226	    usage = "usage:  %prog --help | -h \n\n\t%prog: version 0.9"
   227	    usage = usage + "\tHave Fun!"
   228	    parser = OptionParser(usage)
   229	    parser.disable_interspersed_args()
   230	    parser.add_option("-s", "", dest="sourcefile",
   231	                      help="file with iptables commands, default: rules\n")
   232	    (options, args) = parser.parse_args()
   233	    hlp = "\n\tplease use \"--help\" as argument, abort!\n"
   234	    if options.sourcefile is None:
   235	        options.sourcefile = "rules"
   236	    sourcefile = options.sourcefile
   237	
   238	    chains = Tables(sourcefile)
   239	    chains.table_printout()

and::

   243	    main()
   244	    sys.exit(0)




Chains_Test(unittest.TestCase)
==============================

The tests are enumerated to assure a predefined sequence of evaluating for 
cosmetical reason.

1. A tables group is build first, filter is choosen. The predfined chains
   are given as parameter to the chains object, then their existance and
   the default policy is prooved.

2. Setting policy drop into the filter chains is prooved for each chain,
   an invalid policy keyword is tried and exeption raising is pooved.

3. Append a rule (a valid iptables-statment) into each chain, try to 
   use an invalid filter group and the exception raising for that.

4. Insert rules and then flush them, proof emptiness. Then check exception
   raising for flushing an invalid filter group

5. Create a userdefind chain and verify existance in the objects dictionay.
   Check exception raising on creating a predefined chain.

6. Inserting a rule into an empty chain necessarily fails, exception is verified.

7. Inserting a rule into a nonexisting chain fails with exception.

8. Inserting a rule into a nonempty chain works and is verified.

9. Appending three rules to a chain works and their existance in chain 
   object dictionary is prooved.

10. Try to remove a predefined chain raises exception.

11. This test is removed (commented) for reason of practicability. 
    It's intention was, to check if removal of a nonexisting chain raises 
    exception. The code in the chain object is commented as well, as it is 
    needed to achieve a clean status of the chains from any status. So it 
    was not a good idea to raise an exception just for completeness.

12. Creation and successful removal of an userdefined chain.

13. Just look if an illegal command raises an exception.


Tables_Test(unittest.TestCase)
==============================

1.  Create a Tables object and verify the completeness of all the predefined 
    chains.

2.  Verify correctness of a given iptables -t nat command.

3.  Verify correctness of a given iptables -t mangle command.

4.  Verify correctness of a given iptables -t raw command.

5.  Inserting a rule into a nonexisting chain raises exception.

6.  Try to read a nonexisting file raises exception.

7.  Read file reference-one and verify result.

8.  Read a  file without iptables commands and verify result.
