from singer_sdk.pagination import JSONPathPaginator, BaseAPIPaginator

class ruddrPaginator(BaseAPIPaginator):
    """Pagination class for ruddr."""
    def __init__(self, *args, **kwargs):
        self.start_value = None
        self._finished = False
        self._page_count = 0
        self._value = None



    def get_next(self, response):
        body: dict = response.json()
        hasMore = body.get("hasMore")

        # if no more results, stop pagination
        if not hasMore:
            return

        # leverage JSONPathPaginator to lookup the id of the last result
        return JSONPathPaginator("$.results[-1:].id").get_next(response)