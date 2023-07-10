from gen import *
import sys
import json
from datetime import datetime, timedelta, timezone
import icalendar

if __name__ == '__main__':


    # Abre el archivo JSON especificado como parametro
    f = open(sys.argv[1])
    
    # retorna el archivo json como un diccionario
    data = json.load(f)
    
    f.close()

    # Operaciones para convertir las fechas y horas a datetime
    # para ser almacenadas y llamar al solver con los datos requeridos
    dia_inicio = datetime.strptime(data['start_date'], "%Y-%m-%d")
    dia_fin = datetime.strptime(data['end_date'], "%Y-%m-%d")
    dias = dia_fin - dia_inicio
    
    hora_inicio = datetime.strptime(data['start_time'], '%H:%M:%S')
    hora_fin = datetime.strptime(data['end_time'], '%H:%M:%S')
    horas = hora_fin - hora_inicio
        

    # Crear una instancia con los parametros
    total_teams = len(data['participants'])
    total_days = dias.days+1 #ambos dias incluso
    horas_disponibles = int(horas.total_seconds()/3600) - 1 #no se cuenta la hora de inicio
    slots_per_day = int(horas_disponibles / 2) #cada partido dura 2 horas

    solver = SatSolver(total_teams, total_days, slots_per_day,data['participants'])
    # Ejecutar el metodo solve(), retorna una lista de objetos
    # "Asignation" (Esa clase esta en ./variables/Parser.py)
    asignations = solver.solve()
    hora_inicio= hora_inicio.replace(minute = 0, 
                                     second = 0, 
                                     hour = hora_inicio.hour + 1)    
    """
    print(f'\nTorneo {data["tournament_name"]}')
    print(f'Fecha de inicio: {data["start_date"]}')
    print(f'Fecha de fin: {data["end_date"]}')
    print(f'Hora de inicio: {data["start_time"]}')
    print(f'Hora de fin: {data["end_time"]}')
    print(f'Cantidad de equipos: {total_teams}')
    print(f'Cantidad de dias: {total_days}')
    print(f'Partidos por dia: {slots_per_day}')
    """
    
    if asignations == None:
        print("No existe asignacion posible con los datos suministrados")
        exit()

        
    # Creacion del objeto donde se escribiran los datos para el iCalendar
    cal = icalendar.Calendar()
    cal.add('prodid', '-//My Calendar//example.com//')
    cal.add('version', '2.0')

    
    for asignation in asignations:
        #print(asignation)
        # and extract the relevant information

        # Por cada asignacion se crea un evento respectivo en el calendario
        event_name = f' {asignation.teams[asignation.local-1]} vs {asignation.teams[asignation.away-1]}'
        event_description = f' Local: {asignation.teams[asignation.local-1]}, Visitante: {asignation.teams[asignation.away-1]}'
        event_location = ""
        event_start_time = datetime(dia_inicio.year, 
                                    dia_inicio.month, 
                                    dia_inicio.day + asignation.day-1, 
                                    hora_inicio.hour + 2*(asignation.slot-1), 
                                    0, 
                                    0, 
                                    tzinfo=timezone.utc)
        event_end_time = datetime(dia_inicio.year, 
                                    dia_inicio.month, 
                                    event_start_time.day, 
                                    event_start_time.hour + 2, 
                                    0, 
                                    0, 
                                    tzinfo=timezone.utc)

        # Se agrega el evento al calendario
        event = icalendar.Event()
        event.add('summary', event_name)
        event.add('description', event_description)
        event.add('location', event_location)
        event.add('dtstart', event_start_time)
        event.add('dtend', event_end_time)
        cal.add_component(event)
    
    f = open(data["tournament_name"]+'.ics', 'bw')

    # Se escribe el archivo .ics a disco
    f.write(cal.to_ical())
    
    f.close()

    print(f'Se ha creado el archivo {data["tournament_name"]+".ics"} con las asignaciones')
    print(f'Puede abrir el archivo para agregarlo a su calendario')