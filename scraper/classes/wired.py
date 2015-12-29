"""
Class to extract daily summary from Wired website
"""
from base import *

class Wired (BaseScraper):
    def extractSummaryFromUrl(self):
        response = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(response.read(), "html.parser")
        
        chunks = soup.find('ul', {"id": "most-pop-list"})
        html = 'Wired:'
        html += '<ul>'
        for c in chunks.find_all('li'):
            html += '<li>'
            html += c.find('h5').get_text()
            html += '&nbsp;<a href="' + c.find('a').attrs['href'] + '">Read more</a>'
            html += '</li>'
        html += '</ul>'

        return html