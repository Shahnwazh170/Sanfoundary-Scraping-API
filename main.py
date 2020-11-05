# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from bs4 import BeautifulSoup
import requests

OPTIONS = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
}


def get_answers(soup):
    data_ = []
    divs = soup.find(['div', 'p'], class_=["entry-content", "collapseomatic_content "])
    all_exp = divs.find_all('div', class_='collapseomatic_content')
    for i in all_exp:
        d = {}
        temp = i.text.strip().splitlines()
        d["answer"] = OPTIONS[temp[0][-1]]
        d["explanation"] = temp[1][13::]
        data_.append(d)
    return data_


def process_options(options):
    res = []
    for i in options:
        res.append(i[3::])
    return res


def get_data(url, quiz_size):
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'lxml')

    divs = soup.find(['div', 'p'], class_=["entry-content", "collapseomatic_content "])
    # print(divs.prettify())
    all_p = divs.find_all('p')
    quiz = []

    data_ = {'title': all_p[0].text.strip().splitlines()[0]}
    size = 0
    for i in all_p[1::]:
        if size < quiz_size:
            try:
                t = i.text.strip().splitlines()
                t.pop()
                question = t[0::-4]
                temp = {'question': question, 'options': process_options(t[-4::])}
                quiz.append(temp)
            except:
                pass
            size += 1
        else:
            break
    data_['quiz'] = quiz
    answers = get_answers(soup)
    for i in range(quiz_size):
        quiz[i].update(answers[i])

    # print(answers)
    print(quiz)
    print(data_)


if __name__ == '__main__':
    get_data("https://www.sanfoundry.com/data-structure-questions-answers-single-linked-lists/", 11)
