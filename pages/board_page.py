"""Page Object для работы с досками YouGile."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import allure
from .base_page import BasePage


class BoardPage(BasePage):
    """Page Object для страницы работы с досками."""

    # ЛОКАТОРЫ
    CREATE_BOARD_BUTTON = (By.CSS_SELECTOR, "[data-qa='create-board-btn'], .create-board-btn")
    BOARD_TITLE_INPUT = (By.CSS_SELECTOR, "input[name='title'], [data-qa='board-title-input']")
    BOARD_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea[name='description']")
    SUBMIT_CREATE_BUTTON = (By.CSS_SELECTOR, "[data-qa='submit-board-btn'], button[type='submit']")
    BOARD_ITEM = (By.CSS_SELECTOR, ".board-item, [data-qa='board-item']")
    MODAL_WINDOW = (By.CSS_SELECTOR, ".modal-content, .ant-modal-content")
    ERROR_FIELD = (By.CSS_SELECTOR, ".has-error, .error-field, .ant-form-item-has-error")

    @allure.step("Открыть модальное окно создания доски")
    def open_create_board_modal(self) -> None:
        """Открывает окно создания новой доски."""
        self.find_element(self.CREATE_BOARD_BUTTON).click()

    @allure.step("Создать доску с названием '{title}'")
    def create_board(self, title: str, description: str = "") -> None:
        """Создаёт новую доску с заданным названием."""
        self.find_element(self.BOARD_TITLE_INPUT).send_keys(title)
        if description:
            self.find_element(self.BOARD_DESCRIPTION_INPUT).send_keys(description)
        self.find_element(self.SUBMIT_CREATE_BUTTON).click()

    @allure.step("Проверить наличие доски с названием '{title}'")
    def is_board_present(self, title: str) -> bool:
        """Проверяет, существует ли доска с заданным названием."""
        boards = self.driver.find_elements(*self.BOARD_ITEM)
        for board in boards:
            if title in board.text:
                return True
        return False

    @allure.step("Проверить подсветку поля с ошибкой")
    def is_title_field_highlighted_error(self) -> bool:
        """Проверяет, подсвечено ли поле названия как ошибочное."""
        try:
            field = self.find_element(self.BOARD_TITLE_INPUT, timeout=2)
            parent = field.find_element(By.XPATH, "./..")
            return "error" in parent.get_attribute("class").lower()
        except Exception:
            return False

    @allure.step("Проверить, открыто ли модальное окно")
    def is_create_modal_still_open(self) -> bool:
        """Проверяет, осталось ли открытым модальное окно создания."""
        try:
            return self.find_element(self.MODAL_WINDOW, timeout=2).is_displayed()
        except Exception:
            return False