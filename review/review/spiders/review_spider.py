# encoding: utf-8

from scrapy.spiders import Spider
from scrapy.http import Request
from ..items import ReviewItem
import bs4
from bs4 import BeautifulSoup
from common import headers, cookie, ERROR, loggerInfo
import math


class ReviewSpider(Spider):
    name = "review"
    first_url = 'https://www.glassdoor.com/Reviews/The-Judge-Group-Reviews-E6449.htm?filter.defaultEmploymentStatuses=false&filter.defaultLocation=false'
    second_url = 'https://www.glassdoor.com/Reviews/Compuware-Reviews-E35473.htm?filter.defaultEmploymentStatuses=false&filter.defaultLocation=false'
    url_pattern = '{PREFIX}{PAGE}.htm?filter.defaultEmploymentStatuses=false&filter.defaultLocation=false'

    def __init__(self):
        pass

    def start_requests(self):
        urls = [
            self.first_url,
            self.second_url
        ]
        for url in urls:
            yield Request(url=url, headers=headers, cookies=cookie, callback=self.parse)

    def parse(self, response):
        response_body = response.body
        soup = BeautifulSoup(response_body, "html.parser")
        review_count_div = soup.find('div', class_='padTopSm margRtSm margBot minor')

        review_count = 0
        if review_count_div is None:
            loggerInfo('ERROR review_count_div is None!!!')
        else:
            try:
                review_count_str = review_count_div.text.strip()
                count_str = review_count_str.split('reviews')[0].replace(',', '')
                review_count = int(count_str)
                loggerInfo('review_count: %s' % review_count)
            except Exception as err:
                loggerInfo('ERROR get review count err %s, %s' % (review_count_div.text, err.message))

        url_prefix = response.url.split('?')[0].split('.htm')[0]
        review_page_count = int(math.ceil(review_count / 10.0))
        if review_page_count > 0:
            for page_index in range(1, review_page_count + 1):
                loggerInfo('PAGE_INDEX: %s' % page_index)
                if page_index == 1:
                    url = self.url_pattern.format(PREFIX=url_prefix, PAGE='')
                else:
                    url = self.url_pattern.format(PREFIX=url_prefix, PAGE='_P' + str(page_index))
                yield Request(url=url, headers=headers, cookies=cookie, callback=self.parse_review_response)

    def parse_review_response(self, response):

        response_body = response.body
        soup = BeautifulSoup(response_body, "html.parser")

        corp_name = self.parse_corp_name(soup)

        review_body_list = soup.find_all("li", class_=" empReview cf ")

        loggerInfo('TEST::review_body_list: %s' % len(review_body_list))
        employ_review_list = []
        i = 1
        for review_body in review_body_list:
            loggerInfo('%s' % i)
            i = i + 1
            review = self.parse_review_body(corp_name, review_body)
            employ_review_list.append(review)
        return employ_review_list

    def parse_corp_name(self, soup):
        corp_name_div = soup.find('div', class_='header cell info')
        if corp_name_div is None:
            loggerInfo('ERROR-ERROR parse corp_name err !!!!')
            return ERROR
        else:
            return corp_name_div.text.strip()

    def parse_review_body(self, corp_name, employ_review):
        id_str = ERROR
        summary = ''
        star_total_str = ''
        star_work_life_balance = ''
        star_culture_values = ''
        star_career_opportunities = ''
        star_comp_benefits = ''
        star_sensior_management = ''
        pros_str = ''
        cons_str = ''
        advice_str = ''

        try:
            id_str = employ_review.get('id', '')

            in_soup = BeautifulSoup(str(employ_review), "html.parser")

            top_body = in_soup.find('div', class_=' tbl fill reviewTop')
            top_soup = BeautifulSoup(str(top_body), "html.parser")
            summary = self.get_review_summary(top_soup)

            star_body = top_soup.find('div', class_='gdStarsWrapper cell top')
            star_soup = BeautifulSoup(str(star_body), "html.parser")

            star_total_str = self.get_review_total_star(star_soup)

            (star_work_life_balance, star_culture_values, star_career_opportunities, star_comp_benefits,
             star_sensior_management) = self.get_review_sub_star(star_soup)

            fill_body = in_soup.find('div', class_='tbl fill')
            fill_soup = BeautifulSoup(str(fill_body), "html.parser")

            description_body = fill_soup.find('div', class_='description ')
            description_soup = BeautifulSoup(str(description_body), 'html.parser')

            pros_str = self.get_review_pros(description_soup)
            cons_str = self.get_review_cons(description_soup)

            advice_str = self.get_review_str(description_soup)
        except Exception as err:
            loggerInfo('ERROR-ERROR:parse url %s fail, %s' % (employ_review, err.message))

        data = ReviewItem()
        data['name'] = corp_name
        data['id'] = id_str
        data['summary'] = summary
        data['star_total'] = star_total_str
        data['star_work_life_balance'] = star_work_life_balance
        data['star_culture_values'] = star_culture_values
        data['star_career_opportunities'] = star_career_opportunities
        data['star_comp_benefits'] = star_comp_benefits
        data['star_sensior_management'] = star_sensior_management
        data['pros'] = pros_str
        data['cons'] = cons_str
        data['advice'] = advice_str
        return data

    def get_review_summary(self, top_soup):
        summary_span = top_soup.find('span', class_='summary')
        if summary_span is None:
            return ''
        else:
            return summary_span.string.replace('"', '')

    def get_review_total_star(self, star_soup):
        star_total_span = star_soup.find('span', class_='rating')
        if star_total_span is None:
            return ''
        else:
            return star_total_span.span.get('title', '')

    def get_review_sub_star(self, star_soup):
        star_work_life_balance = ''
        star_culture_values = ''
        star_career_opportunities = ''
        star_comp_benefits = ''
        star_sensior_management = ''

        star_sub_body = star_soup.find('div', class_='subRatings module')
        if star_sub_body is None:
            loggerInfo('ERROR:subRatings module is None!!!')
        else:
            star_sub_soup = BeautifulSoup(str(star_sub_body), "html.parser")

            star_sub_li_list = star_sub_soup.find('ul', class_='undecorated')
            if star_sub_li_list is None:
                loggerInfo('ERROR:star_sub_li_list is None!!! url-undecorated')
            else:
                li_work_life_balance = filter(lambda child: child.div.string.strip() == 'Work/Life Balance',
                                              star_sub_li_list.children)
                if len(li_work_life_balance) > 0:
                    star_work_life_balance = str(li_work_life_balance[0].span.get('title', '')).strip()
                else:
                    star_work_life_balance = ''
                li_culture_values = filter(lambda child: child.div.string.strip() == 'Culture & Values',
                                           star_sub_li_list.children)
                if len(li_culture_values) > 0:
                    star_culture_values = str(li_culture_values[0].span.get('title', '')).strip()
                else:
                    star_culture_values = ''
                li_career_opportunities = filter(lambda child: child.div.string.strip() == 'Career Opportunities',
                                                 star_sub_li_list.children)
                if len(li_career_opportunities) > 0:
                    star_career_opportunities = str(li_career_opportunities[0].span.get('title', '')).strip()
                else:
                    star_career_opportunities = ''
                li_comp_benefits = filter(lambda child: child.div.string.strip() == 'Comp & Benefits',
                                          star_sub_li_list.children)
                if len(li_comp_benefits) > 0:
                    star_comp_benefits = str(li_comp_benefits[0].span.get('title', '')).strip()
                else:
                    star_comp_benefits = ''
                li_sensior_management = filter(lambda child: child.div.string.strip() == 'Senior Management',
                                               star_sub_li_list.children)
                if len(li_sensior_management) > 0:
                    star_sensior_management = str(li_sensior_management[0].span.get('title', '')).strip()
                else:
                    star_sensior_management = ''
        return (star_work_life_balance, star_culture_values, star_career_opportunities, star_comp_benefits,
                star_sensior_management)

    def get_review_pros(self, description_soup):
        pros_list_p = description_soup.find('p', class_=' pros mainText truncateThis wrapToggleStr')
        if pros_list_p is None:
            loggerInfo('ERROR:pros is None!!!')
            return ''
        else:
            pros_list = pros_list_p.contents
            pros_list = filter(lambda x: isinstance(x, bs4.element.NavigableString), pros_list)
            pros_str_list = []
            for pros_item in pros_list:
                str_tmp = pros_item.string.strip()
                if str_tmp.startswith('-'):
                    pros_str_list.append(str_tmp[1:].strip())
                else:
                    pros_str_list.append(str_tmp.strip())
            return '; '.join(pros_str_list)

    def get_review_cons(self, description_soup):
        cons_list_p = description_soup.find('p', class_=' cons mainText truncateThis wrapToggleStr')
        if cons_list_p is None:
            return ''
        else:
            cons_list = cons_list_p.contents
            cons_list = filter(lambda x: isinstance(x, bs4.element.NavigableString), cons_list)
            cons_str_list = []
            for cons_item in cons_list:
                str_tmp = cons_item.string.strip()
                if str_tmp.startswith('-'):
                    cons_str_list.append(str_tmp[1:].strip())
                else:
                    cons_str_list.append(str_tmp.strip())
            return '; '.join(cons_str_list)

    def get_review_str(self, description_soup):
        advice_list = description_soup.find('p', class_=' adviceMgmt mainText truncateThis wrapToggleStr')
        if advice_list is None:
            return ""
        else:
            advice_list = filter(lambda x: isinstance(x, bs4.element.NavigableString), advice_list)
            return '; '.join(advice_list)
