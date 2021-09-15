# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from maketabkhooneh import settings
import pymongo
from pymongo.errors import DuplicateKeyError


class MaketabkhoonehPipeline:
    def __init__(self):
        connection = pymongo.MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        try:
            self.collection.insert(dict(item))
        except DuplicateKeyError:
            print('duplicate caught...')
        except Exception as e:
            print(e)
        else:
            return "Course ADDED..."
