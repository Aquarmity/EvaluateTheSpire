import json
from glob import glob

CHARACTERS = ['IRONCLAD', 'THE_SILENT', 'DEFECT', 'WATCHER']

killers = {}
act_1_boss_wins = {'Hexaghost': 0, 'Slime Boss': 0, 'The Guardian': 0}
act_2_boss_wins = {'Automaton': 0, 'Champ': 0, 'Collector': 0}
act_3_boss_wins = {'Awakened One': 0, 'Donu and Deca': 0, 'Time Eater': 0}

for char in CHARACTERS:
    for fname in glob('runs/' + char + '/*.run'):
        file = open(fname, 'r')
        data = json.load(file)

        if 'killed_by' in data:
            if data['killed_by'] not in killers:
                killers[data['killed_by']] = 1
            else:
                killers[data['killed_by']] += 1

        floor_reached = data['floor_reached']
        for enemy in data['damage_taken']:
            if enemy['floor'] == 16 and floor_reached > 16:
                act_1_boss_wins[enemy['enemies']] += 1
            if enemy['floor'] == 33 and floor_reached > 33:
                act_2_boss_wins[enemy['enemies']] += 1
            if enemy['floor'] == 50 and floor_reached > 50:
                act_3_boss_wins[enemy['enemies']] += 1
        file.close()

killers_sorted = {k: v for k, v in sorted(killers.items(), key=lambda item: item[1], reverse=True)}
print("Deaths per Enemy:")
for k in killers_sorted:
    print(k + ': ', killers_sorted[k])

def print_boss_success_rate(act):
    for boss in act:
        if boss in killers:
            success_rate = f"{(act[boss]/(act[boss] + killers[boss])) * 100:.2f}"
            print(boss + ': ', act[boss], '/', (act[boss] + killers[boss]), '=', success_rate + '%')

print('\nSuccess Rates:')
print_boss_success_rate(act_1_boss_wins)
print_boss_success_rate(act_2_boss_wins)
print_boss_success_rate(act_3_boss_wins)
