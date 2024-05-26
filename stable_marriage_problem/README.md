# Stable Marriage Problem

## Description
This project implements the Gale-Shapley algorithm to solve the stable marriage problem. The algorithm is used to find a stable match between two groups (men and women) based on their preferences.

## Functionality
- **Generation of preferences:** Preferences can be entered manually or randomly generated.
- **Execution of the Gale-Shapley algorithm:** The algorithm finds a stable match based on provided by preferences.
- **Exporting results:** The matches found can be exported to an excel file for analysis and a txt file for reuse via code.

## Requirements
- Python 3.6 or higher (not specified)
- Python libraries: `pandas`, `random`, `copy`

## Usage
1. Download the main.py and stable_marriage.py files to the same folder.
2. Run main.py
3. If the code has formed stable couples, it will return the following message: "The couples are stable, great job :) you can check the output, if you want." You will find an excel file and a txt file for checking.
4. If the code returns the following message, please contact me: "The couples are not stable :( check the output." -- because there is a bug :)

## Steps of of the Gale-Shapley algorithm
1. Save every man's first preference.
2. If a woman is single with only one preference, she is associated with the man. If a woman had multiple preferences, she associates with the man highest in the woman's preferences among the men who proposed.
3. In the men's preference list, women who have paired with or been rejected by them are eliminated.
4. The first two steps are repeated only for single men. The first preferences of the men who remained single are recorded, considering the previously eliminated preferences.
5. The steps are repeated for each single man, until they are all paired.

N.B. Women can fall into one of four categories: single women with only one preference, women already with a partner with only one preference, single women with multiple preferences, women with one partner and multiple preferences.
