# Copyright (c) 2020 baozidai
# Timetable2020 is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import os
from http import cookiejar
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable


def check(the_str, target, replacer):
    if the_str.find(target) > 0:
        return the_str.replace(target, replacer)
    else:
        return the_str


def rome_interger_replace(old_str: str):
    temp = old_str
    replace_dic = (["Ⅰ", "I"], ["Ⅲ", "III"], ["Ⅳ", "IV"])
    for i, j in replace_dic:
        temp = check(temp, i, j)
    return temp


def save_raw_html(res):
    with open("Temp", "wb+") as f:
        f.write(res.content)


class JiaoWu:
    """
    教务类: 用于教务网页的爬取相关工作(可能的联网工作以及其他的工作)
    """
    def __init__(self, user, pwd):
        self.header = {"Host": "jiaowu.sicau.edu.cn",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                       "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                       "Accept-Encoding": "gzip, deflate",
                       "Content-Type": "application/x-www-form-urlencoded",
                       "Content-Length": 76,
                       "Origin": "http://jiaowu.sicau.edu.cn",
                       "Connection": "keep-alive",
                       "Referer": "http://jiaowu.sicau.edu.cn/web/web/web/index.asp",
                       "Cookie": "Hm_lvt_20274609f261feba8dcea77ff3f7070c=1580478863,1580624298,1581235616,1581753905; ASPSESSIONIDCSSCRDQC=OGPFBJGDPAPAGNLKBJMGFGBF; jcrj%5Fzy=%BC%C6%CB%E3%BB%FA%BF%C6%D1%A7%D3%EB%BC%BC%CA%F5; jcrj%5Fxzy=%BC%C6%CB%E3%BB%FA%BF%C6%D1%A7%D3%EB%BC%BC%CA%F5; jcrj%5Ftemp=9718438982; jcrj%5Fxueqi=2019%2D2020%2D2; jcrj%5Fxm=%B4%F7%C1%FA%D6%C1; jcrj%5Fxt%5Fxxq=%D1%C5%B0%B2; jcrj%5Fxt%5Ffb=%D1%C5%B0%B2; jcrj%5Fbanhao=%BC%C6%CB%E3%BB%FA201802; jcrj%5Fuser=201803705; jcrj%5Fpwd=171919; jcrj%5Fauth=True; jcrj%5Fnj=2018; jcrj%5Fsession=jwc%5Fcheck%2Cauth%2Cuser%2Cpwd%2Cxt%5Ffb%2Cxt%5Fxxq%2Csf%2Cxueqi%2Csf%5Fpj%2Ctemp%2Cxm%2Cnj%2Cbanhao%2Cxibie%2Czy%2Cxzy%2Cjwc%5Fcheck%2Ctymfg%2Cxk%5Fzy%2Cxk%5Fcongxiu%2C; jcrj%5Fsf=%D1%A7%C9%FA; jcrj%5Fjwc%5Fcheck=y; jcrj%5Fxibie=%D0%C5%CF%A2%B9%A4%B3%CC%D1%A7%D4%BA; jcrj%5Fsf%5Fpj=%B7%F1; jcrj%5Ftymfg=%C0%B6%C9%AB%BA%A3%CC%B2; jcrj%5Fxk%5Fcongxiu=%3F%3F; jcrj%5Fxk%5Fzy=%3F%3F; Hm_lpvt_20274609f261feba8dcea77ff3f7070c=1581753905",
                       "Upgrade-Insecure-Requests": 1}
        self.cookieJar = cookiejar.CookieJar()
        self.request_operator = requests.session()
        self.user = user
        self.pwd = pwd
        self.request_operator.headers = self.header
        self.sign = ""  # 登陆需要的一个神秘代码，在教务网获得，有时效

    def jiaowu_login(self, url="http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp", lb="S"):
        """
        教务登陆,实例化教务类的session(cookie相关)
        :param url: 登陆API
        :param lb: 登陆身份 另一个是T 教师
        :return:
        """
        data = {"user": self.user, "pwd": self.pwd, "lb": lb, "sign": self.sign}
        self.request_operator = requests.session()
        x = self.request_operator.post(url, data=data)
        x.raise_for_status()
        x.encoding = x.apparent_encoding

    def get_timetable(self, url="http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/zxian_rw_list.asp"):
        """
        获取2020在线网课课表
        :param url: API
        :return:
        """
        x = self.request_operator.get(url)
        x.raise_for_status()
        x.encoding = x.apparent_encoding
        save_raw_html(x)

    def get_sign_code(self):
        """
        取得登录神秘代码
        :return:
        """
        url = "http://jiaowu.sicau.edu.cn/web/web/web/index.asp"
        x = requests.get(url)
        with open("Temp", "wb+") as f:
            f.write(x.content)
        file = open("./Temp", "rb")
        soup = BeautifulSoup(file, "html.parser")
        self.sign = soup.form.find_all("input")[-1]["value"]

    def get_term_lessons(self, url="http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/xuankeshow.asp"):
        """
        取得课程列表，需要前置执行 get_term_cookies
        :param url:
        :return:
        """
        x = self.request_operator.get(url)
        x.raise_for_status()
        x.encoding = x.apparent_encoding
        save_raw_html(x)

    def get_term_cookies(self, xueqi="", api="http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/xszhinan.asp"):
        """
        取得某一学期的cookie,实现分学期选课
        :param xueqi: 学期 上学期是1 下学期是2 2019-2020-1 2019-2020-2
        :param api:
        :return:
        """
        # cookie获得 http://jiaowu.sicau.edu.cn/xuesheng/gongxuan/gongxuan/xszhinan.asp?xueqi=2019-2020-2
        url = api + "?" + xueqi
        x = self.request_operator.get(url)
        x.raise_for_status()


