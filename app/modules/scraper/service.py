from bs4 import BeautifulSoup
from typing import Dict, Optional, Any
from app.modules.scraper.models import ScrapedTarget, ScrapedData, ScrapeMethod
import time
import re


class ScraperClient:
    """Client for scraping web pages using different methods"""

    def scrape(self, target: ScrapedTarget, html_content: str) -> ScrapedData:
        if target.method == ScrapeMethod.BEAUTIFUL_SOUP:
            return self._scrape_with_beautiful_soup(target, html_content)
        elif target.method == ScrapeMethod.REGEX:
            return self._scrape_with_regex(target, html_content)
        else:
            raise ValueError(f"Method for scraping is not supported: {target.method}")

    def _scrape_with_beautiful_soup(
        self, target: ScrapedTarget, html_content: str
    ) -> ScrapedData:
        if len(target.selectors) == 0:
            raise ValueError("No selectors provided for scraping")

        soup = BeautifulSoup(html_content, "html.parser")
        extracted_data = {}

        for selector in target.selectors:
            elements = soup.select(selector)
            extracted_data[selector] = [el.get_text(strip=True) for el in elements]

        return ScrapedData(
            url=target.url,
            data=extracted_data,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            method_used=target.method,
        )

    def _scrape_with_regex(
        self, target: ScrapedTarget, html_content: str
    ) -> ScrapedData:
        if len(target.selectors) == 0:
            raise ValueError("No selectors provided for scraping")

        extracted_data = {}

        for pattern in target.selectors:
            matches = re.findall(pattern, html_content)
            extracted_data[pattern] = matches

        return ScrapedData(
            url=target.url,
            data=extracted_data,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            method_used=target.method,
        )

    def _get_meta_content(self, soup: BeautifulSoup, name: str) -> Optional[str]:
        meta_tag = soup.find("meta", {"name": name})
        if not meta_tag:
            meta_tag = soup.find("meta", {"property": f"og{name}"})
        if not meta_tag:
            meta_tag = soup.find("meta", {"itemprop": name})

        return meta_tag.get("content") if meta_tag else None
