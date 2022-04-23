import math
import re


def get_pagination(request, cls, page_size, page):
    rx = re.compile(r"&page=[0-9]")
    path = request.get_full_path()

    if rx.search(path):
        previous = re.sub(rx, f"&page={page - 1}", path)
        next = re.sub(rx, f"&page={page + 1}", path)
    else:
        previous = path + f"&page={page - 1}"
        next = path + f"&page={page + 1}"

    count = cls.objects.count()
    pages = math.ceil(count / page_size)

    if page - 1 == 0:
        previous = None

    if page + 1 > pages:
        next = None

    return {
        "previous": previous,
        "next": next,
        "current_page": page,
        "number_of_pages": pages,
        "count": count,
    }
