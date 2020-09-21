
from selenium import webdriver
import os
import requests
import urllib


def scroll_to_end(driver):
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')


def scrape(search_keyword, max_images):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')
    driver = webdriver.Chrome(options=chromeOptions,
                              executable_path='./chromedriver.exe')

    driver.get("https://images.google.com/")

    search = driver.find_element_by_xpath(
        "/html/body/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input")

    search.send_keys(search_keyword)

    search_btn = driver.find_element_by_xpath(
        "/html/body/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[1]/button")

    search_btn.click()

    if not os.path.exists('static/'):
        os.mkdir('static')
    if not os.path.exists('static/'+search_keyword):
        os.mkdir('static/'+search_keyword)
        print(search_keyword, "directory created")

    image_count = 0
    image_urls = set()
    start = 0

    while image_count <= max_images:
        scroll_to_end(driver)
        images = driver.find_elements_by_css_selector(".BUooTd")
        print('found images: ', len(images))
        for image in images[start:]:
            try:
                load = image.find_elements_by_css_selector("img.Q4LuWd")[0]
                load.click()
                image_url = driver.find_elements_by_css_selector('img.n3VNCb')[
                    1]
                image_urls.add(image_url.get_attribute('src'))
                image_name = search_keyword+str(image_count)+".jpg"
                urllib.request.urlretrieve(image_url.get_attribute(
                    'src'), "./static/"+search_keyword+"/"+image_name)
                print("downloaded: ", image_name)
                image_count += 1
            except Exception as e:
                continue
            if image_count >= max_images:
                break
        start = len(images)+1
    driver.close()
    return list(image_urls)
