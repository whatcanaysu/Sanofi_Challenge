"""
Datetime functionalities for ensuring continuity of timeseries
"""

import pandas as pd

OFFSET_ALIASES = {
    "H": "Hourly",
    "D": "Daily",
    "W": "Weekly - Sunday",
    "W-SUN": "Weekly - Sunday",
    "W-MON": "Weekly - Monday",
    "W-TUE": "Weekly - Tueday",
    "W-WED": "Weekly - Wednesday",
    "W-THU": "Weekly - Thursday",
    "W-FRI": "Weekly - Friday",
    "W-SAT": "Weekly - Saturday",
    "M": "Month - End",
    "MS": "Month - Start",
    # Add quarterly
    "A": "Year - End",
    "Y": "Year - End",
    "AS": "Year - Start",
    "YS": "Year - Start"
}


def pandas_inferred_frequency(timestamps):
    return pd.infer_freq(timestamps)


def frequency(timestamps):
    """
    Parameters
    ----------
    timestamps: pd.Series or pd.DatetimeIndex with type date in ascending order

    Returns
    ----------
    freq: Inferred Frequency of the given timestamps
    """
    freq = pandas_inferred_frequency(timestamps)
    if freq is None:
        continuous_phases = []
        start_index = 0
        last_index = len(timestamps)
        total = len(timestamps)

        while start_index < total-2:
            while pd.infer_freq(timestamps[start_index:last_index]) is None:
                if last_index - start_index >= 4:
                    last_index -= 1
                else:
                    break
            continuous_phases.append((start_index, last_index-1))
            start_index = last_index
            last_index = total

        observed_frequencies = []
        for phase in continuous_phases:    
            if phase[1] -phase[0] >= 2:
                observed_frequencies.append(pd.infer_freq(timestamps[phase[0]: phase[1]+1]))

        freq = utils.most_frequent(observed_frequencies)

    return OFFSET_ALIASES[freq]


def is_continuous(timestamps, calendar=None):
    if calendar is not None:
        all = pd.Series(data=pd.date_range(start=timestamps.min(), end=timestamps.max(), freq=calendar))
        mask = all.isin(timestamps.values)
        if all[~mask].empty:
            return True
        return False
    if pandas_inferred_frequency(timestamps) is not None:
        return True
    return False