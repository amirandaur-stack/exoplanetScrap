import time
import requests
import re
import csv
import config
from bs4 import BeautifulSoup 

def get_all_planets_data(from_year, to_year) :
    
    current_year = to_year
    planet_list = []
    while current_year >= from_year:
        print(f"Extracting data for {current_year} \n")
        exoplanets_content = get_exoplanets(current_year)
    
        soup = BeautifulSoup(exoplanets_content, 'html.parser')

        table = soup.find("table",  class_="starlist2")
        for row in table.findAll("tr"):
            cells = row.findAll('td')
            if len(cells)==5:
                exoplanet_name = cells[1].get_text(strip=True)
                exoplanet_date = cells[2].get_text(strip=True)  
                sub = cells[3].find('sub')
                if sub:
                    sub.extract()
                exoplanet_mass = cells[3].get_text(strip=True)
                exoplanet_distance = cells[4].get_text(strip=True)
                link_planet = cells[1].find('a')['href']     

                planet_extra_content = get_exoplanet_extra(link_planet)
                soup_planet = BeautifulSoup(planet_extra_content, 'html.parser')
          
                extra_value = soup_planet.find("div", class_="starInfo")
                star = get_extra_value_or_default(extra_value, "Star:")
                size = get_extra_value_or_default(extra_value, "Size:")
                temp = get_extra_value_or_default(extra_value, "Temperature:")
                density = get_extra_value_or_default(extra_value, "Density:")
                year = get_extra_value_or_default(extra_value, "Year of discovery:")             

                element = [exoplanet_name, 
                           exoplanet_date, 
                           exoplanet_mass, 
                           exoplanet_distance, 
                           star, 
                           size, 
                           temp, 
                           density, 
                           year]
                planet_list.append(element)
                print(f"Data extracted for plane {exoplanet_name}")

        print(f"Extracted data for {current_year} \n")
        current_year -= 1

    save_to_file(planet_list)

def get_extra_value_or_default(extract_data_info, text_value) : 
    if extract_data_info == "" :
        return ""
    
    extra_ctrl = extract_data_info.find_all(string=re.compile(text_value))
    if len(extra_ctrl) > 0:
        return extra_ctrl[0].parent.get_text(strip=True).replace(text_value, "")
    else :
        return ""

def get_exoplanets(year) :    
    t_init = time.time()

    full_query_URL = f"{config.query_URL}/exoplanets.php?list={config.exoplanet_list}&year={year}"
    headers = requests.utils.default_headers().update({'User-Agent':config.user_agent})
    r = requests.get(full_query_URL, headers=headers)

    response_delay = time.time() - t_init
    time.sleep(2 * response_delay)

    return r.content

def get_exoplanet_extra(link_planet) :
    t_init = time.time()

    full_query_planet_URL = f"{config.query_URL}/{link_planet}"
    headers = requests.utils.default_headers().update({'User-Agent':config.user_agent})
    r_planet = requests.get(full_query_planet_URL, headers=headers)        
          
    response_delay = time.time() - t_init
    time.sleep(config.waiting_delay_mult * response_delay)    

    return r_planet.content

def save_to_file(planet_list) :
    with open(config.file_path, 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        for planet in planet_list:
            writer.writerow(planet)  