from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
from selenium.webdriver.common.keys import Keys

import csv
import pandas as pd
import numpy as np

import os 
import random

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.action_chains import ActionChains


import logging

from config import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
) # + info: https://realpython.com/python-logging/#using-handlers

 


def sleep_custom(sleep_time):
    if sleep_time >= 10: 
        logging.info("Sleep %ss (custom)", str(sleep_time))
    time.sleep(sleep_time)


def random_sleep():
    #global random_time_min
    #global random_time_max
    delay = random.randint(random_time_min,random_time_max)
    logging.info("Sleep %ss (random)", str(delay))
    time.sleep(delay)

def login(driver):
    logging.info("Login")
    driver.get(url_login)
    input_username = driver.find_element(By.ID, "username")
    input_password = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
    input_username.send_keys(username)
    sleep_custom(2)
    input_password.send_keys(password)
    sleep_custom(2)
    submit_button.click()

def run_search(driver, country, crop):
    logging.info("run_search()")
    
    driver.get(url_search)
    sleep_custom(5)
    
    # Country
    input_mrl_search = driver.find_element(By.XPATH, '//*[@id="crud_search"]/form/div[1]/div[2]/div/span[2]/span[1]/span/ul/li/input')
    input_mrl_search.send_keys(country)
    input_mrl_search.send_keys(Keys.RETURN)
    logging.info("Country: {}".format(country))
    sleep_custom(2)
    
    # Expand
    link_crop = driver.find_element(By.XPATH, '//*[@id="crud_search"]/form/div[2]/h3[1]/a')

    scroll_down(driver)
    #input("avanzar...")
    sleep_custom(1)

    link_crop.click()
    sleep_custom(2)
    
    # Crop
    input_crop_search = driver.find_element(By.XPATH, '//*[@id="crud_search"]/form/div[2]/div[1]/div[2]/div/span/span[1]/span/ul/li/input')
    input_crop_search.send_keys(crop)
    #input_crop_search.send_keys(Keys.RETURN)
    results = driver.find_elements(By.CSS_SELECTOR, 'li.select2-results__option')
    for r in results:
        if r.text == crop:
            r.click()
            break
    logging.info("Crop: {}".format(crop))    
    sleep_custom(2)
    
    # Submit
    button_display = driver.find_element(By.XPATH, "//button[@type='submit']")
    button_display.submit()
    sleep_custom(2)



"""     
def save_table_pandas(driver, country, crop, page):
    logging.debug("save_table_pandas(driver, {}, {}, {})".format(country, crop, page))
    table = driver.find_element(By.XPATH, '//*[@id="crud_list"]/table')
    
    # Read and Convert Web table into data frame
    webtable_df = pd.read_html(table.get_attribute('outerHTML'), header=1)[0]
    
    # duplicate values and fill empty rows
    webtable_clean = webtable_df.replace(np.nan,'EMPTY1234').replace('"', np.nan).ffill().replace('EMPTY1234', np.nan)
    
    # Set filename
    filename = "".join([country,'_', crop,'_', str(page), '.csv'])
    global path
    path_csv = path + "\\" + filename
    
    # Write() to CSV file
    webtable_clean.to_csv(path_csv)
 """


    
