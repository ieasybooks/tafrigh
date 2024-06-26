def format_timestamp(seconds: float, include_hours: bool = False, decimal_marker: str = '.') -> str:
    assert seconds >= 0, 'Non-negative timestamp expected'

    total_milliseconds = int(round(seconds * 1_000))

    hours, total_milliseconds = divmod(total_milliseconds, 3_600_000)
    minutes, total_milliseconds = divmod(total_milliseconds, 60_000)
    seconds, milliseconds = divmod(total_milliseconds, 1_000)

    if include_hours or hours > 0:
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    else:
        time_str = f"{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"

    return time_str
