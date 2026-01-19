from abc import ABC, abstractmethod


# ==========================================
# 1. ABSTRACTION
# ==========================================
class SpaceEntity(ABC):
    """
    Abstract Base Class (ABC).
    This acts as a blueprint. You cannot create an instance of this directly.
    It forces all children to implement specific methods.
    """

    @abstractmethod
    def perform_mission(self):
        """Every space entity must have a mission logic."""
        pass

    @abstractmethod
    def report_status(self):
        """Every space entity must be able to report status."""
        pass


# ==========================================
# 2. CLASS STRUCTURE & ENCAPSULATION
# ==========================================
class Starship(SpaceEntity):
    """
    Parent Class representing a generic ship.
    """

    # Class Variable: Shared by ALL instances of Starship
    fleet_population = 0

    def __init__(self, name, max_speed):
        # Instance Variables: Unique to each object
        self.name = name
        self.max_speed = max_speed

        # Protected Variable: (Convention) Should not be accessed outside class/subclasses
        self._shield_level = 100

        # Private Variable: (Harder to access) strictly internal logic
        self.__fuel = 100

        # Increment class variable
        Starship.fleet_population += 1

    # --- GETTERS & SETTERS (Encapsulation) ---
    @property
    def fuel(self):
        """Getter: Allows reading private __fuel as .fuel"""
        return self.__fuel

    @fuel.setter
    def fuel(self, amount):
        """Setter: Adds logic/validation when modifying fuel."""
        if amount < 0:
            print(f"[{self.name}] Error: Fuel cannot be negative!")
            self.__fuel = 0
        elif amount > 100:
            self.__fuel = 100
        else:
            self.__fuel = amount

    # --- INSTANCE METHOD ---
    def take_damage(self, amount):
        self._shield_level -= amount
        if self._shield_level < 0:
            self._shield_level = 0

    # --- IMPLEMENTING ABSTRACT METHODS ---
    def perform_mission(self):
        return "Patrolling sector."

    def report_status(self):
        return f"{self.name} | Shields: {self._shield_level}% | Fuel: {self.fuel}%"

    # ==========================================
    # 3. MAGIC / DUNDER METHODS
    # ==========================================
    def __str__(self):
        """String representation for end-users (e.g. print(obj))"""
        return f"🚀 Starship '{self.name}' (Speed: {self.max_speed})"

    def __repr__(self):
        """String representation for developers/debugging"""
        return f"Starship(name='{self.name}', max_speed={self.max_speed})"

    def __eq__(self, other):
        """Operator Overloading: Allows use of '==' between two ships"""
        if isinstance(other, Starship):
            return self.max_speed == other.max_speed
        return False


# ==========================================
# 4. INHERITANCE & POLYMORPHISM
# ==========================================
class Fighter(Starship):
    """
    Child Class. Inherits from Starship but specializes behavior.
    """

    def __init__(self, name, max_speed, weapon_type):
        # super() calls the Parent's __init__ method
        super().__init__(name, max_speed)
        self.weapon_type = weapon_type

    # POLYMORPHISM: Overriding the parent's method
    def perform_mission(self):
        # We can still use the parent logic if we want
        return f"Intercepting hostiles with {self.weapon_type}!"

    def fire_weapon(self):
        print(f"[{self.name}] Pew pew! Firing {self.weapon_type}.")


class Transporter(Starship):
    """
    Another Child Class.
    """

    def __init__(self, name, cargo_capacity):
        # Hardcoding speed for transporters
        super().__init__(name, max_speed=20)
        self.cargo = []
        self.capacity = cargo_capacity

    # POLYMORPHISM: Completely different mission logic
    def perform_mission(self):
        return f"Transporting {len(self.cargo)} crates."

    # Operator Overloading: Use '+' to load cargo?
    def __add__(self, item):
        """Allows syntax: ship + 'Supplies' """
        if len(self.cargo) < self.capacity:
            self.cargo.append(item)
            print(f"[{self.name}] Loaded {item}")
        else:
            print(f"[{self.name}] Cargo full!")
        return self  # Return self to allow chaining


# ==========================================
# 5. CLASS & STATIC METHODS
# ==========================================
class FleetCommand:
    """Utility class for managing the fleet."""

    @staticmethod
    def convert_lightyears_to_km(ly):
        """
        Static Method: Belongs to the class, but doesn't need 'self' or class data.
        Just a utility function bundled in the namespace.
        """
        return ly * 9.461e12

    @classmethod
    def create_scout_squadron(cls, count):
        """
        Class Method: Receives the class (cls) as first arg.
        Used often as a 'Factory' to create objects.
        """
        squad = []
        for i in range(count):
            # Creates instances of Fighter using the logic inside this method
            squad.append(Fighter(f"Scout-{i + 1}", 200, "Light Laser"))
        return squad


# ==========================================
# 6. DRIVER CODE (Execution)
# ==========================================
if __name__ == "__main__":
    print("--- 1. Instantiation ---")
    s1 = Fighter("X-Wing", 100, "Proton Torpedoes")
    s2 = Transporter("Nostromo", 2)

    print(f"Created: {s1}")  # Uses __str__
    print(repr(s2))  # Uses __repr__

    print("\n--- 2. Encapsulation & Validation ---")
    s1.fuel = -50  # Triggers the setter validation
    print(f"Fuel after invalid set: {s1.fuel}")
    # print(s1.__fuel)     # This would crash! (Private variable)

    print("\n--- 3. Polymorphism ---")
    fleet = [s1, s2]
    for ship in fleet:
        # Same method name, different behavior based on object type
        print(f"{ship.name}: {ship.perform_mission()}")

    print("\n--- 4. Operator Overloading (Magic Methods) ---")
    s2 + "Food" + "Water" + "Aliens"  # Uses __add__ to load items

    print(f"Are speeds equal? {s1 == s2}")  # Uses __eq__

    print("\n--- 5. Class Methods & Static Methods ---")
    dist_km = FleetCommand.convert_lightyears_to_km(0.5)
    print(f"0.5 Lightyears is {dist_km:.2e} km")

    scouts = FleetCommand.create_scout_squadron(3)
    print(f"Squadron created with {len(scouts)} ships.")

    print("\n--- 6. Class Variables ---")
    print(f"Total Ships Built: {Starship.fleet_population}")