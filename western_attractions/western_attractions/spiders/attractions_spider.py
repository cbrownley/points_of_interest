import re
import scrapy

class WesternAttractionsSpider(scrapy.Spider):
    name = 'western_attractions'
    attractions_url = 'http://www.jurnii.com/rv/rv_guide/us_western_regions_attractions.php'
    start_urls = [attractions_url]

    def parse(self, response):
        # Extract names/titles of attractions
        h4s = response.css("h4::text").extract()
        h4s = [val.encode('ascii','ignore') for val in h4s]
        h4s = [re.sub("\s+", " ", val).strip() for val in h4s]
        h4s = [val for val in h4s if "Address" not in val and "Phone" not in val]
        h4s = filter(None, h4s)

        # Extract website URLs for attractions
        links = response.css('blockquote p a::attr(href)').extract()

        # Extract details associated with each attraction
        for idx, bq in enumerate(response.css("blockquote")):
            data = bq.css("p.smaller_par::text").extract()
            data = [val.encode('ascii','ignore') for val in data]
            data = [re.sub("\s+", " ", val).strip() for val in data]
            data = filter(None, data)
            data.append(links[idx])
            if len(data) == 5:
                address = data[0]
                phone = data[1].replace("Phone: ", "")
                cost = data[2]
                lat_lon = data[3]
                website = data[4]
                yield { "title": h4s[idx], "address": address, "phone": phone,
                        "cost": cost, "lat_lon": lat_lon, "website": website }
