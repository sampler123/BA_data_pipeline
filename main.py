#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Nicolas Götzfried"
"""
Data processing script for Choice-Based Conjoint Analysis conducted via QuestionPro.
The script validate respondents based on three holdouts. Holdout choice set 1 and 3 have to be identical.
The script transforms the QuestionPro wide format into long format. It changes the following:
1. Mapping attributes to levels with dummy variables
2. Adding a none option for every conjoint tasks
3. calculating a time variable, which is necessary for Cox regression
4. enables a priori segmentation via "respondent list"
"""

import pandas as pd  # third-party library
import numpy as np  # third-party library #  not necessary


def validate_holdouts():
    is_valid = []  # return list of valid respondents # use set
    for respondent in holdout_respondents:
        # Iterating through respondentsIDs
        # The dataset size various from 0 to 3, depending on how many times a respondent selected 'none'
        # QuestionPro doesnt export the row, if 'none is selected'

        # dataframe containing selected holdout profiles
        selected_profiles = holdouts.loc[
            (holdouts["Response ID"] == respondent) & (holdouts["Selected"] == 1)]

        size = len(selected_profiles)  # size indicates how many times 'none option' was selected

        if size == 1:  # size 1 => respondent selected 2 times 'none'
            if (selected_profiles.iloc[0]["Concept ID"] == 3) or (selected_profiles.iloc[0]["Concept ID"]) == 4:
                is_valid.append(respondent)
        else:
            if size == 2:  # size 2 => respondent selected 1 time 'none': e.g. concept 1  == concept 5
                if (selected_profiles.iloc[0]["Concept ID"] + 4) == selected_profiles.iloc[1]["Concept ID"]:
                    is_valid.append(respondent)
            else:  # size 3 => no none option: same as size 2
                if (selected_profiles.iloc[0]["Concept ID"] + 4) == selected_profiles.iloc[2]["Concept ID"]:
                    is_valid.append(respondent)
    return is_valid  # list of valid respondent ids


def to_long_format(wide, r_id):
    rows_list = []
    for i in range(0, len(wide.index)):
        # QuestionPro does not export a third row for concept 3 none
        # second rows are the interesting ones, if more concepts are displayed
        # to the user "(i-1) % 2 == 0" has to be updated
        # Creating a List of Rows -> transforming from attributes to levels + adding none option
        # checking if respondent belongs to the filtered respondent list (which im interested in)
        if wide.iloc[i]["Response ID"] in r_id:
            # is it the second concept? if true get row 1 and row 2 , row 3 is none option
            if (i - 1) % 2 == 0:
                row1 = wide.iloc[i - 1]
                row2 = wide.iloc[i]
                # creating 3 rows for the long dataset and adding those to the rows_list
                row1_long = []
                row2_long = []
                row3_long = []
                # adding the mapping from wide format (1-4) to binary long format (0,1)
                choices = {1: [1, 0, 0, 0], 2: [0, 1, 0, 0], 3: [0, 0, 1, 0], 4: [0, 0, 0, 1]}  # hashmap-> wide->long
                for j in range(len(row2)):
                    # Respondent, Task ID
                    if j == 0 or j == 1:
                        row1_long.append(row1[j])
                        row2_long.append(row2[j])
                        row3_long.append(row2[j])
                    # Concept ID
                    elif j == 2:
                        row1_long.append(row1[j])
                        row2_long.append(row2[j])
                        row3_long.append(3)
                    # goals 3, tracking 4, reinforcement 5, self-efficay 6, social support 7, provider 8
                    elif 3 <= j <= 8:
                        # to list() is mandatory, because append works only for lists not numpy arrays
                        row1_long = np.concatenate((row1_long, choices.get(row1[j])), axis=None).tolist() #use list.extend() or just ADD THEM.
                        row2_long = np.concatenate((row2_long, choices.get(row2[j])), axis=None).tolist()
                        row3_long = np.concatenate((row3_long, [0, 0, 0, 0]), axis=None).tolist()
                    # none option level
                    elif j == 9:
                        row1_long.append(0)
                        row2_long.append(0)
                        row3_long.append(1)
                    # selected, if case ow1[j] == 0 & row2[j] == 0: none option is selected
                    elif j == 10:
                        # If concept 1 and concept 2 is not selected, concept 3 'none' is selected
                        if row1[j] == 0 and row2[j] == 0:
                            row1_long.append(0)
                            row2_long.append(0)
                            row3_long.append(1)
                        else:
                            row1_long.append(row1[j])
                            row2_long.append(row2[j])
                            row3_long.append(0)
                rows_list.append(row1_long)
                rows_list.append(row2_long)
                rows_list.append(row3_long)
    return rows_list


