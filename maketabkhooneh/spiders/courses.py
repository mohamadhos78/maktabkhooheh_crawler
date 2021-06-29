import scrapy


class CoursesSpider(scrapy.Spider):
    name = 'courses'
    allowed_domains = ['maktabkhooneh.org']
    start_urls = [
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=58" ,
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=54&sorting=new" ,
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=35&sorting=new" ,
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=89" ,
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=126" ,
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=1" ,
            "https://maktabkhooneh.org/api/learn/?types=PLUS&types=MAKTAB&types=HAMAYESH&sorting=new&selected_category=199" ,
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
        title = response.xpath('//h1[@class="course-intro__title"]/text()').get()
        teacher = response.xpath('//div[@class="teacher-information js-collapsible__title"]/div[@class="ellipsis"]/text()').get()
        teacher_resume = response.xpath('//div[@class="filler js-collapsible__body"]/div[@class="filler--padded rich-text"]/p/text()').get()
        duration = '//div[@class="course-information__value"]/text()'
        sessions_title = response.xpath('//div[@id="seasons_info"]/h2/text()').get()
        sessions = response.xpath('//div[@class="chapter__title"]/text()').getall()
        
