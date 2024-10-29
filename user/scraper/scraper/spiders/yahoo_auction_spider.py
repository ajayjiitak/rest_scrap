

import scrapy
from lxml import html
from ..items import ProductItem  # Ensure you have a ProductItem defined for your scraped data

class YahooAuctionSpider(scrapy.Spider):
    name = 'yahoo_website_crawler'

    def __init__(self, identifier, url=None, query=None, platform=None, product_count=1):
        self.url = url
        self.product_count = 1
        self.max_product_count = product_count
        self.base_url = 'https://auctions.yahoo.co.jp'
        self.identifier = identifier
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

    def start_requests(self):
        if self.url:
            yield scrapy.Request(url=self.url, callback=self.parse_product_links, headers=self.headers)

    def parse_product_links(self, response):
        if response.status == 200:
            doc = html.fromstring(response.body)
            products = doc.xpath("//ul[@class='Products__items']/li") or doc.xpath("//div[@class='Products__list']/ul/li")

            for product in products:
                if self.product_count > self.max_product_count:
                    break

                product_link = product.xpath(".//a/@href")[0]
                product_name = product.xpath(".//h3[@class='Product__title']/a/text()")[0]
                price = product.xpath(".//span[@class='Price__value']/text()")[0]
                photo = product.xpath(".//img/@src")[0]

                yield {
                    'product_title': product_name,
                    'price': price,
                    'photos': photo,
                    'product_url': product_link,
                }

                self.product_count += 1

            next_page_link = doc.xpath("//li[@class='Pager__list Pager__list--next']/a/@href")
            if next_page_link:
                yield scrapy.Request(url=next_page_link[0], callback=self.parse_product_links, headers=self.headers)

    def parse_product(self, response):
        item = ProductItem()
        if response.status == 200:
            doc = html.fromstring(response.body)

            product_name = doc.xpath("//h1[@class='sc-f3a947cb-0 fUNTYt ItemTitle__Component']/span/text()")[0]
            description = doc.xpath("//div[@class='item-description']/text()")[0]
            price = doc.xpath("//dd[@class='Price__value Price__value--buyNow']/text()")[0]
            brand = doc.xpath("//th[text()='ブランド']/following-sibling::td/text()")[0]
            category = doc.xpath("//th[text()='カテゴリ']/following-sibling::td/text()")[0]
            condition = doc.xpath("//th[text()='状態']/following-sibling::td/text()")[0]
            photos = doc.xpath("//div[@class='slick-slide slick-active slick-current']/div/button/img/@src")

            yield {
                'product_name': product_name,
                'description': description,
                'price': price,
                'brand': brand,
                'category': category,
                'condition': condition,
                'photos': photos,
                'product_url': response.url,
            }













# import scrapy
# from lxml import html
# from ..items import ProductItem, BasicProductItem
# from ..helpers.data_helper import get_text, get_first_element, datapush
# from apps.eBay_operations.models.ui_handler import UIChangesDetailedScraping, UIChangesimpleScraping

# class YahooSpider(scrapy.Spider):
#     name = 'yahoo_website_crawler'

#     def __init__(self, identifier, url=None, product_count=1, model=None, black_list_sellers=[], black_list_words=[]):
#         self.url = url
#         self.product_count = 1
#         self.max_product_count = product_count
#         self.identifier = identifier
#         self.black_list_sellers = black_list_sellers
#         self.model = model
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         }

#     def start_requests(self):
#         yield scrapy.Request(url=self.url, callback=self.parse_product_links, headers=self.headers)

#     def parse_product_links(self, response):
#         if response.status == 200:
#             doc = html.fromstring(response.body)
#             products = doc.xpath("//ul[@class='Products__items']/li")
#             if not products:
#                 products = doc.xpath("//div[@class='Products__list']/ul/li")

#             for product in products:
#                 if self.product_count > self.max_product_count:
#                     break
                
#                 product_link = get_first_element(product.xpath("./div/a/@href"))
#                 product_name = get_text(get_first_element(product.xpath(".//h3[@class='Product__title']/a/text()")))
#                 if product_name in self.black_list_words:
#                     continue
#                 price = get_text(get_first_element(product.xpath(".//dd[@class='Price__value']/text()")))
#                 photo = get_first_element(product.xpath(".//img/@src"))
                
#                 item = BasicProductItem()
#                 item.update({
#                     'product_name': product_name,
#                     'price': price,
#                     'photos': photo,
#                     'url': product_link,
#                 })

