"""

"""


import pandas as pd

def set_pandas_display_options() -> None:
    display = pd.options.display

    display.max_columns = 1000
    display.max_rows = 1000
    display.max_colwidth = 199
    display.width = None


def get_csv_data(csv_file):
    """
    Read in excel file with pandas and return one dataframe or a dict of dataframes based on
    the number of sheets found.
    :param csv_file: Full path of excel file
    :return:
    """
    print('Reading csv file %s' % csv_file)
    csv_data = pd.read_csv(csv_file)  # read csv
    print('%s loaded' % csv_file)
    return csv_data  # return csv data frame


def write_csv_data(csv_dataframe, path):
    """
    Write data frame to a csv file.
    :param csv_dataframe: panda dataframe
    :param path: path of csv file
    """
    csv_data = csv_dataframe.to_csv(path, index=False)  # write to csv
    print('Saved to %s' % path)


def get_missing_values_for_feature(feature):
    """
    Get feature missing value rate
    :param feature: feature series
    :return: bool_missing_values
    """
    bool_missing_values = feature.isnull()  # get bool of null/na
    return bool_missing_values


def get_inconsistence_value_for_feature(feature, expected_values, values_only=False):
    """
    Get feature non-matching expected values from series
    :param feature: feature df series
    :return: bool_inconsist_values or inconstence_values
    """
    if values_only:  # get only the inconsistence values
        inconstence_values = []
        for value in feature.unique():
            if value not in expected_values:
                inconstence_values.append(value)
        return inconstence_values
    else:  # get series bool of of inconsitence values
        bool_inconsist_values = (~ feature.isin(expected_values))
    return bool_inconsist_values


def get_bool_rate(bool_values):
    """
    Get feature non-matching expected values from series
    :param feature: feature df series
    :return: rate
    """
    if True in bool_values.unique():  # True in bool series
        true_count = bool_values.value_counts()[True]  # get count of all True
        rate = round((true_count / bool_values.size) * 100, 2)   # true divides by total and then get rounded
    else:
        return 0, 0  # no Tru in bool series
    return true_count, rate


def generate_summary_for_features(csv_df):
    """

    :param csv_df:
    :return:
    """
    summary_table = {"Features": [0, 1, 2, 3, 4, 5, 6, 7], "Missing Values(MV)": [0, 1, 2, 3, 4, 5, 6, 7],
                     "% of MV (MV / n)": [0, 1, 2, 3, 4, 5, 6, 7],
                     "Inconsistency Values(IV)": [0, 1, 2, 3, 4, 5, 6, 7], "% of IV (IV / n)": [0, 1, 2, 3, 4, 5, 6, 7]}
    expected_values = {"pclass": [1, 2, 3], "survived": [0, 1],
                       "sex": ['male', 'female'], "age": ['int'], "sibsp": ['float'],
                       "parch": ['int'], "fare": ['float'], "embarked": ['C', 'Q', 'S']}
    skip_feature_check = ["parch", "fare", "sibsp", "age"]
    index = 0
    inconsistence_features = {}
    missing_value_features = {}
    for feature in csv_df.columns:
        if feature.lower() == 'id':
            continue
        else:
            # add name of feature to Features column
            summary_table['Features'][index] = feature
            if feature.lower() not in skip_feature_check:
                # get inconsistence boolean series
                inconsistence_boolean = get_inconsistence_value_for_feature(csv_df[feature], expected_values[feature])
                # add number of inconsitence and  rate
                summary_table["Inconsistency Values(IV)"][index], summary_table["% of IV (IV / n)"][index] = \
                    get_bool_rate(inconsistence_boolean)
            else:
                summary_table["Inconsistency Values(IV)"][index] = 0
                summary_table["% of IV (IV / n)"][index] = 0
            if summary_table["% of IV (IV / n)"][index] != 0:
                inconsistence_features[feature] = inconsistence_boolean
            # get missing values boolean series
            missing_boolean = get_missing_values_for_feature(csv_df[feature])
            # add number of missing values and rate
            summary_table["Missing Values(MV)"][index], summary_table["% of MV (MV / n)"][index] = \
                get_bool_rate(missing_boolean)
            if summary_table["% of MV (MV / n)"][index] != 0:
                missing_value_features[feature] = missing_boolean
            index += 1  # increase index by 1
    return pd.DataFrame(summary_table), inconsistence_features, missing_value_features


def display_summary_table(summary_df):
    """
    Print Summary Table
    :param summary_df:
    :return:
    """
    print('**************************************Summary Table *****************************************************')
    print(summary_df)
    print(100 * '*')


def display_missing_values(csv_df, missing_value_df):
    """
    print missing values records
    :param csv_df:
    :param missing_value_df:
    :return:
    """
    for feature in missing_value_df.keys():
        print("**************************  Missing values for feature %s *******************************************"
              % feature)
        print(csv_df[missing_value_df[feature]])
        print(100 * '*')


def display_inconsistence_values(csv_df, inconsistence_df):
    """
    Print inconsistence values records
    :param csv_df:
    :param inconsistence_df:
    :return:
    """
    for feature in inconsistence_df.keys():
        print("************************ Inconsistence values for feature %s *****************************************"
              % feature)
        print(csv_df[inconsistence_df[feature]])
        print(100 * '*')


def replace_missing_values(csv_df):
    """
    update the dataframe with a mean or mode value base on data type(
    :param csv_df:
    :return:
    """
    nominal_ordinal = ['pclass', 'survived', 'sex', 'embarked']
    csv_df_copied = csv_df.copy(deep=True)
    for feature in csv_df_copied.columns:
        if feature not in nominal_ordinal:
            mean = round(csv_df_copied[feature].mean(), 1)
            csv_df_copied[feature] = csv_df_copied[feature].fillna(mean)
        else:
            mode = csv_df_copied[feature].mode()[0]
            csv_df_copied[feature] = csv_df_copied[feature].fillna(mode)
    return csv_df_copied


def fix_inconsistence_values(csv_df):
    """
    Replace inconsistence values and update dataframe
    :param feature: csv_df
    :return: csv_df_copied
    """
    csv_df_copied = csv_df.copy(deep=True)
    csv_df_copied['sex'] = csv_df_copied['sex'].replace({'Male': 'male', 'Female': 'female'})
    csv_df_copied['embarked'] = csv_df_copied['embarked'].replace({'Queenstown': 'Q'})
    return csv_df_copied


def get_clean_data(csv_df):
    """
    Update missing and inconsistence values for dataframe
    :param csv_df:
    :return:
    """
    updated_df = replace_missing_values(csv_df)
    cleaned_df = fix_inconsistence_values(updated_df)
    return cleaned_df


def main():
    """
    Main execution
    :return:
    """
    csv_data = get_csv_data('titanic_traning.csv')  # get training data to df
    summary_df, inconsistence_df, missing_value_df = generate_summary_for_features(csv_data)
    set_pandas_display_options()  # set pandas default settings for print
    display_summary_table(summary_df)
    display_inconsistence_values(csv_data, inconsistence_df)
    display_missing_values(csv_data, missing_value_df)
    cleaned_df = get_clean_data(csv_data)
    write_csv_data(cleaned_df, 'cleaned_data.csv')


if __name__ == '__main__':
    main()