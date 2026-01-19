#OBJECTS : BUNDLE OF RELATED ATTRIBUTES(VARIABLES) AND METHODS(FUNCTIONS)
#CLASSES : BLUEPRINT FOR CREATING AND DESIGNING THE STRUCTURES AND LAYOUTS FOR OBJECTS
class car:
    def __init__(self,brand,model,year):
        self.brand = brand
        self.model = model
        self.year = year
    def printcar(self):
        print(f"{self.brand} {self.model} {self.year}")
    def drive(self):
        print("Driving")
    def stop(self):
        print("Stopping")

car1 = car("BMW","M","2009")
print(car1.brand)
print(car1.model)
print(car1.year)
