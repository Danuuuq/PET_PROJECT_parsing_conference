import os
import csv

from itemadapter import ItemAdapter
from scrapy import signals
from scrapy.signalmanager import dispatcher

from .utils import send_email, scp_send_csv

class ParserConferencePipeline:

    def __init__(self):
        self.items = []
        os.makedirs('result', exist_ok=True)

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        sorted_items = sorted(self.items, key=lambda x: x['start_time'])
        fieldnames = ['id', 'date', 'start_time', 'end_time',
                      'room', 'comment', 'organizer', 'manager', 'after_call']
        file = 'result/conf.csv'

        with open(file, mode='w', encoding='UTF-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_items)
        
        # send_email(sorted_items)

        # scp_send_csv(file)
