# encoding: utf-8

from scrapy.item import Item, Field


class ReviewItem(Item):
    name = Field()
    id = Field()
    summary = Field()
    star_total = Field()
    star_work_life_balance = Field()
    star_culture_values = Field()
    star_career_opportunities = Field()
    star_comp_benefits = Field()
    star_sensior_management = Field()
    pros = Field()
    cons = Field()
    advice = Field()
