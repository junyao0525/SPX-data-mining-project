from datetime import timedelta ,datetime
import numpy as np
from logger import *

def date_to_index_in_multiple_file(
        start_date: datetime, 
        end_date  : datetime ):
    
    try:
        init_date = datetime.strptime("2021-01-01", '%Y-%m-%d')

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        # Check if all days in the range are weekends
        all_weekends = all(
            (start_date + timedelta(days=i)).weekday() >= 5
            for i in range((end_date - start_date).days + 1)
        )

        if all_weekends:
            raise ValueError("The date range contains only weekend days. At least one weekday is required.")

        if start_date > init_date:
            days_difference = (start_date - init_date).days
            weekdays = sum(1 for i in range(days_difference) if (init_date + timedelta(days=i)).weekday() < 5)
            start_point = 4803 + weekdays
        elif start_date < init_date:
            days_difference = (init_date - start_date).days
            weekdays = sum(1 for i in range(days_difference) if (start_date + timedelta(days=i)).weekday() < 5)
            start_point = 4803 - weekdays

        if end_date > init_date:
            days_difference = (end_date - init_date).days
            weekdays = sum(1 for i in range(days_difference) if (init_date + timedelta(days=i)).weekday() < 5)
            end_point = 4803 + weekdays
        elif end_date < init_date:
            days_difference = (init_date - end_date).days
            weekdays = sum(1 for i in range(days_difference) if (end_date + timedelta(days=i)).weekday() < 5)
            end_point = 4803 - weekdays
        
        if start_point > end_point:
            index = np.arange(start_point, end_point, -1)
        else:
            index = np.arange(start_point, end_point + 1)  # Include end_point
        
        return index
    
    except (ValueError, TypeError) as e:
        errorLog.error(f'Failed to calculate date index: {e}')
        raise

def date_to_index(dates :datetime):
    try:
        if dates.weekday() >= 5:
            raise ValueError("The provided date is a weekend. Please provide a weekday.")
        
        start_date = datetime.strptime("2021-01-01", '%Y-%m-%d')
        end_date = dates

        if end_date < start_date:
            days_difference = (start_date - end_date).days
            weekdays = sum(1 for i in range(days_difference) if (end_date + timedelta(days=i)).weekday() < 5)
            index = 4803 - weekdays
        else:
            days_difference = (end_date - start_date).days
            weekdays = sum(1 for i in range(days_difference) if (start_date + timedelta(days=i)).weekday() < 5)
            index = 4803 + weekdays

        return index
    except (ValueError, TypeError) as e:
        errorLog.error(f'Failed to calculate date index: {e}')
        raise


def get_date_list (start_date: datetime, end_date: datetime):
    try:
        weekdays = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 5:  # 0=Mon, 4=Fri, 5=Sat, 6=Sun
                weekdays.append(current_date.strftime('%Y%m%d'))
            current_date += timedelta(days=1)
        
        return weekdays
    except (ValueError, TypeError) as e:
        errorLog.error(f'Failed to get date list: {e}')
        raise