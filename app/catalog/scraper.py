import json
import re
import time
from typing import List, Dict

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.shl.com"

CATALOG_URL = (
    "https://www.shl.com/solutions/products/product-catalog/"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    )
}


class SHLCatalogScraper:

    def __init__(self):

        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_page(self, url: str) -> BeautifulSoup:

        response = self.session.get(url, timeout=30)

        response.raise_for_status()

        return BeautifulSoup(response.text, "lxml")

    def get_assessment_links(self) -> List[str]:

        print("Fetching catalog page...")

        soup = self.fetch_page(CATALOG_URL)

        links = set()

        for a in soup.find_all("a", href=True):

            href = a["href"].strip()

            # Ignore empty links
            if not href:
                continue

            # Convert relative URLs to full URLs
            if href.startswith("/"):
                href = BASE_URL + href

            href_lower = href.lower()

            # Keep only catalog assessment pages
            if "/products/product-catalog/view/" not in href_lower:
                continue

            # Exclude job solutions
            if "solution" in href_lower:
                continue

            # Exclude query URLs
            if "?" in href_lower:
                continue

            # Ensure valid SHL URL
            if not href.startswith("https://www.shl.com"):
                continue

            links.add(href)

        print(f"Filtered to {len(links)} assessment links")

        return sorted(list(links))

    def parse_assessment_page(self, url: str) -> Dict:

        print(f"Parsing: {url}")

        try:

            soup = self.fetch_page(url)

            # Title
            title_tag = soup.find("h1")

            title = (
                title_tag.get_text(strip=True)
                if title_tag
                else "Unknown"
            )

            # Description
            paragraphs = soup.find_all("p")

            description = " ".join(
                p.get_text(" ", strip=True)
                for p in paragraphs[:10]
            )

            description = " ".join(description.split())

            full_text = soup.get_text(
                " ",
                strip=True
            ).lower()

            # Infer test type
            test_type = "Unknown"

            if "personality" in full_text:
                test_type = "P"

            elif (
                "ability" in full_text
                or "cognitive" in full_text
                or "knowledge" in full_text
            ):
                test_type = "K"

            elif "simulation" in full_text:
                test_type = "S"

            # Extract duration
            duration = None

            duration_match = re.search(
                r"(\d+)\s*minutes",
                full_text
            )

            if duration_match:
                duration = int(
                    duration_match.group(1)
                )

            # Remote support
            remote_testing = (
                "remote" in full_text
                or "online" in full_text
            )

            # Adaptive testing
            adaptive_support = (
                "adaptive" in full_text
            )

            # Skill extraction
            skills = []

            keywords = [
                "java",
                ".net",
                "sql",
                "python",
                "leadership",
                "communication",
                "customer service",
                "accounting",
                "sales",
                "banking",
                "coding",
                "administration",
            ]

            for keyword in keywords:

                if keyword in full_text:
                    skills.append(keyword)

            return {
                "name": title,
                "url": url,
                "description": description,
                "test_type": test_type,
                "duration_minutes": duration,
                "remote_testing": remote_testing,
                "adaptive_support": adaptive_support,
                "skills": skills,
            }

        except Exception as e:

            print(f"Failed: {url} -> {e}")

            return {}

    def scrape(self) -> List[Dict]:

        links = self.get_assessment_links()

        assessments = []

        for link in links:

            item = self.parse_assessment_page(link)

            if item:
                assessments.append(item)

            time.sleep(1)

        return assessments


def save_catalog(
    data: List[Dict],
    output_path: str = "data/catalog.json"
):

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"Saved {len(data)} assessments")