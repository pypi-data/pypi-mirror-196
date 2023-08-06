import time
import requests
from plink import consts
from bs4 import BeautifulSoup
from termcolor import colored
from plink.result import Result
from urllib.parse import urljoin, urlparse

class Analyser():
    def __init__(self, options):
        self.options = options

    def retrieve_content_by_url(self, url):
        request = requests.get(url)
        content = request.text
        return content

    def retrieve_links_from_html(self, html, base_url):
        soup = BeautifulSoup(html, features="html.parser")
        link_tags = soup.find_all('a')
        links = [tag['href'] for tag in link_tags]
        absolute_links = [urljoin(base_url, link) for link in links]
        return absolute_links

    def analyse_url(self, url):
        try:
            start_time = time.time()
            content = self.retrieve_content_by_url(url)
            end_time = time.time()
            time_taken = end_time-start_time
            friendly_time_taken = "{:.4f}".format(time_taken)
            links = self.retrieve_links_from_html(content, url)
            if self.options.verbose:
                print(colored(f"[{friendly_time_taken}s] Success: " + url, "green"))
            return Result(links=links, status="Success", time_in_s=time_taken)
        except Exception as ex:
            if self.options.verbose:
                print(colored(str(ex), "red"))
                print(colored("Fail: " + url, "red"))
            return Result(status="Fail")
    
    def find_domain_from_url(self, url):
        domain = urlparse(url).netloc
        if domain[:4] == "www.":
            return domain[4:]
        return domain

    def compare_domains_from_urls(self, url1, url2):
        formatted_url1 = self.find_domain_from_url(url1)
        formatted_url2 = self.find_domain_from_url(url2)
        return formatted_url1.lower() == formatted_url2.lower()

    def check_whitelist(self, url):
        return any(self.compare_domains_from_urls(url, w) for w in self.options.whitelist)

    def check_blacklist(self, url):
        return not any(self.compare_domains_from_urls(url, w) for w in self.options.blacklist)

    def check_url_is_allowed(self, url):
        use_whitelist = self.options.whitelist is not None
        use_blacklist = self.options.blacklist is not None

        if (use_whitelist and self.check_whitelist(url)) \
        or (use_blacklist and self.check_blacklist(url)) \
        or (not use_blacklist and not use_whitelist):
            parsed = urlparse(url)
            schemes = consts.ALLOWED_SCHEMES_INSECURE if self.options.allow_insecure else consts.ALLOWED_SCHEMES
            return any(s == parsed.scheme.lower() for s in schemes)

        # URL is either in blacklist, or not in whitelist
        return False

    def print_summary(self, urls_analysed):
        number_of_successful_urls = sum(1 for url in urls_analysed if url[1].status == "Success")
        number_of_failed_urls = len(urls_analysed) - number_of_successful_urls
        print(colored(f"{number_of_successful_urls} successful URLs", "green"))
        print(colored(f"{number_of_failed_urls} failed URLs", "red"))

    def analyse(self):
        # Define default lists to analyse
        analysed_urls = []
        urls_to_analyse = [self.options.start_url]

        # Each "step" is the next level of depth
        for depth in range(0, self.options.depth):
            urls_in_step = urls_to_analyse[:] # Copy list without reference

            # Each "step" contains a list of urls to analyse
            # This list will be empty by the time the step ends
            for url in urls_in_step:
                if url not in [url_result[0] for url_result in analysed_urls]:
                    # Check the blacklist doesn't contain the url OR the whitelist does contain it
                    if (self.check_url_is_allowed(url)):
                        result = self.analyse_url(url)
                        analysed_urls.append((url, result))
                        urls_to_analyse.remove(url)

                        # The URL has been analysed, remove it from this step and add it to the analysed list
                        for url_to_analyse in result.links:
                            if url_to_analyse not in urls_to_analyse:
                                urls_to_analyse.append(url_to_analyse)
        
        self.print_summary(analysed_urls)