# Copyright (c) 2020 baozidai
# Timetable2020 is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from jiaowu import JiaoWu, Timetable

jw = JiaoWu("201803705", "d784512")
jw.get_sign_code()
jw.jiaowu_login()
# jw.get_term_cookies(xueqi="2019-2020-1")
# jw.get_term_lessons()
# index = [2, 9, 10, 11, 12]
# tb = Timetable(open("./Temp", "rt"), "lxml")
# for i in range(len(tb.soup.find_all("div")[2].find_all("table")[1].find_all("tr")) - 1):
#     a_course_info = tb.soup.find_all("div")[2].find_all("table")[1].find_all("tr")[i + 1].find_all("td")
#     if a_course_info[9].get_text() != "":
#         for j in index:
#             print(tb.soup.find_all("div")[2].find_all("table")[1].find_all("tr")[i + 1].find_all("td")[j].get_text(), end=" ")
#         print("")
# print(tb.soup.find_all("div")[2].find_all("table")[1].find_all("tr")[1].find_all("td")[2].get_text())  # 一门课的例子

#
#
# html body div div center table tbody tr td

# tb.process_html_normal_term()
jw.get_timetable()
tb = Timetable(open("Temp"))
tb.process_html()