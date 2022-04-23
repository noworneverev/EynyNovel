from ast import Return
import requests
import bs4
import sys
import pathlib
import os.path


# base_url = "http://www.eyny.com/forum.php?mod=viewthread&tid=12203064&extra=&page="
base_url = "http://www.eyny.com/forum.php?mod=viewthread&tid="
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def get_cookie():
    cookie = {}
    is_exist = False
    # dir = pathlib.Path(__file__).parent.resolve()
    dir = os.path.dirname(sys.executable)        
    is_exist = os.path.isfile(f"{dir}\\cookie.txt") 
    if not is_exist:
        return cookie, is_exist

    with open(f'cookie.txt', mode='r',encoding="utf-8") as myfile:
        cookies = myfile.read().split(';')
        for c in cookies:
            split = c.split('=')
            if len(split) == 2:
                cookie[split[0]] = split[1]
    return cookie, is_exist

def get_title_and_lastpage(cookie, headers, id):
    title = ''
    lastpage = -1

    # get title and last page number
    res = requests.get(f"{base_url}{id}&extra=&page={1}",cookies=cookie,headers=headers)
    soup = bs4.BeautifulSoup(res.text,"lxml")
    title = soup.find("meta", attrs= {"name":"keywords"})
    title = title["content"] if title else "Default Title"
    # lastpage =  soup.find_all("a", {"class": "last"})[0].get_text().split(' ')[1]
    lastpage =  soup.find_all("a", {"class": "last"})
    lastpage =  int(lastpage[0].get_text().split(' ')[1]) if lastpage else -1
    return title, lastpage

def crawl(cookie, headers, id):
    context = ''
    printProgressBar(0,1, prefix = 'Progress:', suffix = 'Complete', length = 50)
    title, lastpage = get_title_and_lastpage(cookie, headers, id)

    if lastpage < 0 :
        return title, context

    for i in range(1, lastpage + 1):
        res = requests.get(f"{base_url}{id}&extra=&page={1}",cookies=cookie,headers=headers)
        soup = bs4.BeautifulSoup(res.text,"lxml")
        for text in soup.find_all("td", class_="t_f"):
            context += text.get_text() + '\n\n'
        printProgressBar(i, lastpage, prefix = 'Progress:', suffix = 'Complete', length = 50)
    return title, context       

def scraping_eyny(id):    
    cookie, is_exist = get_cookie()

    if not is_exist:
        print('目前資料夾無cookie.txt檔案！')
        return

    if not cookie:
        print('cookie.txt 內容無法判讀, 請以分號";"隔開各key-value pair, 例: xxx=yyy; aaa=bbb; ccc=ddd')
        return

    headers={"User-Agent":user_agent}
    
    title, context = crawl(cookie, headers, id)
    
    if context:
        with open(f'{title}.txt', mode='w+',encoding="utf-8") as myfile:
            myfile.write(context)
        print(f"{title}.txt 已完成")
    else:
        print('搜尋無內容，請確認小說編號後再試一次。')


if __name__ == '__main__':        
    if len(sys.argv) == 1:
        print('請輸入小說編號！')
        sys.exit()
    elif len(sys.argv) > 2:
        print('過多引數，請輸入一個小說編號')
        sys.exit()
    else:
        id = sys.argv[1]
        scraping_eyny(id) 