def create_pandas_frame(driver, total_pages, page_number):
    logging.debug("save_table_pandas(driver)")
    table = driver.find_element(By.XPATH, '//*[@id="crud_list"]/table')
    
    # Read and Convert Web table into data frame
    print('Total pages: {}'.format(total_pages))

    
    if str(total_pages) == str(1):
        print('DATAFRAME: sin param header')
        webtable_df = pd.read_html(table.get_attribute('outerHTML'))[0]
    elif str(total_pages) == str(page_number):
        print('DATAFRAME: sin param header - Last Page')
        webtable_df = pd.read_html(table.get_attribute('outerHTML'), header=0)[0]     

        print(webtable_df.columns.tolist())
        print(webtable_df.iloc[0])
        print(webtable_df.iloc[1])
        print(webtable_df.iloc[2])
        print("")
        webtable_df = webtable_df.iloc[1:]
        print(webtable_df.columns.tolist())
        print(webtable_df.iloc[0])
        print(webtable_df.iloc[1])
        print(webtable_df.iloc[2])   
    else: 
        print('DATAFRAME: param header = 1')
        webtable_df = pd.read_html(table.get_attribute('outerHTML'), header=1)[0]
    
    # duplicate values and fill empty rows
    webtable_clean = webtable_df.replace(np.nan,'EMPTY1234').replace('"', np.nan).ffill().replace('EMPTY1234', np.nan)
   
    # Change date format
    
    print(webtable_clean.columns.tolist())

    webtable_clean['Last update'] = pd.to_datetime(webtable_clean['Last update'])
    webtable_clean['Last update'] =  webtable_clean['Last update'].dt.strftime('%Y-%m-%d')
    #webtable_clean.iloc[:, 20] = pd.to_datetime(webtable_clean.iloc[:, 20],  format='%Y-%m-%d', errors='coerce')
    #webtable_clean.iloc[:, 20] =  webtable_clean.iloc[:, 20].dt.strftime('%Y-%m-%d')
       
    return webtable_clean



def pagination_total_pages(driver):
    logging.debug("pagination_total_pages(driver)")  

    SHORT_TIMEOUT  = 30   # give enough time for the loading element to appear
    #LONG_TIMEOUT = 30  # give enough time for loading to finish
    try:
        # wait for loading element to appear
        # - required to prevent prematurely checking if element
        #   has disappeared, before it has had a chance to appear
        WebDriverWait(driver, SHORT_TIMEOUT
            ).until(EC.presence_of_element_located((By.XPATH, '//*[@id="crud_list"]/div[2]')))
        #print("Element visible")
        # then wait for the element to disappear
        #WebDriverWait(driver, LONG_TIMEOUT).until(EC.invisibility_of_element_located((By.ID, "popup_wait")))
        #logging.debug("-> Popup not visible") 
    except TimeoutException:
        print("Timeout Exception")
        # if timeout exception was raised - it may be safe to 
        # assume loading has finished, however this may not 
        # always be the case, use with caution, otherwise handle
        # appropriately.
        pass     
    if driver.find_elements(By.XPATH, '//*[@id="crud_list"]/div[2]'):
        results_info = driver.find_element(By.XPATH, '//*[@id="crud_list"]/div[2]')
    
        #print(results_info.get_attribute('outerHTML'))
        print(results_info.text)
        cant_pages = results_info.text.split('/')[1]
        logging.info("Pages: {}".format(cant_pages))
        return(cant_pages)
    else:
        logging.error("not found: find_elements(By.XPATH, '//*[@id='crud_list']/div[2]'): ")
        return(-1)

def pagination_click_page(page_number):
    logging.debug("pagination_click_page(page_number): {}".format(page_number)) 
    #input("esperando..")
    try:
        if driver.find_elements(By.XPATH, '//*[@id="crud_list"]/nav/ul/li'):
            pagination = driver.find_elements(By.XPATH, '//*[@id="crud_list"]/nav/ul/li')
            #for pa in pagination:
            #    print('for 1: {}'.format(pa.text))

            scroll_down(driver)

            #input("avanzar...")
            sleep_custom(1)
            pagination = driver.find_elements(By.XPATH, '//*[@id="crud_list"]/nav/ul/li')
            for p in pagination:
 
                print('for 2: {}'.format(p.text))
                # element = WebDriverWait(driver, 30).until(
                #    EC.presence_of_element_located((By.XPATH, '//*[@id="crud_list"]/table'))
                # )
                
                if p.text == str(page_number):

                    print("Page: {}".format(p.text))
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(p)).click()
                    #p.click()
                    
                    SHORT_TIMEOUT  = 5   # give enough time for the loading element to appear
                    LONG_TIMEOUT = 30  # give enough time for loading to finish
                    try:
                        # wait for loading element to appear
                        # - required to prevent prematurely checking if element
                        #   has disappeared, before it has had a chance to appear
                        WebDriverWait(driver, SHORT_TIMEOUT
                            ).until(EC.presence_of_element_located((By.ID, 'popup_wait')))
                        #print("Element visible")
                        # then wait for the element to disappear
                        WebDriverWait(driver, LONG_TIMEOUT).until(EC.invisibility_of_element_located((By.ID, "popup_wait")))
                        logging.debug("-> Popup not visible") 
                    except TimeoutException:
                        print("Timeout Exception")
                        # if timeout exception was raised - it may be safe to 
                        # assume loading has finished, however this may not 
                        # always be the case, use with caution, otherwise handle
                        # appropriately.
                        pass 
                    break
    except Exception as e:
        print("Exception in pagination!")
        print(e)                
    

