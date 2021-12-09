import matplotlib.pyplot as plt
import numpy as np
import csv

language_dict = {'Total': [0, 0, 0]}
selected_languages = ['Total', 'Java', 'Python', 'Ruby']

filename = 'repos_2021_500_out.csv'
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        language = row[2]
        builds = int(row[4])
        if language not in language_dict:
            language_dict[language] = [0, 0, 0]

        if builds < 0:
            language_dict[language][0] += 1
            language_dict['Total'][0] += 1
        elif builds <= 50:
            language_dict[language][1] += 1
            language_dict['Total'][1] += 1
        else:
            language_dict[language][2] += 1
            language_dict['Total'][2] += 1


language_list = list(language_dict.items())
# language_list = list(filter(lambda item: item[0] != '\\N', language_list))
language_list = list(filter(lambda item: item[0] in selected_languages, language_list))
language_list.sort(key=lambda e: sum(e[1]))
# language_list = language_list[-6:]

sorted_language = np.array(language_list, dtype=object)
x = sorted_language[:, 0]
y = np.array([k for k in sorted_language[:, 1]])
no_travis = y[:, 0]
lte_travis = y[:, 1]
gt_travis = y[:, 2]

plt.barh(x, no_travis, label='Does Not Use Travis', color='tomato')
plt.barh(x, lte_travis, left=no_travis, label='Uses Travis (<= 50 builds)', color='seagreen')
plt.barh(x, gt_travis, left=lte_travis + no_travis, label='Uses Travis (> 50 builds)', color='lightskyblue')

plt.ylabel('Main Repository Language')
plt.xlabel('#Projects')
plt.title('TRAVIS CI adoption per language')
plt.legend()
plt.savefig('travis_ci_' + filename.split('.')[0] + '.png')
