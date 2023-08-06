import time

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from talkytimes.base import AbstractAutomation


class TalkyTimesAutomation(AbstractAutomation):

    def login_task(self, *, user: str, pw: str) -> None:
        user_input = "/html/body/div[1]/div/div[1]/main/div/div/div/div/div[1]/div/div[1]/form/div/div[1]/div/input"
        pw_input = "/html/body/div[1]/div/div[1]/main/div/div/div/div/div[1]/div/div[1]/form/div/div[2]/div/input"
        login_button = "/html/body/div[1]/div/div[1]/main/div/div/div/div/div[1]/div/div[2]/button"
        self.driver.get(f"{self.url}/auth/login")
        time.sleep(2)
        self.driver.find_element(by=By.XPATH, value=user_input).send_keys(user)
        self.driver.find_element(by=By.XPATH, value=pw_input).send_keys(pw)
        self.driver.find_element(by=By.XPATH, value=login_button).click()
        time.sleep(2)
        print("profile logged")

    def save_users(self, *, count: int) -> None:
        next_button = "/html/body/div[1]/div/div[1]/main/div/div/div[1]/div/div[4]/button[12]"
        element_button = self.driver.find_element(by=By.CLASS_NAME, value='next')
        page_count = 0
        while element_button.is_enabled() and count > 0:
            try:
                page_count += 1
                time.sleep(2)
                users_list = self.driver.find_elements(By.CLASS_NAME, value="person-card")
                for _user in users_list:
                    if not count > 0:
                        return
                    user_url = _user.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
                    user_id = user_url.split("/")[-1]
                    status = _user.find_element(
                        by=By.CSS_SELECTOR,
                        value=".person-card__name svg"
                    ).value_of_css_property("fill")
                    status = True if status.__contains__("65") else False
                    self.db.create_or_update(profile=self.profile, external_id=user_id, status=str(status))
                    count -= 1
                time.sleep(2)
                self.driver.find_element(by=By.XPATH, value=next_button).click()
                element_button = self.driver.find_element(by=By.CLASS_NAME, value='next')
            except Exception as e:
                print("Error get users page", page_count, e)

    def save_user_chat(self):
        users = self.db.get_users()
        for user in users:
            external_id = user.get("id")
            user_info = user.get("user_info")
            status = user_info.get("user_status")
            url = f"{self.url}/user/id/{external_id}"
            self.driver.get(url)
            print(url)
            try:
                button_chat = "/html/body/div[1]/div/div[1]/main/div[2]/div/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/button"
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, button_chat)))
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_chat)))
                button_chat = self.driver.find_element(by=By.XPATH, value=button_chat)
                if not button_chat.text == "Change to mail":
                    button_chat.click()
                messages_text  = "scroll-button__text"
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, messages_text)))
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, messages_text)))
                user_pop = self.driver.find_element(
                    by=By.CLASS_NAME,
                    value=messages_text
                ).text

                user_pop_array = user_pop.split(" ")
                messages = "0"
                mails = "0"
                if not user_pop == "You can’t message inactive users":
                    if (user_pop_array[1] == "message") | (user_pop_array[1] == "messages"):
                        messages = user_pop_array[0]
                        if not user_pop_array[3] == "no":
                            mails = user_pop_array[3]
                    else:
                        if not user_pop_array[3] == "no":
                            messages = user_pop_array[3]
                        mails = user_pop_array[0]
                self.db.update_user(
                    profile=self.profile,
                    external_id=external_id,
                    status=status,
                    messages=messages,
                    emails=mails
                )
            except Exception as e:
                print(external_id, str(e))
