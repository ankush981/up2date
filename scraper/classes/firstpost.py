"""
Class to extract daily summary from Firstpost website
"""
from base import *

class Firstpost (BaseScraper):
    def extractSummaryFromUrl(self):
        response = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(response.read(), "html.parser")

        chunks = soup.find_all('a', class_='catStory-title')

        html = 'Firstpost:'
        html += '<ul>'
        for c in chunks:
            # print(c)
            html += '<li>'
            html += c['title']
            html += '&nbsp;<a href="' + c['href'] + '">Read more</a>'
            html += '</li>'
        html += '</ul>'

        return html