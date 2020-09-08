import scrapy, csv, sys, os, datetime
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

#scrapy runspider pbscraper_full.py -L WARN && python email_custom_full.py

c_date_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
csv_output_file = r"csv_output/data_full_data.csv"
    
def listToString(s):  
    str1 = "\n"
    return (str1.join(s))

r_count = 0
attempt_count = 0

def r_increment():
    global r_count
    r_count = r_count+1

def r_decrease():
    global r_count
    r_count = r_count-1

def attempt_increment():
    global attempt_count
    attempt_count = attempt_count+1
    
class pbScraper(scrapy.Spider):
    name = 'philgeps'
    allow_domains = ['https://www.philgeps.gov.ph']
    start_urls = ['https://www.philgeps.gov.ph/GEPSNONPILOT/Tender/SplashOpportunitiesSearchUI.aspx?menuIndex=3&ClickFrom=OpenOpp&Result=3']

    #CSV and Header Creation =============
    fields=['Reference Number', 'Procuring Entity', 'Title', 'Area of Delivery', 'Solicitation Number', 'Trade Agreement', 'Procurement Mode',
            'Classification', 'Category', 'Approved Budget for the Contract', 'Contract Duration',
            'Client Agency', 'Contact Person', 'Status', 'Associated Components', 'Bid Supplements',
            'Document Request List', 'Date Published', 'Last Updated / Time', 'Closing Date / Time',
            'Description', 'Other Information', 'Created by', 'Date Created']
    with open(csv_output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    #CSV Header Creation End ==============
    
    
    def parse(self, response):
        rows = response.css('table.GridTable tr')
        for row in rows:

            r_increment()
            print("Item :" + str(r_count) + " | " + str(row.css('td')[3].css('a::text').extract_first()))
        
            url_bid = row.css('td')[3].css('a::attr(href)').extract_first()

            if url_bid != None:
                url = ("https://www.philgeps.gov.ph/GEPSNONPILOT/Tender/" + url_bid)
                yield scrapy.Request(url, callback=self.parse_detail)
                #return  #Remove this line to loop continue
        
        r_decrease()

        yield scrapy.FormRequest.from_response(response,
        formdata={'__EVENTTARGET': 'pgCtrlDetailedSearch$nextLB', '__EVENTARGUMENT': ''},
        callback = self.parse,
        dont_click = True)
        
        print("No. of Record Scrapped: " + str(r_count))
        
    
    def parse_detail(self, response):
        ref_num = response.xpath('//*[@id="lblDisplayReferenceNo"]/text()').get()
        ref_num = '=HYPERLINK("' + response.url + '","' + ref_num + '")'
        procuring_entity = response.xpath('//*[@id="lblDisplayProcuringEntity"]/text()').get()
        title_bid = response.xpath('//*[@id="lblDisplayTitle"]/text()').get()
        area_of_delivery = response.xpath('//*[@id="lblDisplayAOD"]/text()').get()
        solicitation_number = response.xpath('//*[@id="lblDisplaySolNumber"]/text()').get()
        trade_agreement = response.xpath('//*[@id="lblDisplayTradeAgree"]/text()').get()
        procurement_mode = response.xpath('//*[@id="lblDisplayProcureMode"]/text()').get()
        classification = response.xpath('//*[@id="lblDisplayClass"]/text()').get()
        category_bid = response.xpath('//*[@id="lblDisplayCategory"]/text()').get()
        approved_budget_for_contract = response.xpath('//*[@id="lblDisplayBudget"]/text()').get()
        contract_duration = response.xpath('//*[@id="lblDisplayPeriod"]/text()').get()
        client_agency = response.xpath('//*[@id="lblDisplayClient"]/text()').get()
        contact_person = response.xpath('//*[@id="lblDisplayContactPerson"]/text()').get()
        status_bid = response.xpath('//*[@id="lblDisplayStatus"]/text()').get()
        associated_components = response.xpath('//*[@id="Table7"]/tbody/tr[2]/td[2]/a/text()').get()
        bid_supplements = response.xpath('//*[@id="lblDisplayBidSupplements"]/text()').get()
        document_request_list = response.xpath('//*[@id="lblDisplayDocReqList"]/text()').get()
        date_published = response.xpath('//*[@id="lblDisplayDatePublish"]/text()').get()
        last_updated = response.xpath('//*[@id="lblDisplayLastUpdateTime"]/text()').get()
        closing_date = response.xpath('//*[@id="lblDisplayCloseDateTime"]/text()').get()
        description_bid = response.xpath('//*[@id="lblAbstractText"]/text()').getall()
        description_bid = listToString(description_bid)
        description_bid = description_bid[0:255]
        if description_bid != None:
            description_bid = " " + description_bid
        description_bid = description_bid.replace("\n", " ")
        other_information = response.xpath('//*[@id="lblOtherInfo"]/text()').get()
        if other_information != None:
            other_information = " " + str(other_information)
        created_by = response.xpath('//*[@id="lblDisplayCreatedBy"]/text()').get()
        date_created = response.xpath('//*[@id="lblDisplayDateCreated"]/text()').get()
        
        field_rows=[ref_num, procuring_entity, title_bid, area_of_delivery, solicitation_number, trade_agreement, procurement_mode, classification, category_bid
                , approved_budget_for_contract, contract_duration, client_agency, contact_person
                , status_bid , associated_components, bid_supplements, document_request_list
                , date_published, last_updated, closing_date, description_bid, other_information
                , created_by, date_created]
            
        with open(csv_output_file, 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(field_rows)
    