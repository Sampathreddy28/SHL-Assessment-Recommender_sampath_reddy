from app.catalog.scraper import (
    SHLCatalogScraper,
    save_catalog,
)


def main():

    scraper = SHLCatalogScraper()

    data = scraper.scrape()

    save_catalog(data)


if __name__ == "__main__":
    main()