def scroll_down(driver):
    print("scroll_down(driver)")
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount==lenOfPage:
                match=True
    print("end scroll_down(driver)")


def create_search_terms():
    # Using readlines()
    file_paises = open('paises.txt', 'r')
    paises = file_paises.readlines()
    
    file_cultivos = open('cultivos.txt', 'r')
    cultivos = file_cultivos.readlines()
    
    dict_terms = []
    
    for pais in paises:
        # Strips the newline character
        for cultivo in cultivos:
            term = {"country": pais.strip(), "crop": cultivo.strip(), "status": 'Pendiente'}
            #print(term) 
            dict_terms.append(term)
    
    logging.info('Combinaciones de búsquedas creadas: %s', len(dict_terms))
    #logging.DEBUG(dict_terms)
    
    return dict_terms


def open_search_terms():
    file = open("export\searches.csv", "r")
    data = list(csv.DictReader(file, delimiter=","))
    file.close()
    #print(data)
    logging.info('Combinaciones de búsquedas encontradas: %s', len(data))
    cant_ready = 0
    cant_pending = 0
    for term in data: 
        if term['status'] == 'Ready':
            cant_ready += 1
        elif term['status'] == 'Pendiente':
            cant_pending +=1
    logging.info('Listas {},  Pendientes: {}'.format(cant_ready, cant_pending))        
    return data

""" def open_crops_countries(driver):
    # Using readlines()
    file_paises = open('paises.txt', 'r')
    paises = file_paises.readlines()
    
    file_cultivos = open('cultivos.txt', 'r')
    cultivos = file_cultivos.readlines()
    
    # Strips the newline character
    for pais in paises:
        # Strips the newline character
        for cultivo in cultivos:
            print("{}, {}".format(pais.strip(), cultivo.strip())) 
            search_an_save(driver, pais.strip(), cultivo.strip())  
    count = 0
    # Strips the newline character
    for pais in paises:
        count += 1
        #print("Line{}: {}".format(count, pais.strip()))
        count2 = 0
        # Strips the newline character
        for cultivo in cultivos:
            count2 += 1
            print("{}, {}".format(pais.strip(), cultivo.strip())) 
            search_an_save(driver, pais.strip(), cultivo.strip())   """

"""    
def search_an_save(driver, country, crop):
    global path
    print("")
    print("search_and_save(driver, {}, {})".format(country, crop))    
    run_search(driver, country, crop)
    sleep_custom(10)    
    #save_table_while(driver, country)
    
    total_pages = pagination_total_pages(driver)
    
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="crud_list"]/table'))
    )
    save_table_pandas(driver, country, crop, 0)
    print(country) 
    country_end_time = datetime.datetime.now()
    print (country_end_time) 
    
    return 1 """

