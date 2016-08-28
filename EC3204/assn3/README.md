 ASSN3: Lowering program representations

Goals. In this assignment, you will go through an experience of (1) analyzing an abstract syntax tree to bind identifiers to functions and variables using a symbol table, (2) transforming an abstract syntax tree into a tuple-based intermediate representation, and (3) performing a top-down instruction selection using the maximal munch approach.

DO. First, read and understand the assn3.py template program to understand how abstract syntax trees and tuple-based intermediate representations are encoded as a combination of lists, dictionaries, tuples, strings, and integers in Python. Second, insert your code into the places in the template program that call the TBI function so that your completed program passes the testing procedure at the main function. Third, design and document a set of instruction selection rules so that the completed program generates the expected output.

DON'T. Do not hardcode your program for the particular input given in the template file. Reaching a point where your program works for the input in the template file is important, but your code must be general enough to work for a variety of input programs.

Template files. You are given the following template files to begin with:

    README.txt: the documentation file
    assn3.py: the template file

The template files are located at /class/ec3204/2015/assn3 in the cs Linux server.

Turning in. Turn in the following files:

    README.txt: the documentation file
    rules.txt: the documentation of your instruction selection rules
    assn3.py: your program derived from the template file

