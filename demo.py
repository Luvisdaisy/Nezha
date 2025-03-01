while True:
    try:
        reviews = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "review-item")))
        for review in reviews:
            try:
                review_link = review.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
                driver.execute_script("window.open('{}', '_blank');".format(review_link))
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(10)
                title, rating, review_content, upvote, downvote = "默认标题", "默认评分", "默认评价", "默认赞成", "默认反对"
                try:
                    content = driver.find_element(By.CLASS_NAME, "article")
                    title = content.find_element(By.TAG_NAME, "h1").text
                    try:
                        rating_class = content.find_element(By.CLASS_NAME, "main-title-rating").get_attribute("class")
                        rating = rating_class.split(" ")[0].split("ar")[1]
                    except:
                        rating = "0"
                    review_content = "\n".join([p.text for p in content.find_element(By.CLASS_NAME, "review-content").find_elements(By.TAG_NAME, "p")])
                    upvote = content.find_element(By.CLASS_NAME, "useful_count").text.split(" ")[1] or "0"
                    downvote = content.find_element(By.CLASS_NAME, "useless_count").text.split(" ")[1] or "0"
                    print(count, "抓取成功", title, rating, upvote, downvote, len(review_content))
                    count += 1
                except:
                    print(f"数据异常: {review_link}", "异常数据: ", title, rating, upvote, downvote, len(review_content))
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                reviews_data.append([title, rating, upvote, downvote, review_content])
            except Exception as e:
                print(f"跳过异常影评: {e}")
        next_button = driver.find_element(By.CSS_SELECTOR, ".next")
        if "disabled" in next_button.get_attribute("class"): break
        next_button.click()
        time.sleep(10)
    except Exception as e:
        print(f"遇到异常: {e}")
        break