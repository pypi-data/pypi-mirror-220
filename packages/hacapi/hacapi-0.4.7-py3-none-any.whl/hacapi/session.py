import requests
from bs4 import BeautifulSoup
from . import payloads

class Session():
    def __init__(self, username, password, session_requests=requests.session()):
        self.username = username
        self.password = password
        self.session_requests = session_requests
        self.login_url = 'https://hac.friscoisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f'

        result = self.session_requests.get(self.login_url)
        tree = BeautifulSoup(result.text, "html.parser")
        authenticity_token = tree.select_one("input[name='__RequestVerificationToken']")["value"]

        login_payload = {
            "VerificationOption": "UsernamePassword",
            "Database": "10",
            "LogOnDetails.Password": self.password,
            "__RequestVerificationToken": authenticity_token,
            "LogOnDetails.UserName": self.username
        }

        self.session_requests.post(self.login_url, data=login_payload, headers={"referer": self.login_url})

    def return_to_current(self):
        urls = "https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx"
        return self.session_requests.get(urls, headers={"referer": urls})

    def return_username(self):
        return self.username

    def reset(self):
        self.session_requests = requests.session()

    def _return_html(self):
        urls = "https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx"

        result = self.session_requests.get(urls, headers={"referer": urls})

        soup = BeautifulSoup(result.text, "html.parser")

        grades_html = soup.find_all(class_="sg-header-heading sg-right")
        name_html = soup.find_all('a', class_="sg-header-heading")

        return grades_html, name_html

    def _initialize_classes(grades_html, names_html):
        class1 = 0
        try:
            class1 = str(grades_html[0])
            class1 = class1[116:121]
        except IndexError:
            print("Enter a valid six digit Student ID and password!")
            exit(0)

        class2 = "0"
        try:
            class2 = str(grades_html[1])
            class2 = class2[116:121]
            if class2 == "":
                class2 = "0"
        except IndexError:
            pass

        class3 = "0"
        try:
            class3 = str(grades_html[2])
            class3 = class3[116:121]
            if class3 == "":
                class3 = "0"
        except IndexError:
            pass

        class4 = "0"
        try:
            class4 = str(grades_html[3])
            class4 = class4[116:121]
            if class4 == "":
                class4 = "0"
        except IndexError:
            pass

        class5 = "0"
        try:
            class5 = str(grades_html[4])
            class5 = class5[116:121]
            if class5 == "":
                class5 = "0"
        except IndexError:
            pass

        class6 = "0"
        try:
            class6 = str(grades_html[5])
            class6 = class6[116:121]
            if class6 == "":
                class6 = "0"
        except IndexError:
            pass

        class7 = "0"
        try:
            class7 = str(grades_html[6])
            class7 = class7[116:121]
            if class7 == "":
                class7 = "0"
        except IndexError:
            pass

        class8 = "0"
        try:
            class8 = str(grades_html[7])
            class8 = class8[116:121]
            if class8 == "":
                class8 = "0"
        except IndexError:
            pass

        class_name_1 = "No class"
        try:
            class_name_1 = (str(names_html[0].text)).strip()
            index_of_deletion = class_name_1.index("-")
            class_name_1 = (class_name_1[index_of_deletion + 4:]).strip()
        except IndexError:
            pass

        class_name_2 = "No class"
        try:
            class_name_2 = (str(names_html[1].text)).strip()
            index_of_deletion = class_name_2.index("-")
            class_name_2 = (class_name_2[index_of_deletion + 4:]).strip()
        except IndexError:
            pass

        class_name_3 = "No class"
        try:
            class_name_3 = (str(names_html[2].text)).strip()
            index_of_deletion = class_name_3.index("-")
            class_name_3 = (class_name_3[index_of_deletion + 4:]).strip()
        except IndexError:
            pass

        class_name_4 = "No class"
        try:
            class_name_4 = (str(names_html[3].text)).strip()
            index_of_deletion = class_name_4.index("-")
            class_name_4 = (class_name_4[index_of_deletion + 4:]).strip()
        except IndexError:
            pass
        class_name_5 = "No class"
        try:
            class_name_5 = (str(names_html[4].text)).strip()
            dash_index = class_name_5.index("-")
            class_name_5 = (class_name_5[dash_index + 4:]).strip()
        except IndexError:
            pass

        class_name_6 = "No class"
        try:
            class_name_6 = (str(names_html[5].text)).strip()
            dash_index = class_name_6.index("-")
            class_name_6 = (class_name_6[dash_index + 4:]).strip()
        except IndexError:
            pass

        class_name_7 = "No class"
        try:
            class_name_7 = (str(names_html[6].text)).strip()
            dash_index = class_name_7.index("-")
            class_name_7 = (class_name_7[dash_index + 4:]).strip()
        except IndexError:
            pass

        class_name_8 = "No class"
        try:
            class_name_8 = (str(names_html[7].text)).strip()
            dash_index = class_name_8.index("-")
            class_name_8 = (class_name_8[dash_index + 4:]).strip()
        except IndexError:
            pass

        return [class_name_1, class_name_2, class_name_3, class_name_4, class_name_5, class_name_6, class_name_7,
                class_name_8], [class1, class2, class3, class4, class5, class6, class7, class8]

    def return_current_grades(self):
        grades_html, name_html = self._return_html()
        classes = self._initialize_classes(grades_html, name_html)

        class_names, class_grades = classes

        class_grades_ = [grade.replace("%", "") for grade in class_grades]

        try:
            class_grades = [float(grade) for grade in class_grades_]
        except ValueError:
            class_grades = [0.0 for _ in class_grades_]
            print("FAILURE")

        return class_names, class_grades

    def return_quarter_grade(self, quarter):
        urls = "https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx"

        payload = {}
        if quarter == 1:
            payload = payloads.payload1
        elif quarter == 2:
            payload = payloads.payload2
        elif quarter == 3:
            payload = payloads.payload3
        elif quarter == 4:
            payload = payloads.payload4

        specific_quarter = self.session_requests.post(urls, data=payload, headers={"referer": urls})

        soup = BeautifulSoup(specific_quarter.text, "html.parser")

        grades_html = soup.find_all(class_="sg-header-heading sg-right")
        name_html = soup.find_all('a', class_="sg-header-heading")

        classes = self._initialize_classes(grades_html, name_html)

        class_names, class_grades = classes

        class_grades_ = [grade.replace("%", "") for grade in class_grades]

        try:
            class_grades = [float(grade) for grade in class_grades_]
        except ValueError:
            class_grades = [0.0 for _ in class_grades_]
            print("\n" + "ERROR: " + "Could not convert " + grade + " to a float." + "\n")

        return class_names, class_grades
