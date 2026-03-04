import random as r
import time as t
import sys

print(
'''
===========================================================================================================================================================
 .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. .----------------. 
 | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. | .--------------. |
 | |   ______     | | |  ____  ____  | | |  _________   | | | _____  _____ | | |     ______   | | |  ____  ____  | | |  _______     | | |  _________   | |
 | |  |_   __ \   | | | |_  _||_  _| | | | |_   ___  |  | | ||_   _||_   _|| | |   .' ___  |  | | | |_   ||   _| | | | |_   __ \    | | | |_   ___  |  | |
 | |    | |__) |  | | |   \ \  / /   | | |   | |_  \_|  | | |  | |    | |  | | |  / .'   \_|  | | |   | |__| |   | | |   | |__) |   | | |   | |_  \_|  | |
 | |    |  ___/   | | |    \ \/ /    | | |   |  _|  _   | | |  | '    ' |  | | |  | |         | | |   |  __  |   | | |   |  __ /    | | |   |  _|  _   | |
 | |   _| |_      | | |    _|  |_    | | |  _| |___/ |  | | |   \ `--' /   | | |  \ `.___.'\  | | |  _| |  | |_  | | |  _| |  \ \_  | | |  _| |___/ |  | |
 | |  |_____|     | | |   |______|   | | | |_________|  | | |    `.__.'    | | |   `._____.'  | | | |____||____| | | | |____| |___| | | | |_________|  | |
 | |              | | |              | | |              | | |              | | |              | | |              | | |              | | |              | |
 | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' | '--------------' |
  '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' '----------------' 
===========================================================================================================================================================
'''
    )

##### CREATING CARDS #####

class Card(object):

    card_values = {
        '9': 1,
        '10': 2,
        'Jack': 3,
        'Queen': 4,
        'King': 5,
	'Ace': 6
    }
    
    def __init__(self, suit, rank):
        """
        :param suit: The face of the card, e.g. Spade or Diamond
        :param rank: The value of the card, e.g 9 or King
        """
        self.suit = suit.capitalize()
        self.rank = rank
        
        trump = 0
        if self.suit == trump:
            card_values = {
                '9': 1,
                '10': 2,
                'Queen': 3,
                'King': 4,
                'Ace': 5,
                'Jack': 7
        }

        if trump == 'Spades':
            if self.suit == 'Clubs' and self.rank == 'Jack':
                card_values = 6
        if trump == 'Clubs':
            if self.suit == 'Spades' and self.rank == 'Jack':
                card_values = 6
        if trump == 'Hearts':
            if self.suit == 'Diamonds' and self.rank == 'Jack':
                card_values = 6
        if trump == 'Diamonds':
            if self.suit == 'Hearts' and self.rank == 'Jack':
                card_values = 6

        self.points = self.card_values[rank]


#CARD IMAGE

def card_image(*cards, return_string=True):
    
    suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
    suits_symbols = ['♠', '♦', '♥', '♣']

    # create an empty list of list, each sublist is a line
    lines = [[] for i in range(9)]

    for index, card in enumerate(cards):
        # "King" should be "K" and "10" should still be "10"
        if card.rank == '10':  # ten is the only one who's rank is 2 char long
            rank = card.rank
            space = ''  # if we write "10" on the card that line will be 1 char to long
        else:
            rank = card.rank[0]  # some have a rank of 'King' this changes that to a simple 'K' ("King" doesn't fit)
            space = ' '  # no "10", we use a blank space to will the void
        # get the cards suit in two steps
        suit = suits_name.index(card.suit)
        suit = suits_symbols[suit]

        # add the individual card on a line by line basis
        lines[0].append('┌─────────┐')
        lines[1].append('│{}{}       │'.format(rank, space))  # use two {} one for char, one for space or char
        lines[2].append('│         │')
        lines[3].append('│         │')
        lines[4].append('│    {}    │'.format(suit))
        lines[5].append('│         │')
        lines[6].append('│         │')
        lines[7].append('│       {}{}│'.format(space, rank))
        lines[8].append('└─────────┘') 

    result = []
    for index, line in enumerate(lines):
        result.append(''.join(lines[index]))

    # hidden cards do not use string
    if return_string:
        return '\n'.join(result)
    else:
        return result

