from django.core.paginator import Paginator

from team_finder.constants import ITEMS_PER_PAGE


def paginate(queryset, request, *, per_page=ITEMS_PER_PAGE, page_kwarg="page"):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get(page_kwarg))
