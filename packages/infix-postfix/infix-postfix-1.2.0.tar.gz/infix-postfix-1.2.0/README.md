<div align="center">
<p>
<image src="./res/banner.jpg"/><br>
An application to convert infix to postfix and vice versa...</p>
</div>

# Key Features
- Runs standalone
- Converts Infix expression to postfix expression.
- Converts postfix expression to infix expression.


# Basic Requirements (Pre-installed)
- Python 3.x
- Windows OS or MacOS or Other Linux Distribution.


# Installation
- Open terminal/cmd in windows/macos respectively.
- Run the command `pip install infix-postfix`.


# Usage
- To convert infix to postfix, run `infix-postfix --infix "${infix_expression}"`
- To convert postfix to infix, run `infix-postfix --postfix "${postfix_expression}"`
> NOTE : Double quotes ("") is must for writing the expression to get correct output..

```
How to write expressions? 
- INFIX expression
    - Correct Methods
        - "( A+B)* C/D"
        - "((A+B)*C/D+E^F)/G"
        - "20.1 + (5 ^ 2 / 2)"
        - "20.1 + ( 5 ^ 2 / 2)"
        - etc...

- POSTFIX ecpression
    - Correct Methods
        - "A B + C * D /"
        - "A B C D + E F + * G / + * H *"
        - "20.1 5 +"
    - Wrong Methods
        - "AB+C*D/"
        - "ABCD+EF+*G/+*H*"
        - "20.1 5+"
        - "20 5+"
    - In One line, You have to give spaces after every value
```


- To run this application in your own application or python script, run
 
```python
from infix_postfix.infix_postfix import infix,postfix
$(variable) = $(infix/postfix){expression}
print($(variable))
```

Example :- 



<image src="./res/example.jpg" />

# Contribution
Anyone is free to contribute to this open source project. 🎉🎉

