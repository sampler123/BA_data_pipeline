# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd


def check_holdouts(respo, holdout_full):
    is_valid = []
    for respondent in respo:
        profile_respondent = holdout_full.loc[(holdout_full["Response ID"] == respondent) & (holdout_full["Selected"] == 1)]
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
    for index in range(1, len(wide.index)):
        # second rows are the interesting ones, if more concepts are displayed to the user 2 has to be updated
        # ['Response ID' 'Task ID' 'Concept ID' 'Ziele' 'Tracking' 'Unter-st�tzung'
        #  'Selbst-wahr-nehmung' 'Soziales' 'Anbieter' 'None' 'Selected']
        if index % 2 == 0:
            row1 = wide.iloc[index-1]
            row2 = wide.iloc[index]
            row3 = []
            # iterating through the single rows to create the None option Row
            #for j in len(row2):


       # dict1 = {}
        # get input row in dictionary format
        # key = col_name
        #dict1.update(blah..)

        #rows_list.append(dict1)

if __name__ == '__main__':
    # reading Data
    full_profile = pd.read_csv("Full_profiles.CSV", delimiter=";")
    # holdouts displayed to user
    holdouts = pd.read_csv("holdouts.CSV", delimiter=";")

    # addtional Information for CBCA
    tasks = 7
    concepts = 2
    #level of attributrs
    goals_level = ["weekly goals", "Menu planning exercise", "Set amount of calorie intake",
                   "daily habit challenge per week"]
    tracking_level = ["tracking via food-database", "tracking via recipes", "Import recipes from websites",
                      "track via photo"]
    reinforcement_level = ["life-score", "surprise challenges", "tracking reminder", "food displayed in color"]
    selfefficay_level = ["food diary", "progress graph of intake", "confidence scale", "feedback on goal progress"]
    socialsupport_level = ["interaction with Family Friends Peers", "invite person to track users food",
                           "role models performing target behavior", "Sharing achievements"]
    provider_level = ["non profit organization", "well known company", "start-up", "insurance company"]

    # Renaming Data to English (questionPro export is german(default language)) "Ziele" -> "goals"
    renamed_columns = ['Response ID', 'Task ID', 'Concept ID', 'goals', 'tracking', 'reinforcement',
                       'self-efficay', 'social support', 'provider', 'Parts Worth', 'selected',
                       'Standard Deviation', 'Confidence Interval Range 1', 'Confidence Interval Range 2']
    full_profile.columns = renamed_columns

    #adding a new level "none" to the dataset
    full_profile["None"] = 0
    columns = list(full_profile.columns)
    full_profile = full_profile[columns[:9] + [columns[-1]] + [columns[10]]]

    # adding "Time" to the dataset #calculated with Formula Backhaus
    full_profile["time"] = -(full_profile["selected"]-2)

    all_respondents = pd.unique(full_profile["Response ID"])
    holdout_respondents = pd.unique(holdouts["Response ID"])

    # symmetric difference for respondents which selected 3 times the none option
    always_none_respondents = list(set(all_respondents) - set(holdout_respondents))

    # Summary

    respondents_full = len(all_respondents)
    respondents_holdouts = len(holdout_respondents)


    # getting valid respondents (checking holdouts)
    valid_respondents = check_holdouts(holdout_respondents, holdouts)

    # Adding User who picked 3 times none in the holdouts
    for resp in always_none_respondents:
        valid_respondents.append(resp)
    print("All respondents: " + str(respondents_full))
    print("Holdout respondents: " + str(len(valid_respondents)))
    print("ValidationRate = " + str(round(((len(valid_respondents) / respondents_full) * 100), 2))
          + "% of all respondents are succesfull in the holdout validation")

    to_long_format(full_profile, valid_respondents)


    # df = pandas.read_csv("export_23.05.csv", sep=";", names=headers, skiprows=[0])
    # none = pandas.DataFrame(columns=headersNone)
    # respondent = "none"
    # counter = 1
    # for index, row in df.iterrows():
    #  if index % (tasks*2) == 0:
    #   print(row._set_value("None", 0))
    #    #print (row)
    #   none = none.append(row)

    # none.to_csv("test.csv")
#
