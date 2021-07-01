import scrapy, json
from maketabkhooneh.items import MaketabkhoonehItem


class CoursesSpider(scrapy.Spider):
    name = 'courses'
    allowed_domains = ['maktabkhooneh.org']
    start_urls = [
            # "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=58" ,
            # "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=54&sorting=new" ,
            # "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=35&sorting=new" ,
            # "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=89" ,
            # "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=126" ,
            # "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=1" ,
            # "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=199" ,
            "https://maktabkhooneh.org/course/%D8%A2%D9%85%D9%88%D8%B2%D8%B4-%D8%B1%D8%A7%DB%8C%DA%AF%D8%A7%D9%86-%D8%A7%D9%85%D9%86%DB%8C%D8%AA-%D8%A7%D9%BE%D9%84%DB%8C%DA%A9%DB%8C%D8%B4%D9%86-mk1222/" ,
        ]

    custom_settings = {
        "LOG_LEVEL" : "WARNING"
    }

    def parse(self, response):
        last_page = response.xpath('/html/body/div[4]/div/div/div/a[last()]/text()').get()
        print(response.url)
        courses = response.xpath('/html/body/div[2]/div/div/a/@href').getall()
        print(f"\n\n\t{last_page}\n\n")
        for course in courses:
            print(f"\n\n\t{'https://maktabkhooneh.org'+course[2:-2]}\n\n")
    
    def course_extractor(self, response):
        course = MaketabkhoonehItem()
        # title = response.xpath('//h1[@class="course-intro__title"]/text()').get()
        # teacher = response.xpath('//div[@class="teacher-information js-collapsible__title"]/div[@class="ellipsis"]/text()').get()
        # teacher_resume = response.xpath('//div[@class="filler js-collapsible__body"]/div[@class="filler--padded rich-text"]/p/text()').get()
        # duration = '//div[@class="course-information__value"]/text()'
        # sessions_title = response.xpath('//div[@id="seasons_info"]/h2/text()').get()
        # sessions = response.xpath('//div[@class="chapter__title"]/text()').getall()
        # json
        # /html/body/div/script[11]
        # /html/body/div/script[12]
        info_json = json.loads(response.xpath('//script[@type="application/ld+json"][3]/text()').get())
        more_json = json.loads(response.xpath('//script[@type="application/ld+json"][4]/text()').get())
        category_json = json.loads(response.xpath('//script[@type="application/ld+json"][5]/text()').get())
        

        course["price"] = {
            "price" : response.xpath('//meta[@name="price"]/@content').get()
            "full_content_access" : more_json["offers"]["price"] ,
            "date" : more_json["offers"]["priceValidUntil"][0]
            }
        course["info"] = {
            "title" : info_json["name"] ,
            "url" : info_json["url"] ,
            "image" : info_json["image"] ,
            "description" : course["description"] = info_json["description"] 
            }
        course["teacher"] = info_json["author"]["name"]
        course["organization"] = {
            "name" : info_json["provider"]["name"] ,
            "email" : info_json["provider"]["email"]
            }
        course["_id"] = more_json["productID"]
        course["category"] = category_json["itemListElement"][1]["item"]["name"]
        print("\n\n",course,"\n\n")

        # course = {
        #     "title" : title ,
        #     "teacher" : teacher ,
        #     "teacher_resume" : teacher_resume ,
        #     "duration" : duration ,
        #     "sessions_title" : sessions_title ,
        #     "sessions" : sessions ,
        # }
        # yield course
        
