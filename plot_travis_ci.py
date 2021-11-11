import matplotlib.pyplot as plt
import numpy as np
import csv

language_dict = {'Total': [0, 0, 0]}

with open('gh-active-projects-legacy-o.csv') as csv_file:
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
language_list.sort(key=lambda e: sum(e[1]))

sorted_language = np.array(language_list, dtype=object)
x = sorted_language[:, 0]
y = np.array([k for k in sorted_language[:, 1]])
no_travis = y[:, 0]
lte_travis = y[:, 1] + no_travis
gt_travis = y[:, 2] + lte_travis
print(sorted_language)

plt.barh(x, no_travis, label='Does Not Use Travis', color='tomato')
plt.barh(x, lte_travis, left=no_travis, label='Uses Travis (<= 50 builds)', color='seagreen')
plt.barh(x, gt_travis, left=lte_travis, label='Uses Travis (> 50 builds)', color='lightskyblue')

plt.ylabel('Main Repository Language')
plt.xlabel('#Projects')
plt.title('TRAVIS CI adoption per language')
plt.legend()
# plt.show()
plt.savefig('travis_ci.png')