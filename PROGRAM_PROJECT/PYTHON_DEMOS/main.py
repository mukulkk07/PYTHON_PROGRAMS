#COLLECTIONS : SINGLE VARIABLES WHICH STORE MULTIPLE VALUES
# LIST = [] ORDERED AND CHANGEABLE, DUPLICATES ARE ALLOWED
# SET = {} UNORDERED AND IMMUTABLE, DUPLICATES NOT ALLOWED, ADDITIONS ARE ALLOWED
# TUPLE = () ORDERED AND UNCHANGEABLE, DUPLICATES ARE ALLOWED, FASTER THAN OTHER COLLECTIONS
fruits=[["apple","banana","orange",],
        ["dragonfruit","kiwi","grapes"]
        ]
for fruit in fruits:
    for fru in fruit:
        print(fru)
    print()

print(fruits[1][2])

num=[[1,2,3],
     [4,5,6],
     [7,8,9],
     ["@","#","%"]]
print(num)
for x in num:
    for y in x:
        print(y,end=" ")
    print()

#DICTIONARIES : {KEY:VALUES} PAIRS WHICH ARE ORDERED AND CHANGEABLE

