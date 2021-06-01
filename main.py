# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np


def check_holdouts(respo, holdout_full):
    is_valid = []
    for respondent in respo:
        profile_respondent = holdout_full.loc[
            (holdout_full["Response ID"] == respondent) & (holdout_full["Selected"] == 1)]
        size = len(profile_respondent)
        if size == 1:
            if (profile_respondent.iloc[0]["Concept ID"] == 3) or (profile_respondent.iloc[0]["Concept ID"]) == 4:
                is_valid.append(respondent)
        else:
            # One none option
            if size == 2:
                if (profile_respondent.iloc[0]["Concept ID"] + 4) == profile_respondent.iloc[1]["Concept ID"]:
                    is_valid.append(respondent)
            else:
                # No None option
                if (profile_respondent.iloc[0]["Concept ID"] + 4) == profile_respondent.iloc[2]["Concept ID"]:
                    is_valid.append(respondent)
    return is_valid


def to_long_format(wide, r_id):
    rows_list = []
    for i in range(0, len(wide.index)):
        # second rows are the interesting ones, if more concepts are displayed to the user 2 has to be updated
        # ['Response ID' 'Task ID' 'Concept ID' 'Ziele' 'Tracking' 'Unter-st�tzung'
        #  'Selbst-wahr-nehmung' 'Soziales' 'Anbieter' 'None' 'Selected', Time]

        # Creating a List of Rows -> transforming from attributes to levels + adding none option
        # is a repsonded im interes in ?
        if wide.iloc[i]["Response ID"] in r_id:
            # is it the second concept? if true get row 1 and row 2 , row 3 is none option
            if (i-1) % 2 == 0:
                row1 = wide.iloc[i - 1]
                row2 = wide.iloc[i]
                row1_long = []
                row2_long = []
                row3_long = []
                # creating 3 rows for the long dataset and adding those to the rows_list
                choices = {1: [1, 0, 0, 0], 2: [0, 1, 0, 0], 3: [0, 0, 1, 0], 4: [0, 0, 0, 1]} # hashmap-> wide->long
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
                        row1_long = np.concatenate((row1_long, choices.get(row1[j])), axis=None).tolist()
                        row2_long = np.concatenate((row2_long, choices.get(row2[j])), axis=None).tolist()
                        row3_long = np.concatenate((row3_long, [0, 0, 0, 0]), axis=None).tolist()
                    # none option
                    elif j == 9:
                        row1_long.append(0)
                        row2_long.append(0)
                        row3_long.append(1)
                    # selected
                    elif j == 10:
                        if row1[j] == 0 & row2[j] == 0:
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
                #print(str(wide.iloc[i]["Response ID"]) + " index: " + str(i))
    return rows_list


if __name__ == '__main__':
    # reading Data
    full_profile = pd.read_csv("Full_profiles.CSV", delimiter=";")
    # holdouts displayed to user
    holdouts = pd.read_csv("holdouts.CSV", delimiter=";")
    # reading respondents which iam interested in (coming from spss)
    conditionCSV = "only_female.csv"
    interested_respondents = pd.read_csv(conditionCSV)
    # addtional Information for CBCA
    tasks = 7
    concepts = 2
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

    #Renaming Data to English (questionPro export is german(default language)) "Ziele" -> "goals"
    renamed_columns = ['Response ID', 'Task ID', 'Concept ID', 'goals', 'tracking', 'reinforcement',
                       'self-efficay', 'social support', 'provider', 'Parts Worth', 'selected',
                       'Standard Deviation', 'Confidence Interval Range 1', 'Confidence Interval Range 2']
    full_profile.columns = renamed_columns

    # adding a new level "none" to the dataset
    full_profile["none"] = -1
    columns = list(full_profile.columns)
    full_profile = full_profile[columns[:9] + [columns[-1]] + [columns[10]]]

    # adding "time" to the dataset with dummy variables
    full_profile["time"] = -1

    all_respondents = pd.unique(full_profile["Response ID"])
    holdout_respondents = pd.unique(holdouts["Response ID"])

    # symmetric difference for respondents which selected 3 times the none option (These are valid respondents)
    always_none_respondents = list(set(all_respondents) - set(holdout_respondents))

    # Summary
    respondents_full = len(all_respondents)
    respondents_holdouts = len(holdout_respondents)

    # getting valid respondents (checking holdouts)
    valid_respondents = check_holdouts(holdout_respondents, holdouts)

    # Adding User who picked 3 times none in the holdouts
    for resp in always_none_respondents:
        valid_respondents.append(resp)

    final_arr = np.concatenate((['Response ID', 'Task ID', 'Concept ID'], goals_level, tracking_level,
                                reinforcement_level, selfefficay_level, socialsupport_level,
                                provider_level, ['none', 'selected']), axis=None).tolist()
    # np.intersect1d(valid_respondents, interested_respondents) -> only valid && interested respondents
    long_format = (to_long_format(full_profile, (np.intersect1d(valid_respondents, interested_respondents))))
    df_final = pd.DataFrame(long_format, columns=final_arr)
    df_final["time"] = (-(df_final["selected"]-2))
    print(df_final)
    df_final.to_csv(conditionCSV[:-4] + "_long_clean.csv", sep=";", index=False)


    print("All respondents: " + str(respondents_full))
    print("Holdout respondents: " + str(len(valid_respondents)))
    print("ValidationRate = " + str(round(((len(valid_respondents) / respondents_full) * 100), 2))
          + "% of all respondents are succesfull in the holdout validation")