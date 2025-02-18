import os
import csv
from datetime import datetime

from itemadapter import ItemAdapter
from scrapy import signals
from scrapy.signalmanager import dispatcher
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base, Conference
from .utils import send_email, scp_send_csv

class ParserConferencePipeline:

    def __init__(self):
        self.items = []
        self.new = []
        self.current_date = datetime.now().strftime('%Y_%m_%d')
        os.makedirs('result', exist_ok=True)
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)
        self.today_conf = self.session.query(Conference).filter(
            Conference.date==datetime.now().date())

    def open_spider(self,spider):
        pass

    def process_item(self, item, spider):
        self.items.append(item)
        conference = Conference(
            id_conf = item['id'],
            date = datetime.strptime(item['date'], '%d.%m.%Y').date(),
            start = datetime.strptime(item['start_time'], '%H:%M').time(),
            end = datetime.strptime(item['end_time'], '%H:%M').time(),
            rooms = ', '.join(item['room']),
            comment = (item.get('comment') or item.get('after_call') or None),
            organizer = item.get('organizer'),
            manager = item.get('manager'),
        )
        if not self.session.query(Conference).filter(
            Conference.id_conf==item['id']).first():
            self.session.add(conference)
            self.session.commit()
            attachment = item.copy()
            attachment.pop('id')
            self.new.append(attachment)
        return item

    def close_spider(self, spider):
        sorted_items = sorted(self.items, key=lambda x: x['start_time'])
        fieldnames = ['id', 'date', 'start_time', 'end_time',
                      'room', 'comment', 'organizer', 'manager', 'after_call']
        file = 'result/conf_{date}.csv'.format(date=self.current_date)

        with open(file, mode='w', encoding='UTF-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_items)
        self.session.close()

        if self.new:
            self.new = sorted(self.new, key=lambda x: x['start_time'])
            send_email(self.new, self.today_conf)

        # scp_send_csv(file)
