
import datetime
import funcs
import config

current_year = datetime.datetime.now().year
from_year = config.min_year
to_year = current_year

from_year_str = input("Select year from (1992 by default): ")
try:    
    from_year = int(from_year_str)

    if from_year < config.min_year :
        from_year = config.min_year
    elif from_year > current_year:
        from_year = current_year     
except :
    from_year = config.min_year

to_year_str = input("Select year to (current year by default): ")
try:    
    to_year = int(to_year_str)

    if to_year < config.min_year :
        to_year = config.min_year    
    elif to_year > current_year:
        to_year = current_year 
    elif to_year < from_year:
        to_year = from_year             
except :
    to_year = current_year


print (f"Reading exoplanets from {from_year} to {to_year}")

funcs.get_all_planets_data(from_year, to_year)

print ("Exoplanet list completed!")