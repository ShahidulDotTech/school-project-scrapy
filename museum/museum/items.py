from stringprep import map_table_b2
import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags 

def remove_symbol(value):
    return value.replace('$', '').replace(',', '').strip()

def remove_whitespaces(value):
    return value.strip()

def email_f(r):
    return r.replace('mailto:', '').strip()

def sup_f(r):
    return r.replace('Meet ', '').strip()

class MuseumItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor = MapCompose(remove_tags, remove_whitespaces), output_processor = TakeFirst())
    project_description = scrapy.Field(input_processor = MapCompose(remove_tags, remove_whitespaces), output_processor = TakeFirst())
    primary_supervisor = scrapy.Field(input_processor = MapCompose(remove_tags, sup_f), output_processor = TakeFirst())
    supervisor_email = scrapy.Field(input_processor = MapCompose(email_f))
    project_link = scrapy.Field()
    dead_line = scrapy.Field(input_processor = MapCompose(remove_tags, remove_whitespaces), output_processor = TakeFirst())

