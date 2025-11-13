import unittest
from arabseed_scraper import ArabSeedScraper

class TestArabSeedScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = ArabSeedScraper()

    def test_get_latest_content(self):
        latest_content = self.scraper.get_latest_content()
        self.assertIsInstance(latest_content, list)
        if latest_content:
            self.assertIsInstance(latest_content[0], dict)
            self.assertIn('title', latest_content[0])
            self.assertIn('url', latest_content[0])

    def test_search_content(self):
        # This test requires a search query that is likely to return results.
        # Using a generic query like "فيلم" (movie)
        search_results = self.scraper.search_content("فيلم")
        self.assertIsInstance(search_results, list)
        if search_results:
            self.assertIsInstance(search_results[0], dict)
            self.assertIn('title', search_results[0])
            self.assertIn('url', search_results[0])

    def test_get_download_links(self):
        # To test this, we need a valid URL from the site.
        # I'll first get the latest content and then use one of the URLs.
        latest_content = self.scraper.get_latest_content()
        if latest_content:
            test_url = latest_content[0]['url']
            download_links = self.scraper.get_download_links(test_url)
            self.assertIsInstance(download_links, list)
            if download_links:
                self.assertIsInstance(download_links[0], dict)
                self.assertIn('quality', download_links[0])
                self.assertIn('server', download_links[0])
                self.assertIn('link', download_links[0])
        else:
            self.skipTest("Could not retrieve latest content to test download links.")

if __name__ == '__main__':
    unittest.main()
