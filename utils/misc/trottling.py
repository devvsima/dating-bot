def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, "trottling_rate_limit", limit)
        if key:
            setattr(func, "trottling_key", key)
        return func

    return decorator
