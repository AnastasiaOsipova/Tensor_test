from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
   


class FindHelpers:
    """ожидание появления элементов на странице"""
    def __init__(self, driver):
        self.driver = driver


    #поиск элемента с ожиданием
    def find_element_with_wait(self, selector, wait_time = 5):
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located(selector), 'Не дождались появления элемента')

    #поиск нескольких элементов с ожиданием
    def find_elements_with_wait(self, selector, wait_time = 5):
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_all_elements_located(selector), 'Не дождались появления элементов')
        

class YandexHeadPage(FindHelpers):
    """Главная страница Яндекса"""   
    def __init__(self, driver):
        FindHelpers.__init__(self, driver)

    search_window = (By.ID, 'text')
    propose_results = (By.CLASS_NAME, 'mini-suggest__popup_theme_tile')
    services = (By.CLASS_NAME, 'services-new__item-title')

    #вводим текст
    def input_text(self, text):
        input_string = self.find_element_with_wait(self.search_window)
        input_string.send_keys(text)
        return input_string

    #проверяем, выпадает ли таблицы с предложенными вариантами
    def check_suggest_table(self): 
        self.find_element_with_wait(self.propose_results)

    #click ENTER
    def click_enter(self, object):
        object.send_keys(Keys.ENTER)
    
    #находим иконки сервисов яндекса и перебираем их, пока не дойдем до картинок
    def click_menu_item(self, text):
        services_list = self.find_elements_with_wait(self.services)
        for service in services_list:
            if service.text == text:
                service.click()
                return 
        assert False, 'Ссылка "Картинки" не найдена'    
    

class YandexResultsPage(FindHelpers):
    """страница с результатами поиска""" 
    def __init__(self, driver):
        FindHelpers.__init__(self, driver)

    results = (By.CLASS_NAME, 'Path')
    text_link = (By.TAG_NAME, 'b')

    #проверяем текст первой ссылки
    def check_first_link(self, text):
        first_link = self.find_elements_with_wait(self.results)[0]   
        link_name = first_link.find_element(self.text_link[0], self.text_link[1])
        assert link_name.text == text + '.ru', 'первая ссылка не ведет на сайт Тензора'


class YandexImagePage(FindHelpers):
    """страница яндекс картинок"""
    def __init__(self, driver):
        FindHelpers.__init__(self, driver)

    all_offers = (By.CLASS_NAME, 'PopularRequestList-Shadow')
    category_name = (By.CLASS_NAME, 'PopularRequestList-SearchText')
        
    #проверяем, соответствует ли адрес текущей ссылки ожидаемому
    def compare_url(self, current_url):
        check_url = self.driver.current_url
        assert current_url in check_url
    
    #получаем имя нужной категории категории
    def get_category_name(self,number):  
        category = self.find_elements_with_wait(self.category_name)
        return category[number].text  

    #кликаем по нужной категории
    def open_category(self,number):
        result = self.find_elements_with_wait(self.all_offers) 
        result[number].click()

    

class YandexImageResultsPage(FindHelpers):
    """страница результатов поиска картинок"""
    def __init__(self, driver):
        FindHelpers.__init__(self, driver)   

    search_string = (By.CLASS_NAME, 'input__control')   
    image = (By.CLASS_NAME, 'justifier__thumb')
    images = (By.CSS_SELECTOR, '.serp-item__thumb.justifier__thumb')
    opened_image = (By.CSS_SELECTOR, 'img.MMImage-Origin')
    search_window = (By.CSS_SELECTOR, '') 
    next_button = (By.CLASS_NAME, 'MediaViewer-ButtonNext')
    last_button = (By.CLASS_NAME, 'MediaViewer-ButtonPrev')

    #проверяем соответствие названия категории и текста, отображаемого в строке поиска
    def check_category_name(self, category_name):
        input_string = self.find_element_with_wait(self.search_string)
        assert category_name == input_string.get_attribute('value'), 'Имя первой категории и название результатов поисков не совпадают'

    #открываем нужную по счету картинку 
    def open_image(self, number):
        image = self.find_elements_with_wait(self.image)
        image[number].click()

    #получаем адрес картинки
    def get_src(self): 
        current_pic = self.find_element_with_wait(self.opened_image)
        return current_pic.get_attribute('src')

    #перелистываем на следующую картинку
    def switch_next_image(self): 
        self.find_element_with_wait(self.next_button).click()

    #проверяем неравенство двух картинок
    def check_disequality_image(self, first_image, second_image):
        assert first_image != second_image, 'картинка не переключилась'    

    #перелистываем на предыдущую картинку
    def switch_last_image(self): 
        back = self.find_element_with_wait(self.last_button)
        back.click()

    #проверяем равенство двух картинок
    def check_equality_image(self, first_image, final_image): 
        assert first_image == final_image, 'отображается не первоначальная картинка'    




