from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv


def VC_Questions(html_text):

    soup = BeautifulSoup(html_text, 'lxml')

    question = soup.select_one("h5", class_="vc-randomizer-h1").getText()
    answer = soup.select("p", class_="paragraph-2 blog-mobile vc-trainer")[1].get_text()

    QA_Dict = {
        "Question" : question,
        "Answer" : answer,
    }

    return QA_Dict


if __name__ == '__main__':
    list_of_dicts = []
    list_of_Q = []
    count = 0

    ### Get page first time
    link = "https://www.basetemplates.com/investor-pitch-training?ref=producthunt"
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get(link)


    while count < 2000:
        #time.sleep(0.5)
        html_text = driver.page_source
        QandA = VC_Questions(html_text)

        question = QandA["Question"]

        if question not in list_of_Q:
            list_of_dicts.append(QandA)
            list_of_Q.append(question)
            count = 0
        else:
            count += 1

        next_question = driver.find_element_by_class_name("form05_button-2")
        next_question.click()

    keys = list_of_dicts[0].keys()

    with open('BaseTemplatesQuestions.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)