#SETTING UP THE DECK

all_cards = []

for n in range (0, 24):
    all_cards.append([])


for n in range (0, 6):
    all_cards[n].append('Spades')

for n in range (6, 12):
    all_cards[n].append('Diamonds')

for n in range (12, 18):
    all_cards[n].append('Hearts')

for n in range (18, 24):
    all_cards[n].append('Clubs')


for n in (0, 6, 12, 18):
    all_cards[n].append('9')

for n in (1, 7, 13, 19):
    all_cards[n].append('10')

for n in (2, 8, 14, 20):
    all_cards[n].append('Jack')

for n in (3, 9, 15, 21):
    all_cards[n].append('Queen')

for n in (4, 10, 16, 22):
    all_cards[n].append('King')

for n in (5, 11, 17, 23):
    all_cards[n].append('Ace')

#print(all_cards)

##### PLAYER #####

player_name = input("Enter your name to begin: ")

##### TEST CASES #####

#hand = []

#card_test = []
#card_test.append('Diamonds')
#card_test.append('9')

#test_card_1 = Card(*card_test)
#test_card_2 = Card('Clubs', 'Ace')
#test_card_3 = Card('Spades', 'Jack')
#test_card_4 = Card('Hearts', '10')
#test_card_5 = Card('Diamonds', 'Queen')

#hand.append(test_card_1)
#hand.append(test_card_2)
#hand.append(test_card_3)
#hand.append(test_card_4)
#hand.append(test_card_5)

#print(card_image(test_card_1, test_card_2, test_card_3, test_card_4, test_card_5))


##### GAME #####

print('\n' * 100)

################

hands = []

for n in range(0, 4):
    hands.append([])

## DEAL ##

buried = []

#SHUFFLE

print("Shuffling cards...")

x = r.sample(range(24), 24)
#t.sleep(5)

print('\n' * 100)

print("Cards have been shuffled!")

#t.sleep(2)

#DEAL

print('\n' * 100)

print("Dealing...")

for n in range(0, 5):
    hands[0].append(Card(*all_cards[x[n]]))

for n in range(5, 10):
    hands[1].append(Card(*all_cards[x[n]]))

for n in range(10, 15):
    hands[2].append(Card(*all_cards[x[n]]))

for n in range(15, 20):
    hands[3].append(Card(*all_cards[x[n]]))

for n in range(20, 24):
    buried.append(Card(*all_cards[x[n]]))

#t.sleep(5)

print('\n' * 100)

print(card_image(buried[0]))
print(f"{buried[0].rank} of {buried[0].suit} has been flipped up!")
print('\n' * 2)

alone1 = 0
alone2 = 0

###### BOTS #####

pickup = 0

while True:

