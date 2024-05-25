"""
Author: Giuseppe Verardi

Creation date: 2024-05-20

Description: This file contains the auxiliary functions necessary for
             implementation of the Gale-Shapley algorithm.
"""

import random
import pandas as pd

def ask_names_and_preferences(names_m, names_f):
    """
    Asks names and preferences for men or women or generates random choices.
    It uses global variables.

    Args:
        names_m: variable containing male names.
        names_f: variable containing female names.

    Returns:
        Male names, female names and list of names for preferences.
    """
    #  dict to record preferences
    preferences_m = {}
    preferences_f = {}

    # variable to make a choice
    choice = input("Do you want to manually enter names or generate them randomly? (m/r): ").lower()

    # enter the values ​​manually
    if choice == 'm':
        try:
            # list for names
            male_names = []
            female_names = []

            # variable to record number of couples
            num_names = int(input("Enter the number of couples to create (greater than zero): "))

            # error handling
            if num_names > 0:
                # enter names manually
                for i in range(num_names):
                    name = input(f"Enter the male name {i+1}: ")
                    male_names.append(name)
                for i in range(num_names):
                    name = input(f"Enter the female name {i+1}: ")
                    female_names.append(name)
                # enter preferences manually
                for name in male_names:
                    preferences_m[name] = []
                    print(f"Enter {name}'s preferences:")
                    for i in range(len(female_names)):
                        preference = input(f"Preference {i + 1}: ")
                        preferences_m[name].append(preference)
                for name in female_names:
                    preferences_f[name] = []
                    print(f"Enter {name}'s preferences:")
                    for i in range(len(male_names)):
                        preference = input(f"Preference {i + 1}: ")
                        preferences_f[name].append(preference)
                # returns names and preferences
                return male_names, female_names, preferences_m, preferences_f
            # error handling
            else:
                print("I told you greater than zero!")
                return ask_names_and_preferences(names_m, names_f)
        # error handling
        except Exception:
            print("Invalid choice, try again.")
            return ask_names_and_preferences(names_m, names_f)

    # enter the values automatically
    elif choice == 'r':
        try:
            # variable to record number of couples
            num_names = int(input("Enter the number of names to generate randomly (range 1-20): "))

            # error handling
            if num_names > 0:
                # enter names automatically
                male_names = random.sample(names_m, k=num_names)
                female_names = random.sample(names_f, k=num_names)
                # enter preferences automatically
                for name in male_names:
                    preferences_m[name] = random.sample(female_names, k=len(female_names))
                for name in female_names:
                    preferences_f[name] = random.sample(male_names, k=len(male_names))
                # returns names and preferences
                return male_names, female_names, preferences_m, preferences_f
            # error handling
            else:
                print("I told you range 1-20!")
                return ask_names_and_preferences(names_m, names_f)
        # error handling
        except Exception:
            print("Invalid choice, try again.")
            return ask_names_and_preferences(names_m, names_f)
    # error handling
    else:
        print("Invalid choice, try again.")
        return ask_names_and_preferences(names_m, names_f)
    
