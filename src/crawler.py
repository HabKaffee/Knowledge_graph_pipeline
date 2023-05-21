import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

to_disable = {
    "profile.managed_default_content_settings.images" : 2,
    "profile.default_content_settings.cookies" : 2
}

browser_options = webdriver.ChromeOptions()
browser_options.add_extension(f'{os.getcwd()}/utils/Crystal-Ad-block.crx')
browser_options.add_experimental_option("prefs", to_disable)
browser_options.add_argument('--disable-application-cache')

categories = ['finance', 'hitech', 'nauka', 'auto']


def prefetch_articles(num_of_articles_per_category):
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
    # driver = webdriver.Chrome(executable_path=f'{os.getcwd()}/utils/chromedriver.exe', options=browser_options)
    
    output = f'{os.getcwd()}/data/links_and_categories.json'
    with tqdm(categories, desc='Crawl categories') as category_pb:
        for category in categories:
            driver.get('https://vesti.ru/' + category)
            count = 0
            while count < num_of_articles_per_category:
                articles = driver.find_elements(By.XPATH, '//h3[contains(@class,"list__title")]')
                count = len(articles)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            articles = driver.find_elements(By.XPATH, '//a[contains(@class, "list__pic-wrapper")]')
            with tqdm(num_of_articles_per_category, desc=f"Write crawled info in {category}") as write_pb:
                for idx in range(num_of_articles_per_category):
                    with open(output, 'a', encoding='utf-8') as file:
                        file.write(json.dumps({
                            'link' : articles[idx].get_attribute('href'),
                            'category' : category
                        }, ensure_ascii=False) + '\n')
                    write_pb.update()
                    write_pb.refresh()
                write_pb.close()
            category_pb.update()
            category_pb.refresh()
        category_pb.close()
    driver.quit()


def crawl_data_from_vesti_ru(num_of_articles_per_category=1000):
    prefetch_articles(num_of_articles_per_category)
    posts = []
    with open(f"{os.getcwd()}/data/links_and_categories.json", 'r', encoding='utf-8') as file:
        for line in file:
            posts.append(json.loads(line))
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)

    articles = []
    with tqdm(posts, desc="Process posts") as progress_bar:
        for post in posts:
            time.sleep(1)
            driver.get(post['link'])
            title = driver.find_element(By.XPATH, "//h1[contains(@class, 'article__title')]").get_attribute('innerText').strip()
            tags = driver.find_elements(By.XPATH, "//a[contains(@class, 'tags__item')]")
            tags = ','.join([i.get_attribute("innerText") for i in tags])
            text = driver.find_elements(By.XPATH, "//div[contains(@class, 'article__text')]")
            text = ' '.join([i.get_attribute("innerText").replace('\n', ' ') for i in text]).strip()

            articles.append({
                'article_id' : post['link'],
                'title' : title,
                'category' : post['category'],
                'tags' : tags,
                'text' : text,
            })
            progress_bar.update()
            progress_bar.refresh()
        progress_bar.close()

    with open(f'{os.getcwd()}/data/crawled_data.json', 'w', encoding='utf-8') as file:
        json_string = json.dumps(articles, indent=2, ensure_ascii=False)
        file.write(json_string)
    os.remove(f'{os.getcwd()}/data/links_and_categories.json')
    driver.quit()