def format_number(value):
    try:
        return f"{int(value):,}"
    except:
        return str(value)


def format_percent(value):
    try:
        return f"{value * 100:.1f}%"
    except:
        return str(value)