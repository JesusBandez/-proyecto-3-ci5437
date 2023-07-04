def generate_variables(total_teams, total_days, slots_per_day):
    for local_team in range(1, total_teams+1):
        for road_team in range(1, total_teams+1):
            if local_team == road_team: continue

            for day in range(1, total_days+1):
                for slot in range(1, slots_per_day+1):
                    yield f'{local_team}{road_team}{day}{slot}'


def generate_days_with_teams(local_team, road_team, total_days, slots_per_day):
    vars = []
    for day in range(1, total_days+1):
        for slot in range(1, slots_per_day+1):
            vars.append(f'{local_team}{road_team}{day}{slot}')
    return vars


def generate_days_per_team(team, day, total_teams, total_slots):
    vars = []
    for oponent in range(1, total_teams+1):
        if oponent == team: continue     
        for slot in range(1, total_slots+1):
            vars.append(f'{team}{oponent}{day}{slot}')
            vars.append(f'{oponent}{team}{day}{slot}')
    return vars


def generate_teams_per_day_and_slot(day, slot, total_teams):
    vars = []
    for local in range(1, total_teams+1):
        for away in range(1, total_teams+1):
            if local == away: continue  
            vars.append(f'{local}{away}{day}{slot}')
    return vars

def generate_no_consecutive_local_games(team, day, total_teams, total_slots):
    vars = []
    for oponent in range(1, total_teams+1):
        if team == oponent: continue        
        for slot in range(1, total_slots+1):            
            vars.append(f'{team}{oponent}{day}{slot}')
            vars.append(f'{team}{oponent}{day+1}{slot}')
    return vars

def generate_no_consecutive_away_games(team, day, total_teams, total_slots):
    vars = []
    for oponent in range(1, total_teams+1):
        if team == oponent: continue        
        for slot in range(1, total_slots+1):            
            vars.append(f'{oponent}{team}{day}{slot}')
            vars.append(f'{oponent}{team}{day+1}{slot}')
    return vars

