# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # particpants = input("How many particpants?")
    particpants = 41
    # tasks = input ("How many tasks?")
    tasks = 7
    # concept = input("How many concepts?")
    concepts = 2
    headers = ["Response ID", "Task ID", "Concept ID", "Goals", "Tracking", "Reinforcement", "Selfefficay", "Social",
               "Provider", "Parts Worth", "Selected", "Standard Deviation", "Confidence Interval Range 1",
               "Confidence Interval Range 2"]
    headersNone = ["Response ID", "Task ID", "Concept ID", "Goals", "Tracking", "Reinforcement", "Selfefficay", "Social",
               "Provider", "None", "Parts Worth", "Selected", "Standard Deviation", "Confidence Interval Range 1",
               "Confidence Interval Range 2"]
    df = pandas.read_csv("export_23.05.csv", sep=";", names=headers, skiprows=[0])
    none = pandas.DataFrame(columns=headersNone)
    respondent = "none"
    counter = 1
    for index, row in df.iterrows():
        if index % (tasks*2) == 0:
            print(row._set_value("None", 0))
            #print (row)
            none = none.append(row)


    none.to_csv("test.csv")
#



    #print(df.head)


