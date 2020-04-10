'''

Homework-1 
Problem-1

'''
# ///////////////////////////////////////////////////////////////////////////

# Display program to user
print("This program converts Celsius temperatures to Fahrenheit", 
       "temperatures.\n")

# Ask the user to input a temperature in Celsius
C = input("Enter a temperature in Celsius\n")   # holds Celsius temperature

# Display the temperature converted to Fahrenheit
try:    # confirm user input is a number
    F = round((9/5)*float(C) + 32, 2)    # holds Fahrenheit conversion
    print(C, "degrees Celsius is equal to", F, "degrees Fahrenheit.")
    
except: # if user input is not a number
    print("A valid number was not entered. End of program.")


# End of script 
