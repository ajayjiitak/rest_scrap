# user/spiders/mericari_spider.py

import random
import scrapy
from lxml import html
from user.models import Product  # Ensure your Product model is correctly imported

class MericariSpider(scrapy.Spider):
    name = 'mericari_website_crawler'

    def __init__(self, identifier, url=None, query=None, platform=None, product_count=3, translation_flag=False,
                 type=None, model=None, black_list_sellers=None, black_list_words=None, is_last_scrapping=False):
        self.url = url
        self.query = query
        self.product_count = 1
        self.max_product_count = product_count
        self.translation_flag = translation_flag
        self.base_url = 'https://www.mercari.com'
        self.type = type
        self.identifier = identifier
        self.black_list_sellers = black_list_sellers or []
        self.black_list_words = black_list_words or []
        self.is_last_scrapping = is_last_scrapping
        self.model = model
        self.headers = {
            'Host': 'www.mercari.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.mercari.com/jp/',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
        }

    def start_requests(self):
        if self.url and self.type == 'search':
            yield scrapy.Request(url=self.url, callback=self.parse_product_links, headers=self.headers)
        else:
            yield scrapy.Request(url=self.url, callback=self.parse_product, headers=self.headers)

    def parse_product_links(self, response):
        if response.status == 200:
            doc = html.fromstring(response.body)
            products = doc.xpath("//section[@class='items-box']")

            random.shuffle(products)
            for product in products:
                if self.product_count > self.max_product_count:
                    break
                product_link = product.xpath("./a/@href")[0]
                product_link = self.base_url + product_link
                product_name = product.xpath(".//h3[@class='items-box-name font-2']/text()")[0].strip()
                sold_out_flag = product.xpath(".//div[@class='item-sold-out-badge']")
                if self.check_substring(self.black_list_words, product_name) or sold_out_flag:
                    continue
                price = product.xpath(".//div[@class='items-box-price font-5']/text()")[0].strip()
                photo = product.xpath(".//img/@data-src")[0]

                # Call function to save to database
                self.save_to_db(product_name, None, price, None, None, None, None, [photo], product_link)

                self.product_count += 1

            next_page_link = doc.xpath("//li[@class='pager-next visible-pc']/ul/li[@class='pager-cell']/a/@href")
            if next_page_link:
                next_page_link = self.base_url + next_page_link[0]
                if self.product_count <= self.max_product_count:
                    yield scrapy.Request(url=next_page_link, callback=self.parse_product_links, headers=self.headers)

    def parse_product(self, response):
        if response.status == 200:
            doc = html.fromstring(response.body)
            product_title = doc.xpath("//h1[@class='item-name']/text()")[0].strip()
            description = doc.xpath("//div[@class='item-description f14']/text()")
            description = description[0].strip() if description else None
            price = doc.xpath("//span[@class='item-price bold']/text()")[0].strip()
            brand = doc.xpath("//th[text()='ブランド']/following-sibling::td/text()")
            brand = brand[0].strip() if brand else None
            category = doc.xpath("//th[text()='カテゴリー']/following-sibling::td/text()")
            category = category[0].strip() if category else None
            condition = doc.xpath("//th[text()='商品の状態']/following-sibling::td/text()")
            condition = condition[0].strip() if condition else None
            seller = doc.xpath("//th[text()='出品者']/following-sibling::td/text()")
            seller = seller[0].strip() if seller else None
            photos = doc.xpath("//span[@class='luminous-gallery']/@data-src")
            photos = [photo.strip() for photo in photos]  # Clean photo URLs
            product_url = response.url  # Current product URL

            # Save to PostgreSQL using Django ORM
            self.save_to_db(product_title, description, price, brand, category, condition, seller, photos, product_url)

    def save_to_db(self, product_title, description, price, brand, category, condition, seller, photos, product_url):
        try:
            # Create a new Product instance and save it to the database
            product = Product(
                product_title=product_title,
                price=price,
                photos=photos,
                product_url=product_url,
                product_name=product_title,  # Assuming product_name is the same as product_title
                description=description,
                brand=brand,
                category=category,
                condition=condition,
                seller=seller,
            )
            product.save()
            self.logger.info(f'Successfully saved: {product_title}')
        except Exception as e:
            self.logger.error(f'Error saving product: {product_title}, {str(e)}')

    def check_substring(self, black_list_words, product_name):
        for word in black_list_words:
            if word in product_name:
                return True
        return False














