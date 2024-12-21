from datetime import datetime


def format_time(timestamp: float | int) -> str:
    formatted_time = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    # Omit hour zeros
    if formatted_time[:2] == '00':
        formatted_time = formatted_time[3:]
    elif formatted_time[0] == '0':
        formatted_time = formatted_time[1:]
    return formatted_time