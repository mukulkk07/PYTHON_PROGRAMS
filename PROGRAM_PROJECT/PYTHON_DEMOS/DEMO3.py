#IF, IF ELSE, IF ELIF ELSE, MATCH CASE CONDITIONAL STATEMENTS
#PYTHON CALCULATOR
op = input("ENTER AN OPERATOR (+, -, *, /, %) ")
N1 = int(input("ENTER A NUMBER "))
N2 = int(input("ENTER A NUMBER "))
if op == "+":
    print(N1 + N2)
elif op == "-":
    print(N1 - N2)
elif op == "*":
    print(N1 * N2)
elif op == "/":
    print(N1 / N2)
elif op == "%":
    print(N1 % N2)
else:
    print("ERROR.....")

