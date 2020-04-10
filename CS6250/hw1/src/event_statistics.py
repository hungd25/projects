import time
import pandas as pd
import numpy as np

# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT


def read_csv(filepath):
    """
    TODO : This function needs to be completed.
    Read the events.csv and mortality_events.csv files. 
    Variables returned from this function are passed as input to the metric functions.
    """
    events = pd.read_csv(filepath + "events.csv")
    mortality = pd.read_csv(filepath + "mortality_events.csv")

    return events, mortality


def event_count_metrics(events, mortality):
    """
    TODO : Implement this function to return the event count metrics.
    Event count is defined as the number of events recorded for a given patient.
    """
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

    # get count/num of unique dead and alive events
    dead_patients = dead_events.groupby("patient_id")["patient_id"].transform("count")
    dead_events_total = dead_events["event_id"].count()
    dead_events_patient_count = dead_events["patient_id"].nunique()
    alive_patients = alive_events.groupby("patient_id")["patient_id"].transform("count")
    alive_events_total = alive_events["event_id"].count()
    alive_events_patient_count = alive_events["patient_id"].nunique()

    # dead and alive event stats
    avg_dead_event_count = dead_events_total / dead_events_patient_count
    max_dead_event_count = dead_patients.max()
    min_dead_event_count = dead_patients.min()
    avg_alive_event_count = alive_events_total / alive_events_patient_count
    max_alive_event_count = alive_patients.max()
    min_alive_event_count = alive_patients.min()

    return (
        min_dead_event_count,
        max_dead_event_count,
        avg_dead_event_count,
        min_alive_event_count,
        max_alive_event_count,
        avg_alive_event_count,
    )


def encounter_count_metrics(events, mortality):
    """
    TODO : Implement this function to return the encounter count metrics.
    Encounter count is defined as the count of unique dates on which a given patient visited the ICU. 
    """
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

    alive_events = alive_events.drop(
        ["deceased", "event_id", "event_description", "value", "time_of_death"], axis=1
    )
    alive_events = alive_events.drop_duplicates()
    dead_events = dead_events.drop(
        ["deceased", "event_id", "event_description", "value", "time_of_death"], axis=1
    )
    dead_events = dead_events.drop_duplicates()

    # get count and num of unique dead and alive encounter
    dead_timestamp_total = dead_events["timestamp"].count()
    dead_patientid_count = dead_events["patient_id"].nunique()
    dead_patients = dead_events.groupby("patient_id")["patient_id"].transform("count")
    alive_timestamp_total = alive_events["timestamp"].count()
    alive_patientid_count = alive_events["patient_id"].nunique()
    alive_patients = alive_events.groupby("patient_id")["patient_id"].transform("count")

    # dead and alive encounter stats
    avg_dead_encounter_count = dead_timestamp_total / dead_patientid_count
    max_dead_encounter_count = dead_patients.max()
    min_dead_encounter_count = dead_patients.min()
    avg_alive_encounter_count = alive_timestamp_total / alive_patientid_count
    max_alive_encounter_count = alive_patients.max()
    min_alive_encounter_count = alive_patients.min()

    return (
        min_dead_encounter_count,
        max_dead_encounter_count,
        avg_dead_encounter_count,
        min_alive_encounter_count,
        max_alive_encounter_count,
        avg_alive_encounter_count,
    )


def record_length_metrics(events, mortality):
    """
    TODO: Implement this function to return the record length metrics.
    Record length is the duration between the first event and the last event for a given patient. 
    """
    events_copied = events.copy(deep=True)
    events_copied["timestamp"] = pd.to_datetime(
        events_copied["timestamp"]
    )  # convert to datetime object
    max_min_events = (
        events_copied[["patient_id", "timestamp"]].groupby("patient_id").agg([max, min])
    )
    events_days = (
        max_min_events["timestamp"]["max"] - max_min_events["timestamp"]["min"]
    )

    # convert dead and alive to days
    dead_events = events_days[mortality["patient_id"]].dt.days
    alive_events = events_days.drop(mortality["patient_id"]).dt.days

    # dead and alive duration stats
    avg_dead_rec_len = dead_events.mean()
    max_dead_rec_len = dead_events.max()
    min_dead_rec_len = dead_events.min()
    avg_alive_rec_len = alive_events.mean()
    max_alive_rec_len = alive_events.max()
    min_alive_rec_len = alive_events.min()

    return (
        min_dead_rec_len,
        max_dead_rec_len,
        avg_dead_rec_len,
        min_alive_rec_len,
        max_alive_rec_len,
        avg_alive_rec_len,
    )


def main():
    """
    DO NOT MODIFY THIS FUNCTION.
    """
    # You may change the following path variable in coding but switch it back when submission.
    train_path = "../data/train/"

    # DO NOT CHANGE ANYTHING BELOW THIS ----------------------------
    events, mortality = read_csv(train_path)

    # Compute the event count metrics
    start_time = time.time()
    event_count = event_count_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute event count metrics: " + str(end_time - start_time) + "s"))
    print(event_count)

    # Compute the encounter count metrics
    start_time = time.time()
    encounter_count = encounter_count_metrics(events, mortality)
    end_time = time.time()
    print(
        ("Time to compute encounter count metrics: " + str(end_time - start_time) + "s")
    )
    print(encounter_count)

    # Compute record length metrics
    start_time = time.time()
    record_length = record_length_metrics(events, mortality)
    end_time = time.time()
    print(
        ("Time to compute record length metrics: " + str(end_time - start_time) + "s")
    )
    print(record_length)


if __name__ == "__main__":
    main()
