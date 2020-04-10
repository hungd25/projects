import utils
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta

# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT


def read_csv(filepath):

    """
    TODO: This function needs to be completed.
    Read the events.csv, mortality_events.csv and event_feature_map.csv files into events, mortality and feature_map.
    
    Return events, mortality and feature_map
    """

    # Columns in events.csv - patient_id,event_id,event_description,timestamp,value
    events = pd.read_csv(filepath + "events.csv")

    # Columns in mortality_event.csv - patient_id,timestamp,label
    mortality = pd.read_csv(filepath + "mortality_events.csv")

    # Columns in event_feature_map.csv - idx,event_id
    feature_map = pd.read_csv(filepath + "event_feature_map.csv")

    return events, mortality, feature_map


def calculate_index_date(events, mortality, deliverables_path):

    """
    TODO: This function needs to be completed.

    Refer to instructions in Q3 a

    Suggested steps:
    1. Create list of patients alive ( mortality_events.csv only contains information about patients deceased)
    2. Split events into two groups based on whether the patient is alive or deceased
    3. Calculate index date for each patient
    
    IMPORTANT:
    Save indx_date to a csv file in the deliverables folder named as etl_index_dates.csv. 
    Use the global variable deliverables_path while specifying the filepath. 
    Each row is of the form patient_id, indx_date.
    The csv file should have a header 
    For example if you are using Pandas, you could write: 
        indx_date.to_csv(deliverables_path + 'etl_index_dates.csv', columns=['patient_id', 'indx_date'], index=False)

    Return indx_date
    """
    mortality_copied = mortality.copy(deep=True)
    dead_date_indx = mortality_copied[['patient_id', 'timestamp']]
    mortality_copied.rename(
        columns={"timestamp": "time_of_death", "label": "deceased"}, inplace=True
    )
    mortality_events = pd.merge(
        events, mortality_copied, on=["patient_id"], how="outer"
    )
    mortality_events.fillna({"deceased": 0}, inplace=True)
    alive_patients = mortality_events[mortality_events["deceased"] == 0]



    alive_patients.drop(["deceased", "event_id", "event_description", "value", "time_of_death"], inplace=True, axis=1)
    alive_patients.drop_duplicates(inplace=True)
    alive_patients['timestamp'] = pd.to_datetime(alive_patients['timestamp'])
    alive_indx_date = alive_patients.loc[alive_patients.groupby("patient_id").timestamp.idxmax()]


    dead_date_indx["timestamp"] = pd.to_datetime(dead_date_indx["timestamp"])
    dead_date_indx["timestamp"] = dead_date_indx["timestamp"] - timedelta(days=30)

    indx_date = pd.concat([alive_indx_date, dead_date_indx]).reset_index(drop=True)
    indx_date = indx_date.rename(columns={"timestamp": "indx_date"})
    indx_date.to_csv(
        deliverables_path + "etl_index_dates.csv",
        columns=["patient_id", "indx_date"],
        index=False,
    )
    return indx_date


def filter_events(events, indx_date, deliverables_path):

    """
    TODO: This function needs to be completed.

    Refer to instructions in Q3 b

    Suggested steps:
    1. Join indx_date with events on patient_id
    2. Filter events occuring in the observation window(IndexDate-2000 to IndexDate)
    
    
    IMPORTANT:
    Save filtered_events to a csv file in the deliverables folder named as etl_filtered_events.csv. 
    Use the global variable deliverables_path while specifying the filepath. 
    Each row is of the form patient_id, event_id, value.
    The csv file should have a header 
    For example if you are using Pandas, you could write: 
        filtered_events.to_csv(deliverables_path + 'etl_filtered_events.csv', columns=['patient_id', 'event_id', 'value'], index=False)

    Return filtered_events
    """

    events_indx_date = pd.merge(events, indx_date, on=["patient_id"])

    events_indx_date["indx_date"] = pd.to_datetime(events_indx_date["indx_date"])
    events_indx_date["timestamp"] = pd.to_datetime(events_indx_date["timestamp"])

    filtered_events = events_indx_date[
        (events_indx_date.timestamp <= events_indx_date.indx_date)
        & (
            events_indx_date.timestamp
            >= events_indx_date.indx_date - timedelta(days=2000)
        )
    ]

    filtered_events.to_csv(
        deliverables_path + "etl_filtered_events.csv",
        columns=["patient_id", "event_id", "value"],
        index=False,
    )
    return filtered_events