# -*- coding: utf-8 -*-
# import random
# import scrapy
# from lxml import html
# from user.models import Product  # Make sure to import your Product model

# class MericariSpider(scrapy.Spider):
#     name = 'mericari_website_crawler'

#     def __init__(self, identifier, url=None, query=None, platform=None, product_count=3, translation_flag=False,
#                  type=None, model=None, black_list_sellers=[], black_list_words=[], is_last_scrapping=False):
#         self.url = url
#         self.query = query
#         self.product_count = 1
#         self.max_product_count = product_count
#         self.translation_flag = translation_flag
#         self.base_url = 'https://www.mercari.com'
#         self.type = type
#         self.identifier = identifier
#         self.black_list_sellers = black_list_sellers
#         self.black_list_words = black_list_words
#         self.is_last_scrapping = is_last_scrapping
#         self.model = model
#         self.headers = {
#             'Host': 'www.mercari.com',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.5',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Referer': 'https://www.mercari.com/jp/',
#             'Upgrade-Insecure-Requests': '1',
#             'Connection': 'keep-alive',
#             'Cache-Control': 'max-age=0',
#             'TE': 'Trailers',
#         }

#     def start_requests(self):
#         if self.url and self.type == 'search':
#             yield scrapy.Request(url=self.url, callback=self.parse_product_links, headers=self.headers)
#         else:
#             yield scrapy.Request(url=self.url, callback=self.parse_product, headers=self.headers)

#     def parse_product_links(self, response):
#         if response.status == 200:
#             doc = html.fromstring(response.body)
#             products = doc.xpath("//section[@class='items-box']")

#             random.shuffle(products)
#             for product in products:
#                 if self.product_count > self.max_product_count:
#                     break
#                 product_link = product.xpath("./a/@href")[0]
#                 product_link = self.base_url + product_link
#                 product_name = product.xpath(".//h3[@class='items-box-name font-2']/text()")[0].strip()
#                 sold_out_flag = product.xpath(".//div[@class='item-sold-out-badge']")
#                 if self.check_substring(self.black_list_words, product_name) or sold_out_flag:
#                     continue
#                 price = product.xpath(".//div[@class='items-box-price font-5']/text()")[0].strip()
#                 photo = product.xpath(".//img/@data-src")[0]
                
#                 # Call function to save to database
#                 self.save_to_db(product_name, price, photo, product_link)

#                 self.product_count += 1

#             next_page_link = doc.xpath("//li[@class='pager-next visible-pc']/ul/li[@class='pager-cell']/a/@href")
#             if next_page_link:
#                 next_page_link = self.base_url + next_page_link[0]
#                 if self.product_count <= self.max_product_count:
#                     yield scrapy.Request(url=next_page_link, callback=self.parse_product_links, headers=self.headers)

#     def parse_product(self, response):
#         if response.status == 200:
#             doc = html.fromstring(response.body)
#             product_title = doc.xpath("//h1[@class='item-name']/text()")[0].strip()
#             description = doc.xpath("//div[@class='item-description f14']/text()")[0].strip()
#             price = doc.xpath("//span[@class='item-price bold']/text()")[0].strip()
#             brand = doc.xpath("//th[text()='ブランド']/following-sibling::td/text()")
#             brand = brand[0].strip() if brand else None
#             category = doc.xpath("//th[text()='カテゴリー']/following-sibling::td/text()")
#             category = category[0].strip() if category else None
#             condition = doc.xpath("//th[text()='商品の状態']/following-sibling::td/text()")
#             condition = condition[0].strip() if condition else None
#             seller = doc.xpath("//th[text()='出品者']/following-sibling::td/text()")
#             seller = seller[0].strip() if seller else None
#             photos = doc.xpath("//span[@class='luminous-gallery']/@data-src")
#             photos = [photo.strip() for photo in photos]  # Clean photo URLs
#             product_url = response.url  # Current product URL

