import json

rg_data = [
    (1, 8, 16, '32:33.104', 10, '1:40.030'),
    (2, 91, 16, '+1.583', 8, '1:40.103'),
    (3, 9, 16, '+1.650', 6, '1:39.916'),
    (4, 19, 16, '+1.731', 5, '1:39.784'),
    (5, 14, 16, '+2.616', 4, '1:39.622'),
    (6, 5, 16, '+3.889', 3, '1:39.649'),
    (7, 4, 16, '+4.436', 2, '1:39.869'),
    (8, 18, 16, '+4.688', 1, '1:39.942'),
    (9, 32, 16, '+4.980', 0, '1:40.206'),
    (10, 21, 16, '+5.339', 0, '1:39.795'),
    (11, 12, 16, '+5.976', 0, '1:40.068'),
    (12, 95, 16, '+7.774', 0, '1:39.969'),
    (13, 20, 16, '+8.306', 0, '1:39.587'),
    (14, 77, 16, '+11.687', 0, '1:40.261'),
    (15, 28, 16, '+11.770', 0, '1:40.032'),
    (16, 3, 12, 'DNF', 0, '1:39.867'),
    (17, 56, 0, 'DNF', 0, ''),
    (18, 55, 0, 'DNF', 0, '')
]

def parse_time(t_str):
    if ':' in t_str:
        m, s = t_str.split(':')
        return float(m) * 60 + float(s)
    elif t_str.startswith('+'):
        return float(t_str[1:])
    return 0

base_time = parse_time(rg_data[0][3])

fls = []
for i, x in enumerate(rg_data):
    if x[5]:
        fls.append((i, parse_time(x[5])))
fls.sort(key=lambda x: x[1])
ranks = {idx: rank + 1 for rank, (idx, _) in enumerate(fls)}

res_rg = []
for i, row in enumerate(rg_data):
    pos, num, laps, t_gap, pts, fl_str = row
    
    status = 'Finished' if t_gap != 'DNF' else 'Retired'
    
    obj = {
        'number': str(num),
        'position': str(pos),
        'grid': '0',
        'laps': str(laps),
        'status': status,
        'points': str(pts),
    }
    
    if t_gap != 'DNF':
        if i == 0:
            t_tot = base_time
        else:
            t_tot = base_time + parse_time(t_gap)
        m = int(t_tot // 60)
        s = t_tot % 60
        t_tot_str = f"{m}:{s:06.3f}"
        obj['Time'] = {'time': t_tot_str}
        
    if fl_str:
        obj['FastestLap'] = {'rank': str(ranks[i]), 'lap': '0', 'Time': {'time': fl_str}}
        
    res_rg.append(obj)

with open('results.json', 'r') as f:
    data = json.load(f)

for item in data:
    if item['raceName'] == 'Canadian Grand Prix':
        # The user accidentally put Feature Race in race1. Let's move it to race2.
        # And put the new Reverse Grid Race in race1.
        feature_race_data = item['Results'].get('race1', [])
        if len(feature_race_data) > 0 and feature_race_data[0]['number'] == '21':
            item['Results']['race2'] = feature_race_data
            
        item['Results']['race1'] = res_rg

def format_race_results(race_list):
    if not race_list:
        return '[]'
    lines = ['[']
    for i, obj in enumerate(race_list):
        line_str = json.dumps(obj, separators=(', ', ': '))
        if i < len(race_list) - 1:
            lines.append('                ' + line_str + ',')
        else:
            lines.append('                ' + line_str)
    lines.append('            ]')
    return '\n'.join(lines)

output_lines = ['[']
for idx, season_data in enumerate(data):
    lines = []
    lines.append('    {')
    lines.append('        "season": "' + season_data['season'] + '",')
    lines.append('        "round": "' + season_data['round'] + '",')
    lines.append('        "raceName": "' + season_data['raceName'] + '",')
    lines.append('        "Circuit": {')
    lines.append('            "circuitId": "' + season_data['Circuit']['circuitId'] + '",')
    lines.append('            "circuitName": "' + season_data['Circuit']['circuitName'] + '"')
    lines.append('        },')
    lines.append('        "Results": {')
    lines.append('            "race1": ' + format_race_results(season_data['Results'].get('race1', [])) + ',')
    lines.append('            "race2": ' + format_race_results(season_data['Results'].get('race2', [])))
    lines.append('        }')
    
    if idx < len(data) - 1:
        lines.append('    },')
    else:
        lines.append('    }')
    output_lines.extend(lines)
output_lines.append(']')

with open('results.json', 'w') as f:
    f.write('\n'.join(output_lines) + '\n')

print("Fixed results.json")
