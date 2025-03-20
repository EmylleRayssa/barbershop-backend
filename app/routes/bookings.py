from fastapi import APIRouter, HTTPException
from pymongo import ASCENDING
from app.database import db
from app.models import Booking
from typing import List
from datetime import datetime, timedelta
from ..utils import generate_available_times

router = APIRouter()


async def get_occupied_intervals(barber_id, date):

    # Buscar agendamentos já feitos para esse barbeiro e dia
    appointments = await db.bookings.find({
                            "barber_id": barber_id,
                            "date": date
                        }).to_list(None)
        
    occupied_intervals = []
    for appt in appointments:
        start_time = datetime.strptime(f"{appt['date']} {appt['time']}", "%Y-%m-%d %H:%M")
        service = await db.services.find({"name": appt["service"]}).to_list(None)

        duration = service[0]["duration"]
        end_time = start_time + timedelta(minutes=duration)
        occupied_intervals.append((start_time, end_time))

    return occupied_intervals

def create_available_times(date, service_duration, occupied_intervals):
    """
    Criar lista de horários disponíveis
    """

    available_times = []
    for time in generate_available_times():
        start_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        end_time = start_time + timedelta(minutes=service_duration)

        # Verificar se esse horário se sobrepõe a algum já ocupado
        is_available = all(
            not (start_time < end and end_time > start)
            for (start, end) in occupied_intervals
        )

        if is_available:
            available_times.append(time)
    return available_times

@router.post("/bookings", response_model=dict)
async def create_booking(booking: Booking):
    """
    Criar um novo agendamento vinculado a um barbeiro
    """
    try:
        db.bookings.insert_one(booking.dict())
    except Exception as e:
        print("An exception occurred ::", e)
        return False
    return {"message": "Agendamento criado com sucesso!"}

@router.get("/available-times", response_model=List[str])
async def get_available_times(barber_id: str, date: str, service_duration: int):
    """
    Retorna horários disponíveis para um barbeiro em uma determinada data considerando a duração do serviço.
    """
    try:
        occupied_intervals = await get_occupied_intervals(barber_id, date)
        available_times = create_available_times(date, service_duration, occupied_intervals)
    except Exception as e:
        print("An exception occurred ::", e)
        return []
    return 


# 🔹 Rota para buscar todos os agendamentos por mês e barbeiro
@router.get("/bookings/all-bookings")
async def get_all_bookings(month: int, year: int):
    """
    Retorna todos os agendamentos de um determinado mês e ano, agrupados por barbeiro.
    """
    try:
        # 🔹 Definir as datas de início e fim do mês
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        # 🔹 Buscar agendamentos no MongoDB
        appointments_cursor = db.bookings.find({
            "date": {"$gte": start_date.strftime("%Y-%m-%d"), "$lt": end_date.strftime("%Y-%m-%d")}
        }).sort("date", ASCENDING)

        # 🔹 Converter para lista e formatar o ObjectId
        appointments = []
        async for appointment in appointments_cursor:
            appointment["_id"] = str(appointment["_id"])  # Converte o ObjectId para string
            appointments.append(appointment)

        return {"status": "success", "appointments": appointments}

    except Exception as e:
        return {"status": "error", "message": str(e)}