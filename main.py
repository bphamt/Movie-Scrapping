from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

CHROME_DRIVER_PATH = r"C:\Users\bpham\Documents\chromedriver"
URL_SCRAPE = "https://www.empireonline.com/movies/features/best-movies-2/"

# Movie list
movie_list = []
order_move_list = []

# Run not headless
# driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
# driver.implicitly_wait(30)

# Run headless
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options, executable_path=CHROME_DRIVER_PATH)

# Grab web data
driver.get(URL_SCRAPE)

# Accept the privacy popup box
# Switch to the iframe of the popup box
driver.switch_to.frame("sp_message_iframe_438751")
# Grab the xpath of the accept all button
accept_button = driver.find_element_by_xpath('/html/body/div/div[3]/div[5]/button[2]')
# Press the accept all button
driver.execute_script("arguments[0].click();", accept_button)
# Switch back to main content
driver.switch_to.default_content()

# Grab element by tag h3
article = driver.find_elements_by_tag_name("h3")

for i in article:
    text = i.text
    # Split text that has either a ":" or ")" in the string
    splitting = (re.split(":|\\)", text))

    # First append if there is an index of 1 & 2, for example ['23', 'The Lord Of The Rings', 'The Two Towers']
    try:
        movie_list.append(f"{splitting[1]}:{splitting[2]}")
    # If there is no Index of 1 or 2
    except IndexError:
        try:
            # Append the 1st index for example ["100", "Stand By Me"]
            movie_list.append(f"{splitting[1]}")
        except IndexError:
            # Append the 0th index for example ["The Godfather"]
            movie_list.append(f"{splitting[0]}")
    finally:
        # Reverse the movie_list
        movie_list.reverse()

for i in range(len(movie_list)):
    # Strip whitespace infront of every string
    movie_list[i] = movie_list[i].lstrip()

    # Add number in front of string
    ordered_string = ''.join((f'{i + 1}: ', f"{movie_list[i]}"))
    order_move_list.append(ordered_string)

# Save data into movies.txt file in order
with open("movies.txt", 'w') as file:
    for item in order_move_list:
        file.write("%s\n" % item)

# Close out of Selenium after it's done
driver.quit()
