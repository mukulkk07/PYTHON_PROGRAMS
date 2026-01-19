from abc import ABC, abstractmethod


# ==========================================
# 1. The Abstract Base Class (The Blueprint)
# ==========================================
class PaymentMethod(ABC):
    """
    This class forces all children to follow a specific rule:
    They MUST have a 'pay' method.
    """

    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def receipt(self):
        pass


# ==========================================
# 2. The Concrete Classes (The Forms)
# ==========================================

class CreditCard(PaymentMethod):
    def __init__(self, card_number, cvc):
        self.card_number = card_number
        self.cvc = cvc

    # POLYMORPHISM IN ACTION:
    # Same method name 'pay', but unique logic for Credit Cards
    def pay(self, amount):
        # In a real app, this would contact a bank API
        print(f"[Credit Card] Verifying security code {self.cvc}...")
        print(f"[Credit Card] Charging ${amount} to card ending in {self.card_number[-4:]}.")

    def receipt(self):
        return "Transaction verified by VISA."


class PayPal(PaymentMethod):
    def __init__(self, email):
        self.email = email

    # POLYMORPHISM IN ACTION:
    # Same method name 'pay', but unique logic for PayPal
    def pay(self, amount):
        print(f"[PayPal] Logging into account {self.email}...")
        print(f"[PayPal] Transferring ${amount} from digital wallet.")

    def receipt(self):
        return f"Sent to email: {self.email}"


class Bitcoin(PaymentMethod):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address

    # POLYMORPHISM IN ACTION:
    # Same method name 'pay', but unique logic for Crypto
    def pay(self, amount):
        print(f"[Bitcoin] Pinging blockchain network...")
        print(f"[Bitcoin] Sending ${amount} equivalent to address {self.wallet_address[:8]}...")

    def receipt(self):
        return "Hash: 0x5f3a... Verified on Blockchain."


# ==========================================
# 3. The Polymorphic Function
# ==========================================

def checkout(payment_object, total_amount):
    """
    This function represents the power of Polymorphism.

    It does not know if 'payment_object' is a Card, PayPal, or Bitcoin.
    It doesn't care. It simply trusts that the object has a .pay() method.
    """
    print(f"\n--- Initiating Checkout for ${total_amount} ---")

    # We treat all objects exactly the same way here
    payment_object.pay(total_amount)
    print(f"Receipt: {payment_object.receipt()}")
    print("---------------------------------------------")


# ==========================================
# Main Execution Block
# ==========================================
if __name__ == "__main__":
    # Create different objects
    my_card = CreditCard("1234-5678-9012-3456", "123")
    my_paypal = PayPal("user@example.com")
    my_crypto = Bitcoin("1A1zP1eP5QGefi2DMPS765")

    # Store them in a list
    # This list contains different types, but they are all 'PaymentMethods'
    shopping_cart = [
        (my_card, 100),
        (my_paypal, 55.50),
        (my_crypto, 2000)
    ]

    # Iterate and process
    for method, cost in shopping_cart:
        # The magic happens here:
        # The 'checkout' function adapts automatically to the object passed to it.
        checkout(method, cost)