#                 # Go to the product detail page for additional information
#                 yield scrapy.Request(url=product_link, callback=self.parse_product_detail, meta={'item': item}, headers=self.headers)

#             # Check for next page (if required)
#             next_page_link = get_first_element(doc.xpath("//li[@class='Pager__list Pager__list--next']/a/@href"))
#             if self.product_count < self.max_product_count and next_page_link:
#                 yield scrapy.Request(url=next_page_link, callback=self.parse_product_links, headers=self.headers)

#     def parse_product_detail(self, response):
#         item = response.meta['item']
#         doc = html.fromstring(response.body)

#         # Extract additional details
#         description = get_text(get_first_element(doc.xpath("//div[@class='ProductDescription']/text()")))
#         brand = get_text(get_first_element(doc.xpath("//th[text()='ブランド']/following-sibling::td/text()")))
#         category = get_text(get_first_element(doc.xpath("//th[text()='カテゴリ']/following-sibling::td/text()")))
#         condition = get_text(get_first_element(doc.xpath("//th[text()='状態']/following-sibling::td/text()")))
#         seller = get_text(get_first_element(doc.xpath("//th[text()='出品者']/following-sibling::td/text()")))

#         # Update item with additional data
#         item.update({
#             'description': description,
#             'brand': brand,
#             'category': category,
#             'condition': condition,
#             'seller': seller,
#         })

#         # Push item data to the database or your data sink
#         datapush(item, self.model, 'detailed', self.identifier)

#         yield item














# -*- coding: utf-8 -*-
# import datetime
# import random
# import re
# from lxml import etree
# import scrapy
# from lxml import html
# from scrapy import signals
# from lxml.etree import tostring
# from ..helpers.data_helper import get_text, get_first_element, get_last_element, clean_text, get_element, \
#     process_spider_stats, trim_data, ebay_commission_calculation, check_substring, update_scrapping_status
# from ..items import ProductItem, BasicProductItem
# from ..helpers.data_helper import datapush
# from apps.eBay_operations.models.ui_handler import UIChangesDetailedScraping, UIChangesimpleScraping

# class YahooSpider(scrapy.Spider):
#     name = 'yahoo_website_crawler'

#     def __init__(self, identifier, url=None, query=None, platform=None, product_count=1, translation_flag=False,
#                  type=None, model=None, black_list_sellers=[], black_list_words=[], is_last_scrapping=False):
#         self.url = url
#         self.query = query
#         self.platform = platform
#         self.product_count = 1
#         self.max_product_count = product_count
#         self.translation_flag = translation_flag
#         self.type = type
#         self.base_url = 'https://auctions.yahoo.co.jp'
#         self.identifier = identifier
#         self.black_list_sellers = black_list_sellers
#         self.black_list_words = black_list_words
#         self.is_last_scrapping = is_last_scrapping
#         self.model = model
#         self.headers = {
#             'Host': 'auctions.yahoo.co.jp',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#             'Referer': 'https://auctions.yahoo.co.jp/',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.5',
#             'Accept-Encoding': 'gzip, deflate, br',
#             'Connection': 'keep-alive',
#             'Upgrade-Insecure-Requests': '1',
#         }

#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(YahooSpider, cls).from_crawler(crawler, *args, **kwargs)
#         crawler.signals.connect(spider.spider_closed, signals.spider_closed)
#         return spider

#     def table_mapping(self):
#         mapping_data = {
#             "ブランド": 'brand',
#             "カテゴリ": 'category',
#             "サイズ": 'size',
#             "状態": 'condition',
#         }
#         return mapping_data

#     def start_requests(self):
#         if self.url and self.type == 'search':
#             yield scrapy.Request(url=self.url, callback=self.parse_product_links, headers=self.headers)
#         else:
#             yield scrapy.Request(url=self.url, callback=self.parse_product, headers=self.headers)

#     def parse_product_links(self, response):
#         if response.status == 200:
#             item = BasicProductItem()            
#             doc = html.fromstring(response.body)
#             with open('first_page.html', 'w', encoding='utf-8') as f:
#                 f.write(response.text)
#             allpaths = UIChangesimpleScraping.objects.filter(platform_id__name='Auction Yahoo')
#             pathdict = {key.field_name: key.xpath for key in allpaths}
#             products = doc.xpath("//ul[@class='Products__items']/li")
#             if not products:
#                 products = doc.xpath("//div[@class='Products__list']/ul/li")
#             if not products:
#                 products = doc.xpath(pathdict['products'])
                
