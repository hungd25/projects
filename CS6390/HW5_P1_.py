"""


"""
import numpy as np


def get_insurance_data(datafile):
    """
    This function load text file and returns numpy array
    :param datafile:
    :return:
    """
    return np.loadtxt(fname=datafile, delimiter="\t", dtype=str)


def get_age_data(insurance):
    """
    This function returns a slice the age column and return array of age
    :param insurance:
    :return:
    """
    return np.asfarray(insurance[1:, 0], float)


def get_sex_data(insurance):
    """
    This function returns a slice sex data from insurance
    :param insurance:
    :return:
    """
    return insurance[1:, 1]


def get_bmi_data(insurance):
    """
    This function returns a slice bmi data from insurance as float
    :param insurance:
    :return:
    """
    return np.asfarray(insurance[1:, 2], float)


def get_children_data(insurance):
    """
    This function returns a slice children data from insurance as integer
    :param insurance:
    :return:
    """
    return np.asfarray(insurance[1:, 3], int)


def get_smoker_data(insurance):
    """
    This function returns a slice smoker data from insurance
    :param insurance:
    :return:
    """
    return insurance[1:, 4]


def get_region_data(insurance):
    """
    This function returns a slice region data from insurance
    :param insurance:
    :return:
    """
    return insurance[1:, 5]


def get_stats(data, name):
    """
    This function returns the stats(mean,sd, median) for the data
    after it removes any zero value from array
    :param data:
    :param name:
    :return:
    """
    data = data[data != 0]
    mean = np.around(np.mean(data), decimals=2)
    standard_deviation = np.around(np.std(data), decimals=2)
    median = np.around(np.median(np.sort(data)), decimals=2)
    return np.array([name, str(mean), str(standard_deviation), str(median)])


def get_bmi_stats(bmi_data):
    """
    This function gets the bmi stats
    :param bmi_data:
    :return:
    """
    bmi_stats = get_stats(bmi_data, 'bmi')
    return bmi_stats


def get_age_stats(age_data):
    """
    This function gets the age stats
    :param age_data:
    :return:
    """
    bmi_stats = get_stats(age_data, 'age')
    return bmi_stats


def get_bmi_smoker_stats(smoker_data, bmi_data):
    """
    This function gets bmi stats for smokers
    :param smoker_data:
    :param bmi_data:
    :return:
    """
    smoker_bmi = np.where(smoker_data == 'yes', bmi_data, 0)
    non_smoker_bmi = np.where(smoker_data == 'no', bmi_data, 0)
    smoker_bmi_stats = get_stats(smoker_bmi, 'smoker_bmi')
    non_smoker_stats = get_stats(non_smoker_bmi, 'non_smoker_bmi')
    return np.concatenate((smoker_bmi_stats, non_smoker_stats))


def get_bmi_region_stats(region_data, bmi_data):
    """
    This function get bmi stats by region
    :param region_data:
    :param bmi_data:
    :return:
    """
    northeast_bmi = np.where(region_data == 'northeast', bmi_data, 0)
    southeast_bmi = np.where(region_data == 'southeast', bmi_data, 0)
    southwest_bmi = np.where(region_data == 'southwest', bmi_data, 0)
    northwest_bmi = np.where(region_data == 'northwest', bmi_data, 0)
    northeast_bmi_stats = get_stats(northeast_bmi, 'northeast_bmi')
    southeast_bmi_stats = get_stats(southeast_bmi, 'southeast_bmi')
    southwest_bmi_stats = get_stats(southwest_bmi, 'southwest_bmi')
    northwest_bmi_stats = get_stats(northwest_bmi, 'northwest_bmi')
    return np.concatenate((northeast_bmi_stats, southeast_bmi_stats,
                          southwest_bmi_stats, northwest_bmi_stats), axis=0)


def get_bmi_sex_stats(sex_data, bmi_data):
    """
    This function get the bmi stats by sex
    :param sex_data:
    :param bmi_data:
    :return:
    """
    male_bmi = np.where(sex_data == 'male', bmi_data, 0)
    female_bmi = np.where(sex_data == 'female', bmi_data, 0)
    male_bmi_stats = get_stats(male_bmi, 'male_bmi')
    female_stats = get_stats(female_bmi, 'female_bmi')
    return np.concatenate((male_bmi_stats, female_stats))


def get_bmi_children_stats(children_data, bmi_data):
    """
    This function get the bmi stats with people that have more than 2 children
    :param children_data:
    :param bmi_data:
    :return:
    """
    children_bmi = np.where(children_data > 2, bmi_data, 0)
    children_bmi_stats = get_stats(children_bmi, 'children_bmi')
    return children_bmi_stats


def get_expenses_data(insurance):
    """
    This function slice the expense from insurance and return by descending order
    :param insurance:
    :return:
    """
    expenses = np.flip(np.sort(np.asfarray(insurance[1:, 6], float)))
    return np.asfarray(expenses, str)


def get_expenses_bmi_stats(expenses_data, insurance):
    """
    This function
    :param expenses_data:
    :return:
    """
    end_index = int(.2 * expenses_data.size)
    expenses_twenty_percent = expenses_data[0:end_index]
    bmi_data = np.where(expenses_twenty_percent == insurance[1:] )


def combine_results(children_stats, region_stats,
                    smoker_stats, sex_stats,
                    age_stats, bmi_stats):
    """
    This function concatenate all stats data into np array
    :param children_stats:
    :param region_stats:
    :param smoker_stats:
    :param sex_stats:
    :param age_stats:
    :param bmi_stats:
    :return:
    """
    headers = np.array(['type', 'mean', 'standard_deviation', 'median'])
    return (np.concatenate((headers, children_stats, region_stats,
                           smoker_stats, sex_stats,
                           age_stats, bmi_stats))).reshape(12, 4)


def save_stats_to_file(stats_data, file_name):
    """
    This function writes the stat data to a txt file
    :param stats_data:
    :param file_name:
    :return:
    """
    np.savetxt(file_name, stats_data, delimiter=' ', fmt='%20s')



insurance = get_insurance_data('insurance.txt')
bmi_data = get_bmi_data(insurance)
age_data = get_age_data(insurance)
region_data = get_region_data(insurance)
sex_data = get_sex_data(insurance)
children_data = get_children_data(insurance)
smoker_data = get_smoker_data(insurance)
bmi_stats = get_bmi_stats(bmi_data)
age_stats = get_age_stats(age_data)
children_stats = get_bmi_children_stats(children_data, bmi_data)
region_stats = get_bmi_region_stats(region_data,bmi_data)
smoker_stats = get_bmi_smoker_stats(smoker_data, bmi_data)
sex_stats = get_bmi_sex_stats(sex_data, bmi_data)
results = combine_results(children_stats, region_stats,
                          smoker_stats, sex_stats,
                         age_stats, bmi_stats)
save_stats_to_file(results, 'insurance_results.txt')

