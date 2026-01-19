import random
import os
import time

# --- Configuration ---
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {r: i for i, r in enumerate(RANKS, start=2)}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = RANK_VALUES[rank]
        self.sort_value = SUITS.index(suit) * 100 + self.value

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def __lt__(self, other):
        return self.sort_value < other.sort_value


class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.hand = []
        self.is_human = is_human
        self.bid = 0
        self.tricks_won = 0
        self.score = 0

    def play_card(self, lead_suit, trump_suit):
        if self.is_human:
            return self._human_move(lead_suit)
        else:
            return self._ai_move(lead_suit, trump_suit)

    def _human_move(self, lead_suit):
        valid_indices = self._get_valid_indices(lead_suit)

        while True:
            try:
                choice = int(input(f"Select card (1-{len(self.hand)}): ")) - 1
                if choice in valid_indices:
                    return self.hand.pop(choice)
                else:
                    if 0 <= choice < len(self.hand):
                        print(f">> You must follow suit ({lead_suit})!")
                    else:
                        print(">> Invalid number.")
            except ValueError:
                print(">> Please enter a number.")

    def _ai_move(self, lead_suit, trump_suit):
        # AI Logic:
        # 1. Must follow suit.
        # 2. If can win and needs tricks, play high.
        # 3. Simple version: Random valid move.
        valid_indices = self._get_valid_indices(lead_suit)

        # Smart-ish selection: if we have valid cards, pick one
        # For simplicity in this demo, AI plays random valid card
        chosen_idx = random.choice(valid_indices)

        time.sleep(1)  # Thinking time
        return self.hand.pop(chosen_idx)

    def _get_valid_indices(self, lead_suit):
        # Indices of cards that follow suit
        matches = [i for i, card in enumerate(self.hand) if card.suit == lead_suit]
        if matches:
            return matches
        # If no match, any card is valid
        return list(range(len(self.hand)))


def determine_trick_winner(played_cards, trump_suit):
    """
    played_cards: list of tuples (Player, Card)
    Returns: The Player object who won.
    """
    lead_suit = played_cards[0][1].suit
    winner = played_cards[0][0]
    winning_card = played_cards[0][1]

    for player, card in played_cards[1:]:
        # If card is trump and current winner is not trump, or card is higher trump
        if card.suit == trump_suit:
            if winning_card.suit != trump_suit:
                winner = player;
                winning_card = card
            elif card.value > winning_card.value:
                winner = player;
                winning_card = card
        # If card is lead suit and current winner is lead suit (and no trumps seen yet)
        elif card.suit == lead_suit and winning_card.suit == lead_suit:
            if card.value > winning_card.value:
                winner = player;
                winning_card = card

    return winner


def print_table(round_num, trump_card, players, trick_log, lead_card=None):
    clear_screen()
    print(f"=== JUDGEMENT: ROUND {round_num} ===")
    print(f"Trump Suit: [{trump_card.suit}] (Trump Card: {trump_card})")
    print("-" * 40)

    # Scoreboard / Status
    print(f"{'Player':<10} | {'Bid':<5} | {'Won':<5} | {'Score':<5}")
    print("-" * 40)
    for p in players:
        print(f"{p.name:<10} | {p.bid:<5} | {p.tricks_won:<5} | {p.score:<5}")
    print("-" * 40)

    # Trick History
    if trick_log:
        print(f"Last Trick: {trick_log}")

    print("\nCurrent Play:")
    if lead_card:
        print(f"Lead Suit: {lead_card.suit}")
    else:
        print("Lead Suit: None (New Trick)")
    print("-" * 40)


def main():
    # Setup
    deck = [Card(r, s) for s in SUITS for r in RANKS]
    human = Player("You", is_human=True)
    bot1 = Player("Alice")
    bot2 = Player("Bob")
    bot3 = Player("Charlie")
    players = [human, bot1, bot2, bot3]

    # Game Loop (Rounds 1 to 5)
    total_rounds = 5

    for round_num in range(1, total_rounds + 1):
        # 1. Prepare Round
        random.shuffle(deck)
        current_deck = deck.copy()

        # Deal cards
        for p in players:
            p.hand = []
            p.bid = 0
            p.tricks_won = 0
            for _ in range(round_num):
                p.hand.append(current_deck.pop())
            p.hand.sort()  # Sort cards for tidiness

        # Determine Trump
        trump_revealed = current_deck.pop()
        trump_suit = trump_revealed.suit

        # 2. Bidding Phase
        clear_screen()
        print(f"=== ROUND {round_num} BIDDING ===")
        print(f"Trump is: {trump_suit} ({trump_revealed})")
        print(f"Your Hand: {human.hand}")

        # Get Human Bid
        while True:
            try:
                b = int(input(f"Predict wins (0-{round_num}): "))
                if 0 <= b <= round_num:
                    human.bid = b
                    break
            except ValueError:
                pass

        # Get AI Bids (Simple AI: Bid 1 for every Ace or King, +1 if many trumps)
        for p in players:
            if not p.is_human:
                # Rudimentary logic
                high_cards = sum(1 for c in p.hand if c.value > 11)
                trumps = sum(1 for c in p.hand if c.suit == trump_suit)
                p.bid = min(round_num, high_cards + (1 if trumps >= 2 else 0))
                # Judgement "Hook" rule (Total bids != Total cards) is usually played,
                # but omitted here for simplicity.

        # 3. Trick Taking Phase
        start_player_idx = 0  # In real game, rotates. Here fixed for simplicity.
        last_trick_msg = ""

        for trick_idx in range(round_num):
            played_cards = []  # List of (Player, Card)
            lead_card = None

            # Rotate players so winner of last trick starts, or round start order
            # (Simplified: Just iterating list, but respecting lead)

            # Re-order player list based on start_player_idx
            ordered_players = players[start_player_idx:] + players[:start_player_idx]

            for i, p in enumerate(ordered_players):
                # Display Update
                if p.is_human:
                    print_table(round_num, trump_revealed, players, last_trick_msg, lead_card)
                    print(f"Your Hand: {['(' + str(idx + 1) + ')' + str(c) for idx, c in enumerate(p.hand)]}")
                else:
                    print(f"{p.name} is thinking...")

                # Play Card
                lead_suit_curr = lead_card.suit if lead_card else None
                card_played = p.play_card(lead_suit_curr, trump_suit)

                if i == 0:
                    lead_card = card_played

                print(f">> {p.name} plays {card_played}")
                played_cards.append((p, card_played))
                time.sleep(0.8)

            # Evaluate Trick
            winner = determine_trick_winner(played_cards, trump_suit)
            winner.tricks_won += 1
            last_trick_msg = f"{winner.name} won with {dict(played_cards)[winner]}"

            print(f"\n>> {last_trick_msg}")
            time.sleep(2)

            # Winner leads next trick
            start_player_idx = players.index(winner)

        # 4. End of Round Scoring
        clear_screen()
        print(f"=== ROUND {round_num} RESULTS ===")
        for p in players:
            if p.tricks_won == p.bid:
                points = 10 + p.tricks_won
                p.score += points
                print(f"{p.name}: Predict {p.bid}, Won {p.tricks_won} -> SUCCESS (+{points})")
            else:
                print(f"{p.name}: Predict {p.bid}, Won {p.tricks_won} -> FAIL (0)")

        input("\nPress [ENTER] for next round...")

    # End Game
    clear_screen()
    print("=== FINAL SCORES ===")
    players.sort(key=lambda x: x.score, reverse=True)
    for i, p in enumerate(players):
        print(f"{i + 1}. {p.name}: {p.score} points")


if __name__ == "__main__":
    main()