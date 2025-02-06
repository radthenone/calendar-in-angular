from datetime import datetime, timedelta

from django.utils import timezone


def grid_range_for_month(year: int, month: int) -> tuple:
    """
    Calculate the start and end dates for a month grid.

    The month grid is a 6-week period that includes the entire month.
    The start date is the first day of the week that includes the first day of the month.
    The end date is 41 days after the start date.

    Args:
        year (int): The year of the month.
        month (int): The month (1-12).

    Returns:
        tuple: A tuple containing the start and end dates of the month grid.
    """
    # Create a timezone-aware date object for the first day of the month
    first_day = timezone.make_aware(datetime(year, month, 1))

    # Calculate the start date by subtracting the weekday of the first day
    # This ensures that the start date is the first day of the week
    grid_start = first_day - timedelta(days=first_day.weekday())

    # Calculate the end date by adding 41 days to the start date
    grid_end = grid_start + timedelta(days=41)

    # Return the start and end dates as a tuple
    return grid_start, grid_end


def get_prev_month(year: int, month: int):
    if month == 1:
        return year - 1, 12
    return year, month - 1


def get_next_month(year: int, month: int):
    if month == 12:
        return year + 1, 1
    return year, month + 1
