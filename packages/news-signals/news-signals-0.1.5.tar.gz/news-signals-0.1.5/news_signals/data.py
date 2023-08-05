import pandas as pd

from .log import create_logger


logger = create_logger(__name__)


def arrow_to_aylien_date(arrow_dt):
    return arrow_dt.datetime.isoformat()[:-6]+'Z'


def datetime_to_aylien_str(dt):
    """
    Convert python datetime object to the string format
    used by Aylien newsAPI
    """
    # Note splitting on '+' cuts off non-UTC datetime information
    dt_str = dt.isoformat().split('+')[0]
    # force UTC
    if 'T' not in dt_str:
        dt_str = f'{dt_str}T00:00:00.0'
    dt_str = f'{dt_str}Z'

    return dt_str


def aylien_ts_to_df(data, dt_index=False, ts_count_name=None,
                    normalize=False, freq=None):
    """
    :param data: response from aylien timeseries endpoint
    :param dt_index: if True, the dataframe will have an index
    of type datetime
    :param ts_count_name: if not None, we'll add a column
    that renames the 'count' column. This is useful when
    we're planning to combine multiple timeseries into
    one dataframe.
    """
    ts = []
    # backwards compatibility
    if type(data) is dict:
        data = data['time_series']
    for r in data:
        zr = dict(**r)
        timestamp = f'{r["published_at"]}'
        if normalize:
            timestamp = pd.Timestamp(timestamp).floor(freq=freq)
        zr['published_at'] = timestamp
        ts.append(zr)

    orig_len = len(data)
    df = pd.DataFrame(ts)
    df['date'] = pd.to_datetime(df['published_at'], utc=True)
    if dt_index:
        df['date'] = pd.DatetimeIndex(df['date'])
        df.set_index('date', inplace=True)
    else:
        df.set_index('published_at', inplace=True)
    if ts_count_name is not None:
        df = df.rename(columns={'count': ts_count_name})
    assert len(df) == orig_len
    return df
