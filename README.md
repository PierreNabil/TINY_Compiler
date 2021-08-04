# TINY_Compiler
Scanner and Parser for the TINY Programming Language.
4th year 1st term Compilers Project.

## Description
In this project, we draw the Syntax Tree and/or Parse Tree of any TINY language code.

## Usage
To use the GUI for this project, run main.exe in [dist](https://github.com/PierreNabil/4th_CSE_Compilers_Project/tree/main/dist) or run main.py using python.
You can find more details on how to use the GUI in the pdf provided in the project.

## TINY Language:
### Token List:

Token Text | Token Type Name
-----------|----------------
if | IF
then | THEN
else | ELSE
end | END
repeat | REPEAT
until | UNTIL
read | READ
write | WRITE
\+ | PLUS
\- | MINUS
\* | MULT
/ | DIV
= | EQUAL
\< | LESSTHAN
\> | GREATERTHAN
\( | OPENBRACKET
\) | CLOSEDBRACKET
; | SEMICOLON
:= | ASSIGN
number | NUMBER
identifier | IDENTIFIER

### Grammar:

program -> stmt_seq

stmt_seq -> stmt_seq ; stmt | stmt

stmt -> if_stmt | repeat_stmt | assign_stmt | read_stmt | write_stmt

if_stmt -> _**if**_ exp _**then**_ stmt_seq _**end**_ | _**if**_ exp _**then**_ stmt_seq _**else**_ stmt_seq _**end**_

repeat_stmt -> _**repeat**_ stmt_seq _**until**_ exp

assign_stmt -> _**IDENTIFIER**_ _**:=**_ exp

read_stmt -> _**read**_ _**IDENTIFIER**_

write_stmt -> _**write**_ exp

exp -> simple_exp comp_op simple_exp | simple_exp

simple_exp -> simple_exp add_op term | term

term -> term mul_op factor | factor

factor -> _**(**_ exp _**)**_ | _**NUMBER**_ | _**IDENTIFIER**_

comp_op -> _**=**_ | _**\>**_ | _**\<**_

add_op -> _**\+**_ | _**\-**_

mul_op -> _**\***_ | _**/**_

### Example Output:
#### Input Code:

    {Sample Program in the TINY Language - Computes Factorial}
    read x; {input an integer}
    if x>0 then {don't compute if x <=0}
        fact := 1;
        repeat
            fact := fact * x;
            x := x - 1
        until x=0;
        write fact {output factorial of x}
    end

#### Tokens Found:
Token Text | Token Type Name
-----------|----------------
read|READ
x|IDENTIFIER
;|SEMICOLON
if|IF
x|IDENTIFIER
\>|GREATERTHAN
0|NUMBER
then|THEN
fact|IDENTIFIER
:=|ASSIGN
1|NUMBER
;|SEMICOLON
repeat|REPEAT
fact|IDENTIFIER
:=|ASSIGN
fact|IDENTIFIER
\*|MULT
x|IDENTIFIER
;|SEMICOLON
x|IDENTIFIER
:=|ASSIGN
x|IDENTIFIER
\-|MINUS
1|NUMBER
until|UNTIL
x|IDENTIFIER
=|EQUAL
0|NUMBER
;|SEMICOLON
write|WRITE
fact|IDENTIFIER
end|END
;|SEMICOLON
write|WRITE
x|IDENTIFIER
\+|PLUS
5|NUMBER


#### Output Trees:
Parse Tree:
![Parse Tree](/myParsetree.png)

Syntax Tree:
![Syntax Tree](/mySyntaxtree.png)
