'''
Homework-1
Problem-2

'''
# ///////////////////////////////////////////////////////////////////////////

# Display program to user
print("This program calculates the balance of an account after", 
       "a specified number of years")

# Ask the user to input the principal amount, annual interest rate, 
# number of times per year, and the number of years

# P holds principal amount originally deposited 
P = input("Enter the principal amount.\n")   
# r holds annual interest rate
r = input("Enter the annual interest rate (in decimals).\n")
# holds number of times per year interest is compounded
n = input("Enter the number of times per year that interest is compounded." 
          + "(If interest is compounded monthly, enter 12. " 
          + "If interest is compounded quarterly, enter 4.)\n")
# t holds the specified number of years
t = input("Enter the specified number of years.\n")

# Program calculates balance if values are valid
try:
    A = float(P) * (1 + (float(r)/float(n)))**(float(n)*float(t))
    print("\nThe balance in the account after", t, "years is", "$", round(A, 2))

except:
    print("A valid number was not entered above. End of program.")


# End of script 
