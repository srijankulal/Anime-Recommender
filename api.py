from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains
# from main import db,app,AnimeRec


url='https://myanimelist.net/recommendations.php?s=recentrecs&t=anime'

global lock;


def scrap(AnimeRec):
    global lock
    lock=False
    driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-v-53da086b]'))
        )
        button.click()
    except:
        pass
    
    count=0
    anime={}
    complete='False'
    # # Perform the hover action on the hover element
    actions = ActionChains(driver)
    # actions.move_to_element(hover_element).perform()
    hover_elements = driver.find_elements(By.CLASS_NAME, 'hoverinfo_trigger')
    for hover_element in hover_elements:
        if lock==False:
            print('Scraping')
            actions.key_down(Keys.CONTROL).click(hover_element).perform()
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            try:
                Engname=soup.find('p',class_='title-english title-inherit').text if soup.find('p',class_='title-english title-inherit') else soup.find('h1',class_='title-name h1_bold_none').text
            except:
                Engname='N/A'
            try:
                Japname=soup.find('h1',class_='title-name h1_bold_none').text
            except:
                Japname='N/A'
            try:
                
                Type = soup.find('span', class_='dark_text', text='Type:').find_next_sibling('a').text
            except:
                Type='N/A'
            try:
                status=soup.find('span', class_='dark_text', text='Status:').next_sibling.strip() #next sibling bcz the result come after Status
            except:
                status='N/A'
            try:
                genre = [genre.text for genre in soup.find_all('a', href=lambda href: href and "/anime/genre/" in href)] #href argument is a lambda function that filters these <a> tags to only include those whose href attribute contains the substring "/anime/genre/".
                genres = ', '.join(genre)
            except:
                genres='N/A'
            try:
                episodes=int(soup.find('span', class_='dark_text', text='Episodes:').next_sibling.strip())
            except:
                episodes='N/A'
            try:
                image=soup.find('img',class_='lazyloaded').get('src')
            except:
                image='N/A'
            # print(image)

            # anime[count] = {
            #     'Engname': Engname,
            #     'Japname': Japname,
            #     'Type': Type,
            #     'status': status,
            #     'genre': genres,
            #     'episodes': episodes
            # }
            #Creates the object of the class AnimeRec
            anime=AnimeRec(Engname=Engname,Japname=Japname,Type=Type,status=status,genre=genres,episodes=episodes,image=image)
            anime.store()#store the object in the database and commit the changes the object is itself the argument
            
            # print(f'The anime list {anime[count]}')
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            count+=1
            time.sleep(2)  
        else:
            print("Scraping stopped")
            complete='stop'
            break        

        # Close the WebDriver
    if complete=='False':
        driver.quit()
        return 'Scraping completed'
    elif complete=='stop':
        driver.quit()
        return 'Scraping stopped'

    
    
def close():
    global lock
    print('Closing')
    lock=True
    
    
    




