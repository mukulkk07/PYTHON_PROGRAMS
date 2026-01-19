import random

num= random.randint(1,20)
options=("rock","paper","scissors")
cards=["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
random.shuffle(cards)
option=random.choice(options)
print(num)
print(option)
for x in cards:
    for y in x:
        print(y,end=" ")
    print()

#NUMBER GUESSIGN GAME

print(" PLEASE ENTER A NUMBER TO GUESS (FROM 1 TO 20)")
cor=random.randint(1,20)
while True:
    ans=int(input("ENTER THE NUMBER HERE"))
    if ans<1 or ans>20:
        print("REMEBER.....THE NUMBER IS FROM 1 TO 20!!!!")
        continue
    elif ans==cor:
        print("THE ANSWER IS CORRECT!!!! CONGRATULATIONS!!!")
        break
    elif ans<cor:
        print("OOPS.... TOO LOW... THE ANSWER IS NOT CORRECT!!!!")
    elif ans>cor:
        print("OOPS.... TOO HIGH... THE ANSWER IS NOT CORRECT!!!!")
    else:
        print("ERROR.......")