#             for product in products:                   
#                 if self.product_count > self.max_product_count:
#                     break
                
#                 product_link = get_first_element(product.xpath("./div/a/@href")) or get_first_element(product.xpath(pathdict['product_link']))
#                 product_name = get_text(get_first_element(product.xpath(pathdict['product_name']))) or get_text(get_first_element(product.xpath(".//h3[@class='Product__title']/a/@data-auction-title")))
#                 if check_substring(self.black_list_words, product_name):
#                     continue
#                 price = get_text(get_first_element(product.xpath(pathdict["price"])))
#                 photo = get_first_element(product.xpath(pathdict["photo"]))
                
#                 item.update({
#                     'url': product_link,
#                     'platform': 'Auction Yahoo',
#                     'photos': photo,
#                     'price': price,
#                     'count': self.product_count,
#                     'product_name': product_name,
#                 })

#                 # Check for additional status and bid information
#                 check_price_status = get_text(get_last_element(product.xpath(pathdict['check_price_status']))) or 'fixed'
#                 bid_status = get_text(get_first_element(product.xpath(pathdict['bid_status'])))
                
#                 for key, values in item.items():
#                     if values is None:             
#                         UIChangesimpleScraping.objects.filter(ui_change_status=False, platform_name="Auction Yahoo", target=item[key]).update(ui_change_status=True)
                        
#                 if (bid_status and '入札' in bid_status) or not bid_status:
#                     datapush(item, self.model, self.type, self.identifier)
#                     self.product_count += 1

#             next_page_link = get_first_element(doc.xpath("//li[@class='Pager__list Pager__list--next']/a/@href"))
#             if self.product_count <= self.max_product_count and next_page_link:
#                 yield scrapy.Request(url=next_page_link, callback=self.parse_product_links, headers=self.headers)
            

#     def parse_product(self, response):
#         item = ProductItem()
#         if response.status == 200:
#             doc = html.fromstring(response.body)
#             detailed_path = UIChangesDetailedScraping.objects.filter(platform_id__name='Auction Yahoo')
#             detailedpathDict = {key.field_name: key.xpath for key in detailed_path}

#             product_name = get_text(get_first_element(doc.xpath(detailedpathDict['product_name']))) or get_text(get_first_element(doc.xpath("//h1[@class='sc-f3a947cb-0 fUNTYt ItemTitle__Component']/span/text()")))
#             seller_name = get_text(get_first_element(doc.xpath(detailedpathDict['seller_name'])))
#             table_element = get_first_element(doc.xpath("//table[@class='Section__table']"))
#             parsed_table_data = self.parse_table(table_element)
#             description = get_text(get_first_element(doc.xpath(detailedpathDict['description'])))
#             price = clean_text(get_first_element(doc.xpath("//dd[@class='Price__value Price__value--buyNow']/text()")))

#             item.update({
#                 "product_name": product_name,
#                 "platform": 'Auction Yahoo',
#                 "description": description,
#                 "price": ebay_commission_calculation(price, 'Auction Yahoo') if price else 0,
#                 "seller": seller_name,
#                 "url": response.url,
#                 "photos": doc.xpath(detailedpathDict['photo']) or doc.xpath("//div[@class='slick-slide slick-active slick-current']/div/button/img/@src"),
#             })
#             item.update(parsed_table_data)

#             if item.get("seller") in self.black_list_sellers:
#                 return  # Skip blacklisted sellers
            
#             datapush(item, self.model, self.type, self.identifier)
#             yield item

#     def parse_table(self, table_element):
#         table_data = {}
#         rows = table_element.xpath(".//tr")
#         mapping_data = self.table_mapping()
#         for row in rows:
#             key = get_first_element(row.xpath("./th/text()"))
#             key = mapping_data.get(key) if key else None            
#             if key:
#                 value = self.get_row_value(row, key)
#                 table_data[key] = value
#         return table_data

#     def get_row_value(self, row, key):
#         if key == 'size':
#             return get_text(get_element(-1, row.xpath("./td/ul/li"))) or get_text(get_element(-1, row.xpath("./td")))
#         elif key == 'category':
#             return get_text(get_element(-2, row.xpath("./td/ul/li/a")))
#         elif key == 'brand':
#             return get_text(get_element(-1, row.xpath("./td/a")))
#         elif key == 'condition':
#             return get_text(get_element(-1, row.xpath("./td/a")))
#         return None













# import scrapy

