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


if __name__ == '__main__':
    # all displayed profiles for every respondents
    full_profile = pd.read_csv("Full_profiles.CSV", delimiter=";")
    # only holdouts displayed to user
    holdouts = pd.read_csv("holdouts.CSV", delimiter=";")

    all_respondents = pd.unique(full_profile["Response ID"])
    holdout_respondents = pd.unique(holdouts["Response ID"])

    # symmetric difference for respondents which selected 3 times the none option
    always_none_respondents = list(set(all_respondents) - set(holdout_respondents))

    # Summary
    tasks = 7
    concepts = 2
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




    headers = ["Response ID", "Task ID", "Concept ID", "Goals", "Tracking", "Reinforcement", "Selfefficay", "Social",
               "Provider", "Parts Worth", "Selected", "Standard Deviation", "Confidence Interval Range 1",
               "Confidence Interval Range 2"]
    headersNone = ["Response ID", "Task ID", "Concept ID", "Goals", "Tracking", "Reinforcement", "Selfefficay",
                   "Social",
                   "Provider", "None", "Parts Worth", "Selected", "Standard Deviation", "Confidence Interval Range 1",
                   "Confidence Interval Range 2"]
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
