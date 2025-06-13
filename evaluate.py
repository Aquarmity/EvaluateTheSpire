import json
from glob import glob
import matplotlib.pyplot as plt
import time

CHARACTERS = ['IRONCLAD', 'THE_SILENT', 'DEFECT', 'WATCHER']
ROOM_TYPE_KEY = {'M': 'Monster', '?': '?', '$': 'Shop', 'T': 'Treasure', 'R': 'Rest', 'E': 'Elite', 'BOSS': 'Boss'}

killers = {}
act_1_boss_wins = {'Hexaghost': 0, 'Slime Boss': 0, 'The Guardian': 0}
act_2_boss_wins = {'Automaton': 0, 'Champ': 0, 'Collector': 0}
act_3_boss_wins = {'Awakened One': 0, 'Donu and Deca': 0, 'Time Eater': 0}
act_4_boss_wins = {'The Heart': 0}
rooms_encountered = {'M': 0, '?': 0, '$': 0, 'T': 0, 'R': 0, 'E': 0, 'BOSS': 0}

run_count = 0
floor_deaths = [0] * 57
act_3_win_time = 0
act_3_wins = 0
run_time = 0

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
        if floor_reached == 56:
            act_4_boss_wins['The Heart'] += 1

        for room in rooms_encountered:
            rooms_encountered[room] += data['path_taken'].count(room)
        run_count += 1

        floor_deaths[data['floor_reached']] += 1
        run_time += data['playtime']
        if floor_reached > 50:
            act_3_win_time += data['playtime']
            act_3_wins += 1

        file.close()

killers_sorted = {k: v for k, v in sorted(killers.items(), key=lambda item: item[1], reverse=True)}
print('Deaths per Enemy:')
for k in killers_sorted:
    print(k + ': ', killers_sorted[k])

def print_boss_success_rate(act):
    for boss in act:
        if boss in killers:
            success_rate = f"{(act[boss]/(act[boss] + killers[boss])) * 100:.2f}"
            print(boss + ': ', act[boss], '/', (act[boss] + killers[boss]), '=', success_rate + '%')

print('\nBoss Success Rates:')
print_boss_success_rate(act_1_boss_wins)
print_boss_success_rate(act_2_boss_wins)
print_boss_success_rate(act_3_boss_wins)
print_boss_success_rate(act_4_boss_wins)

print('\nAverage Run:')

total_rooms = 0
for room in rooms_encountered:
    total_rooms += rooms_encountered[room]
    print(ROOM_TYPE_KEY[room] + ': ', round(rooms_encountered[room] / run_count, 2))
print('Average Run Length:', round(total_rooms / run_count, 2))

survivors = [run_count]
for deaths in floor_deaths:
    survivors.append(survivors[-1] - deaths)
survivors.pop()

print('\nAverage Run Time:', time.strftime('%H:%M:%S', time.gmtime(run_time / run_count)))
print('Average Act 3 Win Time:', time.strftime('%H:%M:%S', time.gmtime(act_3_win_time / act_3_wins)))
      
plt.figure(figsize=(12, 6))
plt.subplot(121)
plt.plot(range(57), survivors)
plt.xlim([0, 56])
plt.ylim([0, max(survivors) * 1.05])
plt.xlabel('Floor')
plt.ylabel('Surviving Runs')
plt.title('Run Survivorship')
plt.grid(True)
plt.subplot(122)
plt.bar(range(57), floor_deaths, width=1.0)
plt.xlim([0, 56])
plt.ylim([0, max(floor_deaths) * 1.05])
plt.xlabel('Floor')
plt.ylabel('# Runs')
plt.title('Run Lengths')
plt.show()