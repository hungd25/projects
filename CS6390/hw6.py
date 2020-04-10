"""


"""

import pandas as pd


def get_excel_data(excel_file):
    """
    Read in excel file with pandas and return one dataframe or a dict of dataframes based on
    the number of sheets found.
    :param excel_file: Full path of excel file
    :return:
    """
    excel_workbook = pd.ExcelFile(excel_file)
    sheet_names = excel_workbook.sheet_names
    if len(sheet_names) > 1:
        workbook_dfs = {}
        for sheet in sheet_names:
            sheet_df = excel_workbook.parse(sheet_name=sheet)  # read sheet by name
            sheet_df.fillna(method='ffill', inplace=True)  # replace nan value with last valid observation forward
            workbook_dfs[sheet] = sheet_df  # add sheet df to dict
            print('%s loaded' % sheet)
        return sheet_names, workbook_dfs  # return a dict of sheets dfs
    else:  # no sheet's name
        df = excel_workbook.parse(sheet_names[0])  # read workbook
        df.fillna(method='ffill', inplace=True)  # replace nan value with last valid observation forward
        print('%s loaded' % excel_file)
        return df  # return workbook


def get_feature_survival_classifier(feature_survived):
    """
    One R feature survival classifier.
    1. Get unique values from feature
    2. Loop through through unique values and get survival count
    3. Update and return a dict of predicted feature survival
    0 = Not survived, 1 = survived
    :param feature_survived: Two columns of feature and survived
    :return: predict_feature_survival
    """
    unique_values = feature_survived.iloc[:, 0].unique()  # get the unique values from column
    first_col_name = feature_survived.columns[0]  # get the first column's name
    predict_feature_survival = {}  # empty dict
    for value in unique_values:
        value_survived = feature_survived[feature_survived[first_col_name] == value]  # get all the survived for value
        survival_count = value_survived.groupby('survived').size()  # get all a list of size for survived for values
        if survival_count.size == 2:
            if survival_count[0] > survival_count[1]:
                # if not survived(0) is greater than survived(1), value = index[0]
                predict_feature_survival[value] = int(survival_count.index[0])
            else:
                predict_feature_survival[value] = int(survival_count.index[1])  # else value = index[1]
        else:
            predict_feature_survival[value] = int(survival_count.index[0])
    print('Survived classifier for %s' % predict_feature_survival)
    return predict_feature_survival  # return a dict of survived classifier for each value


def get_feature_survived_for_training(features, training_data):
    """
    1.Get the feature column and the survived column from training dataframe.
    2.Call OneR function to get survived classifier for each feature.
    3.Return a dictionary of feature dataframes
    :param features: A list of the columns for training
    :param training_data: the data frame for the training data
    :return:
    """
    training_features_survived = {}  # empty dict
    for feature in features:
        feature_survived = training_data[[feature, 'survived']]  # extract only feature and survived column
        print("Getting survived classifier for %s" % feature)
        training_features_survived[feature] = get_feature_survival_classifier(feature_survived)  # get survived value
    return training_features_survived  # return dict of survived classifier for all features


def predict_survival_for_feature(test_feature, feature_survived, prediction_dataframe):
    """
        For each row in feature dataframe predict survived classifier(0,1) based on predicted training data.
    :param test_feature: The feature survived dataframe from test data
    :param feature_survived: The feature survived dataframe from training data
    :param prediction_dataframe:  The prediction dataframe to store the survived classifier
    :return:
    """
    prediction_copy = prediction_dataframe.copy(deep=True)
    for index in test_feature.index:
        value = test_feature.loc[index]  # get the value for each row
        prediction_copy.loc[index, 'Prediction'] = feature_survived[value]  # insert (0 or 1) into survived column
    return prediction_copy  # return updated test_feature with survived df


