Goals. In this assignment, you will practice (1) transforming a left-recursive context free grammar into a right-recursive one, (2) writing a recursive descent parser and (3) generating an abstract syntax tree.

DO. First, transform the left-recursive context free grammar (nanoc.g) into right-recursive one (nanoc_right.g). Second, compute the predict sets for each production in the right-recursive grammar (predict.txt). Third, write a recursive descent parser by filling in code inside each procedure for non-terminals (cparse.py). Finally, place some code inside each non-terminal routine so that the parser returns an abstract syntax tree in the end.

DON'T. Do not use any parser generators (e.g., flex). This assignment is self-contained in that you can complete this assignment by inserting statements inside the functions. It is OK to define and use your own functions inside the cparse.py file.

Template files. You are given the following template files to begin with:

    README.txt: the documentation file
    nanoc.g: the grammar file
    cparse.py: the parser template
    gcd.c: the input file
    gcd_output.py: the expected output file

The template files are located at /class/ec3204/2015/assn2 in the cs Linux server.

Turning in. Turn in the following files:

    README.txt: the documentation file
    nanoc_right.g: the transformed grammar without right-recursion
    predict.txt: the text file of enumerating the predict sets of each non-terminal
    cparse.py: the parser for nanoc_right.g