def aggregate_events(
    filtered_events_df, mortality_df, feature_map_df, deliverables_path
):
    """
    TODO: This function needs to be completed.

    Refer to instructions in Q3 c

    Suggested steps:
    1. Replace event_id's with index available in event_feature_map.csv
    2. Remove events with n/a values
    3. Aggregate events using sum and count to calculate feature value
    4. Normalize the values obtained above using min-max normalization(the min value will be 0 in all scenarios)


    IMPORTANT:
    Save aggregated_events to a csv file in the deliverables folder named as etl_aggregated_events.csv.
    Use the global variable deliverables_path while specifying the filepath.
    Each row is of the form patient_id, event_id, value.
    The csv file should have a header .
    For example if you are using Pandas, you could write:
        aggregated_events.to_csv(deliverables_path + 'etl_aggregated_events.csv', columns=['patient_id', 'feature_id', 'feature_value'], index=False)

    Return filtered_events
    """
    # Replace event_id's with index available in event_feature_map.csv

    filtered_events_map = pd.merge(filtered_events_df, feature_map_df, on="event_id")
    filtered_events_map = filtered_events_map[["patient_id", "idx", "value"]]
    # Remove events with n/a values
    filtered_events_map = filtered_events_map[pd.notnull(filtered_events_map["value"])]

    # get all of the diagnostic and drug event by index id less than 2680
    diags_drugs_events = filtered_events_map[filtered_events_map["idx"] < 2680]

    # get all of the lab event by index id greater than 2680
    lab_events = filtered_events_map[filtered_events_map["idx"] >= 2680]

    # Max and Sum of all diagnostics and drug events
    diag_drug_events_sum = diags_drugs_events.groupby(["patient_id", "idx"]).agg("sum").reset_index()
    diag_drug_events_max = diag_drug_events_sum.groupby(["idx"]).agg("max").reset_index()

    diag_drug_events_max.rename(columns={"value": "max"}, inplace=True)
    diag_drug_events_max.drop(["patient_id"], axis=1, inplace=True)

    # merge max events with sum events
    sum_max_diag_drug = pd.merge(diag_drug_events_sum, diag_drug_events_max, on="idx")
    sum_max_diag_drug["feature_value"] = sum_max_diag_drug["value"] / sum_max_diag_drug["max"]
    # drop un-needed features
    sum_max_diag_drug = sum_max_diag_drug.drop(["value", "max"], axis=1)
    sum_max_diag_drug = sum_max_diag_drug.rename(
        columns={"idx": "feature_id"}
    )


    # count all lab events
    lab_event_count = lab_events.groupby(["patient_id", "idx"]).agg("count").reset_index()

    # get lab events max
    lab_event_max = lab_event_count.groupby(["idx"]).agg("max").reset_index()


    lab_event_max.rename(columns={"value": "max"}, inplace=True)
    lab_event_max.drop(["patient_id"], axis=1, inplace=True)

    # merge lab events max with count
    lab_event_count_max = pd.merge(lab_event_count, lab_event_max, on="idx")
    lab_event_count_max["feature_value"] = lab_event_count_max["value"] / lab_event_count_max["max"]
    # drop un-needed features
    lab_event_count_max.drop(["value", "max"], axis=1, inplace=True)
    lab_event_count_max = lab_event_count_max.rename(columns={"idx": "feature_id"})

    # merge the diags, drugs and lab events back
    aggregated_events = pd.concat([sum_max_diag_drug, lab_event_count_max]).reset_index(drop=True)
    aggregated_events.to_csv(
        deliverables_path + "etl_aggregated_events.csv",
        columns=["patient_id", "feature_id", "feature_value"],
        index=False,
    )

    return aggregated_events


def create_features(events, mortality, feature_map):
    deliverables_path = "../deliverables/"

    # Calculate index date
    indx_date = calculate_index_date(events, mortality, deliverables_path)

    # Filter events in the observation window
    filtered_events = filter_events(events, indx_date, deliverables_path)

    # Aggregate the event values for each patient
    aggregated_events = aggregate_events(
        filtered_events, mortality, feature_map, deliverables_path
    )

    """
    TODO: Complete the code below by creating two dictionaries - 
    1. patient_features :  Key - patient_id and value is array of tuples(feature_id, feature_value)
    2. mortality : Key - patient_id and value is mortality label
    """
    # patient_features :  Key - patient_id and value is array of tuples(feature_id, feature_value) to dictionary
    patient_features = (
        aggregated_events.groupby("patient_id")[["feature_id", "feature_value"]]
        .apply(lambda x: [tuple(x) for x in x.values])
        .to_dict()
    )


    mortality_copied = mortality.copy(deep=True)
    mortality_copied.rename(
        columns={"timestamp": "time_of_death", "label": "deceased"}, inplace=True
    )
    mortality_events = pd.merge(
        events, mortality_copied, on=["patient_id"], how="outer"
    )
    mortality_events.fillna({"deceased": 0}, inplace=True)
    alive_events = mortality_events[mortality_events["deceased"] == 0]
    dead_events = mortality_events[mortality_events["deceased"] == 1]

    # merge deceased and alive events
    alive_deceased_events = pd.concat([alive_events, dead_events]).reset_index(drop=True)
    alive_deceased_events.drop(
        ["event_id", "event_description", "timestamp", "value"], axis=1, inplace=True
    )

    # convert mortality Series to Dict
    mortality = pd.Series(alive_deceased_events.deceased.values, index=alive_deceased_events.patient_id).to_dict()

    return patient_features, mortality


def save_svmlight(patient_features, mortality, op_file, op_deliverable):
    """
    TODO: This function needs to be completed

    Refer to instructions in Q3 d

    Create two files:
    1. op_file - which saves the features in svmlight format. (See instructions in Q3d for detailed explanation)
    2. op_deliverable - which saves the features in following format:
       patient_id1 label feature_id:feature_value feature_id:feature_value feature_id:feature_value ...
       patient_id2 label feature_id:feature_value feature_id:feature_value feature_id:feature_value ...

    Note: Please make sure the features are ordered in ascending order, and patients are stored in ascending order as well.
    """
    deliverable1 = open(op_file, "wb")
    deliverable2 = open(op_deliverable, "wb")
    for patient_id in sorted(patient_features):
        feature_values = ""
        for item in sorted(patient_features[patient_id]):
            feature_values += (
                " " + str(int(item[0])) + ":" + format(item[1], ".6f")
            )
        svmlight_format = str(mortality[patient_id]) + feature_values + " \n"
        # write to op file
        deliverable1.write(bytes((svmlight_format), "UTF-8"))
        # write to op deliverable file
        deliverable2.write(bytes((str(int(patient_id)) + " " + svmlight_format), "UTF-8"))


def main():
    train_path = "../data/train/"
    events, mortality, feature_map = read_csv(train_path)
    patient_features, mortality = create_features(events, mortality, feature_map)
    save_svmlight(
        patient_features,
        mortality,
        "../deliverables/features_svmlight.train",
        "../deliverables/features.train",
    )


if __name__ == "__main__":
    main()