#             # Save to PostgreSQL using Django ORM
#             self.save_to_db(product_title, description, price, brand, category, condition, seller, photos, product_url)

#     def save_to_db(self, product_title, description, price, brand, category, condition, seller, photos, product_url):
#         try:
#             # Create a new Product instance and save it to the database
#             product = Product(
#                 product_title=product_title,
#                 price=price,
#                 photos=photos,
#                 product_url=product_url,
#                 product_name=product_title,  # Assuming product_name is the same as product_title
#                 description=description,
#                 brand=brand,
#                 category=category,
#                 condition=condition,
#                 seller=seller,
#             )
#             product.save()
#             self.logger.info(f'Successfully saved: {product_title}')
#         except Exception as e:
#             self.logger.error(f'Error saving product: {product_title}, {str(e)}')

#     def check_substring(self, black_list_words, product_name):
#         for word in black_list_words:
#             if word in product_name:
#                 return True
#         return False
















# import random
# import scrapy
# from lxml import html
# # from ..helpers.data_helper import get_text, get_first_element, get_last_element, clean_text, check_substring

# class MericariSpider(scrapy.Spider):
#     name = 'mericari_website_crawler'
    
#     def __init__(self, url, scrape_type='simple', **kwargs):
#         super().__init__(**kwargs)
#         self.url = url
#         self.scrape_type = scrape_type
#         self.base_url = 'https://www.mercari.com'
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
#         }

#     def start_requests(self):
#         yield scrapy.Request(url=self.url, callback=self.parse_product_links if self.scrape_type == 'simple' else self.parse_product, headers=self.headers)

#     def parse_product_links(self, response):
#         item = {}
#         if response.status == 200:
#             doc = html.fromstring(response.body)
#             products = doc.xpath("//section[@class='items-box']")
#             random.shuffle(products)
#             for product in products:
#                 item['product_title'] = get_text(get_first_element(product.xpath(".//h3[@class='items-box-name font-2']")))
#                 item['price'] = get_text(get_first_element(product.xpath(".//div[@class='items-box-price font-5']")))
#                 item['photos'] = get_first_element(product.xpath(".//img/@data-src"))
#                 item['url'] = self.base_url + get_first_element(product.xpath("./a/@href"))
#                 break  # Return only one item for simple scrape
#         return item

#     def parse_product(self, response):
#         item = {}
#         if response.status == 200:
#             doc = html.fromstring(response.body)
#             item["product_name"] = get_text(get_first_element(doc.xpath("//h1[@class='item-name']")))
#             item["description"] = get_text(get_first_element(doc.xpath("//div[@class='item-description f14']")))
#             item["price"] = get_text(get_first_element(doc.xpath("//span[@class='item-price bold']")))
#             item["photos"] = doc.xpath("//span[@class='luminous-gallery']/@data-src")
#             item["url"] = response.url
#             item["brand"] = clean_text(get_last_element(doc.xpath("//table[@class='item-detail-table']//a/div/text()")))
#             item["category"] = clean_text(get_last_element(doc.xpath("//table[@class='item-detail-table']//a/div/text()")))
#             item["condition"] = clean_text(get_last_element(doc.xpath("//table[@class='item-detail-table']//td/text()")))
#             item["seller"] = clean_text(get_first_element(doc.xpath("//table[@class='item-detail-table']//a/text()")))
#         return item