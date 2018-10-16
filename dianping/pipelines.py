# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DianpingPipeline(object):
    def __init__(self):
        # self.file = open('teacher.json', 'wb')
        self.file = open('dianping.json', 'wb')

    def process_item(self, item, spider):
        # content = json.dumps(dict(item)) + "\n"
        print("*****************")
        content = dict(item)
        content = str(content)
        content = content.encode('utf-8')
        # print(content)
        # print(type(content))
        self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()