class Timetable:
    def __init__(self, raw_file, parser="html.parser"):
        self.raw_file = raw_file
        self.soup = BeautifulSoup(raw_file, parser)
        self.baked_data = None

    def process_html(self):  # 处理网课课表的HTML文件
        ptb = PrettyTable()
        ptb.field_names = ["课程",
                           "教师",
                           "周次",
                           "上课时间",
                           "QQ群号",
                           "开课网址"
                           ]
        index = [2, 4, 5, 6, 12, 13]
        for i in range(len(self.soup.find_all('table')[5].find_all('tr')) - 1):
            i += 1
            one_lesson = []
            for j in index:
                one_lesson.append(self.soup.find_all('table')[5].find_all('tr')[i].find_all('td')[j].get_text())
            ptb.add_row(one_lesson)
        print(ptb)

    def process_html_normal_term(self):  # 处理常规课表HTML
        # TODO： 解析数据形成json或者其他格式
        """
        解析正常的课表
        :return:
        """

        ptb = PrettyTable(encoding="UTF-8")
        ptb.field_names = ["课程",
                           "性质",
                           "上课时间",
                           "教室",
                           "周次",
                           "教师"
                           ]
        index = [2, 3, 9, 10, 11, 12]
        for i in range(len(self.soup.find_all("div")[2].find_all("table")[1].find_all("tr")) - 1):
            a_course_info = self.soup.find_all("div")[2].find_all("table")[1].find_all("tr")[i + 1].find_all("td")
            one_lesson = []
            if a_course_info[9].get_text() != "":
                for j in index:
                    temp: str = self.soup.find_all("div")[2].find_all("table")[1].find_all("tr")[i + 1].find_all("td")[
                        j].get_text()
                    temp = rome_interger_replace(temp)
                    one_lesson.append(temp)
                ptb.add_row(one_lesson)
        print(ptb)


if __name__ == "__main__":
    user = input("请输入学号\n")
    pwd = input("请输入密码\n")
    jw = JiaoWu(user, pwd)
    jw.get_sign_code()
    jw.jiaowu_login()
    jw.get_timetable()
    tb = Timetable(open("./Temp", "rb"))  # 若需要封装exe,必修按 rb 形式读出
    tb.process_html()
    os.system("pause")
