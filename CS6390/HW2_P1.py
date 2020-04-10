"""

"""

# Variables to represent the grade thresholds
A_score = 90.0
B_score = 80.0
C_score = 70.0
D_score = 60.0


def validate_input(score_in):
    """
        This function validates the user input, convert user input to float and return value
        : argument score_in
        : return float(score)
    """
    score = 0.0
    try:
        score = float(score_in)  # Convert user input to float number
        if score > 100.0 or score < 0.0:  # check input for negative number and out of limit
            print("Score should be between 0.0 and 100.0")  # inform user of negative digit
            exit()  # exit program

    except ValueError:  # throw exception for float function during version of a non digit
        print("Please enter only numbers")  # inform user of string input
        exit()  # exit program

    return score  # return the decimal/float number


def calculate_grade(score):
    """
        This function determine grade letter based on score
        : argument score
        : return string grade
    """

    if score >= A_score:  # score > 90.0
        grade = 'A'
    elif score >= B_score:  # score > 80.0
        grade = 'B'
    elif score >= C_score:  # score > 70.0
        grade = 'C'
    elif score >= D_score:  # score > 60.0
        grade = 'D'
    else:
        grade = 'F'  # score not in grade threshold

    return grade  # return the letter grade


# Get a test score from the user.
score_input = input('Enter a score between 0.0 and 100.0: ')

# get validated input.
score_validated = validate_input(score_input)

# get grade.
course_grade = calculate_grade(score_validated)
print(course_grade + " Grade")  # print results

# End of script
