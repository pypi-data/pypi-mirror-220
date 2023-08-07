import pytz
from datetime import datetime


def timezone_converter(date_time, from_timezone, to_timezone):
    """
    Convert a date and time from one timezone to another.

    Args:
        date_time_str (str): The input date and time in the format "YYYY-MM-DD HH:MM:SS".
        from_timezone (str): The original timezone, e.g., "America/New_York".
        to_timezone (str): The target timezone, e.g., "Europe/London".

    Returns:
        str: The converted date and time in the format "YYYY-MM-DD HH:MM:SS".
        """
    # Parse the input date and time string into a datetime object
    date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

    # Get the time zone objects for the provided timezones
    from_tz = pytz.timezone(from_timezone)
    to_tz = pytz.timezone(to_timezone)

    # Convert the datetime object to the original timezone
    date_time_obj = from_tz.localize(date_time_obj)

    # Convert the datetime object to the target timezone
    converted_date_time_obj = date_time_obj.astimezone(to_tz)

    # Format the converted datetime object as a string
    converted_date_time_str = converted_date_time_obj.strftime(
        "%Y-%m-%d %H:%M:%S")

    return converted_date_time_str
