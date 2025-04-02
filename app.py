from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.labirint.ru/rating/votes/"

try:
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "genres-carousel__item")))

    books_data = []

    books = driver.find_elements(By.CLASS_NAME, "genres-carousel__item")
    for book in books[:10]:
        try:
            title = book.find_element(By.CLASS_NAME, "book-qtip").text.strip()
        except:
            title = "N/A"

        try:
            author = book.find_element(By.CLASS_NAME, "genres-carousel-author").text.strip()
        except:
            author = "N/A"

        try:
            price = book.find_element(By.CLASS_NAME, "price-val").text.strip()
        except:
            price = "N/A"

        try:
            rating = book.find_element(By.CLASS_NAME, "rating-number").text.strip()
            rating = float(rating.replace(',', '.'))
        except:
            rating = 0.0

        if rating > 4.5:
            books_data.append({
                "Title": title,
                "Author": author,
                "Price": price,
                "Rating": rating
            })

finally:
    driver.quit()

if books_data:
    df = pd.DataFrame(books_data)
    df.to_csv("books_data.csv", index=False, encoding="utf-8")
    print("Данные успешно сохранены в файл 'books_data.csv'")
else:
    print("Нет данных для сохранения.")
