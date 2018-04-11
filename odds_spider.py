# to run type "scrapy runspider odds_spider.py" with -o for output options
# data retrieved from e.g. https://www.teamrankings.com/nfl-odds-week-9
# had to download entire webpage from browser because scraping via url didn't work

import scrapy
from dateutil import parser
import pytz as tz


short_teams = {
    'Arizona': 'ARI',
    'Atlanta': 'ATL',
    'Baltimore': 'BAL',
    'Buffalo': 'BUF',
    'Carolina': 'CAR',
    'Chicago': 'CHI',
    'Cincinnati': 'CIN',
    'Cleveland': 'CLE',
    'Dallas': 'DAL',
    'Denver': 'DEN',
    'Detroit': 'DET',
    'Green Bay': 'GB',
    'Houston': 'HOU',
    'Indianapolis': 'IND',
    'Jacksonville': 'JAX',
    'Kansas City': 'KC',
    'LA Chargers': 'LAC',
    'LA Rams': 'LAR',
    'Miami': 'MIA',
    'Minnesota': 'MIN',
    'New England': 'NE',
    'New Orleans': 'NO',
    'NY Giants': 'NYG',
    'NY Jets': 'NYJ',
    'Oakland': 'OAK',
    'Philadelphia': 'PHI',
    'Pittsburgh': 'PIT',
    'San Francisco': 'SF',
    'Seattle': 'SEA',
    'Tampa Bay': 'TB',
    'Tennessee': 'TEN',
    'Washington': 'WAS',
}

class OddsSpider(scrapy.Spider):
    name = "Odds"
    custom_settings = {
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    }
    start_urls = [
        f'file:///Users/holdren/Development/nfl-parser/pages/week{x}.html' for x in range(1,12)
    ]

    def parse(self, response):
        for day_div in response.selector.xpath('//body/div/div/div/main/div/div/div/div'):

            day = day_div.css('h2::text').extract_first()

            for table in day_div.css('table'):
                gametime = table.css('th.text-left::text').extract_first().strip()

                rows = table.css('tbody').css('tr')
                away_team = rows[0].css('a::text').extract_first()
                home_team = rows[1].css('a::text').extract_first()
                # The following td's seem like they're off by one, but using the 
                # pseudo-selector ::text skips the Team names, probably because they're links
                away_score = rows[0].css('td::text')[0].extract()
                home_score = rows[1].css('td::text')[0].extract()
                away_spread = rows[0].css('td::text')[1].extract()
                home_spread = rows[1].css('td::text')[1].extract()
                over_under = rows[0].css('td::text')[2].extract()
                away_ml = rows[0].css('td::text')[3].extract()
                home_ml = rows[1].css('td::text')[3].extract()

                timestring = f'{day} {gametime}'
                dt = parser.parse(timestring)
                ET = tz.timezone('US/Eastern')
                dt = ET.localize(dt)

                yield {
                    'gametime': dt.isoformat(),
                    'away': short_teams[away_team],
                    'home': short_teams[home_team],
                    'away_score': away_score,
                    'home_score': home_score,
                    'away_spread': away_spread,
                    'home_spread': home_spread,
                    'over_under': over_under,
                    'away_ml': away_ml,
                    'home_ml': home_ml
                }

        # userful if you want to go any more
        # # next_page = response.css('li.next a::attr("href")').extract_first()
        # if next_page is not None:
        # yield response.follow(next_page, self.parse)