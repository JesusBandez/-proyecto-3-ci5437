from variables.generators import (
    generate_variables,
    generate_days_with_teams,
    generate_days_per_team,
    generate_teams_per_day_and_slot
)
from variables.condicionales import (
    sum_greater_or_equal,
    sum_less_or_equal
    
)
from bidict import bidict
import subprocess
import sys

GLUCOSE_PATH = './'
CNF_FILE_NAME = 'cnf.cnf'
GLUCOSE_FILE_NAME = 'gluc.gluc'

class SatSolver():
    def __init__(self, total_teams, 
                total_days, slots_per_day):
        self.total_teams = total_teams
        self.total_days = total_days
        self.slots_per_day = slots_per_day
        self.generate_bi_dict(total_teams, total_days, slots_per_day)
        self.clauses = 0
        self.constraints = ''

    def generate_bi_dict(self, *args):
        vars_set = [var for var in generate_variables(*args)]
        glucose_vars = range(1, len(vars_set)+1)
        vars_dict = {var:str(glucose_var) for var, glucose_var in zip(vars_set, glucose_vars)}
        self.bidict = bidict(vars_dict)

    def increase_outputs(self, args):        
        self.constraints += args[0]
        self.clauses += args[1]

    # Restricciones
    def each_team_plays_with_another_exactly_one_time(self):
        'Cada equipo debe jugar contra otro exactamente una vez'
        for local_team in range(1, self.total_teams+1):
            for road_team in range(1, self.total_teams+1):
                if local_team == road_team: continue
                vars = generate_days_with_teams(local_team, road_team, 
                                                self.total_days, self.slots_per_day)

                self.increase_outputs(sum_greater_or_equal(self.bidict, vars, 1))                
                self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))
                

    def at_most_one_game_a_day_per_team(self):
        'A lo mas un equipo puede jugar una vez por dia'
        for team in range(1, self.total_teams+1):
            for day in range(1, self.total_days+1):
                vars = generate_days_per_team(team, day,
                    self.total_teams, self.slots_per_day)
                
                self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))

    def only_one_game_per_day_and_slot(self):
        'No puede haber dos juegos al mismo tiempo'
        for day in range(1, self.total_days+1):
            for slot in range(1, self.slots_per_day+1):
                vars = generate_teams_per_day_and_slot(day, slot, self.total_teams)

            self.increase_outputs(sum_less_or_equal(self.bidict, vars, 1))




    ##############

    def call_glucose(self):
        subprocess.run(['./glucose', CNF_FILE_NAME, GLUCOSE_FILE_NAME,  '-model', '-verb=0'], 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def parse_output(self):
        if not self.output: return None
        vars = self.output.split()
        vars = list(filter(lambda x: int(x) > 0, vars))
        self.output = [self.bidict.inverse[var] for var in vars]
        print(self.output)
        
    def solve(self):
        self.each_team_plays_with_another_exactly_one_time()
        self.at_most_one_game_a_day_per_team()
        self.only_one_game_per_day_and_slot()
        self.constraints = f'p cnf {len(self.bidict)} {self.clauses}\n{self.constraints}'

        with open(CNF_FILE_NAME, 'w') as f:
            f.write(self.constraints)
            f.close()

        self.call_glucose()
        with open(GLUCOSE_FILE_NAME, 'r') as f:
            self.output = f.readline().strip()
            if self.output == "UNSAT":
                self.output = None
        self.parse_output()
            

                           

                


if __name__ == '__main__':

    total_teams = 5
    total_days = 20
    slots_per_day = 1

    solver = SatSolver(total_teams, total_days, slots_per_day)
    solver.solve()
    

    
