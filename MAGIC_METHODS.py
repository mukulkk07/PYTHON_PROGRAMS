class MagicGrimoire:
    """
    A class representing a Wizard's Spellbook.
    Demonstrates the power of Python's Magic (Dunder) Methods.
    """

    # ==========================================
    # 1. Initialization & Construction
    # ==========================================
    def __init__(self, owner, mana_capacity):
        """Called when a new object is created: book = MagicGrimoire(...)"""
        self.owner = owner
        self.mana = mana_capacity
        self.spells = {}  # Dictionary to store {spell_name: power_level}
        print(f"--> [__init__] A new Grimoire bound to {self.owner} created.")

    # ==========================================
    # 2. String Representation
    # ==========================================
    def __str__(self):
        """
        Called by: print(book) or str(book)
        Purpose: A readable string for end-users.
        """
        return f"Grimoire of {self.owner} (Containing {len(self.spells)} spells)"

    def __repr__(self):
        """
        Called by: repr(book) or checking the object in the interactive shell.
        Purpose: An unambiguous string for developers (often used for debugging).
        """
        return f"MagicGrimoire(owner='{self.owner}', mana={self.mana}, spells={self.spells})"

    # ==========================================
    # 3. Container Emulation (Dictionary behavior)
    # ==========================================
    def __len__(self):
        """Called by: len(book)"""
        return len(self.spells)

    def __getitem__(self, spell_name):
        """Called by: book['Fireball']"""
        if spell_name in self.spells:
            return f"Reading spell details: {spell_name} (Power: {self.spells[spell_name]})"
        return "Spell not found (The pages are blank)."

    def __setitem__(self, spell_name, power):
        """Called by: book['Fireball'] = 50"""
        self.spells[spell_name] = power
        print(f"--> [__setitem__] Inscribed '{spell_name}' with power {power}.")

    def __contains__(self, spell_name):
        """Called by: 'Fireball' in book"""
        return spell_name in self.spells

    # ==========================================
    # 4. Arithmetic Operators (Math)
    # ==========================================
    def __add__(self, other):
        """
        Called by: book1 + book2
        Purpose: Merges two books into a new one.
        """
        if isinstance(other, MagicGrimoire):
            new_owner = f"{self.owner} & {other.owner}"
            new_mana = self.mana + other.mana
            new_book = MagicGrimoire(new_owner, new_mana)

            # Merge spells
            new_book.spells.update(self.spells)
            new_book.spells.update(other.spells)

            print(f"--> [__add__] Fused two Grimoires into one!")
            return new_book
        return NotImplemented

    # ==========================================
    # 5. Comparison Operators
    # ==========================================
    def __gt__(self, other):
        """
        Called by: book1 > book2
        Logic: A book is 'greater' if it has more mana capacity.
        """
        return self.mana > other.mana

    # ==========================================
    # 6. Callable Objects
    # ==========================================
    def __call__(self, spell_name):
        """
        Called by: book('Fireball')
        Purpose: Allows the object itself to be used like a function.
        """
        if spell_name in self.spells:
            return f"*** CASTING {spell_name}! *** (Cost: {self.spells[spell_name]} Mana)"
        return "Fizzle... You don't know that spell."


# ==========================================
# Main Execution Block
# ==========================================
if __name__ == "__main__":

    print("--- 1. Initialization (__init__) ---")
    gandalf_book = MagicGrimoire("Gandalf", 100)
    saruman_book = MagicGrimoire("Saruman", 80)

    print("\n--- 2. Representation (__str__ vs __repr__) ---")
    # Uses __str__
    print(f"User View: {gandalf_book}")
    # Uses __repr__
    print(f"Dev View:  {repr(gandalf_book)}")

    print("\n--- 3. Container Methods (__setitem__, __getitem__, __len__) ---")
    # Uses __setitem__
    gandalf_book['Light'] = 10
    gandalf_book['Fireball'] = 50

    # Uses __len__
    print(f"Number of spells: {len(gandalf_book)}")

    # Uses __getitem__
    print(gandalf_book['Fireball'])

    # Uses __contains__
    if 'Light' in gandalf_book:
        print("Yes, the spell 'Light' is in the book.")

    print("\n--- 4. Comparison (__gt__) ---")
    if gandalf_book > saruman_book:
        print(f"{gandalf_book.owner}'s book is stronger than {saruman_book.owner}'s.")

    print("\n--- 5. Arithmetic (__add__) ---")
    # This triggers __add__. It creates a new book merging both.
    merged_book = gandalf_book + saruman_book
    print(merged_book)  # Uses __str__ on the new book

    print("\n--- 6. Callable (__call__) ---")
    # We are calling the object instance as if it were a function!
    cast_result = gandalf_book('Fireball')
    print(cast_result)