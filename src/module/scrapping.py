

class Extract:
    def __init__(self, page_start: int, page_end: int) -> None:
        """Initializing the extraction class involves providing the URL from which data
        is to be extracted, as well as specifying the range of pages from which
        extraction is to be performed.

        Args:
            page_start (int): Start of page number to be extracted.
            page_end (int): End of page number to be extracted.
        """
        self.url = "https://store.steampowered.com/search/?"
        self.page_start = page_start
        self.page_end = page_end

    def get_links(self) -> list[str]:
        """This method returns a list of all the links
        on the different page to be extracted.

        Returns:
            list[str]: A list of all the links to be extracted.
        """
        return [
            self.url + str(f"page={i}")
            for i in range(self.page_start, self.page_end)]
