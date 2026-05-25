import json

data = [
    (1, 21, 17, '31:13.288', 27, '1:48.888'),
    (2, 5, 17, '+10.955', 18, '1:48.801'),
    (3, 4, 17, '+12.912', 15, '1:49.196'),
    (4, 9, 17, '+13.215', 12, '1:49.188'),
    (5, 8, 17, '+13.752', 10, '1:49.358'),
    (6, 12, 17, '+14.148', 9, '1:48.724'),
    (7, 3, 17, '+17.940', 6, '1:49.392'),
    (8, 19, 17, '+18.752', 4, '1:49.235'),
    (9, 20, 17, '+18.877', 2, '1:48.906'),
    (10, 18, 17, '+22.662', 1, '1:49.069'),
    (11, 28, 17, '+31.262', 0, '1:49.690'),
    (12, 32, 17, '+32.182', 0, '1:49.074'),
    (13, 95, 17, '+36.238', 0, '1:50.023'),
    (14, 56, 17, '+37.089', 0, '1:50.533'),
    (15, 14, 17, '+38.637', 0, '1:49.102'),
    (16, 91, 17, '+41.516', 0, '1:50.418'),
    (17, 55, 17, '+64.931', 0, '1:52.114'),
    (18, 77, 17, '+73.670', 0, '1:52.021')
]

def parse_time(t_str):
    if ':' in t_str:
        m, s = t_str.split(':')
        return float(m) * 60 + float(s)
    elif t_str.startswith('+'):
        return float(t_str[1:])
    return 0

base_time = parse_time(data[0][3])

fls = [(i, parse_time(x[5])) for i, x in enumerate(data)]
fls.sort(key=lambda x: x[1])
ranks = {idx: rank + 1 for rank, (idx, _) in enumerate(fls)}

res = []
for i, row in enumerate(data):
    pos, num, laps, t_gap, pts, fl_str = row
    
    if i == 0:
        t_tot = base_time
    else:
        t_tot = base_time + parse_time(t_gap)
        
    m = int(t_tot // 60)
    s = t_tot % 60
    t_tot_str = f"{m}:{s:06.3f}"
    
    # We leave grid as 0 if unknown, but for pole sitter Alisha Palmowski (No. 21) it's 1.
    # Let's just set it to 0 for everyone to follow "simpler way" unless we know it.
    grid = '1' if num == 21 else '0'
    
    # Check if there is a 2nd place grid we know from the results (we only know pole was Palmowski).
    res.append({
        'number': str(num),
        'position': str(pos),
        'grid': grid,
        'laps': str(laps),
        'status': 'Finished',
        'points': str(pts),
        'Time': {'time': t_tot_str},
        'FastestLap': {'rank': str(ranks[i]), 'lap': '0', 'Time': {'time': fl_str}}
    })

# Now format this into the results.json format
output = {
    "season": "2026",
    "round": "2",
    "raceName": "Canadian Grand Prix",
    "Circuit": {
        "circuitId": "montreal",
        "circuitName": "Circuit Gilles-Villeneuve"
    },
    "Results": {
        "race1": [],
        "race2": res
    }
}

# The results.json is a list of these objects.
with open('results.json', 'r') as f:
    existing_data = json.load(f)

# check if round 2 already exists
found = False
for item in existing_data:
    if item['round'] == '2':
        item['Results']['race2'] = res
        found = True
        break

if not found:
    existing_data.append(output)

with open('results.json', 'w') as f:
    json.dump(existing_data, f, indent=4)

print("Updated results.json")
