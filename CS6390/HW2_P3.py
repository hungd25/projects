"""

"""


def get_input():
    """
    # Get height and weight from the user and validate. If inputs are (negative numbers or strings),
     the program should throw an error message.
    : return: height, weight
    """

    try:
        # get user input and convert to type float
        height_input = float(input("Enter the person's height: "))
        weight_input = float(input("Enter the person's weight: "))

        # check for negative numbers
        if height_input > 0.0 and weight_input > 0.0:
            return height_input, weight_input  # return height and weight
        else:
            print("Negative values are not allowed.")
            exit()  # exit program
    # if string values, then throw error message
    except ValueError:  # throw exception for float function during version of a non digit
        print("Please enter only numbers.")  # inform user of string input
        exit()  # exit program


def calculate_bmi(height_in, weight_in):
    """
    This function calculates the body mass index
    : param h: height
    : param w: weight
    : return: bmi: body mass index
    """

    try:
        bmi = (weight_in * 703) / (height_in ** 2)  # calculate bmi
        return bmi  # return bmi
    except Exception as error:  # throws error when problem with calculation
        print("There was error calculating BMI, message: %s" % error)  # print error message
        exit()  # exit program


def calculate_weight_category(bmi):
    """
    This function to compute one of the three weight categories
    : param bmi:
    : return: weight_category
    """
    if 18.5 < bmi < 25:  # if bmi is between 18.5 and 25
        weight_category = 'optimal'  # set category to optimal
    elif bmi < 18.5:  # if bmi is less than 18.5
        weight_category = 'underweight'  # set category to underweight
    else:  # bmi > 25
        weight_category = 'overweight'  # set category to overweight
    return weight_category  # return weight_cat


# get input
height, weight = get_input()

# get BMI
BMI = calculate_bmi(height, weight)
# get weight category and print it
print('Based on your BMI of %s . You are %s' % (round(BMI, 2), calculate_weight_category(BMI)))

# End of script
