from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import statistics


# ==========================================
# 1. ABSTRACT BASE CLASS (Abstraction)
# ==========================================
class Student(ABC):
    """
    Abstract base class representing a generic student.
    Enforces that all child classes must implement specific methods.
    """

    # Class variable: Tracks total enrollment
    total_enrollment = 0

    def __init__(self, name: str, roll_no: int):
        self.name = name
        self.roll_no = roll_no
        # Encapsulation: Grades are private to prevent direct tampering
        self._grades: Dict[str, float] = {}
        Student.total_enrollment += 1

    @property
    def gpa(self) -> float:
        """Calculates GPA dynamically based on current grades."""
        if not self._grades:
            return 0.0
        return round(statistics.mean(self._grades.values()), 2)

    def add_grade(self, subject: str, score: float) -> None:
        """Secure method to add grades with validation."""
        if 0.0 <= score <= 100.0:
            self._grades[subject] = score
        else:
            print(f"Error: Grade {score} for {self.name} is out of bounds (0-100).")

    @abstractmethod
    def get_academic_status(self) -> str:
        """
        Polymorphic Method:
        Every subclass must define its own version of 'academic status'.
        """
        pass

    def __str__(self):
        return f"ID: {self.roll_no} | Name: {self.name}"


# ==========================================
# 2. INHERITANCE & SPECIALIZATION
# ==========================================
class Undergraduate(Student):
    """
    Represents a standard bachelor's student.
    """

    def __init__(self, name: str, roll_no: int, major: str, year: int):
        super().__init__(name, roll_no)
        self.major = major
        self.year = year

    # POLYMORPHISM: Implementation specific to Undergrads
    def get_academic_status(self) -> str:
        base_status = "Good Standing" if self.gpa >= 60 else "Academic Probation"
        return f"[Undergrad - Year {self.year}] Major: {self.major} | Status: {base_status}"

    def attend_lecture(self):
        return f"{self.name} is attending a lecture on {self.major}."


class ResearchScholar(Student):
    """
    Represents a PhD or Masters student doing research.
    """

    def __init__(self, name: str, roll_no: int, thesis_topic: str):
        super().__init__(name, roll_no)
        self.thesis_topic = thesis_topic
        self.publications = 0

    # POLYMORPHISM: Implementation specific to Researchers
    def get_academic_status(self) -> str:
        # Research scholars are judged by publications, not just GPA
        status = "On Track" if self.publications > 0 else "Needs Publications"
        return f"[Researcher] Thesis: '{self.thesis_topic}' | Status: {status}"

    def publish_paper(self):
        self.publications += 1
        return f"{self.name} published a new paper! Total: {self.publications}"


# ==========================================
# 3. CLASSROOM MANAGER (Composition)
# ==========================================
class UniversityClass:
    """
    Container class to manage the group of students.
    """

    def __init__(self, course_name: str):
        self.course_name = course_name
        self.students: List[Student] = []

    def enroll_student(self, student: Student):
        self.students.append(student)

    def generate_report(self):
        print(f"\n--- Report for {self.course_name} ---")
        print(f"{'Roll No':<10} {'Name':<20} {'GPA':<10} {'Details'}")
        print("-" * 80)

        for student in self.students:
            # Here is POLYMORPHISM in action:
            # We call .get_academic_status() on every student.
            # The program automatically selects the correct version (Undergrad vs Researcher).
            details = student.get_academic_status()
            print(f"{student.roll_no:<10} {student.name:<20} {student.gpa:<10} {details}")


# ==========================================
# 4. DRIVER CODE
# ==========================================
if __name__ == "__main__":
    # Initialize the Classroom
    comp_sci_101 = UniversityClass("CS Advanced Seminar")

    # --- Create 5 Students (Mix of types) ---

    # 1. An Undergraduate (Freshman)
    s1 = Undergraduate("Alice Vance", 101, "Computer Science", 1)
    s1.add_grade("Python", 92)
    s1.add_grade("Math", 88)

    # 2. An Undergraduate (Senior)
    s2 = Undergraduate("Bob Smith", 102, "Physics", 4)
    s2.add_grade("Quantum Mech", 45)  # Low grade
    s2.add_grade("Calculus", 60)

    # 3. A Research Scholar (PhD)
    s3 = ResearchScholar("Charlie Zheng", 103, "AI Ethics")
    s3.add_grade("Research Methodology", 95)
    s3.publish_paper()  # Specific method for researchers

    # 4. An Undergraduate (Junior)
    s4 = Undergraduate("Diana Prince", 104, "Cybersecurity", 3)
    s4.add_grade("Cryptography", 98)
    s4.add_grade("Networks", 91)

    # 5. A Research Scholar (Masters)
    s5 = ResearchScholar("Evan Wright", 105, "Blockchain")
    s5.add_grade("Data Structures", 82)
    # Evan has no publications yet

    # --- Enroll them ---
    roster = [s1, s2, s3, s4, s5]
    for s in roster:
        comp_sci_101.enroll_student(s)

    # --- Run the Report ---
    # This demonstrates Polymorphism: different output formats for different object types
    comp_sci_101.generate_report()

    print("\n--- Individual Activities ---")
    print(s1.attend_lecture())  # Method only exists on Undergraduate
    print(s3.publish_paper())  # Method only exists on ResearchScholar