def gale_shapley(men_preferences, women_preferences, matching):
    """
    Uses the Gale-Shapley algorithm.

    Args:
        men_preferences: list of men's preferences.
        women_preferences: list of women's preferences.
        matching: empty list of couples.

    Returns:
        Nothing.
        Manipulates the list containing the couples.
    """
    # let's create lists of men and women
    all_men = [man for man in men_preferences.keys()]
    all_women = [woman for woman in women_preferences.keys()]

    # we initialize the variable
    n = len(all_men)

    # run the algorithm as long as there are single men
    while n != 0:

        # let's create two lists to record men and women paired
        paired_men = [man for man, woman in matching]
        paired_women = [woman for man, woman in matching]

        # list of single men and women
        single_men = [single_man for single_man in all_men if single_man not in paired_men]
        single_women = [single_woman for single_woman in all_women if single_woman not in paired_women]

        # dict to record every man's first preference
        top_pref = {}
        # scroll through each man and record his first preference
        for man, preferences in men_preferences.items():
            if man in single_men:
                top_pref[man] = preferences[0]

        # dict with every woman as key and men as values to record proposals
        proposals_for_women = {}
        # we register suitors for each woman
        for man, woman in top_pref.items():
            if woman in proposals_for_women:
                proposals_for_women[woman].append(man)
            else:
                proposals_for_women[woman] = [man]

        # we filter the women who have received one proposal
        women_one_proposal = [woman for woman, man in proposals_for_women.items() if len(man) == 1]

        # create couples for women with one proposal
        for woman in women_one_proposal:
            # check if the woman is single
            if woman in single_women:
                # create the couple between the man who made the proposal and the woman who received only one proposal
                matching.append((proposals_for_women[woman][0], woman))
                # let's remove the woman from the man's preferences
                men_preferences[proposals_for_women[woman][0]].remove(woman)

            else:
                # let's find the suitor and index who made these proposals
                suitor = proposals_for_women[woman][0]
                suitor_index = women_preferences[woman].index(suitor)

                # let's find actual partner of woman and index
                partner = [m for m, w in matching if woman == w][0]
                partner_index = women_preferences[woman].index(partner)

                # we define the woman's preference based on the index
                if suitor_index < partner_index:
                    # remove old couple
                    matching.remove((partner, woman))
                    # record new partner
                    partner = suitor
                    # we add the couple to the list
                    matching.append((partner, woman))
                    # the man was chosen, we remove the woman from his preferences
                    men_preferences[partner].remove(woman)

                else:
                    # the man was rejected, we remove the woman from his preferences
                    men_preferences[suitor].remove(woman)

        # we filter the women who have received more proposals
        women_with_multiple_proposals = [(woman, len(man)) for woman, man in proposals_for_women.items() if len(man) > 1]

        # sort the list in descending order of len(men)
        women_with_multiple_proposals_sorted = sorted(women_with_multiple_proposals, key=lambda x: x[1], reverse=True)

        # we take every woman with more than one preference without len(men)
        women_with_multiple_proposals = [woman for woman, len in women_with_multiple_proposals_sorted]

        # iterate through every woman with multiple proposals
        for woman in women_with_multiple_proposals:
            # let's find the men who made these proposals
            suitors = proposals_for_women[woman]

            # check if the woman is single
            if woman in single_women:
                # we define a max index corresponding to the last man chosen
                last_max_index = len(women_preferences[woman]) - 1

                # we iterate over all the suitors
                for suitor in suitors:
                    # let's take the suitor index
                    suitor_index = women_preferences[woman].index(suitor)
                    # we have at least two suitors, so the condition will be true at least once
                    if suitor_index < last_max_index:
                        # the suitor is the new partner
                        new_partner = suitor
                        # update index of last man
                        last_max_index = suitor_index
                        # the man was chosen, we remove the woman from his preferences
                        men_preferences[new_partner].remove(woman)
                    else:
                        # the suitor was rejected, we remove the woman from his preferences
                        men_preferences[suitor].remove(woman)

                # we add the new couple to the list
                matching.append((new_partner, woman))

            else:
                # let's find actual partner of woman and index
                partner = [m for m, w in matching if woman == w][0]
                partner_index = women_preferences[woman].index(partner)

                # we iterate over all the suitors
                for suitor in suitors:
                    # let's take the suitor index
                    suitor_index = women_preferences[woman].index(suitor)
                    # we have at least two suitors, so the condition will be true at least once
                    if suitor_index < partner_index:
                        # remove old couple
                        matching.remove((partner, woman))
                        # the suitor is the new partner
                        partner = suitor
                        # update index of partner
                        partner_index = suitor_index
                        # we add the new couple to the list
                        matching.append((partner, woman))
                        # the man was chosen, we remove the woman from his preferences
                        men_preferences[partner].remove(woman)
                    else:
                        # the suitor was rejected, we remove the woman from his preferences
                        men_preferences[suitor].remove(woman)

        # update number of single men
        n = len(single_men)

def stability_test(men_preferences, women_preferences, matching):
    """
    Carries out a test of the stability of the couples.

    Args:
        men_preferences: list of men's preferences.
        women_preferences: list of women's preferences.
        matching: list of couples formed.

    Returns:
        A boolean variable that is true if the couples are stable, false otherwise.
    """
    # get values of each matching
    for man, woman in matching:
        pref_woman = women_preferences[woman]
        partner_index = pref_woman.index(man)
    
        # we see all the men that the woman prefers over the current one
        for new_man in pref_woman[:partner_index]:
            # let's take the woman's index in new_man's preferences
            woman_new_man_index = men_preferences[new_man].index(woman)
            # let's take the index of the new_man's current partner
            couple_selected = list(filter(lambda couples: couples[0] == new_man, matching))
            partner_new_man_index = men_preferences[new_man].index(couple_selected[0][1])
            # let's compare the two indices
            if woman_new_man_index < partner_new_man_index:
                return False
    
    return True

def generate_excel(pref_men, pref_women, matching):
    """
    Create an excel file with the output needed for the analyses.

    Args:
        pref_men: list of men's preferences.
        pref_women: list of women's preferences.
        matching: list of couples formed.

    Returns:
        Nothing.
    """
    # convert dictionaries to pandas DataFrame
    df_men = pd.DataFrame.from_dict(pref_men, orient='index')
    df_women = pd.DataFrame.from_dict(pref_women, orient='index')

    # transpose the DataFrames to have the men's and women's names as columns
    df_men = df_men.transpose()
    df_women = df_women.transpose()

    # create DataFrame for men and women list
    df_list_men = pd.DataFrame(list(pref_men.keys()), columns=['Men'])
    df_list_women = pd.DataFrame(list(pref_women.keys()), columns=['Women'])

    # concatenate the two DataFrames
    df_list = pd.concat([df_list_men, df_list_women], axis=1)

    # extract the two columns from the list of pairs
    men = [coppia[0] for coppia in matching]
    women = [coppia[1] for coppia in matching]

    # create DataFrame with couples
    df = pd.DataFrame({'Men': men, 'Women': women})

    # save the DataFrames in two Excel sheets
    with pd.ExcelWriter('output.xlsx') as writer:
        df_list.to_excel(writer, sheet_name='list men and women', index=False)
        df_men.to_excel(writer, sheet_name='preferences men')
        df_women.to_excel(writer, sheet_name='preferences women')
        df.to_excel(writer, sheet_name='couples', index=False)

def write_txt(var, file):
    """
    Create a txt file with the output needed for the analyses.

    Args:
        var: list of variables.
        file: file's name.

    Returns:
        Nothing.
    """
    with open(file, 'w') as file:
        file.write(str(var) + '\n')
