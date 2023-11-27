from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver=webdriver.Chrome()
driver.get("http://sdetchallenge.fetch.com/") 

# Applying Ternary Search with filter1 and filter2
def find_bar_filter1(bars):
    group1 = bars[:3]
    group2 = bars[3:6]
    group3 = bars[6:]

    print("Weighings List:")
    first_weigh = weigh(group1, group2)
    
    if first_weigh == '<':
       find_bar_filter2(group1)
    elif first_weigh == '>':
        find_bar_filter2(group2)
    else:
        find_bar_filter2(group3)
    
    return None

def find_bar_filter2(bars):
    second_weigh = weigh(bars[0], bars[1])
    if second_weigh == '<': # fake bar is bars[0]
        message_alert(bars[0])
    elif second_weigh == '>': # fake bar is bars[1]
        message_alert(bars[1])
    else: # fake bar is bars[2]
        message_alert(bars[2])

    return None

# Site iteraction functon: Inserts numbers into Bowls, Weighs, and returns Result 
def weigh(group1, group2):
    for num in range(len(group1)): # Input numbers into left bowl
        driver.find_element(By.ID, "left_" + str(num)).send_keys(group1[num])
    for num in range(len(group2)): # Input numbers into right bowl
        driver.find_element(By.ID, "right_" + str(num)).send_keys(group2[num])
    
    driver.find_element(By.ID, "weigh").click()
    wait = WebDriverWait(driver, 10)  # Setting maximum wait time of 10 seconds for weighing to appear

    if len(group1) == 3: # Wait for first weighing
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[5]/ol/li')))
        print(driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[5]/ol/li').text) 
    elif len(group1) == 1: # Wait for second weiging
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[5]/ol/li[2]')))
        print(driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[5]/ol/li[2]').text) 

    results = driver.find_element(By.ID, 'reset').text # weighing results
    reset = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[4]/button[1]").click() # Resetting bowls

    return (results)

# Prints Weighings, Fake bar number, and Clicks the fake gold bar number and handles the alert message
def message_alert(fake_bar_num):
    print("Total Weighings: 2") # There should always be 2 weighings
    print("Fake bar number is:", fake_bar_num)
    fake_bar_button = driver.find_element(By.ID, "coin_" + fake_bar_num)
    fake_bar_button.click()
    try: # Check for alert and close the alert
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"Alert message: {alert_text}")
        alert.accept()
    except:
        print("No alert present.")
    return None    

bars = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

find_bar_filter1(bars)

driver.quit()
