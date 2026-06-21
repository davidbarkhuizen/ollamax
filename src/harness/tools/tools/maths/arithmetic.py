async def add(x: float, y: float) -> str:
    """
    returns the sum of two real numbers (floats)

    Args:
        x: first addend
        y: second addend

    Returns:
        A sum as a float
    """
    return str(x + y)


async def subtract(minuend: float, subtrahend: float) -> str:
    """
    return the difference between two real numbers (floats)

    Args:
        x: minuend
        y: subtrahend

    Returns:
        The difference as a float
    """

    return str(minuend - subtrahend)


async def multiply(x: float, y: float) -> str:
    """
    return the product of two real numbers (floats)

    Args:
        x: first factor
        y: second factor

    Returns:
        The product of the two factors as a float
    """

    return str(x * y)


async def divide(dividend: float, divisor: float) -> str:
    """
    return the quotient of two real numbers (floats)

    Args:
        x: dividend
        y: divisor

    Returns:
        The quotient of the two numbers
    """

    return str(dividend / divisor)
