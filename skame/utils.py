def compose(f, g, *rest):
    """Compose the given functions into one function.

    :returns: A function that is the composition of the given functions.
    :rtype: function
    """
    if not rest:
        return lambda *args, **kwargs: f(g(*args, **kwargs))
    return compose(f, compose(g, *rest))
