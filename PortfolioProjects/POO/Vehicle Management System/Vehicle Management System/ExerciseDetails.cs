//--------------Objective-----------------
//Create an abstract class.
//Derive subclasses from it.
//Implement abstract methods in the subclasses.


//-----------Description---------------------
//A vehicle park is composed of cars and trucks, which share common characteristics grouped in the Vehicle class.
//**Each vehicle is defined by:
//A registration number (automatically incremented each time a new vehicle is created),
//The model year,
//The price.
//All attributes in the Vehicle class are private, which means you must provide accessors (get) and mutators (set), or use properties.
//The Vehicle class also contains two abstract methods:
//Start()
//Accelerate()
//These will be defined in the derived classes with their own custom messages.
//The ToString() method in the Vehicle class returns a string containing:
//The registration number
//The model year
//The price
//The Car and Truck classes extend the Vehicle class and provide concrete implementations of the Start() and Accelerate() methods, each displaying personalized messages.

//--------------Tasks---------------------
//Create the abstract class Vehicle.
//Create the Car and Truck classes that inherit from it.
//Create a Test class that tests both the Car and Truck classes.