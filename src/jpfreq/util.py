def percent_of(part: [int|float], total: [int|float]):
    if total == 0:
        return 0

    return (part / total) * 100