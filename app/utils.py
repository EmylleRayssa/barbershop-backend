from datetime import datetime, time, timedelta

def generate_available_times():
    """
    Função para gerar horários de 30 em 30 minutos
    """
    start_time = time(8, 0)  # 08:00
    end_time = time(18, 0)   # 18:00
    interval = timedelta(minutes=15)

    times = []
    current_time = start_time

    while current_time < end_time:
        times.append(current_time.strftime("%H:%M"))
        current_time = (datetime.combine(datetime.today(), current_time) + interval).time()

    return times