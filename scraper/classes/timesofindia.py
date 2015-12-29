"""
Class to extract daily summary from TimesOfIndia website
"""
from base import *

class TimesOfIndia (BaseScraper):
    def extractSummaryFromUrl(self):
        response = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(response.read(), "html.parser")

        chunks = soup.find('div', class_="top-story")

        html = 'Times of India:'
        html += '<ul>'

        skip = 0 # skip second link in ToI top stories because it is an icon related to first link
        for a in chunks.find_all('a', {'title': True, 'href': True}):
            skip += 1
            if skip == 2:
                continue
            html += '<li>'
            html += a.attrs['title']
            link = a.attrs['href']
            # some links in ToI begin with http:// while some are relative
            if link.startswith('/'):
                link = self.url + link
            html += '&nbsp;<a href="' + link + '">Read more</a>'
            html += '</li>'
        html += '</ul>'

        return html