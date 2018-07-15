import scrapy
from scrapy import signals
import json, codecs
from spiders.common import loggerInfo

class ReviewFilePipeline(object):

    # def open_spider(self, spider):
    #     self.file = open('items.jl', 'w')
    #
    # def close_spider(self, spider):
    #     self.file.close()

    def process_item(self, item, spider):
        try:
            fp = open(item['name'], 'a')
            line = json.dumps(dict(item)) + "\n"
            fp.write(line)
            fp.close()
        except Exception as err:
            loggerInfo('ERROR-ERROR write file %s err: %s' % (item['name'], err.message))

