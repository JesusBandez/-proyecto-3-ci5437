import itertools
from bidict import bidict
import sys

def generate_variables(total_teams, total_days, slots_per_day):
    for local_team in range(1, total_teams+1):
        for road_team in range(1, total_teams+1):
            if local_team == road_team: continue

            for day in range(1, total_days+1):
                for slot in range(1, slots_per_day+1):
                    yield f'{local_team}{road_team}{day}{slot}'

def generate_days_with_teams(local_team, road_team, total_days, slots_per_day):
    for day in range(1, total_days+1):
        for slot in range(1, slots_per_day+1):
            yield f'{local_team}{road_team}{day}{slot}'



def generate_bi_dict(*args):

    vars_set = [var for var in generate_variables(*args)]
    glucose_vars = range(1, len(vars_set)+1)
    vars_dict = {var:str(glucose_var) for var, glucose_var in zip(vars_set, glucose_vars)}

    return bidict(vars_dict)


total_teams = 3
total_days = 2
slots_per_day = 1

bi_vars_dict = generate_bi_dict(total_teams, total_days, slots_per_day)
clauses = 0

# Cada equipo debe jugar contra otro de local exactamente una vez
for local_team in range(1, total_teams+1):
    for road_team in range(1, total_teams+1):
        if local_team == road_team: continue
        vars = [var for var in generate_days_with_teams(local_team, road_team, 
                                                        total_days, slots_per_day)]
                                       
        subsets = list(itertools.combinations(vars, 2))
        clauses += len(subsets)

        out = ''
        for subet in subsets:
            for var in subet:
                out += f'-{bi_vars_dict[var]} '

            out += '0\n'

        subsets = list(itertools.combinations(vars, len(vars)))
        clauses += len(subsets)

        
        for subet in subsets:
            for var in subet:
                out += f'{bi_vars_dict[var]} '

            out += '0\n'
        print(out)

print(f'p cnf {len(bi_vars_dict)} {clauses}')
print(bi_vars_dict, file=sys.stderr)



# subsets = list(itertools.combinations(bi_vars_dict, 2))
# clauses = len(subsets)

# out = ''
# for subet in subsets:
#     for var in subet:
#         out += f'-{bi_vars_dict[var]} '

#     out += '0\n'

# print(out)

# subsets = list(itertools.combinations(bi_vars_dict, len(bi_vars_dict)-2+1))

# out = ''
# for subet in subsets:
#     for var in subet:
#         out += f'{bi_vars_dict[var]} '

#     out += '0\n'

# print(out)
# out = f'p cnf {len(bi_vars_dict)} {clauses +len(subsets)}'
# print(out)

