from datetime import datetime
import re

import scrapy

from parser_conference.items import ParserConferenceItem

class ConferenceSpider(scrapy.Spider):
    name = "conference"
    current_time = datetime.now().strftime('%Y-%m-%d')
    url = f"""http://vcs.gazsvyaz.gazprom.ru/issues?c%5B%5D=due_date&c%5B%5D=cf_6&c%5B%5D=cf_7&c%5B%5D=subject&c%5B%5D=cf_5&c%5B%5D=cf_3&c%5B%5D=description&f%5B%5D=status_id&f%5B%5D=due_date&f%5B%5D=&group_by=&op%5Bdue_date%5D=%3D&op%5Bstatus_id%5D=o&per_page=50&set_filter=1&utf8=%E2%9C%93&v%5Bdue_date%5D%5B%5D={current_time}"""
    allowed_domains = ["vcs.gazsvyaz.gazprom.ru"]
    start_urls = [url]

    def parse(self, response):
        all_conf = response.css('div.autoscroll tbody tr')
        conf = {}
        for row in all_conf:
            if row.css('.issue::attr(id)').get():
                conf['id'] = row.css('a::text').get()
                conf['date'] = row.css('td.due_date::text').get()
                conf['start_time'] = row.css('td.cf_6::text').get()
                conf['end_time'] = row.css('td.cf_7::text').get()
                conf['organizer'] = row.css('td.cf_5::text').get()
                if re.search(r'^(?!.*[Фф]илиал).*?\s[Ии]нвест[»"]$', conf['organizer']):
                    conf['manager'] = row.css('td.cf_3::text').get()
                else:
                    conf['manager'] = None
            else:
                room = row.css('li::text').re(r'^(?!.*[Фф]илиал).*?\s[Ии]нвест[»"]\s*\(к.*')
                comment = row.css('strong:contains("По")::text').get()
                after_call = row.css('em::text').re_first(r'^.*?\s[Ии]нвест»\s*\([к3]*')
                if len(room) == 0:
                    conf = {}
                else:
                    conf['room'] = room
                    conf['comment'] = comment
                    conf['after_call'] = after_call
                    yield ParserConferenceItem(conf)
