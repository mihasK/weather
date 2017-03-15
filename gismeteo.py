import scrapy

class GismeteoSpider(scrapy.Spider):
    name = 'gismeteospider'



    def __init__(self, start_year=2000, end_year=2001, *args, **kwargs):
        super(GismeteoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            'https://www.gismeteo.ru/diary/4248/{year}/{month}/'.format(year=y, month=m)
            for y in range(int(start_year), int(end_year) + 1)
            for m in range(1,13)]

    def parse(self, response):

        # Validate table scheme

        headers = response.xpath('//*[@id="data_block"]/table/tr[1]/th')
        assert len(headers) == 3

        header_values = response.xpath('//*[@id="data_block"]/table/tr[2]/th/text()').extract()

        print(header_values)

        assert header_values == ['Температура',
                                 'Давление',
                                 'Облачность',
                                 'Явления',
                                 'Ветер',
                                 'Температура',
                                 'Давление',
                                 'Облачность',
                                 'Явления',
                                 'Ветер']

        y,m = response.url.split('/')[-3:-1]

        def extract_from_row(row, xpath):
            value = row.xpath(xpath).extract()
            try:
                return value[0]
            except IndexError:
                self.logging.error('Error extracting data from the row: %s' % value)

        for row in response.xpath('//*[@id="data_block"]/table/tbody/tr'):
            day_info = dict()
            assert len(row.xpath('td')) == 11

            day_info['source_url'] = response.url
            day_info['year'] = y
            day_info['month'] = m
            day_info['day'] = row.xpath('td[1]/text()').extract_first()
            day_info['temperature_day'] = row.xpath('td[2]/text()').extract_first()
            day_info['pressure_day'] = row.xpath('td[3]/text()').extract_first()
            day_info['temperature_evening'] = row.xpath('td[7]/text()').extract_first()
            day_info['pressure_evening'] = row.xpath('td[8]/text()').extract_first()

            yield day_info

        #for title in response.css('h2.entry-title'):
      #      yield {'title': title.css('a ::text').extract_first()}

      #  next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
    #    if next_page:
  #          yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