if __name__ == '__main__':
    # reading "Full Profile" for all Respondents, 7 conjoint tasks each respondent
    full_profile = pd.read_csv("Full_profiles.CSV", delimiter=";")
    # reading holdouts, 3 holdout tasks each respondent
    holdouts = pd.read_csv("holdouts.CSV", delimiter=";")
    # reading a list of respondents im interested in (filtering done by spss)
    conditionCSV = "onlyOne.csv"
    interested_respondents = pd.read_csv(conditionCSV) # Welche Spalte sind die repsondents?
    # addtional Information for CBCA
    # tasks = 7
    # concepts = 2

    # level of attributrs
    goals_level = ["weekly goals", "menu planning exercise", "set amount of calorie intake",
                   "daily habit challenge per week"]
    tracking_level = ["tracking via food-database", "tracking via recipes", "Import recipes from websites",
                      "track via photo"]
    reinforcement_level = ["life-score", "surprise challenges", "tracking reminder", "food displayed in color"]
    selfefficay_level = ["food diary", "progress graph of intake", "confidence scale", "feedback on goal progress"]
    socialsupport_level = ["interaction with Family Friends Peers", "invite person to track users food",
                           "role models performing target behavior", "Sharing achievements"]
    provider_level = ["non profit organization", "well known company", "start-up", "insurance company"]

    # attributes in English (questionPro export is german(default language)) "Ziele" -> "goals"
    renamed_columns = ['Response ID', 'Task ID', 'Concept ID', 'goals', 'tracking', 'reinforcement',
                       'self-efficay', 'social support', 'provider', 'Parts Worth', 'selected',
                       'Standard Deviation', 'Confidence Interval Range 1', 'Confidence Interval Range 2']

    # renaming attributes from German to English
    full_profile.columns = renamed_columns

    # adding a new level "none" at index 10 to the dataset (filled with dummy value -1)
    full_profile["none"] = -1
    columns = list(full_profile.columns)
    full_profile = full_profile[columns[:9] + [columns[-1]] + [columns[10]]]

    # adding "time" to the end of the dataset with dummy values -1
    full_profile["time"] = -1

    all_respondents = pd.unique(full_profile["Response ID"])
    holdout_respondents = pd.unique(holdouts["Response ID"])

    # symmetric difference for respondents which selected 3 times the none option (These are valid respondents)
    always_none_respondents = list(set(all_respondents) - set(holdout_respondents)) # why list conversion?

    # getting valid respondents (checking holdouts) (list of valid respondents)
    valid_respondents = validate_holdouts()

    # Adding User who picked 3 times none in the holdouts, they are not part of the holdouts
    # dataset, because QuestionPro does not export the none option rows
    for resp in always_none_respondents:
        valid_respondents.append(resp)

    # final dataset header in long format (including levels not attributes)
    final_arr = np.concatenate((['Response ID', 'Task ID', 'Concept ID'], goals_level, tracking_level,
                                reinforcement_level, selfefficay_level, socialsupport_level,
                                provider_level, ['none', 'selected']), axis=None).tolist() # use list.extend or itertools.chain or just ADD THEM.
    # getting Data into long format, adding None options
    long_format = (to_long_format(full_profile, (np.intersect1d(valid_respondents, interested_respondents)))) # use set.intersection()
    df_final = pd.DataFrame(long_format, columns=final_arr)

    # adding time variable for Cox Regression (Backhaus et.al) (-(selected-2))
    df_final["time"] = (-(df_final["selected"] - 2))

    # saving Data
    df_final.to_csv(conditionCSV[:-4] + "_long_clean.csv", sep=";", index=False)

    # Summary for complete Dataset not on filtered one
    print("All respondents: " + str(len(all_respondents)))
    print("Holdout positive respondents: " + str(len(holdout_respondents)))
    print("cleaned respondents: " + str(len(valid_respondents)))
    print("ValidationRate = " + str(round(((len(valid_respondents) / len(all_respondents)) * 100), 2))
          + "% of all respondents are succesfull in the holdout validation")
