from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

symbols = [AKnave, AKnight, BKnave, BKnight, CKnave, CKnight]

#modifications to the program begin here
statements = []
characters = []
knowledge00 = And()

while True:
    character = input("Enter a character: ")
    characters.append(character)
    if character == "":
        break
    while True:
        var = input("Enter a statement for " + character + ": ")
        if var == "":
            break
        statements.append([character, var])

know = []

for character, statement in statements:
    #if character is A then connect to A symbols (same with other letters)
    if character.upper() == "A":
        charactera = AKnight
        characterb = AKnave
    elif character.upper() == "B":
        charactera = BKnight
        characterb = BKnave
    elif character.upper() == "C":
        charactera = CKnight
        characterb = CKnave
    
    #parsing through "and" statements
    if "&" in statement:
        statea = Symbol("")
        stateb = Symbol("")
        for i in symbols:
            if statement.split(" & ")[0] == str(i):
                statea = i
            if statement.split(" & ")[1] == str(i):
                stateb = i
        knowledge00.add(
                Implication(charactera, And(statea, stateb)),
                Implication(characterb, Not(And(statea, stateb))),
            )
#this knowledge base was created to test the functionality of input-based logic statements

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    #general structure
    Or(AKnave, AKnight), 
    Not(And(AKnave, AKnight)),

    #Either A is both a knight or a knave, or it is just a knave
    Implication(AKnight, And(AKnave, AKnight)),
    Implication(AKnave, Not(And(AKnave, AKnight)))
)
print(knowledge0)
# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    #general structure
    Or(AKnave, AKnight), 
    Not(And(AKnight, AKnave)), 

    Or(BKnave, BKnight), 
    Not(And(BKnight, BKnave)),
    
    Or(And(AKnave, BKnave), AKnave), #Either both A and B are knaves, or just A
    Implication(AKnave, Not(And(AKnave, BKnave))), #If A is a knave, A and B both cannot be knaves
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #general structure
    Or(AKnave, AKnight), 
    Not(And(AKnight, AKnave)), 

    Or(BKnave, BKnight), 
    Not(And(BKnight, BKnave)),

    #Evaluation of B's statement
    Implication(BKnight, And(Not(And(BKnight, AKnight)), Not(And(BKnave, AKnave)))), 
    Implication(BKnave, Or(And(BKnight, AKnight), And(BKnave, AKnave))),

    #Evaluation of A's statement
    Implication(AKnave, And(Not(And(BKnight, AKnight)), Not(And(BKnave, AKnave)))),
    Implication(AKnight, Or(And(BKnight, AKnight), And(BKnave, AKnave))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(    
    #general structure
    Or(AKnave, AKnight), 
    Not(And(AKnight, AKnave)), 

    Or(BKnave, BKnight), 
    Not(And(BKnight, BKnave)),

    Or(CKnave, CKnight), 
    Not(And(CKnight, CKnave)),

    Implication(BKnave, Not(And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave))))),
    
    #statements
    Implication(BKnight, And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))), #If B is knight, its statement about A must be true
    Implication(BKnave, Not(CKnave)),
    Implication(BKnight, CKnave),
    Biconditional(BKnave, CKnight), #if B is knave, C is knight
    Biconditional(BKnight, CKnave), #if B is knight, C is knave
    Or(CKnave, BKnave), #Either C is knave as B said, or B is a knave
    Implication(AKnight, CKnight), #If A is a knight, then C is a knight
    Implication(CKnight, AKnight), #If C is a knight, then it was truthful about A
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
