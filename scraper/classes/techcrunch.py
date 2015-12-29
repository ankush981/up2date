"""
Class to extract daily summary from TechCrunch website
"""
from base import *

class TechCrunch (BaseScraper):
    def extractSummaryFromUrl(self):
        response = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(response.read(), "html.parser")
        
        chunks = soup.find_all('li', {"class": "river-block", "data-sharetitle": True, "data-permalink": True})
        html = 'TechCrunch:'
        html += '<ul>'
        for c in chunks:
            html += '<li>'
            html += c.attrs['data-sharetitle']
            html += '&nbsp;<a href="' + c.attrs['data-permalink'] + '">Read more</a>'
            html += '</li>'
        html += '</ul>'

        return html