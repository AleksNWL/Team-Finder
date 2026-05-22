def get_favorite_ids(user):
    if not user.is_authenticated:
        return set()
    return set(user.favorites.values_list("pk", flat=True))
