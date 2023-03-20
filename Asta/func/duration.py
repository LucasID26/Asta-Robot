
TIME_DURATION_UNITS = ( ('minggu', 60 * 60 * 24 * 7), ('hari', 60 * 60 * 24), ('jam', 60 * 60), ('menit', 60), ('detik', 1))
def duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}' .format(amount, unit, "" if amount == 1 else ""))
    return ', '.join(parts) 