#BOT 1

    print("Player 1 is choosing...")

    num_spades1 = 0
    num_hearts1 = 0
    num_clubs1 = 0
    num_diamonds1 = 0

    if hands[1][0].suit == 'Spades':
        num_spades1 += 1
    elif hands[1][0].suit == 'Hearts':
        num_hearts1 += 1
    elif hands[1][0].suit == 'Clubs':
        num_clubs1 += 1
    elif hands[1][0].suit == 'Diamonds':
        num_diamonds1 += 1

    if hands[1][1].suit == 'Spades':
        num_spades1 += 1
    elif hands[1][1].suit == 'Hearts':
        num_hearts1 += 1
    elif hands[1][1].suit == 'Clubs':
        num_clubs1 += 1
    elif hands[1][1].suit == 'Diamonds':
        num_diamonds1 += 1
        
    if hands[1][2].suit == 'Spades':
        num_spades1 += 1
    elif hands[1][2].suit == 'Hearts':
        num_hearts1 += 1
    elif hands[1][2].suit == 'Clubs':
        num_clubs1 += 1
    elif hands[1][2].suit == 'Diamonds':
        num_diamonds1 += 1

    if hands[1][3].suit == 'Spades':
        num_spades1 += 1
    elif hands[1][3].suit == 'Hearts':
        num_hearts1 += 1
    elif hands[1][3].suit == 'Clubs':
        num_clubs1 += 1
    elif hands[1][3].suit == 'Diamonds':
        num_diamonds1 += 1

    if hands[1][4].suit == 'Spades':
        num_spades1 += 1
    elif hands[1][4].suit == 'Hearts':
        num_hearts1 += 1
    elif hands[1][4].suit == 'Clubs':
        num_clubs1 += 1
    elif hands[1][4].suit == 'Diamonds':
        num_diamonds1 += 1

    #t.sleep(2)

    if buried[0].suit=='Spades' and num_spades1>=3:
        print('Player 1: "Pick that shit up!"')
        pickup = 1
        trump = buried[0].suit
        break
    elif buried[0].suit=='Hearts' and num_hearts1>=3:
        print('Player 1: "Pick that shit up!"')
        pickup = 1
        trump = buried[0].suit
        break
    elif buried[0].suit=='Clubs' and num_clubs1>=3:
        print('Player 1: "Pick that shit up!"')
        pickup = 1
        trump = buried[0].suit
        break
    elif buried[0].suit=='Diamonds' and num_diamonds1>=3:
        print('Player 1: "Pick that shit up!"')
        pickup = 1
        trump = buried[0].suit
        break
    else:
        print('Player 1: "Fuck that, pass."')

    print('\n' * 2)

    #BOT 2

    print("Player 2 is choosing...")

    num_spades2 = 0
    num_hearts2 = 0
    num_clubs2 = 0
    num_diamonds2 = 0

    if hands[2][0].suit == 'Spades':
        num_spades2 += 1
    elif hands[2][0].suit == 'Hearts':
        num_hearts2 += 1
    elif hands[2][0].suit == 'Clubs':
        num_clubs2 += 1
    elif hands[2][0].suit == 'Diamonds':
        num_diamonds2 += 1

    if hands[2][1].suit == 'Spades':
        num_spades2 += 1
    elif hands[2][1].suit == 'Hearts':
        num_hearts2 += 1
    elif hands[2][1].suit == 'Clubs':
        num_clubs2 += 1
    elif hands[2][1].suit == 'Diamonds':
        num_diamonds2 += 1
        
    if hands[2][2].suit == 'Spades':
        num_spades2 += 1
    elif hands[2][2].suit == 'Hearts':
        num_hearts2 += 1
    elif hands[2][2].suit == 'Clubs':
        num_clubs2 += 1
    elif hands[2][2].suit == 'Diamonds':
        num_diamonds2 += 1

    if hands[2][3].suit == 'Spades':
        num_spades2 += 1
    elif hands[2][3].suit == 'Hearts':
        num_hearts2 += 1
    elif hands[2][3].suit == 'Clubs':
        num_clubs2 += 1
    elif hands[2][3].suit == 'Diamonds':
        num_diamonds2 += 1

    if hands[2][4].suit == 'Spades':
        num_spades2 += 1
    elif hands[2][4].suit == 'Hearts':
        num_hearts2 += 1
    elif hands[2][4].suit == 'Clubs':
        num_clubs2 += 1
    elif hands[2][4].suit == 'Diamonds':
        num_diamonds2 += 1

    #t.sleep(2)

    if buried[0].suit=='Spades' and num_spades2>=3:
        print('Player 2: "Pick it up!"')
        pickup = 1
        trump = buried[0].suit
        break
    elif buried[0].suit=='Hearts' and num_hearts2>=3:
        print('Player 2: "Pick it up!"')
        pickup = 1
        trump = buried[0].suit
        break
    elif buried[0].suit=='Clubs' and num_clubs2>=3:
        print('Player 2: "Pick it up!"')
        pickup = 1
        trump = buried[0].suit
        break
    elif buried[0].suit=='Diamonds' and num_diamonds2>=3:
        print('Player 2: "Pick it up!"')
        pickup = 1
        trump = buried[0].suit
        break
    else:
        print('Player 2: "Pass."')

    print('\n' * 2)

    #BOT 3

    print("Player 3 is choosing...")

    num_spades3 = 0
    num_hearts3 = 0
    num_clubs3 = 0
    num_diamonds3 = 0

    if hands[3][0].suit == 'Spades':
        num_spades3 += 1
    elif hands[3][0].suit == 'Hearts':
        num_hearts3 += 1
    elif hands[3][0].suit == 'Clubs':
        num_clubs3 += 1
    elif hands[3][0].suit == 'Diamonds':
        num_diamonds3 += 1

    if hands[3][1].suit == 'Spades':
        num_spades3 += 1
    elif hands[3][1].suit == 'Hearts':
        num_hearts3 += 1
    elif hands[3][1].suit == 'Clubs':
        num_clubs3 += 1
    elif hands[3][1].suit == 'Diamonds':
        num_diamonds3 += 1
        
    if hands[3][2].suit == 'Spades':
        num_spades3 += 1
    elif hands[3][2].suit == 'Hearts':
        num_hearts3 += 1
    elif hands[3][2].suit == 'Clubs':
        num_clubs3 += 1
    elif hands[3][2].suit == 'Diamonds':
        num_diamonds3 += 1

    if hands[3][3].suit == 'Spades':
        num_spades3 += 1
    elif hands[3][3].suit == 'Hearts':
        num_hearts3 += 1
    elif hands[3][3].suit == 'Clubs':
        num_clubs3 += 1
    elif hands[3][3].suit == 'Diamonds':
        num_diamonds3 += 1

    if hands[3][4].suit == 'Spades':
        num_spades3 += 1
    elif hands[3][4].suit == 'Hearts':
        num_hearts3 += 1
    elif hands[3][4].suit == 'Clubs':
        num_clubs3 += 1
    elif hands[3][4].suit == 'Diamonds':
        num_diamonds3 += 1

    #t.sleep(2)

    if buried[0].suit=='Spades' and num_spades3>=3:
        print('Player 3: "Pick it up!"')
        pickup = 1
        trump = buried[0].suit
        break
    elif buried[0].suit=='Hearts' and num_hearts3>=3:
        print('Player 3: "Pick it up!"')
        pickup = 1
        trump = buried[0].suit
        break
    elif buried[0].suit=='Clubs' and num_clubs3>=3:
        print('Player 3: "Pick it up!"')
        pickup = 1
        trump = buried[0].suit
        break
    elif buried[0].suit=='Diamonds' and num_diamonds3>=3:
        print('Player 3: "Pick it up!"')
        pickup = 1
        trump = buried[0].suit
        break
    else:
        print('Player 3: "Pass."')

    print('\n' * 2)

    print(player_name, "is choosing...")
    
    print("Flipped up:")
    print(card_image(buried[0]))
    print('\n' * 2)
    print("Your hand:")
    print(card_image(*hands[0]))
    print("")
    print("Would you like to pass or pick up?")
    
    option1 = 0
    while option1 == 0:
        option = input()

        print(player_name + ":", option)

        if option.capitalize() == 'Pass':
            option1 = 1
        elif option.capitalize() == 'Pick up' or option.capitalize() == 'Pick it up':
            option1 = 1
            pickup = 1
            trump = buried[0].suit
            break
        else:
            print("Player 1: Hey dumbass, thats not an option!")
    
    if pickup == 1:
        break

    #####

    print("Player 1 is choosing...")

    #t.sleep(2)

    if num_spades1>=3:
        print('Player 1: "Spades!"')
        break
    elif num_hearts1>=3:
        print('Player 1: "Hearts!"')
        break
    elif num_clubs1>=3:
        print('Player 1: "Clubs!"')
        break
    elif num_diamonds1>=3:
        print('Player 1: "Diamonds!"')
        break
    else:
        print('Player 1: "Pass."')

    print('\n' * 2)

    print("Player 2 is choosing...")

    #t.sleep(2)

    if num_spades2>=3:
        print('Player 2: "Spades!"')
        break
    elif num_hearts2>=3:
        print('Player 2: "Hearts!"')
        break
    elif num_clubs2>=3:
        print('Player 2: "Clubs!"')
        break
    elif num_diamonds2>=3:
        print('Player 2: "Diamonds!"')
        break
    else:
        print('Player 2: "Pass."')

    print('\n' * 2)

    print("Player 3 is choosing...")

    #t.sleep(2)

    if num_spades3>=3:
        print('Player 3: "Spades!"')
        break
    elif num_hearts3>=3:
        print('Player 3: "Hearts!"')
        break
    elif num_clubs3>=3:
        print('Player 3: "Clubs!"')
        break
    elif num_diamonds3>=3:
        print('Player 3: "Diamonds!"')
        break
    else:
        print('Player 3: "Pass."')

    print('\n' * 2)

    print("Looks like", player_name, "is screwed! You have to call it!")
    print('')
    print("Your hand:")
    print(card_image(*hands[0]))
    print("")
    print("What would you like to call?")

    option2 = 0

    while option2 == 0:
        option = input()

        print(player_name + ":", option)

        if option.capitalize() == buried[0].suit:
            print("Player 1: You can't call what you just flipped over idiot!")
        elif option.capitalize() == 'Spades':
            trump = 'Spades'
            option2 = 1
            break
        elif option.capitalize() == 'Hearts':
            trump = 'Hearts'
            option2 = 1
            break
        elif option.capitalize() == 'Clubs':
            trump = 'Clubs'
            option2 = 1
            break
        elif option.capitalize() == 'Diamonds':
            trump = 'Diamonds'
            option2 = 1
            break
        
