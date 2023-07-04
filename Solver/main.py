from gen import *
import sys
import json
from datetime import datetime

if __name__ == '__main__':


    # Opening JSON file
    f = open(sys.argv[1])
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    #print(data)
    
    # Closing file
    f.close()

    date1 = datetime.strptime(data['start_date'], "%Y-%m-%d")
    date2 = datetime.strptime(data['end_date'], "%Y-%m-%d")
    delta = date2 - date1
    #print(f'Difference is {delta.days} days')

    hora_inicio = datetime.strptime(data['start_time'], '%H:%M:%S')
    hora_fin = datetime.strptime(data['end_time'], '%H:%M:%S')
    horas = hora_fin - hora_inicio
    #print(f'Difference is {int(horas.total_seconds()/3600)} horas')

    """
    print("Participants:")
    for i in data['participants']:
        print(i)
    """


    # Crear una instancia con los parametros
    total_teams = len(data['participants'])
    total_days = delta.days+1 #ambos dias incluso
    horas_disponibles = int(horas.total_seconds()/3600) - 1 #no se cuenta la hora de inicio
    slots_per_day = int(horas_disponibles / 2) #cada partido dura 2 horas

    solver = SatSolver(total_teams, total_days, slots_per_day,data['participants'])
    # Ejecutar el metodo solve(), retorna una lista de objetos
    # "Asignation" (Esa clase esta en ./variables/Parser.py)
    asignations = solver.solve()
    
    print(f'\nTorneo {data["tournament_name"]}')
    print(f'Fecha de inicio: {data["start_date"]}')
    print(f'Fecha de fin: {data["end_date"]}')
    print(f'Hora de inicio: {data["start_time"]}')
    print(f'Hora de fin: {data["end_time"]}')
    print(f'Cantidad de equipos: {total_teams}')
    print(f'Cantidad de dias: {total_days}')
    print(f'Partidos por dia: {slots_per_day}')
    
    if asignations == None:
        print("No existe asignacion posible con los datos suministrados")
        exit()

    print("\nAsignaciones:")
    # Imprimir asignaciones
    for asignation in asignations:
        print(asignation)