"""

"""


def kinetic_energy(mass, velocity):
    """
    : param mass:
    : param velocity:
    : return kinetic energy

    This function calculate kinetic energy and returns kinetic energy

    """
    ke = 0.5 * mass * (velocity * velocity)  # calculate kinetic energy
    return ke


# Display program to user
print("This program calculates the kinetic energy of an object.")

mass_float = 0.0
velocity_float = 0.0

# Ask the user to enter mass and velocity
try:
    mass_float = float(input("Enter the object's mass in kilograms: "))
    velocity_float = float(input("Enter the object's velocity in meters per second: "))

    if mass_float < 0.0 or velocity_float < 0.0:  # check input for negative number
        print("Negative values are not allowed.")
        exit()  # exit program
except ValueError:  # throw exception for float function during version of a non digit
    print("Please enter only numbers.")  # inform user of string input
    exit()  # exit program

# Call kinetic function
kin_energy = kinetic_energy(mass_float, velocity_float)

# Print kinetic energy rounded to nearest 2 decimal
print("The object's kinetic energy is equal to",
      round(kin_energy, 2), "Joules.")

# End of script