#PICKING UP

if pickup == 1:
    
    print("Which card would you like to get rid of?")
    print("")
    print(card_image(*hands[0]))
    print("    (1)    " + "    (2)    " + "    (3)    " + "    (4)    " + "    (5)    ")
    

    
    while True:
        get_rid = int(input())

        if get_rid in list(range(1, 6)):
            hands[0].pop(get_rid - 1)
            break
        else:
            print("You must pick a card between 1 and 5!")

    hands[0].append(buried[0])
    
    print("Your new hand:")
    print(card_image(*hands[0]))

##### TRICK 1 #####

thrown = []

#BOT 1

print("Player 1's turn...")
t.sleep(2)

while True:
    for n, _ in enumerate(hands[1]):
        if hands[1][n].rank == 'Jack' and hands[1][n].suit == trump:
            print("Player 1 throws:")
            print(card_image(hands[1][n]))
            thrown.append(hands[1][n])
            hands[0].pop(n)
            break
    if thrown:
        break
    for n, _ in enumerate(hands[1]):
        if hands[1][n].rank == 'Ace' and hands[1][n].suit != trump:
            print("Player 1 throws:")
            print(card_image(hands[1][n]))
            thrown.append(hands[1][n])
            hands[0].pop(n)
            break
    if thrown:
        break
    for n, _ in enumerate(hands[1]):
        if hands[1][n].rank == 'King' and hands[1][n].suit != trump:
            print("Player 1 throws:")
            print(card_image(hands[1][n]))
            thrown.append(hands[1][n])
            hands[0].pop(n)
            break
    if thrown:
        break
    for n, _ in enumerate(hands[1]):
        if hands[1][n].rank == 'Queen' and hands[1][n].suit != trump:
            print("Player 1 throws:")
            print(card_image(hands[1][n]))
            thrown.append(hands[1][n])
            hands[0].pop(n)
            break
    if thrown:
        break
    for n, _ in enumerate(hands[1]):
        if hands[1][n].rank == 'Jack' and hands[1][n].suit != trump:
            print("Player 1 throws:")
            print(card_image(hands[1][n]))
            thrown.append(hands[1][n])
            hands[0].pop(n)
            break
    if thrown:
        break
    for n, _ in enumerate(hands[1]):
        if hands[1][n].rank == '10' and hands[1][n].suit != trump:
            print("Player 1 throws:")
            print(card_image(hands[1][n]))
            thrown.append(hands[1][n])
            hands[0].pop(n)
            break
    for n, _ in enumerate(hands[1]):
        if hands[1][n].rank == '9' and hands[1][n].suit != trump:
            print("Player 1 throws:")
            print(card_image(hands[1][n]))
            thrown.append(hands[1][n])
            hands[0].pop(n)
            break
    if thrown:
        break
    for n, _ in enumerate(hands[1]):
        if hands[1][n].rank == 'Jack' and hands[1][n].suit != trump:
            if trump == 'Spades':
                if hands[1][n].suit == 'Clubs':
                    print("Player 1 throws:")
                    print(card_image(hands[1][n]))
                    thrown.append(hands[1][n])
                    hands[0].pop(n)
                    break
            if trump == 'Clubs':
                if hands[1][n].suit == 'Spades':
                    print("Player 1 throws:")
                    print(card_image(hands[1][n]))
                    thrown.append(hands[1][n])
                    hands[0].pop(n)
                    break
            if trump == 'Hearts':
                if hands[1][n].suit == 'Diamonds':
                    print("Player 1 throws:")
                    print(card_image(hands[1][n]))
                    thrown.append(hands[1][n])
                    hands[0].pop(n)
                    break
            if trump == 'Diamonds':
                if hands[1][n].suit == 'Hearts':
                    print("Player 1 throws:")
                    print(card_image(hands[1][n]))
                    thrown.append(hands[1][n])
                    hands[0].pop(n)
                    break
        
