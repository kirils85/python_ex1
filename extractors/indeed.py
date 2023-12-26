"""
from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs



if response.status_code != 200:
    print("Cant request page")
else:
    print(response.text)
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def get_page_count(keyword):
    chrome_options = Options()
    #브라우저 꺼짐 방지 코드
    #chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    browser = webdriver.Chrome(options = chrome_options)

    base_url = "https://kr.indeed.com/jobs?q="

    
    browser.get(f"{base_url}{keyword}")
    #print(browser.page_source.encode('utf8'))
    #results = []
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("ul", class_="css-1g90gv6 eu4oa1w0")
    if pagination == None:
        return 1
    pages = pagination.find_all("li", recursive=False)
    count = len(pages)
    if count >= 5:
        return 5
    else :
        return count 

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    results = []
    for page in range(pages):
        chrome_options = Options()
        #브라우저 꺼짐 방지 코드
        #chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        browser = webdriver.Chrome(options = chrome_options)

        base_url = "https://kr.indeed.com/jobs"

        
        browser.get(f"{base_url}?q={keyword}&start={page*10}")
        #print(browser.page_source.encode('utf8'))
        
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="css-zu9cdh eu4oa1w0")
        jobs = job_list.find_all('li',recursive=False)
        #job_list = soup.find("ul",class_="jobsearch-ResultsList")
        #jobs = job_list.find_all('li',recursive=False)
        for job in jobs:
            zone = job.find("div",class_="mosaic-zone")
            if zone == None:
                #print("job li")
                #h2 = job.find("h2", class_="jobTitle")
                #a = h2.find("a")
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span",attrs={"data-testid": "company-name"})
                location = job.find("div",attrs={"data-testid": "text-location"})
                job_data = {
                    'link': f"https://kr.indeed.com/{link}",
                    'company' : company.string,
                    'location' : location.string,
                    'position' : title
                }
                results.append(job_data)

    return results