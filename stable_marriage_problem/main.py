"""
Author: Giuseppe Verardi

Creation date: 2024-05-20

Description: This file contains the implementation of the Gale-Shapley algorithm.
             The functions necessary are in stable_marriage file.
"""

# import libraries
import copy
from stable_marriage import ask_names_and_preferences, gale_shapley, stability_test, generate_excel, write_txt

### GLOBAL VARIABLE ###

# list of twenty male names
men_list = [
    "Alberto", "Alessandro", "Angelo", "Bartolomeo", "Davide", "Fabio", "Federico", "Gaetano", "Giovanni", "Giuseppe",
     "Luca", "Lucio", "Marco", "Matteo",  "Michele", "Paolo", "Roberto", "Salvatore", "Simone", "Stefano"
]

# list of twenty female names
women_list = [
    "Alessia", "Annalisa", "Carlotta", "Chiara", "Cristina", "Elena", "Federica", "Giulia", "Ida", "Ilaria",
    "Lucia", "Marianna", "Marina", "Martina", "Paola", "Rosa", "Sara", "Silvia", "Vanessa", "Viola"
]

# list to fill
couples = []

# let's create the necessary input variables
male_names, female_names, pref_men, pref_women = ask_names_and_preferences(men_list, women_list)

# let's create a copy of the preferences to test if the output is stable
pref_men_test = copy.deepcopy(pref_men)
pref_women_test = copy.deepcopy(pref_women)

# we run the Gale-Shapley algorithm
gale_shapley(pref_men, pref_women, couples)

# create variable for txt file
parameters = "Male names: " + str(male_names) + '\n\n' +\
"Female names: "+ str(female_names) + '\n\n' +\
"Male preferences: " + str(pref_men_test) + '\n\n' +\
"Female preferences: " + str(pref_women_test) + '\n\n' +\
"Couples formed: " + str(couples)

# let's do a test
bool = stability_test(pref_men_test, pref_women_test, couples)
if bool:
    print("The couples are stable, great job :) you can check the output, if you want.")
    generate_excel(pref_men_test, pref_women_test, couples)
    write_txt(parameters, 'output.txt')
else:
    print("The couples are not stable :( check the output.")
    generate_excel(pref_men_test, pref_women_test, couples)
    write_txt(parameters, 'output.txt')