def get_feature_survived_for_test(training_features_survived, test_data_frames, prediction_dataframes):
    """
        Get survived classifier for each feature with test data
    :param training_features_survived: training data(feature and survived columns)
    :param test_data_frames:  test data frames
    :param prediction_dataframes: prediction dataframes
    :return:
    """
    test_features_predicted_survived = {}  # empty dict
    for sheet_name in prediction_dataframes:
        feature = sheet_name.replace('_Based_Prediction', '').lower()
        if feature == 'prediction_success_rate':  # skip the prediciton df
            continue
        print("Predicting survived for feature %s" % feature)
        prediction_df = prediction_dataframes[sheet_name]
        test_predicted = predict_survival_for_feature(test_data_frames[feature],
                                                      training_features_survived[feature],
                                                      prediction_df)  # get survival
        test_features_predicted_survived[sheet_name] = test_predicted  # add predicted df to dict
    return test_features_predicted_survived  # return predicted df dict


def get_predicted_success_rate(prediction_sheet_names, results_df, success_rate_df):
    """
        Success rate is the total number of correct predictions divide by the total instances
    :param prediction_sheet_names: a list of sheet names from prediction excel file
    :param results_df:  A dict of results dataframes for all the predicted features
    :param success_rate_df:  The dataframe from the success rate sheet
    :return:
    """
    success_rate_copied = success_rate_df.copy()  # copied the success rate dataframe
    index = 0
    for sheet_name in prediction_sheet_names:
        if sheet_name.lower() == 'prediction_success_rate':  # skip the prediciton df
            continue
        prediction_compared =\
            results_df[sheet_name]['Prediction'] == results_df[sheet_name]['Ground truth']  # Compare survived values
        true_count = prediction_compared[prediction_compared].eq(True).size  # get count of True
        success_rate = (true_count / results_df[sheet_name]['Prediction'].size) * 100  # divide true count by total
        success_rate_copied.loc[index, 'Success Rate '] = "{0:.2f}%".format(success_rate)
        index += 1
    results_df['Prediction_Success_Rate'] = success_rate_copied
    return results_df


def write_results_to_excel(excel_writer, sheet_names, dataframes_list, save=False):
    """
    Write pd dataframes to workbook, each dataframe is a sheet.
    :param excel_writer: the Excel writer object
    :param sheet_names: list of the sheet names
    :param dataframes_list: list of dataframes to write to sheet
    :param save: Save the workbook or not
    :return:
    """
    for sheet_name in sheet_names:
        print("Writing data frame to sheet %s" % sheet_name)
        dataframes_list[sheet_name].to_excel(excel_writer, sheet_name=sheet_name, index=False)  # write data frame sheet
    if save:
        excel_writer.save()  # save worksheet
        excel_writer.close()  # close workbook


def main():
    excel_writer = pd.ExcelWriter('titanic_test_predictions.xlsx', engine='xlsxwriter')  # create an instance of writer
    training_data = get_excel_data('titanic_traning.xlsx')  # get training data to df
    testing_data = get_excel_data('titanic_test.xlsx')  # get testing data to df
    prediction_sheet_names, prediction_dfs = get_excel_data('titanic_test_predictions.xlsx')  # get prediction data df
    predict_features = ['gender','pclass', 'sibsp', 'parch', 'embarked']  # list of features to predict
    training_features_survived = get_feature_survived_for_training(predict_features, training_data)  # feature survived
    results_df = get_feature_survived_for_test(training_features_survived,
                                               testing_data, prediction_dfs)  # get predictions for features
    success_rate_df = prediction_dfs['Prediction_Success_Rate']
    success_rate_results = get_predicted_success_rate(prediction_sheet_names,
                                                      results_df, success_rate_df)  # get prediction rates
    write_results_to_excel(excel_writer, prediction_sheet_names,
                           success_rate_results, save=True)  # write results to prediction workbook
    print('Completed! Please check titanic_test_prediciton.xlsx for results.')


if __name__ == '__main__':
    main()