def save_frame_to_csv(pd_frame, country, crop, page): 
    # Set filename
    crop_clean = crop.replace(':', '')
    filename = "".join([country,'_', crop_clean,'_', str(page), '.csv'])
    global path
    path_csv = path + "\\" + filename
    
    # Write() to CSV file
    pd_frame.to_csv(path_csv)
    # pd_frame['Last update'] = pd.to_datetime(pd_frame['Last update'])
    # pd_frame['Last update'] =  pd_frame['Last update'].dt.strftime('%Y-%m-%d')
    # save_frame_to_csv(pd_frame, 'CANADA', 'DATE', 'DATE')
    filename_excel = "".join([country,'_', crop_clean,'_', str(page), '.xlsx'])
    path_xls = path + "\\" + filename_excel
    pd_frame.to_excel (path_xls)






def search_an_save_pagination(driver, country, crop):
    global path
    print("")
    print("search_an_save_pagination(driver, {}, {})".format(country, crop))    

    
    country_crop_start_time = datetime.datetime.now()
    run_search(driver, country, crop)
    sleep_custom(13)
    #save_table_while(driver, country)


    SHORT_TIMEOUT  = 5   # give enough time for the loading element to appear
    LONG_TIMEOUT = 90  # give enough time for loading to finish
    try:
        # then wait for the element to disappear
        WebDriverWait(driver, LONG_TIMEOUT).until(EC.invisibility_of_element_located((By.ID, "popup_wait")))
        logging.debug("-> Popup not visible") 
    except TimeoutException:
        print("Timeout Exception")
        # if timeout exception was raised - it may be safe to 
        # assume loading has finished, however this may not 
        # always be the case, use with caution, otherwise handle
        # appropriately.
        pass 

    total_pages = pagination_total_pages(driver)
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="crud_list"]/table'))
    )
    pages_frames = []
    if int(total_pages) < 0:
        return -1
    elif int(total_pages) == 1:
        #save_table_pandas(driver, country, crop, 1)
        page_number = 1
        pd_frame = create_pandas_frame(driver, total_pages, page_number)
        pages_frames.append(pd_frame)
        #save_frame_to_csv(pd_frame, country, crop, 'ALL')
        #return 1
    elif int(total_pages) > 1:
        for page_number in range (1, int(total_pages)+1):
            print('Page number to click: {}'.format(page_number))
            pagination_click_page(page_number)
            print('Clicked')
            sleep_custom(10)
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="crud_list"]/table'))
            )
            #save_table_pandas(driver, country, crop, page_number)
            pd_frame = create_pandas_frame(driver, total_pages, page_number)     
            #save_frame_to_csv(pd_frame, country, crop, page_number)
            
            pages_frames.append(pd_frame)
            
    country_crop_end_time = datetime.datetime.now()
    country_crop_total_time = country_crop_end_time - country_crop_start_time
    logging.info("{} / {}.  {} pages. Total time: {}".format(country, crop, total_pages, country_crop_total_time))
    
    country_frame = pd.concat(pages_frames)
    save_frame_to_csv(country_frame, country, crop, 'ALL')
    
    return 1


def save_csv_terms_from_dict(terms):
    filename = "".join(['export\searches.csv'])
    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL, quotechar='"')
        # Strips the newline character
        wr.writerow(["country", "crop", "status"])
        for term in terms:
            wr.writerow([term['country'], term['crop'], term['status']]) 

def create_load_search_terms():
    # check whether directory already exists
    if not os.path.exists(path):
        os.mkdir(path)
        
        logging.info("Folder %s created!" % path)
        
    if os.path.isfile('export\searches.csv') == False:
        logging.info('Creando export\searches.csv desde paises.txt y cultivos.txt')
        terms = create_search_terms()
        save_csv_terms_from_dict(terms)
    else: 
        logging.info('export\searches.csv existe, retomando estado')
        terms = open_search_terms()
        #for term in terms: print(term)
    return terms




def check_liability_page(driver):
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/h1'))
    )
    if driver.find_elements(By.XPATH, '//*[@id="content"]/h1'):
        content_title = driver.find_element(By.XPATH, '//*[@id="content"]/h1')
        if content_title.text ==  title_terms_page:
            logging.info("{} section".format(title_terms_page))
            #print(content_title.text)
            button_display = driver.find_element(By.XPATH, '//*[@id="content"]/form/div/button')
            button_display.submit()
            sleep_custom(3)
        else:
            logging.debug("Title -{}- not found".format(title_terms_page))
    elif content_title.text == title_welcome_page:
        logging.info("{} section".format(title_welcome_page))
    else:
        logging.error("Pagina no esperada")
        input()
        exit()

