import unittest
from plink import options, analyser

def create_default_analyser():
    o = options.Options()
    a = analyser.Analyser(options)
    return a

class TestAnalyser(unittest.TestCase):
    def test_retrieve_links_from_html(self):
        base_url = "https://www.jessica.im/"
        test_link = f"{base_url}/Blog"
        test_html = f'<a href="{test_link}"></a>'
        a = create_default_analyser()
        result = a.retrieve_links_from_html(test_html, base_url)
        result_contains_link = any(x == test_link for x in result)
        self.assertTrue(result_contains_link)

    def test_relative_retrieve_links_from_html(self):
        expected_link = "https://www.jessica.im/Blog"
        base_url = "https://www.jessica.im/"
        test_link = f"/Blog"
        test_html = f'<a href="{test_link}"></a>'
        a = create_default_analyser()
        result = a.retrieve_links_from_html(test_html, base_url)
        result_contains_link = any(x == expected_link for x in result)
        self.assertTrue(result_contains_link)

    def test_no_links_in_html(self):
        base_url = "https://www.jessica.im/"
        test_html = f'<p>no links here!</p>'
        a = create_default_analyser()
        result = a.retrieve_links_from_html(test_html, base_url)
        self.assertEqual(len(result), 0)
    
    def test_find_domain_from_url(self):
        test_url = "https://jessica.im/Blog"
        expected_domain = "jessica.im"
        a = create_default_analyser()
        result = a.find_domain_from_url(test_url)
        self.assertEqual(result, expected_domain)

    def test_www_find_domain_from_url(self):
        test_url = "https://www.jessica.im/Blog"
        expected_domain = "jessica.im"
        a = create_default_analyser()
        result = a.find_domain_from_url(test_url)
        self.assertEqual(result, expected_domain)

    def test_compare_same_urls(self):
        test_url1 = "https://jessica.im/Blog"
        test_url2 = "https://jessica.im/Blog"
        a = create_default_analyser()
        result = a.compare_domains_from_urls(test_url1, test_url2)
        self.assertTrue(result)

    def test_compare_same_domain_urls(self):
        test_url1 = "https://jessica.im/Blog"
        test_url2 = "https://jessica.im/Contact"
        a = create_default_analyser()
        result = a.compare_domains_from_urls(test_url1, test_url2)
        self.assertTrue(result)

    def test_compare_same_urls_case_insensitive(self):
        test_url1 = "httPs://jEssica.im/bloG"
        test_url2 = "https://jessica.im/Blog"
        a = create_default_analyser()
        result = a.compare_domains_from_urls(test_url1, test_url2)
        self.assertTrue(result)
    
    def test_compare_different_urls(self):
        test_url1 = "https://jessica.im/Blog"
        test_url2 = "https://github.com/Jessicaward"
        a = create_default_analyser()
        result = a.compare_domains_from_urls(test_url1, test_url2)
        self.assertFalse(result)

    def test_compare_different_urls(self):
        test_url1 = "https://jessica.im/Blog"
        test_url2 = "https://github.com/Jessicaward"
        a = create_default_analyser()
        result = a.compare_domains_from_urls(test_url1, test_url2)
        self.assertFalse(result)

    def test_check_whitelisted_url(self):
        whitelisted_url = "https://jessica.im/"
        test_url = "https://jessica.im/Blog"
        o = options.Options(whitelist=[whitelisted_url])
        a = analyser.Analyser(o)
        result = a.check_whitelist(test_url)
        self.assertTrue(result)

    def test_check_non_whitelisted_url(self):
        whitelisted_url = "https://jessica.im/"
        test_url = "https://github.com/Jessicaward"
        o = options.Options(whitelist=[whitelisted_url])
        a = analyser.Analyser(o)
        result = a.check_whitelist(test_url)
        self.assertFalse(result)

    def test_check_blacklisted_url(self):
        blacklisted_url = "https://jessica.im/"
        test_url = "https://github.com/Jessicaward"
        o = options.Options(blacklist=[blacklisted_url])
        a = analyser.Analyser(o)
        result = a.check_blacklist(test_url)
        self.assertTrue(result)

    def test_check_blacklisted_url(self):
        blacklisted_url = "https://jessica.im/"
        test_url = "https://jessica.im/Blog"
        o = options.Options(blacklist=[blacklisted_url])
        a = analyser.Analyser(o)
        result = a.check_blacklist(test_url)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()