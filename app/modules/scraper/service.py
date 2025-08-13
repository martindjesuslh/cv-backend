import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, Any
from app.modules.scraper.models import ScrapedTarget, ScrapedData, ScrapeMethod
from app.core.config.settings import settings
import time
import re


class _ScraperClient:
    """Client for scraping web pages using different methods"""

    def __init__(self):
        self.timeout = settings.SCRAPED_TIMEOUT or 30
        self.session = requests.Session()

    def scrape(
        self, target: ScrapedTarget, html_content: Optional[str] = None
    ) -> ScrapedData:
        if target.method == ScrapeMethod.BEAUTIFUL_SOUP:
            return self._scrape_with_beautiful_soup(target, html_content)
        elif target.method == ScrapeMethod.REGEX:
            return self._scrape_with_regex(target, html_content)
        else:
            raise ValueError(f"Method for scraping is not supported: {target.method}")

    def _scrape_with_beautiful_soup(
        self, target: ScrapedTarget, html_content: Optional[str] = None
    ) -> ScrapedData:
        content = html_content

        if not html_content:
            content = self._get_page(target=target)

        soup = BeautifulSoup(content, "html.parser")
        extracted_data = {}

        if not target.selectors:
            extracted_data = self._extract_general_info(soup)
        else:
            for selector in target.selectors:
                elements = soup.select(selector)
                extracted_data[selector] = [
                    elem.get_text(strip=True) for elem in elements
                ]

        return ScrapedData(
            url=target.url,
            data=extracted_data,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            method_used=target.method,
        )

    def _scrape_with_regex(
        self, target: ScrapedTarget, html_content: Optional[str] = None
    ) -> ScrapedData:
        content = html_content

        if not content:
            content = self._get_page(target=target)

        extracted_data = {}

        for patter in target.selectors:
            matches = re.findall(patter, content)
            extracted_data[patter] = matches

        return ScrapedData(
            url=target.url,
            data=extracted_data,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            method_used=target.method,
        )

    def _get_page(self, target: ScrapedTarget) -> str:
        response = self.session.get(
            url=target.url,
            headers=target.headers,
            timeout=target.timeout or self.timeout,
        )

        response.raise_for_status()

        return response.text

    def _extract_general_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        return {
            "title": soup.title.string if soup.title else None,
            "meta_description": self._get_meta_content(soup, "description"),
            "meta_keywords": self._get_meta_content(soup, "keywords"),
            "headings": {
                f"h{i}": [h.get_text(strip=True) for h in soup.find_all(f"h{i}")]
                for i in range(1, 7)
            },
            "links": [a.get("href") for a in soup.find_all("a", href=True)],
        }

    def _get_meta_content(self, soup: BeautifulSoup, name: str) -> Optional[str]:
        meta_tag = soup.find("meta", {"name": name})
        if not meta_tag:
            meta_tag = soup.find("meta", {"property": f"og{name}"})
        if not meta_tag:
            meta_tag = soup.find("meta", {"itemprop": name})

        return meta_tag.get("content") if meta_tag else None

    def _get_default_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }


scraped_client = _ScraperClient()
