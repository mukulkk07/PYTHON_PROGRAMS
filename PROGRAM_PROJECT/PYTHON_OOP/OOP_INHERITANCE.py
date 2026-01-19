class Person:
    """
    The Base Class (Parent).
    Represents a generic person in the university.
    """

    def __init__(self, name, age, email):
        # These attributes are common to all children of this class
        self.name = name
        self.age = age
        self.email = email
        print(f"-> Person Constructor called for {self.name}")

    def introduce(self):
        """A method that can be used by all subclasses"""
        return f"Hi, I'm {self.name}, and I am {self.age} years old."

    def get_role(self):
        """This method is intended to be overridden by child classes"""
        return "Generic Person"


class Student(Person):
    """
    Derived Class (Child).
    Inherits from Person.
    """

    def __init__(self, name, age, email, student_id):
        # 1. Initialize the Parent class using super()
        # This ensures 'name', 'age', and 'email' are set up correctly by the logic in Person
        super().__init__(name, age, email)

        # 2. Add attributes specific to Student
        self.student_id = student_id
        self.courses = []
        print(f"   -> Student Constructor called for {self.name}")

    def enroll(self, course_name):
        """New method specific to Student"""
        self.courses.append(course_name)
        print(f"{self.name} has enrolled in {course_name}.")

    # METHOD OVERRIDING:
    # We replace the parent's get_role method with a specialized one
    def get_role(self):
        return "Student"

    def show_info(self):
        # We can access parent methods (introduce) and child data (student_id)
        base_intro = self.introduce()
        return f"{base_intro} I am a student with ID: {self.student_id}."


class Professor(Person):
    """
    Derived Class (Child).
    Inherits from Person.
    """

    def __init__(self, name, age, email, staff_id, salary):
        # Initialize Parent
        super().__init__(name, age, email)

        # Add attributes specific to Professor
        self.staff_id = staff_id
        self.salary = salary
        print(f"   -> Professor Constructor called for {self.name}")

    # METHOD OVERRIDING
    def get_role(self):
        return "Professor"

    def give_raise(self, percentage):
        """New method specific to Professor"""
        raise_amount = self.salary * (percentage / 100)
        self.salary += raise_amount
        print(f"{self.name} got a raise! New salary: ${self.salary:.2f}")


# ==========================================
# Main Execution Block
# ==========================================
if __name__ == "__main__":
    print("--- 1. Creating a Student Object ---")
    # 'alice' is an instance of Student.
    # Notice it triggers the Person constructor first, then the Student constructor.
    alice = Student("Alice Smith", 20, "alice@uni.edu", "S12345")

    print("\n--- 2. Using Inherited Methods ---")
    # Alice can use introduce() even though it was defined in Person, not Student
    print(alice.introduce())

    print("\n--- 3. Using Child-Specific Methods ---")
    alice.enroll("Computer Science 101")
    alice.enroll("History 200")

    print("\n--- 4. Creating a Professor Object ---")
    # 'dr_bob' is an instance of Professor
    dr_bob = Professor("Dr. Bob Jones", 45, "bob@uni.edu", "P9876", 80000)

    print("\n--- 5. Demonstrating Polymorphism (Overriding) ---")
    # Both classes have a get_role() method, but they behave differently
    people = [alice, dr_bob]

    for person in people:
        print(f"{person.name} is a: {person.get_role()}")

    print("\n--- 6. Modifying Child State ---")
    dr_bob.give_raise(10)