def accept_all_cookies(driver):
    logging.info("Aceptando Cookies")
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="tarteaucitronPersonalize2"]'))
    )
    if driver.find_elements(By.XPATH, '//*[@id="tarteaucitronPersonalize2"]'):
        logging.debug('Cookie Button found, clicking')
        cookie_button = driver.find_element(By.XPATH, '//*[@id="tarteaucitronPersonalize2"]')
        cookie_button.click()

def salir():
    #time.sleep(10)
    print("Saliendo...")
    driver.quit()
    exit()

def check_input_files():
    existen = True
    if os.path.isfile('paises.txt') == False:
        logging.info('paises.txt no existe,  saliendo...')
        existen = False
    if os.path.isfile('cultivos.txt') == False:
        logging.info('cultivos.txt no existe,  saliendo...')
        existen = False
    return existen
    
terms = []

def menu(driver):
    try:
        print("")
        print("************MAIN MENU**************")
        #time.sleep(1)
        print()
        choice = input("""
                        A: Crear Terminos
                        A1: Imprimir Terminos                        
                        B: Login
                        C: Aceptar cookies
                        D: Check Liability page

                        E: Leer terminos y buscarlos PAGINADO

                        T: Secuencia Test
                        S: Secuencia completa
                        X: Salir del menu
                        Q: Quit

                        Please enter your choice: """)
        if choice == "A" or choice =="a":
            global terms
            terms = create_load_search_terms()
        if choice == "A1" or choice =="a1":
            for term in terms: print(term)
        elif choice == "B" or choice =="b":
            login(driver)
        elif choice == "C" or choice =="c":
            accept_all_cookies(driver)
        elif choice == "D" or choice =="d":        
           check_liability_page(driver)
        elif choice == "E" or choice =="e":
            read_terms_search_save(driver, terms) 
        elif choice == "S" or choice =="s":
            complete_run(driver)
        elif choice == "T" or choice =="t":
            login(driver)
            sleep_custom(10)
            accept_all_cookies(driver)
        elif choice=="X" or choice=="x":
            return
        elif choice=="Q" or choice=="q":
            salir()
        else:
            print("Debe seleccionar una opcion valida.")
            print("Pruebe de nuevo")
        menu(driver)
    except Exception as e:
        print("EXCEPCION!")
        print("EXCEPCION!")
        print(e)

def read_terms_search_save(driver, terms):
    for term in terms:
        
        pais = term['country']
        cultivo = term['crop']
        if term['status'] == 'Ready':
            print('{},{}: Skipped'.format(pais, cultivo)) 
            continue
        if pais != 'pais': 
            res = search_an_save_pagination(driver, pais, cultivo)
            if res == 1: 
                term['status']='Ready'
                #print(term)
                save_csv_terms_from_dict(terms)
            else:
                print("Error in search_an_save")
                term['status']='Error'
                print(term)
            random_sleep()


def complete_run(driver):
    if check_input_files() == False:
        return
    terms = create_load_search_terms()
    login(driver)
    logging.info("Title: {}".format(driver.title))
    sleep_custom(5)
    accept_all_cookies(driver)
    sleep_custom(3)
    check_liability_page(driver)
    start_time = datetime.datetime.now()
    logging.info(start_time) 
    read_terms_search_save(driver, terms)    
    end_time = datetime.datetime.now()
    logging.info("Finished")
    logging.info(end_time) 
    logging.info(end_time - start_time) 

cwd = os.getcwd()
path = cwd + "\export"
logging.info('Path is set to: %s', path)


driver = webdriver.Chrome()

#menu(driver)
complete_run(driver)


