"""


"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def set_pandas_display_options() -> None:
    display = pd.options.display

    display.max_columns = 1000
    display.max_rows = 1000
    display.max_colwidth = 199
    display.width = None


def get_excel_data(excel_file):
    """
    Read in excel file with pandas and return one dataframe or a dict of dataframes based on
    the number of sheets found.
    :param excel_file: Full path of excel file
    :return:
    """
    excel_workbook = pd.ExcelFile(excel_file)
    sheet_names = excel_workbook.sheet_names
    df = excel_workbook.parse(sheet_names[0])  # read workbook
    print('%s loaded' % excel_file)
    return df  # return workbook


def replace_missing_values(ecoli_df):
    """
    update the dataframe with a mean value
    :param ecoli_df:
    :return:
    """
    ecoli_df_copied = ecoli_df.copy(deep=True)
    for feature in ecoli_df_copied.columns:
        mean = round(ecoli_df_copied[feature].mean(), 2)  # fill in na with mean
        ecoli_df_copied[feature] = ecoli_df_copied[feature].fillna(mean)  # update series with new values
    return ecoli_df_copied


def drop_unused_columns(df):
    """
    Drop the all the unused columns
    :param df:
    :return:
    """
    df_copied = df.copy(deep=True)
    dropped_columns_df = df_copied.drop(columns=["Sample ID", "Station ID","Date Collected", "Water Temp",
                                                 "Flow Stream",	"Transparency", "E.coli Holding Time",
                                                 "Days Since Precipitation","Water Depth",	"Water Flow",
                                                 "Wind Intensity", "Present Weather", "Water Surface",
                                                 "Water Color",	"Water Odor", "Tide", "Primary Contact",
                                                 "Evidence of Recreation","Sample Depth",
                                                 "Field Temp", "Flow Severity"])
    return dropped_columns_df


def reindex_data_by_date(ecoli_df):
    """
    Use the Date Collected as the df index
    :param ecoli_df:
    :return:
    """
    ecoli_df_copied = ecoli_df.copy(deep=True)
    ecoli_df_copied['Date Collected'] = pd.to_datetime(ecoli_df_copied['Date Collected'])  # convert datetime object
    ecoli_df_copied.index = ecoli_df_copied['Date Collected']  # replace index with datetime object
    return ecoli_df_copied


def clean_data(ecoli_df):
    """
    1. reindex the df with date collected
    2. drop any unused columns
    3. replace missing values with feature's mean
    :param ecoli_df:
    :return:
    """
    date_index_df = reindex_data_by_date(ecoli_df)
    updated_columns_df = drop_unused_columns(date_index_df)
    cleaned_df = replace_missing_values(updated_columns_df)
    return cleaned_df


def plot_ecoli_avg(ecoli_df, date_type):
    """
    Plot the ecoli average by year or month
    :param ecoli_df:
    :param date_type: Y or M
    :return:
    """
    # Set up the matplotlib figure
    f = plt.figure()
    avg_by_date = ecoli_df.resample(date_type).mean()  # average for Y or M calculations
    if date_type == 'Y':
        avg_by_date.index = avg_by_date.index.year  # change index to Year only
        avg_by_date.index.name = 'Year' # change index name to Year
    else:
        avg_by_date.index = avg_by_date.index.strftime('%b')  # change to abbreviated month format
        avg_by_date.index.name = 'Month'  # change index name to month
        avg_by_date = avg_by_date.groupby('Month').sum()  # sum up all the months
    # Plot the average base on date type(Y or M)
    sns.barplot(x=avg_by_date.index, y='E.coli', data=avg_by_date)
    plt.show()


def get_ecoli_correlation(ecoli_df):
    """
    Get the Ecoli correlation with the chemicals by pearson method
    :param ecoli_df:
    :return:
    """
    ecoli_df_copied = ecoli_df.copy(deep=True)
    ecoli_corr = ecoli_df_copied.corr(method='pearson')  # Correlation calculations
    return ecoli_corr


def plot_ecoli_correlation(ecoli_corr, cleaned_ecoli_df):
    """
    Plot the Ecoli Correlation
    :param ecoli_corr:
    :param cleaned_ecoli_df:
    :return:
    """
    sns.set(style="white")

    # Generate a mask for the upper triangle
    mask = np.zeros_like(ecoli_corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(ecoli_corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.show()


def display_ecoli_correlation(ecoli_corr):
    """
    Print the correlation summary
    :param ecoli_corr:
    :return:
    """
    print("------------------------------------Ecoli Correalation-----------------------------------------------------")
    print(ecoli_corr)


def main():
    """
    Main entry for script
    :return:
    """
    set_pandas_display_options()  # set pandas default settings for print
    ecoli_df = get_excel_data("Ecoli Data.xlsx")  # get the ecoli data
    cleaned_ecoli_df = clean_data(ecoli_df)  # clean the ecoli data
    plot_ecoli_avg(cleaned_ecoli_df, "Y")  # plot the ecloi average by Year
    plot_ecoli_avg(cleaned_ecoli_df, "M")  # plot the ecoli avergage by Month
    ecoli_corr = get_ecoli_correlation(cleaned_ecoli_df)  # get the ecoli and chemical correlations
    display_ecoli_correlation(ecoli_corr)  # print the correlation
    plot_ecoli_correlation(ecoli_corr, cleaned_ecoli_df)  # plot the correlations


if __name__ == '__main__':
    main()  # call main function