#BOT 2

print("Player 2's turn...")
t.sleep(2)

while True:
    for n, _ in enumerate(hands[2]):
        if thrown[0].suit != trump and hands[2][n].suit == thrown[0].suit and hands[2][n].points > thrown[0].points:
            print("Player 2 throws:")
            print(card_image(hands[2][n]))
            thrown.append(hands[2][n])
            hands[2].pop(n)
            break
    try:
        testvar = thrown[1]
        break
    except:
        pass
    for n, _ in enumerate(hands[2]):
        if thrown[0].suit != trump and hands[2][n].suit == thrown[0].suit:
            print("Player 2 throws:")
            print(card_image(hands[2][n]))
            thrown.append(hands[2][n])
            hands[2].pop(n)
            break
    try:
        testvar = thrown[1]
        break
    except:
        pass
    for n, _ in enumerate(hands[2]):
        if thrown[0].suit != trump and hands[2][n].suit == trump:
            print("Player 2 throws:")
            print(card_image(hands[2][n]))
            thrown.append(hands[2][n])
            hands[2].pop(n)
            break
    try:
        testvar = thrown[1]
        break
    except:
        pass
    for n, _ in enumerate(hands[2]):
        if thrown[0].suit == trump and hands[2][n].suit == thrown[0].suit and hands[2][n].points > thrown[0].points:
            print("Player 2 throws:")
            print(card_image(hands[2][n]))
            thrown.append(hands[2][n])
            hands[2].pop(n)
            break
    try:
        testvar = thrown[1]
        break
    except:
        pass
    for n, _ in enumerate(hands[2]):
        if thrown[0].suit == trump and hands[2][n].suit == thrown[0].suit:
            print("Player 2 throws:")
            print(card_image(hands[2][n]))
            thrown.append(hands[2][n])
            hands[2].pop(n)
            break
    try:
        testvar = thrown[1]
        break
    except:
        pass
    for n, _ in enumerate(hands[2]):
        if hands[2][n].rank == '9':
            print("Player 2 throws:")
            print(card_image(hands[2][n]))
            thrown.append(hands[2][n])
            hands[2].pop(n)
            break
    try:
        testvar = thrown[1]
        break
    except:
        pass
    for n, _ in enumerate(hands[2]):
        if hands[2][n].rank == '10':
            print("Player 2 throws:")
            print(card_image(hands[2][n]))
            thrown.append(hands[2][n])
            hands[2].pop(n)
            break
    try:
        testvar = thrown[1]
        break
    except:
        pass
    for n, _ in enumerate(hands[2]):
        if hands[2][n].rank == 'Jack':
            print("Player 2 throws:")
            print(card_image(hands[2][n]))
            thrown.append(hands[2][n])
            hands[2].pop(n)
            break
    try:
        testvar = thrown[1]
        break
    except:
        pass
    for n, _ in enumerate(hands[2]):
        if hands[2][n].rank == 'Queen':
            print("Player 2 throws:")
            print(card_image(hands[2][n]))
            thrown.append(hands[2][n])
            hands[2].pop(n)
            break
    try:
        testvar = thrown[1]
        break
    except:
        pass
    for n, _ in enumerate(hands[2]):
        if hands[2][n].rank == 'King':
            print("Player 2 throws:")
            print(card_image(hands[2][n]))
            thrown.append(hands[2][n])
            hands[2].pop(n)
            break
    try:
        testvar = thrown[1]
        break
    except:
        pass
    
    print("THERE IS A PROBLEM WITH THE CODE!!")

