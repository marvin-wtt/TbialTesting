from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username_prefix = 'test'
username_suffix = ''
password = 'password'
num_players = 4
app_url = "http://localhost:8080/"
game_name = "Test Game"


def login(driver, username):
    # Click on the "Sign in" button
    sign_in_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Sign in")]'))
    )
    sign_in_link.click()

    # Enter the username
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]'))
    )
    username_input.send_keys(username)

    # Enter the password
    password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    password_input.send_keys(password)

    # Click the "Log in" button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'vaadin-button[part="vaadin-login-submit"]'))
    )
    login_button.click()

    # Wait to be back on root page
    WebDriverWait(driver, 10).until(EC.url_to_be(app_url))


def create_lobby(driver: any, name: str, max_players: int):
    # Click on the "New Game" button
    new_game_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//vaadin-button[text()="New game"]'))
    )
    new_game_button.click()

    # Enter the lobby name
    lobby_name_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"]#input-vaadin-text-field-9'))
    )
    lobby_name_input.clear()
    lobby_name_input.send_keys(name)

    # Click the max players button
    max_players_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//vaadin-button[contains(text(), "{max_players}")]'))
    )
    max_players_button.click()

    # Click the "Public" button
    public_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//vaadin-button[contains(text(), "Public")]'))
    )
    public_button.click()

    # Click the "Create" button
    create_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//vaadin-button[contains(text(), "Create")]'))
    )
    create_button.click()


def join_lobby(driver, lobby_name: str):
    # Click on the lobby name
    lobby_name_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//*[text()="{lobby_name}"]'))
    )
    lobby_name_element.click()

    # Click on the "Join" button
    join_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//vaadin-button[contains(text(), "Join")]'))
    )
    join_button.click()


def start_game(driver):
    # Click on the "Join" button
    join_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//vaadin-button[contains(text(), "Start")]'))
    )
    join_button.click()

    WebDriverWait(driver, 10).until(EC.url_to_be(app_url+"game-table"))


def create_tab(index: int):
    # Create Firefox options object
    options = Options()

    # Disable sharing of profiles between instances
    options.set_preference("browser.link.open_newwindow", 3)

    # Create a new browser instance with the specified options
    driver = webdriver.Firefox(options=options)
    # Open aoo
    driver.get(app_url)

    return driver


def main():
    # Loop through the desired number of tabs and perform the automation
    drivers = []
    for i in range(1, num_players + 1):
        driver = create_tab(i)
        drivers.append(driver)

    # Login
    for i in range(1, num_players + 1):
        username = f"{username_prefix}{i}{username_suffix}"
        login(drivers[i - 1], username)

    # Create lobby
    create_lobby(drivers[0], game_name, num_players)

    # Join lobby
    for i in range(2, num_players + 1):
        join_lobby(drivers[i - 1], game_name)

    # Start game
    start_game(drivers[0])


if __name__ == '__main__':
    main()
