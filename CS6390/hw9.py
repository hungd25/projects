"""



"""

import pandas as pd
from datetime import datetime


# Import Data with pandas read excel
student = pd.read_excel('Student.xlsx')
match_history = pd.read_excel('Match_History.xlsx')
tutor = pd.read_excel('Tutor.xlsx')

# 1. Tutors with Dropped status and achieved cert after 4/01/2018
tutor_dropped = tutor['CertDate'] = pd.to_datetime(tutor['CertDate'])  # Convert CertDate column to datetime object
# query tutorstaty = dropped and Certdate > 2018-04-01
tutor_dropped = tutor[(tutor['TutorStatus'] == "Dropped") & (tutor['CertDate'] > pd.Timestamp(2018,4,1))]
print('*' * 100)
print('#1 Tutors with Dropped status and achieved cert after 4/01/2018')
print(tutor_dropped)
print('*' * 100)


# 2. Average length of time a student has stayed in the program
student_time = match_history['StartDate'] = pd.to_datetime(match_history['StartDate'])  # convert StartDate to datetime
# Fill Enddate NA with today's date
student_time = match_history['EndDate'] = match_history['EndDate'].fillna(pd.to_datetime(datetime.today().date()))
# Subtract enddate with Stardate and get average
avg_time = (match_history['EndDate'] - match_history['StartDate']).mean()
print('#2 length of time a student has stayed in the program')
print(avg_time)
print('*' * 100)


# 3. Students who have been matched in 2018 with a tutor whos status is Temp Stop
tutor_match = match_history.merge(tutor, how='inner')  # merge match history with tutor table inner join
tutor_match = tutor_match[pd.DatetimeIndex(tutor_match['StartDate']).year == 2018] # filter only 2018 startdate
tutor_match = tutor_match[tutor_match['TutorStatus'] == 'Temp Stop']  # filter by Dropped Status
print('# 3. Students who have been matched in 2018 with a tutor whos status is Temp Stop')
print(tutor_match)
print('*' * 100)


# 4. Students read scores who were taught by a tutor whos status is Dropped
# Select ReadScore where TutorStatus is Dropped
read_scores = student[student['StudentID'] == int(match_history[tutor.merge(match_history)
                                                  ['TutorStatus'] == 'Dropped']['StudentID'])]['ReadScore']
print('# 4. Students read scores who were taught by a tutor whos status is Dropped')
print(read_scores)
print('*' * 100)

# 5. Tutors who taught two or more students
# group student with more than 2 tutors and create new boolean table
two_plus = pd.DataFrame({'2+students':(match_history.groupby('StudentID').size() >=2)})
two_plus.index.name = 'index'  # rename index for merge to work
two_plus['StudentID'] = two_plus.index  # add STudentId column
two_plus_match = match_history.merge(two_plus)  # merge match_history with new boolean table
tutor_two_plus = two_plus_match[two_plus_match['2+students'] == True]  # filter by 2+ students only
print('2# 5. Tutors who taught two or more students')
print(tutor_two_plus)
print('*' * 100)

# 6. List of all students, their read score, their tutors, and tutors status 
matched_student = match_history.merge(student, how='outer')  # merge match history with student outer join
Student_Tutor = matched_student.merge(tutor, how='outer')  # merge new table with tutor outer join
Student_Tutor[['StudentID', 'TutorID', 'TutorStatus']].to_excel('Student_Tutor.xlsx')   # save only selected columns
print('# 6. List of all students, their read score, their tutors, and tutors status ')
print(Student_Tutor[['StudentID','ReadScore', 'TutorID', 'TutorStatus']])
print('Saved to Student_Tutor.xlsx')
print('*' * 100)

# 7. For each student group, list the number of tutors who have been matched with that group
student_match = match_history.merge(student, how='outer')  # merge match history with student outer join
# Group by StudentGroup with TutorID match
num_student_match = student_match.groupby('StudentGroup')['TutorID'].count()
print('# 7. For each student group, list the number of tutors who have been matched with that group')
print(num_student_match)
print('*' * 100)
# 8. List all active students who started in May and June
# Filter by students that started in May or June
students_active = match_history[(pd.DatetimeIndex(match_history['StartDate']).month == 5)
              | (pd.DatetimeIndex(match_history['StartDate']).month == 6)]
print('# 8. List all active students who started in May and June')
print(students_active)
print('*' * 100)

# 9. All students who have not been tutored yet
student_match = match_history.merge(student, how='outer')  # merge match history with students outer join
students_not_tutored = student_match[student_match['MatchID'].isna()]  # filter by MatchID is null
print('# 9. All students who have not been tutored yet')
print(students_not_tutored)
print('*' * 100)

# 10. All tutors who did not tutor any students
tutor_match = match_history.merge(tutor, how='outer')  # merge match history with tutor outer join
tutors_not_matched = tutor_match[tutor_match['MatchID'].isna()]  # filter by MatchID is null
print('# 10. All tutors who did not tutor any students')
print(tutors_not_matched)
print('*' * 100)


# End of scripts