# # class YahooAuctionSpider(scrapy.Spider):
# #     name = "yahoo_auction"

# #     def __init__(self, url=None, *args, **kwargs):
# #         super(YahooAuctionSpider, self).__init__(*args, **kwargs)
# #         self.start_urls = [url]  # Accept URL as input

# #     def parse(self, response):
# #         yield {
# #             'product_name': response.css('selector_for_product_name::text').get(),
# #             'price': response.css('selector_for_price::text').get(),
# #             'photos': response.css('selector_for_photos::attr(src)').getall(),
# #             'product_url': response.url,
# #         }


# class YahooAuctionSpider(scrapy.Spider):
#     name = 'yahoo_spider'
#     scraped_data = []  # Initialize an empty list to store scraped data

#     def parse_product_links(self, response):
#         # Scrape product links and store in scraped_data
#         for product in response.xpath('//some_xpath'):
#             item = {
#                 'title': product.xpath('.//title_xpath/text()').get(),
#                 'price': float(product.xpath('.//price_xpath/text()').get().replace('¥', '').replace(',', '')),
#                 'photos': product.xpath('.//photo_xpath/@src').getall(),
#                 'product_url': response.urljoin(product.xpath('.//product_url_xpath/@href').get()),
#             }
#             self.scraped_data.append(item)

#     def parse_product(self, response):
#         # Scrape detailed product information and store in scraped_data
#         item = {
#             'product_name': response.xpath('//name_xpath/text()').get(),
#             'description': response.xpath('//description_xpath/text()').get(),
#             'price': float(response.xpath('//price_xpath/text()').get().replace('¥', '').replace(',', '')),
#             'brand': response.xpath('//brand_xpath/text()').get(),
#             'category': response.xpath('//category_xpath/text()').get(),
#             'photos': response.xpath('//photo_xpath/@src').getall(),
#             'condition': response.xpath('//condition_xpath/text()').get(),
#             'seller': response.xpath('//seller_xpath/text()').get(),
#         }
#         self.scraped_data.append(item)





# import scrapy

# class YahooAuctionSpider(scrapy.Spider):
#     name = 'yahoo_auction'
#     allowed_domains = ['auctions.yahoo.co.jp']
#     start_urls = ['https://auctions.yahoo.co.jp/']

#     custom_settings = {
#         'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
#         'DOWNLOAD_DELAY': 2,
#         'FEED_FORMAT': 'json',
#         'FEED_URI': 'output.json',
#     }

#     def parse(self, response):
#         # Extract product links from the main page
#         product_links = response.xpath('//a[@class="Link--title"]/@href').getall()
#         for link in product_links:
#             yield response.follow(link, self.parse_product)

#         # Handle pagination (if applicable)
#         next_page = response.xpath('//a[@class="pagination__next"]/@href').get()
#         if next_page:
#             yield response.follow(next_page, self.parse)

#     def parse_product(self, response):
#         # Extract product details
#         product = {}
#         try:
#             product['name'] = response.xpath('//h1/text()').get(default='').strip()  # Product title
#             price = response.xpath('//span[@class="Price--price"]/text()').get(default='0')
#             product['price'] = int(price.replace('¥', '').replace(',', '').strip()) if price.isdigit() else None  # Price
#             product['url'] = response.url  # Product URL
            
#             # Additional fields
#             product['description'] = response.xpath('//div[@class="item-description"]//text()').getall()
#             product['description'] = ' '.join(product['description']).strip()  # Description
            
#             product['brand'] = response.xpath('//span[contains(text(),"Brand")]/following-sibling::span/text()').get(default='').strip()  # Brand (placeholder XPath)
#             product['category'] = response.xpath('//span[contains(text(),"Category")]/following-sibling::span/text()').get(default='').strip()  # Category (placeholder XPath)
#             product['condition'] = response.xpath('//span[contains(text(),"Condition")]/following-sibling::span/text()').get(default='').strip()  # Condition (placeholder XPath)
#             product['photos'] = response.xpath('//img[@class="item-image"]/@src').getall()  # Photos (placeholder XPath)
#             product['seller'] = response.xpath('//span[contains(text(),"Seller")]/following-sibling::span/text()').get(default='').strip()  # Seller (placeholder XPath)

#             # Yield the product item
#             yield product
#         except Exception as e:
#             self.logger.error(f"Error extracting product data: {e}")

#     def start_requests(self):
#         for url in self.start_urls:
#             yield scrapy.Request(url, callback=self.parse)