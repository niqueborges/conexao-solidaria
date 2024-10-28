from datetime import datetime
import pytz


def format_date(dt: datetime) -> str:
    """
    Converte a data e hora fornecida para o fuso horário
    de São Paulo e retorna no formato `%d-%m-%Y %H:%M:%S`.
    """
    # Define o fuso horário de São Paulo
    sao_paulo_tz = pytz.timezone("America/Sao_Paulo")

    # Converte a data para o fuso horário de São Paulo
    sao_paulo_dt = dt.astimezone(sao_paulo_tz)

    # Retorna a data formatada
    return sao_paulo_dt.strftime("%d-%m-%Y %H:%M:%S")
