from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

count = 1

# 配置 ChromeDriver
chrome_driver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")

# 初始化 WebDriver
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.douban.com")
time.sleep(3)
input("请手动登录豆瓣，登录成功后按回车键继续...")

# 目标影评页面
movie_url = "https://movie.douban.com/subject/34780991/reviews"
driver.get(movie_url)

time.sleep(5)

wait = WebDriverWait(driver, 10)
reviews_data = []

while True:
    try:
        reviews = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "review-item"))
        )
        for review in reviews:
            try:
                review_link = review.find_element(
                    By.CSS_SELECTOR, "h2 a"
                ).get_attribute("href")
                driver.execute_script(
                    "window.open('{}', '_blank');".format(review_link)
                )
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(10)

                title, rating, review_content, upvote, downvote = (
                    "默认标题",
                    "默认评分",
                    "默认评价",
                    "默认赞成",
                    "默认反对",
                )

                try:
                    content = driver.find_element(By.CLASS_NAME, "article")
                    title = content.find_element(By.TAG_NAME, "h1").text

                    try:
                        rating_element = content.find_element(
                            By.CLASS_NAME, "main-title-rating"
                        )
                        rating_class = rating_element.get_attribute("class")
                        rating = rating_class.split(" ")[0].split("ar")[1]
                    except:
                        rating = "0"

                    review_content_element = content.find_element(
                        By.CLASS_NAME, "review-content"
                    )
                    review_content = "\n".join(
                        [
                            p.text
                            for p in review_content_element.find_elements(
                                By.TAG_NAME, "p"
                            )
                        ]
                    )
                    upvote = (
                        content.find_element(By.CLASS_NAME, "useful_count").text.split(
                            " "
                        )[1]
                        or "0"
                    )
                    downvote = (
                        content.find_element(By.CLASS_NAME, "useless_count").text.split(
                            " "
                        )[1]
                        or "0"
                    )

                    print(
                        count,
                        " 抓取成功",
                        title,
                        rating,
                        upvote,
                        downvote,
                        len(review_content),
                    )
                    count += 1
                except:
                    print(f"数据异常: {review_link}")
                    print(
                        "异常数据: ",
                        title,
                        rating,
                        upvote,
                        downvote,
                        len(review_content),
                    )

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                reviews_data.append([title, rating, upvote, downvote, review_content])
            except Exception as e:
                print(f"跳过异常影评: {e}")

        next_button = driver.find_element(By.CSS_SELECTOR, ".next")
        if "disabled" in next_button.get_attribute("class"):
            break
        next_button.click()
        time.sleep(10)
    except Exception as e:
        print(f"遇到异常: {e}")
        break

driver.quit()

# 保存数据到 CSV 文件
file_path = "douban_reviews.csv"
df = pd.DataFrame(
    reviews_data, columns=["title", "rating", "upvote", "downvote", "review"]
)
mode, header = ("a", False) if os.path.exists(file_path) else ("w", True)
df.to_csv(file_path, index=False, encoding="utf-8-sig", mode=mode, header=header)

print("影评数据已保存到 douban_reviews.csv")
