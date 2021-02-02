import random
import re
import requests
import time
import colorama
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup as BS

class Codeforces:
    def __init__(self):
        self.session = requests.session()
        self.csrf_token_pattern = r'name=["\']csrf_token["\'] value=["\'](.*?)["\']'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        }
        self.programTypeId = {
            'GNU C11': 43,
            'Clang++17 Diagnostics': 52,
            'GNU C++11': 42,
            'GNU C++14': 50,
            'GNU C++17': 54,
            'GNU C++17 (64)': 61,
            'MS C++': 2,
            'MS C++ 2017': 59,
            'Mono C#': 9,
            'D': 28,
            'Go': 32,
            'Haskell': 12,
            'Java 11': 60,
            'Java 8': 36,
            'Kotlin': 48,
            'Ocaml': 19,
            'Delphi': 3,
            'FPC': 4,
            'PascalABC.NET': 51,
            'Perl': 13,
            'PHP': 6,
            'Python 2': 7,
            'Python 3': 31,
            'PyPy 2': 40,
            'PyPy 3': 41,
            'Ruby': 8,
            'Rust': 49,
            'Scala': 20,
            'JavaScript': 34,
            'Node.js': 55
        } 

    def login(self, username, password):
        self.username = username
        url = 'https://codeforces.com/enter'
        result = self.session.get(url, headers=self.headers)
        data = {
            'csrf_token': re.findall(self.csrf_token_pattern, result.text)[0],
            'action': 'enter',
            'handleOrEmail': username,
            'password': password,
        }
        self.session.post(url, data=data, headers=self.headers)

    def check_login(self):
        url = 'https://codeforces.com'
        result = self.session.get(url, headers=self.headers)
        if self.username in result.text:
            print(Fore.GREEN + 'Success!')
            print(Style.RESET_ALL, end = '')
            return True
        print(Fore.RED + 'Login failed!')
        print(Style.RESET_ALL, end = '')
        return False

    def submit(self, problem, code, language):
        url = 'https://codeforces.com/problemset/submit'
        result = self.session.get(url, headers=self.headers)
        data = {
            'csrf_token': re.findall(self.csrf_token_pattern, result.text)[0],
            'action': 'submitSolutionFormSubmitted',
            'submittedProblemCode': problem,
            'programTypeId': self.programTypeId[language],
            'tabSize': 4,
            'sourceFile': code, 
        }
        url = 'https://codeforces.com/problemset/submit?csrf_token=' + re.findall(self.csrf_token_pattern, result.text)[0]
        self.session.post(url, data=data, headers=self.headers)


if __name__ == '__main__':
    colorama.init()
    print('----Codeforces problem solving bot v1.1----')
    codeforces = Codeforces()
    lgn = input("Login: ")
    pas = input("Password: ")
    codeforces.login(lgn, pas)
    if codeforces.check_login():
        t = int(input("How many tasks to solve: "))
        print("Start solve {0} tasks... ".format(t))
        tasks = set()
        while True:
            r = requests.get('https://codeforces.com/problemset/status')
            html1 = BS(r.content, 'lxml')
            if len(tasks) == t:
                    break
            k = -1
            for el in html1.select('.status-frame-datatable')[0].find_all('tr'):
                if len(tasks) == t:
                    break
                k+=1
                if k == 0:
                    continue
                language = str(el.find_all('td')[4].get_text(strip = True))
                if language not in codeforces.programTypeId:
                    continue
                if len(el.select('.submissionVerdictWrapper')) == 0:
                    continue
                verdict = str(el.select('.submissionVerdictWrapper')[0]['submissionverdict'])
                if verdict != 'OK':
                    continue
                code = ""
                task = ""
                url = 'https://codeforces.com' + el.find('a', class_ = 'view-source')['href']
                r = requests.get(url)
                html = BS(r.content, 'lxml')
                task = html.find_all('a')[25].text
                code = html.select('.linenums')[0].text
                if ':' in task:
                    continue
                if task in tasks:
                    continue
                print('Left: ', t - len(tasks))
                tasks.add(task)
                codeforces.submit(task,code,language)
    print('Finish!')
    input("Press ENTER to exit: ")


#---- Выход ентер (если консоль)
#---- В конце текст готово (если консоль)
#---- Проверка на с++ (или языки)
# интерфейс
#---- список задач для сделания