from datetime import datetime


def format_date(date, style="dic"):
    """
    Format the given date in a specified style.

    Args:
        date (str): The input date in the format "YYYY-MM-DD".
        style (str): The formatting style. Possible values: "short", "medium", "long".
                        Default is "short".

    Returns:
        str: The formatted date according to the specified style.
    """
    # Parse the input date string into a datetime object
    date_obj = datetime.strptime(date, "%Y-%m-%d")

    if style == "b-DD-YYYY":
        # Format date in medium style (e.g., "Jul 19, 2023")
        formatted_date = date_obj.strftime("%b %d, %Y")
    elif style == "B-DD-YYYY":
        # Format date in long style (e.g., "July 19, 2023")
        formatted_date = date_obj.strftime("%B %d, %Y")
    elif style == "YYYY-MM-DD":
        # Default: Format date in short style (e.g., "2023-07-19")
        formatted_date = date_obj.strftime("%Y-%m-%d")
    elif style == "B-DD-YYYY":
        # Format date in long style (e.g., "July 19, 2023")
        formatted_date = date_obj.strftime("%B %d, %Y")
    elif style == "DD-MM-YYYY":
        # Format date in long style (e.g., "19.07.2023")
        formatted_date = date_obj.strftime("%d.%m.%Y")
    elif style == "dic":
        # Format date in dictionary style
        d_Y = date_obj.strftime("%Y")
        d_m = date_obj.strftime("%m")
        d_d = date_obj.strftime("%d")
        d_b = date_obj.strftime("%b")
        d_B = date_obj.strftime("%B")
        formatted_date = [d_Y, d_m, d_d, d_b, d_B]

    return formatted_date


def format_time(time, style="12h"):
    """
    Format the given time in a specified style.

    Args:
        time (str): The input time in the format "HH:MM:SS".
        style (str): The formatting style. Possible values: "12h", "24h".
                    Default is "12h".

    Returns:
        str: The formatted time according to the specified style.
    """
    # Parse the input time string into a datetime object
    time_obj = datetime.strptime(time, "%H:%M:%S")

    if style == "24h":
        # Format time in 24-hour style (e.g., "12:30")
        formatted_time = time_obj.strftime("%H:%M")
    else:
        # Default: Format time in 12-hour style with AM/PM (e.g., "12:30 PM")
        formatted_time = time_obj.strftime("%I:%M %p")

    return formatted_time
