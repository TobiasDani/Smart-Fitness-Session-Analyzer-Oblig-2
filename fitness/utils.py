def calculate_average(values):
    """Return the average of a list of numeric values."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def calculate_minimum(values):
    """Return the smallest value in a list."""
    if not values:
        return None
    return min(values)


def calculate_maximum(values):
    """Return the largest value in a list."""
    if not values:
        return None
    return max(values)


def calculate_drop(first_values, second_values):
    """Measure how much the average changes from the first to second part."""
    if not first_values or not second_values:
        return 0.0
    return calculate_average(first_values) - calculate_average(second_values)

