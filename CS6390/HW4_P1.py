"""

"""


def get_world_series_wins(file_location):
    """
    This function reads the World Series Data and return a list type per line
    :param file_location:
    :return: list of wins
    """
    series_file = open(file_location, 'r')  # open file with read only
    series_wins = series_file.read().splitlines()  # read all lines and return a list
    series_file.close()  # close file
    return series_wins  # return series of wins


def get_team_wins_count(series_wins):
    """
    This function count how many times a win based on the number of appearences in the list
    :param series_wins:
    :return: win_counts
    """
    win_counts = {}  # creates a empty dictionary
    for team in series_wins:  # loop through series wins
        if team in win_counts:  # if team(key) in win counts just add one to win count
            win_counts[team] += 1  # add one to current win count
        else:
            win_counts[team] = 1  # if team(key) not in win_counts add key and value 1
    return win_counts  # return win_counts


def get_team_wins_year(series_wins):
    """
    This function  append the year of to team base on appearences in the list
    :param series_wins:
    :return: win_years
    """
    win_years = {}  # creates a empty dictionary
    year = 1903  # initialize year
    for team in series_wins:
        if year == 1904 or year == 1994:  # if year is 1904 or 1994, skip it
            year += 1  # increment year by 1
        if team in win_years:  # if team(key) in win_years append the year to list
            win_years[team].append(year)
        else:
            win_years[team] = [year]  #if team(key) not in win_years, value is list with year
        year += 1  # increment year by 1
    return win_years  # return win_years


def show_team_win_year(win_years):
    """
    This function print the win years
    :param win_years:
    :return:
    """
    print("%s" % ('-' * 50))  # print 50 dashes
    print('{:26} {}'.format('Team:', 'Win Years')) # print title
    print("%s" % ('-' * 50))  # print 50 dashes
    for team in sorted(win_years.keys()):  # loop through a sorted win_years by key
        print("{:26} {}".format(team + ":", win_years[team]))


def show_team_total_wins(win_counts):
    """
    This function print the win counts
    :param win_counts:
    :return:
    """
    print("%s" % ('-' * 50))  # print 50 dashes
    print('{:26} {}'.format('Team:', 'Total Wins')) # print title
    print("%s" % ('-' * 50))  # print 50 dashes
    for team in sorted(win_counts, reverse=True, key=win_counts.get):  # loop sorted win_counts by value descending
        print("{:26} {}".format(team + ":", win_counts[team]))


def show_team_win_bar_graph(win_counts):
    """
    This function print the win counts
    :param win_counts:
    :return:
    """
    print("%s" % ('-' * 50))  # print 50 dashes
    print('{:26} {}'.format('Team:', 'Total Wins Bar Graph')) # print title
    print("%s" % ('-' * 50))  # print 50 dashes
    for team in sorted(win_counts, reverse=True, key=win_counts.get):  # loop sorted win_counts by value descending
        print("{:26} {}".format((team + "("+ str(win_counts[team]) + ")" + ":"), '*' * win_counts[team]))



file_location = "WorldSeriesWinners.txt"  # location of file
series_wins = get_world_series_wins(file_location)  # call read file and store wins data
win_counts = get_team_wins_count(series_wins)  # call get win count with series wins
win_years = get_team_wins_year(series_wins)  # call get team win years with series wins
show_team_win_year(win_years)  # call print win years
show_team_total_wins(win_counts)  # call print total wins count
show_team_win_bar_graph(win_counts)  # call print total wins bar graph