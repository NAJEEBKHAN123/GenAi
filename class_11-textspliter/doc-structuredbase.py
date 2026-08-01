from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

text = """ class Car:
    # Class attributes
    wheels = 4 

    def __init__(self, brand, color, fuel_efficiency=15):
        # Instance attributes initialized by the user
        self.brand = brand  
        self.color = color  
        self.fuel_efficiency = fuel_efficiency  # km per liter
        
        # Hidden or default state attributes
        self.engine_on = False
        self.odometer = 0       # Total distance tracked in km
        self.fuel_level = 50     # Starts with a full 50-liter tank

    # Method to control engine state
    def toggle_engine(self):
        self.engine_on = not self.engine_on
        status = "started" if self.engine_on else "shut off"
        return f"The {self.brand}'s engine has been {status}."

    # Method that updates internal state (odometer and fuel)
    def drive(self, distance_km):
        if not self.engine_on:
            return "Start the engine first!"
        
        # Calculate required fuel for this trip
        fuel_needed = distance_km / self.fuel_efficiency
        
        if self.fuel_level >= fuel_needed:
            self.odometer += distance_km
            self.fuel_level -= fuel_needed
            return f"The {self.color} {self.brand} drove {distance_km} km."
        else:
            # Not enough fuel for the full trip
            possible_distance = self.fuel_level * self.fuel_efficiency
            self.odometer += possible_distance
            self.fuel_level = 0
            return f"Ran out of gas! Only managed to drive {possible_distance:.1f} km."

    # Method to add resources to the object
    def refuel(self, liters):
        self.fuel_level = min(50, self.fuel_level + liters)  # Max tank size is 50L
        return f"Refueled. Current fuel level: {self.fuel_level} liters."

    # Method to check the dashboard status
    def check_dashboard(self):
        return {
            "Odometer": f"{self.odometer} km",
            "Fuel": f"{self.fuel_level:.1f} L",
            "Engine Running": self.engine_on
        }
"""

# CHANGE THIS LINE from Language.MARKDOWN to Language.PYTHON
splitter = RecursiveCharacterTextSplitter.from_language(
    language = Language.PYTHON,
    chunk_size = 1500,
    chunk_overlap = 0
)

chunks = splitter.split_text(text)

print(f"Total Chunks: {len(chunks)}")
print("\n--- First Chunk ---")
print(chunks[0])

