from users.constants import (
    FILTER_INTERESTED_IN_MY,
    FILTER_OWNERS_OF_FAVORITE,
    FILTER_OWNERS_OF_PARTICIPATING,
    FILTER_PARTICIPANTS_OF_MY,
)
from users.models import User


def get_filtered_users(request):
    queryset = User.objects.order_by("-date_joined")
    active_filter = request.GET.get("filter")
    if not request.user.is_authenticated or not active_filter:
        return queryset, active_filter

    user = request.user
    if active_filter == FILTER_OWNERS_OF_FAVORITE:
        queryset = queryset.filter(owned_projects__in=user.favorites.all())
    elif active_filter == FILTER_OWNERS_OF_PARTICIPATING:
        queryset = queryset.filter(
            owned_projects__participants=user,
        ).exclude(pk=user.pk)
    elif active_filter == FILTER_INTERESTED_IN_MY:
        queryset = queryset.filter(favorites__owner=user)
    elif active_filter == FILTER_PARTICIPANTS_OF_MY:
        queryset = queryset.filter(
            participated_projects__owner=user,
        ).exclude(pk=user.pk)
    else:
        active_filter = None
    return queryset.distinct(), active_filter
