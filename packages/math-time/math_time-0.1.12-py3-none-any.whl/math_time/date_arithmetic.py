from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def add_days(date, num_days):
    """
    Add a specified number of days to a given date.

    Args:
        date_str (str): The input date in the format "YYYY-MM-DD".
        num_days (int): The number of days to add.

    Returns:
        str: The resulting date after adding the specified number of days in the format "YYYY-MM-DD".
    """
    # Parse the input date string into a datetime object
    date_obj = datetime.strptime(date, "%Y-%m-%d")

    # Add the specified number of days to the date
    result_date_obj = date_obj + timedelta(days=num_days)

    # Format the resulting datetime object as a string
    result_date_str = result_date_obj.strftime("%Y-%m-%d")

    return result_date_str


def subtract_days(date_str, num_days):
    """
    Subtract a specified number of days from a given date.

    Args:
        date_str (str): The input date in the format "YYYY-MM-DD".
        num_days (int): The number of days to subtract.

    Returns:
        str: The resulting date after subtracting the specified number of days in the format "YYYY-MM-DD".
    """
    # Parse the input date string into a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Subtract the specified number of days from the date
    result_date_obj = date_obj - timedelta(days=num_days)

    # Format the resulting datetime object as a string
    result_date_str = result_date_obj.strftime("%Y-%m-%d")

    return result_date_str


def add_months(date_str, num_months):
    """
    Add a specified number of months to a given date.

    Args:
        date_str (str): The input date in the format "YYYY-MM-DD".
        num_months (int): The number of months to add.

    Returns:
        str: The resulting date after adding the specified number of months in the format "YYYY-MM-DD".
    """
    # Parse the input date string into a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Add the specified number of months to the date
    result_date_obj = date_obj + relativedelta(months=num_months)

    # Format the resulting datetime object as a string
    result_date_str = result_date_obj.strftime("%Y-%m-%d")

    return result_date_str


def subtract_months(date, num_months):
    """
    Subtract a specified number of months from a given date.

    Args:
        date_str (str): The input date in the format "YYYY-MM-DD".
        num_months (int): The number of months to subtract.

    Returns:
        str: The resulting date after subtracting the specified number of months in the format "YYYY-MM-DD".
    """
    # Parse the input date string into a datetime object
    date_obj = datetime.strptime(date, "%Y-%m-%d")

    # Calculate the new year and month after subtraction
    new_year = date_obj.year
    new_month = date_obj.month - num_months

    # Handle the case where the result crosses a year boundary
    while new_month <= 0:
        new_year -= 1
        new_month += 12

    # Calculate the resulting date
    result_date_obj = date_obj.replace(year=new_year, month=new_month)

    # Format the resulting datetime object as a string
    result_date_str = result_date_obj.strftime("%Y-%m-%d")

    return result_date_str
