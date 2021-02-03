# ONCE INSIDE THE "start_urls"...
# 1. SCROLLING 2 TIMES WITH SELENIUM TO LOAD A BUNCH OF OPINIONS ON "start_urls".
# 2. STORE THE LINKS OF EVERY PROFILE LOADED IN THE LAST POINT.
# 3. ACCESS TO THE USER IN A NEW DRIVE BY CLICKING ON ITS LINK AND CLICK ON "OPINIONES". THEN, MAKE SCROLLING 2 TIMES TO LOAD THE A BUNCH OF OPINIONS FROM THIS
# USER.
# 4. RETRIEVE THE "NAME", "OPINION TITLE", "SCORE" AND "DESCRIPTION".
# 5. CLOSE THE USER DRIVER, SAVE THE DATA AND REPEAT THE PROCESS WITH THE OTHER USERS.

# NOTE: WE ARE GOIN TO MAKE JUST "2 SCROLLS", NO MORE. IT'S NOT NECESSARY RIGHT NOW WE ARE LEARNING. THE MAIN REASON IS, WE WILL STORE A LOT OF INFORMATION AND FOR NOW, I DON'T WANT THAT.

from time import sleep
import random, json
# SELENIUM:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_url = "https://www.google.com/search?client=firefox-b-d&tbm=lcl&sxsrf=ALeKk02ssQfToU1_MMY6QxMjc8uo-pEVMw%3A1612217570627&ei=4nwYYPvPJYOwtQWoqbboDA&q=mariscos+roque&oq=mariscos+roque&gs_l=psy-ab.12...0.0.0.16069.0.0.0.0.0.0.0.0..0.0....0...1c..64.psy-ab..0.0.0....0.w9F6u758n-0#lrd=0x85d21dc691e7e125:0x5274c6e8436676c2,1,,,&rlfi=hd:;si:5941592509274027714,l,Cg5tYXJpc2NvcyByb3F1ZVogCg5tYXJpc2NvcyByb3F1ZSIObWFyaXNjb3Mgcm9xdWU,y,nuBUzXcOn9o;mv:[[19.5437008,-99.188699],[19.494498999999998,-99.2390769]]"
        
def intelligent_waiting(driver, xpath):
    """This function help us aesthetic, since we just declare a line instead of the whole expression below."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )
        
# Setting our automated browser:
def setting_driver(url):
    """This function creates a driver."""
    driver = None # To avoid multiple drivers available at the same time.
    
    opts = Options()
    ua = "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/88.0.4324.96 Chrome/88.0.4324.96 Safari/537.36"
    opts.add_argument(ua)
    driver = webdriver.Chrome("./chromedriver.exe", options = opts)
    driver.get(url)
    
    return driver

def save_data(data, number_of_user):
    """This function saves the given data."""
    
    try:
        with open(f"Opinions_from_Google/user_number_{number_of_user}.json", 'w') as json_outfile:
            json.dump(data, json_outfile, ensure_ascii=False) # ENSURE_ASCII = FALSE. This way WE MAKE READABLE THE JSON FILE FOR THE HUMANS.
        print("DATA FROM THIS USER HAS BEEN STORED SUCCESSFULLY!!! LET'S GO WITH THE NEXT USER.")
    except Exception as e:
        print("¡Something went wrong when storing the data. The error is the following:!")
        print(e)

main_driver = setting_driver(start_url) # We start opening the main/seed url in order to obtain the users links.

# Scrolling 2 times to load a bunch of users in the main/seed url:
scrolling_js_code = "document.getElementsByClassName('review-dialog-list')[0].scroll(0, 20000)"
scroll = 0
while (scroll < 2): # Since we're just going to make 2 scrolls.
    intelligent_waiting(main_driver, "//div[@class='review-dialog-list']//div[@class='gws-localreviews__general-reviews-block']/div[contains(@class, 'gws-localreviews__google-review')]")
    sleep(1) # We add an extra time to be sure that everything has loaded.
    main_driver.execute_script(scrolling_js_code)
    scroll += 1

users_links = main_driver.find_elements(By.XPATH, "//div[@class='review-dialog-list']//a[@class='Msppse']") # Retrieving profiles inside the main/seed url.
print("#"*60)
print(f"¡¡¡{len(users_links)} USERS LINKS RETRIEVED!!!")
print("#"*60)

# Algorithm to extract data:
for i,user in enumerate(users_links, start=1): # For every USER.
    try:
        user_data = dict()
        driver = setting_driver(user.get_attribute("href"))
        intelligent_waiting(driver, "//button[text()='Opiniones']") # We wait for the "Opiniones" button to load.
        opiniones_button = driver.find_element(By.XPATH, "//button[text()='Opiniones']") # Once it has loaded, we retrieve it and;
        opiniones_button.click() # We click on it.
        
        # Scrolling just 1 time:
        intelligent_waiting(driver, "//div[@class='section-review ripple-container GLOBAL__gm2-body-2 section-review-clickable section-review-with-padding section-review-side-margin-small']")
        scrolling_js_code = "document.getElementsByClassName('section-layout section-scrollbox scrollable-y scrollable-show')[0].scroll(0, 20000)"
        driver.execute_script(scrolling_js_code)
        intelligent_waiting(driver, "//div[@class='section-review ripple-container GLOBAL__gm2-body-2 section-review-clickable section-review-with-padding section-review-side-margin-small']")
        sleep(random.uniform(4,4)) # We add an extra time to be sure that everything has loaded.
            
        User_Name = driver.find_element(By.XPATH, "//h1[contains(@class, 'section-profile-header-name')]").text
        user_data["User_Name"] = User_Name
        user_data["Opinions"] = []
        containers = driver.find_elements(By.XPATH, "//div[@class='section-review-content']")
        for container in containers:
            review = container.find_element(By.XPATH, ".//div[@class='section-review-title section-review-title-consistent-with-review-text']/span").text
            score = container.find_element(By.XPATH, ".//span[@class='section-review-stars']").get_attribute("aria-label")
            score = int(list(filter(str.isdigit, score.strip()))[0]) # This way, we keep with the number itself.
            description = container.find_element(By.XPATH, './/span[@class="section-review-text"]').text
            user_data["Opinions"].append({"Review_Title":f"{review}", "Score":f"{score}", "Description":f"{description}"})
        
        print("#"*60)
        print(f"User: {user_data['User_Name']}; Number of opinions: {len(user_data['Opinions'])}")
        save_data(user_data, i) # HERE, WE SAVE THE DATA WE GATHER FROM THE CURRENT USER.
        driver.close() # We close the current driver. Remember we are creating a new driver per user.
        print("#"*60)
        
    except Exception as e:
        print("\n¡¡¡Something went wrong with this user. The error is:")
        print(e) # We print out the error.
        print("Let's try with the next one!!!")
        print('\r')
        driver.close()

main_driver.close() # We close the driver (in other words, the main page), where we extracted the users links.