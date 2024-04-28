import datetime
from typing import List, Optional

from lxml.cssselect import CSSSelector

from fundus.parser import ArticleBody, BaseParser, ParserProxy, attribute
from fundus.parser.utility import (
    extract_article_body_with_selector,
    generic_author_parsing,
    generic_date_parsing,
)

class HamburgerAbendblattParser(ParserProxy):
    class V1(BaseParser):
        #_paragraph_selector = CSSSelector("div[data-element*=story-body] > p")
        _paragraph_selector = CSSSelector("div.article-body > p")

        @attribute
        def body(self) -> ArticleBody:
            #return self.precomputed.meta.get("og:description")

            # return extract_article_body_with_selector(
            #     self.precomputed.meta.get("og:description"),
            #     paragraph_selector=self._paragraph_selector,
            # )
        
            return extract_article_body_with_selector(
                self.precomputed.doc,
                paragraph_selector=self._paragraph_selector,
            )

        @attribute
        def publishing_date(self) -> Optional[datetime.datetime]:
            return generic_date_parsing(self.precomputed.ld.bf_search("datePublished"))

        @attribute
        def authors(self) -> List[str]:
            return generic_author_parsing(self.precomputed.ld.bf_search("author"))

        @attribute
        def title(self) -> Optional[str]:
            return self.precomputed.meta.get("og:title")