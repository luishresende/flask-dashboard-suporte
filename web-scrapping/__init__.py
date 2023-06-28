from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from time import sleep


def downDetector():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = uc.Chrome(options=options)
    driver.get('https://downdetector.com.br')
    html_content = driver.page_source
    '''try:
        elemento = driver.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input')
        elemento.click()
        sleep(10)
    except WebDriverException as er:
        print('deu ruim\n', er)'''
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')

    captions = soup.find_all('div', class_='caption')
    warning_companies = list()
    danger_companies = list()
    for caption in captions:
        sparkline = str(caption.find('svg')['class'][0])
        if sparkline != 'sucess':
            titulo = str(caption.find('h5'))
            if sparkline == 'danger':
                danger_companies.append(titulo[titulo.index('<h5>') + len('<h5>'):titulo.index('</h5>')])
            elif sparkline == 'warning':
                warning_companies.append(titulo[titulo.index('<h5>') + len('<h5>'):titulo.index('</h5>')])

    print(warning_companies, danger_companies)

    return warning_companies, danger_companies


downDetector()
