from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from io import StringIO
import pandas as pd

email = 'aidenridgway22@gmail.com'
password = 'cARpeU9Vx!'
state = 'oh'


# Function to scrape data from the website
def scraper(start_month, start_day, start_year, end_month, end_day, end_year):

    # Designates Google Chrome as the browser used to access the page, then searches for the MRCC page.
    driver = webdriver.Chrome()
    driver.get("https://mrcc.purdue.edu/CLIMATE/")

    # Designates the text boxes for the email and password by searching for their id in inspect element.
    email_field = driver.find_element(by='id', value='textName')
    password_field = driver.find_element(by='id', value='textPwd')

    # Fills in the login info
    email_field.send_keys(email)
    password_field.send_keys(password)

    # Finds the login button using inspect element type, name, and value, and presses the button.
    login_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][name="Submit"][value="Log In"]')
    login_button.click()

    # Function to navigate the page, find the correct data, and scrape it
    def textGrabber(variable):

        # Navigates to the dd page
        driver.get("https://mrcc.purdue.edu/CLIMATE/nClimDiv/clidiv_daily_data.jsp")

        # Selects the state
        state_select = Select(driver.find_element(By.ID, 'selectState'))
        state_select.select_by_value(state)

        # Selects the start month
        mo1_select = Select(driver.find_element(By.ID, 'mo1'))
        mo1_select.select_by_value(start_month)

        # Selects the start day
        dy1_select = Select(driver.find_element(By.ID, 'dy1'))
        dy1_select.select_by_value(start_day)

        # Selects the start year
        yr1_select = Select(driver.find_element(By.ID, 'yr1'))
        yr1_select.select_by_value(start_year)

        # Selects the end month
        mo2_select = Select(driver.find_element(By.ID, 'mo2'))
        mo2_select.select_by_value(end_month)

        # Selects the end day
        dy2_select = Select(driver.find_element(By.ID, 'dy2'))
        dy2_select.select_by_value(end_day)

        # Selects the end year
        yr2_select = Select(driver.find_element(By.ID, 'yr2'))
        yr2_select.select_by_value(end_year)

        # Finds the appropriate radio button for the type of degree day
        radio_button = driver.find_element(By.CSS_SELECTOR,
                                           'input[name="variable"][type="radio"][value="' + variable + '"]')
        radio_button.click()

        # Submits the form
        submit_button = driver.find_element(By.ID, 'GetClimateData')
        submit_button.click()

        # Wait for the result to load
        element = driver.find_element(By.ID, 'result')

        # Extract text from the element
        ddText = element.text
        lines = ddText.split('\n')

        # Skip the first five lines
        lines = lines[6:]

        lines = lines[:-6]

        # Rejoin the lines into a single string
        table_text = '\n'.join(lines)

        return table_text.strip()

    # Clean up and convert the table data into DataFrames
    df1 = pd.read_csv(StringIO(textGrabber(variable='1')), delim_whitespace=True)

    print(df1)

    df2 = pd.read_csv(StringIO(textGrabber(variable='2')), delim_whitespace=True)
    print(df2)
    # Close the WebDriver to free up system resources
    driver.quit()

    # Combine the two DataFrames into one final DataFrame
    final_df = pd.concat([df1[['cd', 'DD', 'Normal', 'Departure', 'Percent']], df2[['DD', 'Normal', 'Departure', 'Percent']]], axis=1)

    # Rename the columns to have unique names
    final_df.columns = ['cd', 'W_DD', 'W_Normal', 'W_Departure', 'W_Percent', 'C_DD', 'C_Normal', 'C_Departure', 'C_Percent']

    # Display the DataFrame
    print(final_df)
    final_df.info()

    return final_df

