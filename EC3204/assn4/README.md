 Register Allocation Using Liveness Analysis and Graph Coloring

Goals. In this assignment, you will go through an experience of implementing (1) a liveness analysis and (2) a coloring-based register allocator without spilling.

DO. First, read and understand the assn4.py template program to understand how intermediate representations and interference graphs are expressed as combinations of sets, lists, dictionaries, tuples, strings, and integers in Python. Second, add your code to the places that calls the TBI function to complete the template program to pass the testing procedure at the main function. Register spilling is optional in this homework assignment. The input in the template program can be colored by the six registers in IA32. In a situation where your register allocator must spill a register, your program may simply abort after printing an error message.

DON'T. Do not hardcode your program so that your program only work for the particular input given in the template file. Reaching a point where your program works for the hardcoded input in the template file is important, but your code must be general enough to work for a variety of input programs.

Template files. You are given the following template files to begin with:

    README.txt: the documentation file
    assn4.py: the template file

The template files are located at /class/ec3204_2014/assn4 in the cs Linux server.

Turning in. Turn in the following files:

    README.txt: the documentation file
    assn4.py: your program derived from the template file

