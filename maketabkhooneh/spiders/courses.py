import scrapy
import json
from scrapy.http import Request
from maketabkhooneh.items import MaketabkhoonehItem


class CoursesSpider(scrapy.Spider):
    name = 'maktabkhooneh'
    # allowed_domains = ['maktabkhooneh.org']
    start_urls = [
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=58",
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=54",
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=35",
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=89",
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=126",
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=1",
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=199",
            # "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=null",
        ]

    custom_settings = {
        # "LOG_LEVEL": "WARNING",
        # "CLOSESPIDER_ITEMCOUNT" : 100 ,
    }
    total = 0

    def parse(self, response):
        print(response.url)
        # last_page = response.xpath('/html/body/div[4]/div/div/div/a[last()]/text()').get()
        next_page = response.xpath(
            '/html/body/div[1]/div/div/a[2]/@href').get()
        courses = response.xpath('/html/body/div[2]/div/div/a/@href').getall()
        # yield(f"\n\n\t{last_page}\n\n")
        self.total = self.total + len(courses)

        for course in courses:
            # yield Request(
            #     'https://maktabkhooneh.org'+course[2:-2],
            #     callback=self.extract
            #     )
            # print(course)
            yield response.follow(url=course[2:-2], callback=self.extract)
        # Next Page
        if next_page:
            #  for i in range(int(last_page)):
            yield Request(
                    response.urljoin(next_page[2:-2]),
                    callback=self.parse
                    )
            # print(response.urljoin(next_page[2:-2]))

    def extract(self, response):
        # print("\n"*4, response.url, response.status, "\n"*4)
        course_data = dict()
        data = response.xpath(
            '//script[@type="application/ld+json"]/text()').getall()
        # print("\n\n", data)
        for d in data:
            course_data = {**course_data, **json.loads(d)}
        course = MaketabkhoonehItem()
        # info_json = json.loads(response.xpath(
        #     '//script[@type="application/ld+json"][3]/text()').get())
        # more_json = json.loads(response.xpath(
        #     '//script[@type="application/ld+json"][4]/text()').get())
        # category_json = json.loads(response.xpath(
        #     '//script[@type="application/ld+json"][5]/text()').get())
        # print(course_data)
        course["price"] = {
            "price": response.xpath('//meta[@name="price"]/@content').get(),
            "full_access_date":
                course_data["offers"]["priceValidUntil"][0],
            "full_access_price": course_data["offers"]["price"]
            }
        course["info"] = {
            "title": course_data["name"],
            "url": course_data["url"],
            "image": course_data["image"],
            "description": course_data["description"],
            "time": response.xpath(
                '//div[@class="chapter__clock-text"]/text()').get(),
            "video": response.xpath(
                '//meta[@property="og:video"]/@content').get()
            }
        if "author" in course_data:
            course["teacher"] = {
                "name": course_data["author"]["name"],
                "resume": " ".join(response.xpath(
                    '//div[@class="filler--padded rich-text"]/p/text()').getall()),
                }
        else:
            course["teacher"] = {
                "name": "",
                "resume": " ".join(response.xpath(
                    '//div[@class="filler--padded rich-text"]/p/text()').getall()),
                }
        # course["time"] = {
        #     "required_time": response.xpath(
        #         '//div[@class="course-information"][1]/div[2]/text()').get(),
        #     "access_limaitaion": response.xpath(
        #         '//div[@class="course-information"][2]/div[2]/text()').get()
        # }
        if "provider" in course_data:
            course["organization"] = {
                "name": course_data["provider"]["name"],
                "email": course_data["provider"]["email"]
                }
        else:
            course["organization"] = {
                "name": "",
                "email": ""
                }
        course["_id"] = course_data["productID"]
        if "provider" in course_data:
            course["category"] = course_data["itemListElement"][1]["item"]["name"]
        else:
            course["category"] = "دیگر"

        # print("\n\n",course,"\n\n")

        # course = {
        #     "title" : title ,
        #     "teacher" : teacher ,
        #     "teacher_resume" : teacher_resume ,
        #     "duration" : duration ,
        #     "sessions_title" : sessions_title ,
        #     "sessions" : sessions ,
        # }
        print(self.total)
        return course
