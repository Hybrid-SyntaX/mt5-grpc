import numpy as np

def rates_to_numpy(rates):
    """
    Convert Rates protobuf data to a structured NumPy array.

    Parameters:
    - rates: A Rates protobuf object containing the data.

    Returns:
    - A structured NumPy array containing the rates data.
    """

    # Extract data from the Rates protobuf object
    timestamps = rates.time
    highs = rates.high
    lows = rates.low
    opens = rates.open
    closes = rates.close
    real_volumes = rates.real_volume
    tick_volumes = rates.tick_volume
    spread = rates.spread

    # Check if all fields have the same length
    lengths = {len(timestamps), len(highs), len(lows), len(opens), len(closes), len(real_volumes),
               len(tick_volumes), len(spread)}

    if len(lengths) > 1:
        raise ValueError("All input fields must have the same length. Found lengths: {}".format(lengths))

    # Convert timestamps to a readable format (e.g., string)
    # time_strings = np.array([ts.ToDatetime().isoformat() for ts in timestamps], dtype='U25')

    # Create a structured NumPy array
    dtype = [('time', '<i8'), ('open', '<f8'), ('high', '<f8'), ('low', '<f8'), ('close', '<f8'),
             ('tick_volume', '<u8'), ('spread', '<i4'), ('real_volume', '<u8')]
    data = np.zeros(len(timestamps), dtype=dtype)

    # Fill the structured array
    data['time'] = timestamps
    data['high'] = highs
    data['low'] = lows
    data['open'] = opens
    data['close'] = closes
    data['real_volume'] = real_volumes
    data['tick_volume'] = tick_volumes
    data['spread'] = spread

    return data


def ticks_to_numpy(ticks):
    """
    Convert Ticks protobuf data to a structured NumPy array.

    Parameters:
    - ticks: A Ticks protobuf object containing the data.

    Returns:
    - A structured NumPy array containing the ticks data.
    """

    # Extract data from the Ticks protobuf object
    times = ticks.time
    bids = ticks.bid
    asks = ticks.ask
    lasts = ticks.last
    volumes = ticks.volume
    time_msc = ticks.time_msc
    flags = ticks.flags
    volume_reals = ticks.volume_real  # SIC !

    # Check if all fields have the same length
    lengths = {len(times), len(bids), len(asks), len(lasts), len(volumes), len(time_msc), len(flags),
               len(volume_reals)}

    if len(lengths) > 1:
        raise ValueError("All input fields must have the same length. Found lengths: {}".format(lengths))

    # Create a structured NumPy array
    dtype = [('time', 'i8'), ('bid', 'f8'), ('ask', 'f8'), ('last', 'f8'),
             ('volume', 'u8'), ('time_msc', 'i8'), ('flags', 'u4'), ('volume_real', 'f8')]
    data = np.zeros(len(times), dtype=dtype)

    # Fill the structured array
    data['time'] = times
    data['bid'] = bids
    data['ask'] = asks
    data['last'] = lasts
    data['volume'] = volumes
    data['time_msc'] = time_msc
    data['flags'] = flags
    data['volume_real'] = volume_reals

    return data
