from datetime import date
from .abs import DownloadsPaginator
from .booklists import Booklists, OrderOptions


class ZlibProfile:
    __r = None
    cookies = {}
    mirror = None

    def __init__(self, request, cookies, mirror):
        self.__r = request
        self.cookies = cookies
        self.mirror = mirror

    async def download_history(self, page: int = 1, date_from: date = None, date_to: date = None):
        if date_from:
            assert type(date_from) is date
        if date_to:
            assert type(date_to) is date
        if page:
            assert type(page) is int

        dfrom = date_from.strftime('%y-%m-%d') if date_from else ''
        dto = date_to.strftime('%y-%m-%d') if date_to else ''
        url = self.mirror + '/users/dstats.php?date_from=%s&date_to=%s' % (dfrom, dto)

        paginator = DownloadsPaginator(url, page, self.__r, self.mirror)
        return await paginator.init()

    async def search_public_booklists(self, q: str, count: int = 10, order: OrderOptions = ""):
        if order:
            assert isinstance(order, OrderOptions)
        
        paginator = Booklists(self.__r, self.cookies, self.mirror)
        return await paginator.search_public(q, count=count, order=order)

    async def search_private_booklists(self, q: str, count: int = 10, order: OrderOptions = ""):
        if order:
            assert isinstance(order, OrderOptions)
        
        paginator = Booklists(self.__r, self.cookies, self.mirror)
        return await paginator.search_private(q, count=count, order=order)
