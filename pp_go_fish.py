import random


class Cards:
    def __init__(self):  
        self.deck = []  
        self.comp_hand = [] 
        self.comp_books = []  
        self.player_hand = []  
        self.player_books = []  

        for x in range(2, 15):  
            for y in range(1, 5):  
                if x == 11:  
                    self.deck.append('J')
                elif x == 12:  
                    self.deck.append('Q')
                elif x == 13:  
                    self.deck.append('K')
                elif x == 14:  
                    self.deck.append('A')
                else: 
                    self.deck.append(x)

        for x in range(0, 7):
            card = random.choice(self.deck)
            self.comp_hand.append(card)
            self.deck.remove(card)

        for x in range(0, 7):
            card = random.choice(self.deck)
            self.player_hand.append(card)
            self.deck.remove(card)

    def take_card(self, turn, card):
        if turn == 'user':
            self.player_hand.remove(card)
        else:
            self.comp_hand.remove(card)

    def add_card(self, turn, card):
        if turn == 'user':
            self.player_hand.append(card)
        else:
            self.comp_hand.append(card)

    def hand_statement(self):
        user_str = " "
        for x in range(2, 15):
            if x == 11:
                curr = 'J'
            elif x == 12:
                curr = 'Q'
            elif x == 13:
                curr = 'K'
            elif x == 14:
                curr = 'A'
            else:
                curr = str(x)

            if x < 11:
                count = self.player_hand.count(x)
            else:
                count = self.player_hand.count(curr)

            while count > 0:
                user_str = user_str + curr + ", "
                count = count - 1

        books_str = str(self.player_books).strip('[]')
        print(f"Your Hand: " + user_str.replace("'", ""))
        print("Your Books: " + books_str.replace("'", ""))

    def draw_card(self, player):
        card = random.choice(self.deck)
        self.deck.remove(card)
        if player == "comp":
            self.comp_hand.append(card)
        else:
            self.player_hand.append(card)

    def check_for_books(self, player):
        if player == "user":
            for c in self.player_hand:
                num = self.player_hand.count(c)
                if num == 4:
                    for x in range(0, 4):
                        self.player_hand.remove(c)
                    self.player_books.append(c)
        else:
            for c in self.comp_hand:
                num = self.comp_hand.count(c)
                if num == 4:
                    for x in range(0, 4):
                        self.comp_hand.remove(c)
                    self.comp_books.append(c)


fishy_deck = Cards()
turn = "user"
face_cards = ['K', 'Q', 'J', 'A']
reg_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10]
num_strings = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
face_strings = ['King', 'Queen', 'Jack', 'Ace']
face_card = 0


def player_admission(user_input):
    card_type = -1
    try:
        if ' ' in user_input:
            card_type = -2  
        elif user_input.upper() in (card.upper() for card in face_cards):
            card_type = 1  
        elif user_input.upper() in (card.upper() for card in face_strings):
            card_type = 1  
        elif user_input.upper() in (card.upper() for card in num_strings):
            card_type = 0  
        elif int(user_input) in reg_cards:
            card_type = 0  
        return card_type
    except ValueError:  
        card_type = -2;  
        return card_type

def adjust_card(card_type, user_input):
    if card_type == 0:  
        if user_input.upper() in (card.upper() for card in num_strings):
            return int(reg_cards[num_strings.index(user_input)])
        else:
            return int(user_input)
    else:  
        return user_input[0].upper()

def incorrect_guess(turn):
    fishy_deck.draw_card(turn)
    fishy_deck.check_for_books(turn)

    if turn == 'user':
        print("Go Fish!")
        fishy_deck.hand_statement()
    else:
        print("The Computer has gone fishing... Your turn!")

def correct_guess(turn, card, count, card_type):
    if card_type == 0:  
        index = reg_cards.index(card)
        card_string = num_strings[index]  
    else:  
        index = face_cards.index(card)
        card_string = face_strings[index]  

    if count > 1:
        card_string = card_string + "s"  

    if turn == 'user':
        print(f"I had {str(count)} {card_string}")
        print("You get to go again!")
    else:
        print(f"Thanks for the {card_string}")

    updated_hand(count, card, turn)  

def updated_hand(count, card, turn):
    if turn == 'user':  
        opp = 'comp'
    else:
        opp = 'user'

    while count > 0:  
        fishy_deck.take_card(opp, card)  
        fishy_deck.add_card(turn, card)  
        count = count - 1

    fishy_deck.check_for_books(turn)

while len(fishy_deck.player_hand) > 0 and len(fishy_deck.comp_hand) > 0 and len(fishy_deck.deck) > 0:
    if turn == "user":  
        print("\n")
        fishy_deck.hand_statement()  

        user_input = input("Which card would you like to ask me for? ")
        cardType = player_admission(user_input)

        if cardType == -1:  
            print("Invalid input, please ask for a valid card (i.e. 2 - 10, J, Q, K, A)")
        elif cardType == -2:  
            print("Invalid input, please type only a single card")
        else:
            card = adjust_card(cardType, user_input)
            count = fishy_deck.comp_hand.count(card)  
            if count == 0:  
                incorrect_guess(turn)
                turn = "comp"  
            else:  
                correct_guess(turn, card, count, cardType)
                turn = "user"  

    if turn == "comp":  
        print("\n")
        card = random.choice(fishy_deck.comp_hand)  
        cardType = player_admission(str(card))
        print("Do you have any " + str(card) + "s")
        count = fishy_deck.player_hand.count(card)  

        if count == 0: 
            incorrect_guess(turn)
            turn = "user"  
        else:
            correct_guess(turn, card, count, cardType)
            turn = "comp"  

print("\n")
print("Game Over... There are no more cards in the deck!")
comp_books = len(fishy_deck.comp_books)
player_books = len(fishy_deck.player_books)

print(f"You completed {str(player_books)} books.")
print(f"The Computer completed {str(comp_books)} books.")

if comp_books > player_books:
    print("The computer has won!")
elif player_books > comp_books:
    print("YOU WIN!")
else:
    print("You and the Computer have tied!")
