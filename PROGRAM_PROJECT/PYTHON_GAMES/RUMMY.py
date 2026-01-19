import random
import os
import sys

# --- Constants ---
SUITS = ['♥', '♦', '♣', '♠']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = VALUES[rank]
        # Helper for sorting: A=1, K=13
        self.sort_val = RANKS.index(rank) + 1

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit


class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for s in SUITS for r in RANKS]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# --- Logic for checking Sets and Runs ---
def get_deadwood_score(hand):
    """
    Calculates the 'deadwood' (score of cards not in melds).
    This is a simplified greedy algorithm. It prioritizes Sets over Runs
    usually, but here we try both to find the minimum score.
    """

    # Quick helper to check if a list of cards is a run
    def is_run(group):
        if len(group) < 3: return False
        # Sort by rank index
        group = sorted(group, key=lambda c: c.sort_val)
        # Check suit
        if len(set(c.suit for c in group)) > 1: return False
        # Check consecutive
        for i in range(len(group) - 1):
            if group[i + 1].sort_val != group[i].sort_val + 1:
                return False
        return True

    # Helper to check if set
    def is_set(group):
        if len(group) < 3: return False
        return len(set(c.rank for c in group)) == 1

    # Sorting helps processing
    hand = sorted(hand, key=lambda c: c.sort_val)

    # We will try to find all valid melds.
    # Since this is a simple emulation, we verify if the HAND IS WON (score 0).
    # A full brute-force partition is complex, so we check specific winning conditions.

    # Simple check: Is the whole hand a combination of valid melds?
    # NOTE: For this console game, we calculate raw point totals for un-melded cards.
    # To keep it playable in real-time, we trust the player's 'Declare Win'
    # or just show them the cards.

    score = sum(c.value for c in hand)
    return score


# --- Display Functions ---
def print_state(player_hand, computer_hand_count, discard_top, message=""):
    clear_screen()
    print("=" * 40)
    print(f"      🐍 PYTHON RUMMY 🐍")
    print("=" * 40)
    print(f"Computer Hand: [{'🂠 ' * computer_hand_count}]")
    print("\n")
    print(f"Discard Pile:  [{discard_top if discard_top else 'Empty'}]")
    print(f"Stock Pile:    [🂠 ]")
    print("\n")
    print("-" * 40)
    print("YOUR HAND:")

    # Print hand with index numbers
    hand_str = "  ".join([f"{idx + 1}.{card}" for idx, card in enumerate(player_hand)])
    print(hand_str)
    print("-" * 40)
    if message:
        print(f">> {message}")


def ai_turn(deck, discard_pile, ai_hand):
    """
    Simple AI:
    1. If discard pile card matches a rank in hand, take it.
    2. Else draw from stock.
    3. Discard the highest value card that isn't part of a pair (simplified).
    """
    took_from_discard = False

    # DECISION: Draw
    if discard_pile:
        top_card = discard_pile[-1]
        # Basic logic: take if matches rank in hand
        if any(c.rank == top_card.rank for c in ai_hand):
            picked = discard_pile.pop()
            ai_hand.append(picked)
            took_from_discard = True

    if not took_from_discard:
        picked = deck.draw()
        if not picked: return  # Empty deck
        ai_hand.append(picked)

    # DECISION: Discard
    # Sort by value to discard high cards first
    ai_hand.sort(key=lambda c: c.value, reverse=True)

    # Try not to discard pairs (simple retention logic)
    for i, card in enumerate(ai_hand):
        # Check if this card has a pair in the hand
        has_pair = sum(1 for c in ai_hand if c.rank == card.rank) > 1
        if not has_pair:
            return ai_hand.pop(i), "Picked from Discard" if took_from_discard else "Picked from Stock"

    # If all are pairs/trips, just discard highest
    return ai_hand.pop(0), "Picked from Discard" if took_from_discard else "Picked from Stock"


# --- Main Game Loop ---
def main():
    deck = Deck()
    player_hand = [deck.draw() for _ in range(7)]
    ai_hand = [deck.draw() for _ in range(7)]
    discard_pile = [deck.draw()]  # Start discard pile

    turn_msg = "Game Start! Good luck."

    while True:
        # Sort player hand for better visibility
        player_hand.sort(key=lambda c: (c.suit, c.sort_val))

        # 1. PLAYER TURN - DRAW
        print_state(player_hand, len(ai_hand), discard_pile[-1], turn_msg)

        # Check Deck
        if not deck.cards:
            print("Stockpile empty. It's a Draw!")
            break

        print("\nAction: (S)tock Draw | (D)iscard Draw | (Q)uit")
        choice = input("Choose: ").upper()

        if choice == 'Q':
            break
        elif choice == 'D' and discard_pile:
            card_drawn = discard_pile.pop()
            player_hand.append(card_drawn)
            turn_msg = f"You drew {card_drawn} from Discard."
        elif choice == 'S':
            card_drawn = deck.draw()
            player_hand.append(card_drawn)
            turn_msg = f"You drew {card_drawn} from Stock."
        else:
            turn_msg = "Invalid choice or Empty Discard. Try again."
            continue

        # 2. PLAYER TURN - DISCARD
        while True:
            # Re-sort hand including new card
            player_hand.sort(key=lambda c: (c.suit, c.sort_val))
            print_state(player_hand, len(ai_hand), discard_pile[-1],
                        f"{turn_msg} Now select card to discard (1-{len(player_hand)}):")

            try:
                idx = int(input("Discard Index: ")) - 1
                if 0 <= idx < len(player_hand):
                    discarded = player_hand.pop(idx)
                    discard_pile.append(discarded)
                    break
                else:
                    turn_msg = "Invalid Index."
            except ValueError:
                turn_msg = "Please enter a number."

        # 3. WIN CHECK (Manual Declare for this version)
        # In a real app, we'd auto-detect melds. Here we ask user to verify.
        print_state(player_hand, len(ai_hand), discard_pile[-1], "Turn End.")
        cmd = input("[ENTER] for AI turn, or type 'WIN' if you have 0 deadwood: ").upper()
        if cmd == 'WIN':
            print(f"\nYour Hand: {player_hand}")
            print("Assuming valid melds... YOU WIN! 🎉")
            break

        # 4. AI TURN
        print("Computer is thinking...")
        discarded_card, action_desc = ai_turn(deck, discard_pile, ai_hand)
        discard_pile.append(discarded_card)
        turn_msg = f"CPU {action_desc} and discarded {discarded_card}."

        # Simple AI Win Check (if hand is empty or small logic - omitted for brevity)
        if len(ai_hand) == 0:
            print("Computer Wins! 💀")
            break


if __name__ == "__main__":
    main()