# Comp-Struct-2D
ISTD 2D Challenge - 50.002 section

# Colab

1. You can fork a copy of this repo and clone to your computer. 

2. Create a new branch using `git checkout -b BRANCHNAME`

3. Commit the code and push to a new branch, and open a pull request.

The rule of thumb is that don't push code to master branch directly.


# Optimized carry-lookahead 32 bit adder

The idea is adapated from the 50.002 2D handout. See the diagram in the handout.

# CNF file generation output

```
Console Output
Parsing from /home/administrator/WebBC2CNF/files/adder32bit_1004514.bc
Using file format version 1.1
The circuit has 760 gates
The circuit has 728 gates and 1171 edges after sharing
The circuit has 697 gates after CNF normalization
The circuit has 695 gates and 1136 edges after sharing
The max-min height of the circuit is 8
The max-max height of the circuit is 66
The circuit has 695 relevant gates
The circuit has 65 relevant input gates
Computing cnf size... done
The cnf has 539 variables and 1614 clauses
Printing the CNF formula...
Done
```

# Test CNF UNSAT

At `./CS2D/`, run `java -jar findsolssat/findsolssat.jar lookahead.cnf`

Expected: `Unsat : true`

![Terminal Output](https://github.com/jzhang38/Comp-Struct-2D/blob/yingjie/assets/out.png)


