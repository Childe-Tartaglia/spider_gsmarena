from distutils.command.build import build
from io import BufferedRandom
from xml.dom import NO_MODIFICATION_ALLOWED_ERR
import scrapy
from spider_gsmarena .items import SpiderGsmarenaItem


class GsmarenaSpider(scrapy.Spider):
    name = 'gsmarena'
    allowed_domains = ['www.gsmarena.com']
    start_urls = ['https://www.gsmarena.com/makers.php3']

    # 爬取品牌列表页
    def parse(self, response):
        brand_list = response.xpath('//div[@class="st-text"]/table/tr/td/a')

        for i in brand_list:
            brand = i.xpath('./text()').extract_first()
            href = i.xpath('./@href').extract_first()

            # 手机列表首页的url地址
            url = 'https://www.gsmarena.com/' + href
            # print(url)

            # 对手机列表首页发起访问
            yield scrapy.Request(url=url, callback=self.parse_phone, meta={'brand': brand})

    # 爬取手机列表首页

    def parse_phone(self, response):

        # 接收brand
        brand = response.meta['brand']
        # self.parse_specification_direct()
        href_spercification = response.xpath(
            '//div[@class="makers"]/ul/li/a/@href').extract()

        for m in href_spercification:
            # 手机参数页url
            url_spercification = 'https://www.gsmarena.com/' + m

            # 访问参数页
            yield scrapy.Request(url=url_spercification, callback=self.parse_specification, meta={'brand': brand})
        href_phone_list = response.xpath(
            '//div[@class="nav-pages"]/a/@href').extract()

        for n in href_phone_list:
            # 手机列表其他页url
            url_phone_list = 'https://www.gsmarena.com/' + n

            # 访问手机列表其他页
            yield scrapy.Request(url=url_phone_list, callback=self.parse_phone_list, meta={'brand': brand})

    # 爬取手机参数页面

    def parse_specification(self, response):

        brand = response.meta['brand']

        item = SpiderGsmarenaItem()

        item['brand'] = brand

        item['model_name'] = response.xpath(
            '//div/h1[@data-spec="modelname"]/text()').get()

        # item['network_technology']

        item['net2g'] = response.xpath('//td[@data-spec="net2g"]/text()').get()

        item['net3g'] = response.xpath('//td[@data-spec="net3g"]/text()').get()

        item['net4g'] = response.xpath('//td[@data-spec="net4g"]/text()').get()

        item['net5g'] = response.xpath('//td[@data-spec="net5g"]/text()').get()

        item['speed'] = response.xpath('//td[@data-spec="speed"]/text()').get()

        item['announced_date'] = response.xpath(
            '//td[@data-spec="year"]/text()').get()

        item['status'] = response.xpath(
            '//td[@data-spec="status"]/text()').get()

        item['body_dimensions'] = response.xpath(
            '//td[@data-spec="dimensions"]/text()').get()

        item['weight'] = response.xpath(
            '//td[@data-spec="weight"]/text()').get()

        item['build'] = response.xpath('//td[@data-spec="build"]/text()').get()

        item['sim'] = response.xpath('//td[@data-spec="sim"]/text()').get()

        item['body_other'] = response.xpath(
            '//td[@data-spec="bodyother"]/text()').getall()

        item['display_type'] = response.xpath(
            '//td[@data-spec="displaytype"]/text()').get()

        item['display_size'] = response.xpath(
            '//td[@data-spec="displaysize"]/text()').get()

        item['display_resolution'] = response.xpath(
            '//td[@data-spec="displayresolution"]/text()').get()

        item['display_protection'] = response.xpath(
            '//td[@data-spec="displayprotection"]/text()').get()

        item['display_other'] = response.xpath(
            '//td[@data-spec="displayother"]/text()').getall()

        item['platform_os'] = response.xpath(
            '//td[@data-spec="os"]/text()').get()

        item['chipset'] = response.xpath(
            '//td[@data-spec="chipset"]/text()').get()
        item['cpu'] = response.xpath('//td[@data-spec="cpu"]/text()').get()

        item['gpu'] = response.xpath('//td[@data-spec="gpu"]/text()').get()
        item['memorycard_slot'] = response.xpath(
            '//td[@data-spec="memoryslot"]/text()').get()
        item['internal_memory'] = response.xpath(
            '//td[@data-spec="internalmemory"]/text()').get()

        item['memory_other'] = response.xpath(
            '//td[@data-spec="memoryother"]/text()').get()

        item['camera1_type'] = response.xpath(
            '//a[@href="glossary.php3?term=camera"]/text()').get()

        item['camera1_modules'] = response.xpath(
            '//td[@data-spec="cam1modules"]/text()').getall()

        item['camera1_features'] = response.xpath(
            '//td[@data-spec="cam1features"]/text()').get()

        item['camera1_video'] = response.xpath(
            '//td[@data-spec="cam1video"]/text()').get()

        item['camera2_type'] = response.xpath(
            '//a[@href="glossary.php3?term=secondary-camera"]/text()').get()

        item['camera2_modules'] = response.xpath(
            '//td[@data-spec="cam2modules"]/text()').getall()

        item['camera2_features'] = response.xpath(
            '//td[@data-spec="cam2features"]/text()').get()

        item['camera2_video'] = response.xpath(
            '//td[@data-spec="cam2video"]/text()').get()

        item['loudspeaker'] = response.xpath(
            '//div[@id="specs-list"]/table[9]/tr[1]/td[2]/text()').get()

        item['mm35_jack'] = response.xpath(
            '//div[@id="specs-list"]/table[9]/tr[2]/td[2]/text()').get()

        item['wlan'] = response.xpath('//td[@data-spec="wlan"]/text()').get()

        item['bluetooth'] = response.xpath(
            '//td[@data-spec="bluetooth"]/text()').get()

        item['gps'] = response.xpath('//td[@data-spec="gps"]/text()').get()

        item['nfc'] = response.xpath('//td[@data-spec="nfc"]/text()').get()

        item['radio'] = response.xpath('//td[@data-spec="radio"]/text()').get()

        item['usb'] = response.xpath('//td[@data-spec="usb"]/text()').get()

        item['sensors'] = response.xpath(
            '//td[@data-spec="sensors"]/text()').get()

        item['features_other'] = response.xpath(
            '//td[@data-spec="featuresother"]/text()').getall()

        item['battery_type'] = response.xpath(
            '//td[@data-spec="batdescription1"]/text()').get()

        item['charging'] = response.xpath(
            '//div[@id="specs-list"]/table[12]/tr[2]/td[2]/text()').getall()

        item['colors'] = response.xpath(
            '//td[@data-spec="colors"]/text()').get()

        item['models'] = response.xpath(
            '//td[@data-spec="models"]/text()').get()

        item['sar'] = response.xpath('//td[@data-spec="sar-us"]/text()').get()

        item['sar_eu'] = response.xpath(
            '//td[@data-spec="sar-eu"]/text()').get()

        # item['price']

        item['test_performance'] = response.xpath(
            '//td[@data-spec="tbench"]/text()').getall()

        # item['test_display']
        # item['test_camera']
        # item['test_loudspeaker']

        # item['audio_quality']

        item['battery_life'] = response.xpath(
            '//a[@onclick="showBatteryPopup(event, 10509); "]/text()').get()

        yield item

    # 爬取手机列表其他页

    def parse_phone_list(self, response):

        # 接收brand
        brand = response.meta['brand']
        href_spercification = response.xpath(
            '//div[@class="makers"]/ul/li/a/@href').extract()

        for m in href_spercification:
            # 手机参数页url
            url_spercification = 'https://www.gsmarena.com/' + m

            # 访问参数页
            yield scrapy.Request(url=url_spercification, callback=self.parse_specification, meta={'brand': brand})