#BOT 3

print("Player 3's turn...")
t.sleep(2)

while True:
    for n, _ in enumerate(hands[3]):
        if thrown[0].suit != trump and hands[3][n].suit == thrown[0].suit and hands[3][n].points > thrown[0].points:
            print("Player 3 throws:")
            print(card_image(hands[3][n]))
            thrown.append(hands[3][n])
            hands[3].pop(n)
            break
    try:
        testvar = thrown[2]
        break
    except:
        pass
    for n, _ in enumerate(hands[3]):
        if thrown[0].suit != trump and hands[3][n].suit == thrown[0].suit:
            print("Player 3 throws:")
            print(card_image(hands[3][n]))
            thrown.append(hands[3][n])
            hands[3].pop(n)
            break
    try:
        testvar = thrown[2]
        break
    except:
        pass
    for n, _ in enumerate(hands[3]):
        if thrown[0].suit != trump and thrown[1].suit == trump and hands[3][n].suit == trump and hands[3][n].points > thrown[1].points:
            print("Player 3 throws:")
            print(card_image(hands[3][n]))
            thrown.append(hands[3][n])
            hands[3].pop(n)
            break
    try:
        testvar = thrown[2]
        break
    except:
        pass
    for n, _ in enumerate(hands[3]):
        if thrown[0].suit == trump and hands[3][n].suit == thrown[0].suit and hands[3][n].points > thrown[1].points and hands[3][n].points > thrown[0].points:
            print("Player 3 throws:")
            print(card_image(hands[3][n]))
            thrown.append(hands[3][n])
            hands[3].pop(n)
            break
    try:
        testvar = thrown[2]
        break
    except:
        pass
    for n, _ in enumerate(hands[3]):
        if thrown[0].suit == trump and hands[3][n].suit == thrown[0].suit:
            print("Player 3 throws:")
            print(card_image(hands[3][n]))
            thrown.append(hands[3][n])
            hands[3].pop(n)
            break
    try:
        testvar = thrown[2]
        break
    except:
        pass
    for n, _ in enumerate(hands[3]):
        if hands[3][n].rank == '9':
            print("Player 3 throws:")
            print(card_image(hands[3][n]))
            thrown.append(hands[3][n])
            hands[3].pop(n)
            break
    try:
        testvar = thrown[2]
        break
    except:
        pass
    for n, _ in enumerate(hands[3]):
        if hands[3][n].rank == '10':
            print("Player 3 throws:")
            print(card_image(hands[3][n]))
            thrown.append(hands[3][n])
            hands[3].pop(n)
            break
    try:
        testvar = thrown[2]
        break
    except:
        pass
    for n, _ in enumerate(hands[3]):
        if hands[3][n].rank == 'Jack':
            print("Player 3 throws:")
            print(card_image(hands[3][n]))
            thrown.append(hands[3][n])
            hands[3].pop(n)
            break
    try:
        testvar = thrown[2]
        break
    except:
        pass
    for n, _ in enumerate(hands[3]):
        if hands[3][n].rank == 'Queen':
            print("Player 3 throws:")
            print(card_image(hands[3][n]))
            thrown.append(hands[3][n])
            hands[3].pop(n)
            break
    try:
        testvar = thrown[2]
        break
    except:
        pass
    for n, _ in enumerate(hands[3]):
        if hands[3][n].rank == 'King':
            print("Player 3 throws:")
            print(card_image(hands[3][n]))
            thrown.append(hands[3][n])
            hands[3].pop(n)
            break
    try:
        testvar = thrown[2]
        break
    except:
        pass
    
    print("THERE IS A PROBLEM WITH THE CODE!!")
#PLAYER

print("Which card would you like to throw?")
print("")
print(card_image(*hands[0]))
print("    (1)    " + "    (2)    " + "    (3)    " + "    (4)    " + "    (5)    ")

player_thrown_1 = int(input())

while True:
    if player_thrown_1 in range(1, 6):
        print("Player 2 throws:")
        print(card_image(hands[0][player_thrown_1 - 1]))
        thrown.append(hands[0][player_thrown_1 - 1])
        hands[0].pop(player_thrown_1 - 1)
        break
    else:
        print("You must pick a card between 1 and 5!")

#END OF TRICK 1

#print(card_image(*thrown))

#for n in thrown:
#    if n.suit == trump and n.rank == 'Jack':
#        if thrown.index(n) == 0        
#print(thrown.index(n))



#print(card_image(*hands[0]))
