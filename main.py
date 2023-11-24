from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import image
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
from PyQt5.QtCore import QBasicTimer
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMessageBox, QToolTip, QMenu, QAction
import mysql.connector
import mysql.connector
import validators
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
global mydb
mydb = mysql.connector.connect(host="localhost",user="root",password="root",database="mydatabase")
def print_option(text,type):
    defaultfont = QtGui.QFont('Arial', 13)
    msg = QMessageBox()
    msg.setFont(defaultfont)
    msg.setWindowIcon(QIcon("image/shopping-cart.png"))
    msg.setIcon(type)
    msg.setText(text)
    msg.setWindowTitle("Message")
    msg.setWindowIcon(QtGui.QIcon("image/loge.png"))
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()
class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('ui.ui', self)
        self.show()
        self.submit_2.clicked.connect(self.switch)
        self.setWindowTitle("Auto Subscribe")
        self.setWindowIcon(QIcon("image/loge.png"))
    def switch(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_pass.text()
        mycursor = mydb.cursor()
        try:
            if username == '' or password == '':
                print_option("Please Enter All Fields", QMessageBox.Warning)
            else:
                my_q=("""SELECT * FROM user WHERE username = %s """)
                my_d=(str(username),)
                mycursor.execute(my_q,my_d)
                myruselt=mycursor.fetchall()
                if myruselt == []:
                    print_option("NO Valid Username ", QMessageBox.Warning)
                else:
                    for row in myruselt:
                        if row[1]==username and row[2]==password:
                            self.open_view()
                        else: print_option("Password Not Correct ", QMessageBox.Warning)
        except Exception as error:
            print_option("Error Connection ", QMessageBox.Warning)
    def open_view(self):
        self.window3 = View()
        self.close()
        self.window3.show()
class Help(QtWidgets.QMainWindow):
    def __init__(self):
        super(Help, self).__init__()
        uic.loadUi('help.ui', self)
        self.show()
class View(QtWidgets.QMainWindow):
    def __init__(self):
        super(View, self).__init__()
        uic.loadUi('view.ui', self)
        #self.setWindowTitle("Auto Subscribe")
        #self.setWindowIcon(QIcon("image/loge.png"))
        self.show()
        self.tabWidget.tabBar().setVisible(False)
        self.handell_buttons()
        self.tabWidget.setCurrentIndex(7)
        self.links()
        global list_show , list_url,list_last_email_sub
        global myresult_emails
        list_show=[]
        list_last_email_sub=[]
        list_url=[]
    def exit_pro(self):
        self.window3 = Login()
        self.close()
        self.window3.show()
    def help_pro(self):
        self.window3 = Help()
        self.window3.show()
    def links(self):
        self.telegram_label.setText('<a href="https://t.me/HazemKhaledAbdelwahab_OPM48" style="color: #42b6f5; font: 14px; text-decoration: None ; hover :{background-color : black };">Hazem Khaled</a>')
        self.telegram_label.setOpenExternalLinks(True)
        self.telegram_label.setStyleSheet("QLabel:hover{background-color:#464a47}")
    def handell_buttons(self):
        self.fox_sub.clicked.connect(self.foxSub)
        self.exit.clicked.connect(self.exit_pro)
        self.Help.clicked.connect(self.help_pro)
        self.add_email.clicked.connect(self.changetab_email)
        self.sub_button.clicked.connect(self.changetab_sub)
        self.url_button.clicked.connect(self.changetab_url)
        self.sub_all.clicked.connect(self.auto_sub)
        self.sub_info.clicked.connect(self.inser_url_info)
        self.insert_email.clicked.connect(self.insert_emails)
        self.back_button_1.clicked.connect(self.changetab_list)
        self.back_button_2.clicked.connect(self.changetab_list)
        self.back_button_3.clicked.connect(self.changetab_list)
        self.back_button_4.clicked.connect(self.changetab_list)
        self.back_button_5.clicked.connect(self.changetab_list)
        self.back_button7.clicked.connect(self.changetab_list)
        self.remove.clicked.connect(self.remove_email)
        self.update_email.clicked.connect(self.update_mail)
        self.up_email.clicked.connect(self.update_mail_new)
        self.delete_url.clicked.connect(self.sh_urls)
        self.dele_url.clicked.connect(self.del_urls)
        self.load_fill.clicked.connect(self.upload_file)
        self.delete_all.clicked.connect(self.del_all)
        self.show_sub_emails.clicked.connect(self.show_last_sub_email)
        self.dele_sub_email.clicked.connect(self.dele_last_sub_email)
        self.pt_image.clicked.connect(self.test_image)
        self.insert_image.clicked.connect(self.test_image)

    def dele_last_sub_email(self):
        try:
            if list_last_email_sub == []:
                print_option("There are no emails ", QMessageBox.Warning)
            else:
                mycursor = mydb.cursor()
                sql = "DELETE FROM email WHERE email IN (%s)" % ",".join(["%s"] * len(list_last_email_sub))
                sql2 = """ ALTER TABLE email AUTO_INCREMENT = 1 """
                mycursor.execute(sql,list_last_email_sub)
                mycursor.execute(sql2)
                mydb.commit()
                print_option("All Emails Delete", QMessageBox.Information)
            list_last_email_sub.clear()
        except Exception as error:
            print("An error occurred:", error)
            #print_option("Please Select email", QMessageBox.Information)
    def show_last_sub_email(self):
        self.tabWidget.setCurrentIndex(4)
        self.show_sub_email.addItems(list_last_email_sub)
    def login_b(self):
        self.window1 = Login()
        self.close()
        self.window1.show()
    def changetab_option(self):
        self.tabWidget.setCurrentIndex(4)
    def changetab_email(self):
        self.tabWidget.setCurrentIndex(2)
    def changetab_list(self):
        self.tabWidget.setCurrentIndex(3)
        self.email_add.clear()
        self.url_text.clear()
        self.em_id.clear()
        self.butt_id.clear()
        self.show_urls.clear()
        self.show_sub_email.clear()
    def changetab_sub(self):
        list_show.clear()
        self.show_emails.clear()
        self.show_sub_email.clear()
        self.tabWidget.setCurrentIndex(0)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM email")
        myresult_emails = mycursor.fetchall()
        for email in myresult_emails:
           list_show.append(email[1])
        self.show_emails.addItems(list_show)
    def changetab_url(self):
        self.tabWidget.setCurrentIndex(1)
    def auto_sub(self):
        #print(list_show)
        try:
            count= self.show_emails.count()
            if count == 0 :
                print_option("There are no emails", QMessageBox.Warning)
            else:
                mycursor = mydb.cursor()
                mycursor.execute("SELECT * FROM infoweb")
                myresul = mycursor.fetchall()
                for email in list_show:
                    for url in myresul:
                        options = webdriver.FirefoxOptions()
                        options.set_preference("browser.privatebrowsing.autostart", True)
                        driver = webdriver.Firefox(options=options)
                        driver.get('{}'.format(url[1]))
                        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, "{}".format(url[2]))))
                        email_input.send_keys(email)
                        time.sleep(2)
                        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"{}".format(url[3]))))
                        submit_button.click()
                        time.sleep(6)
                        driver.close()
                    list_last_email_sub.append(email)
                print_option("All email  have been successfully subscribe ", QMessageBox.Information)
                list_show.clear()
        except Exception as error:
            print_option("Browsing context has been discarded", QMessageBox.Warning)
    def inser_url_info(self):
        url = self.url_text.text()
        text_sub = self.em_id.text()
        button_id = self.butt_id.text()
        print(url,text_sub,button_id)
        if url =="" or text_sub == "" or button_id == "" :
            print_option("Please Enter All fields ", QMessageBox.Warning)
        else:
            if validators.url(url) == True:
                try:
                    cursor = mydb.cursor()
                    insert = """INSERT INTO infoweb (URL,EmailInput,EmSubmit) VALUES (%s,%s,%s) """
                    record = (url,text_sub,button_id)
                    print(record)
                    cursor.execute(insert, record)
                    mydb.commit()
                    print_option("Url have been Add successfully", QMessageBox.Warning)

                    self.url_text.clear()
                    self.em_id.clear()
                    self.butt_id.clear()
                except Exception as error:
                    #self.message_info.setText(str(error))
                    print("An error occurred:", error)
            else:
                print_option("Please Enter Valid Url ", QMessageBox.Warning)
    def insert_emails(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        list_to_insert = []
        email = self.email_add.text()
        list_to_insert.append(email)
        if (re.fullmatch(regex, email)):
            try:
                cursor = mydb.cursor()
                insert = """INSERT INTO email (email) VALUES (%s) """
                record = (email)
                cursor.execute(insert, list_to_insert)
                mydb.commit()
                print_option("Email has been added successfully ",QMessageBox.Information)
                self.email_add.clear()
            except Exception as error:
                #self.message_email.setText(str(error))
                print("An error occurred:", error)
        else:
            print_option("Please Enter Valid Email ", QMessageBox.Warning)
            #self.message_email.setText("Please Enter Valid Email")
    def remove_email(self):
        try:
            count = self.show_emails.count()
            if count == 0:
                print_option("There are no emails", QMessageBox.Warning)
            else:
                email_select=(self.show_emails.currentItem().text(),)
                mycursor = mydb.cursor()
                sql = """DELETE FROM email WHERE email = %s """
                mycursor.execute(sql,email_select)
                mydb.commit()
                current_row = self.show_emails.currentRow()
                if current_row >= 0:
                    current_item = self.show_emails.takeItem(current_row)
                    del current_item
                print_option("Email has been deleted successfully ", QMessageBox.Information)
        except Exception as error:
            #print("An error occurred:", error)
            print_option("Please Select email", QMessageBox.Information)
    def update_mail(self):
        try:
            count = self.show_emails.count()
            if count == 0:
                print_option("There are no emails", QMessageBox.Warning)
            else:
                self.tabWidget.setCurrentIndex(5)
                self.email_upda.setText(str(self.show_emails.currentItem().text()))
        except Exception as error:
            self.tabWidget.setCurrentIndex(0)
            print_option("Please Select email", QMessageBox.Information)
    def update_mail_new(self,x):
        try:

            old_email = self.show_emails.currentItem().text()
            #print(old_email,)
            new_email = self.email_upda.text()
            #print(new_email)
            mycursor = mydb.cursor()
            sql = """UPDATE email SET email = %s WHERE email = %s"""
            val = (new_email, old_email)
            mycursor.execute(sql, val)
            mydb.commit()
            self.email_upda.clear()
            print_option("Email has been Updated successfully ", QMessageBox.Information)
            self.tabWidget.setCurrentIndex(3)
        except Exception as error:
            #print("An error occurred:", error)
            print_option(str(error), QMessageBox.Information)
    def sh_urls(self):
        list_show_url=[]
        try:
            self.tabWidget.setCurrentIndex(6)
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM infoweb")
            myresul = mycursor.fetchall()
            mydb.commit()
            for url in myresul:
                list_show_url.append(url[1])
            self.show_urls.addItems(list_show_url)
            list_show_url.clear()
        except Exception as error:
            #print("An error occurred:", error)
            print_option(str(error), QMessageBox.Information)
            print(error)
    def del_urls(self):
        try:
            print(self.show_urls.currentItem().text())
            url_select=(self.show_urls.currentItem().text(),)
            mycursor = mydb.cursor()
            sql = """DELETE FROM infoweb WHERE URL = %s """
            mycursor.execute(sql, url_select)
            mydb.commit()
            current_row = self.show_urls.currentRow()
            if current_row >= 0:
                current_item = self.show_urls.takeItem(current_row)
                del current_item
            print_option("URL has been deleted successfully ", QMessageBox.Information)

        except Exception as error:
            # print("An error occurred:", error)
            print_option("Please Select Url", QMessageBox.Information)
    def upload_file(self):
        try:
            filepath, _ = QFileDialog.getOpenFileName(None, 'Select File', '', 'Text Files (*.txt)')
            if filepath == '':
                print_option("No File Select", QMessageBox.Warning)
            else:
                with open(filepath, 'r') as file:
                    data = file.readlines()
                records = []
                for email in data:
                    email = email.strip()
                    if email:
                        records.append((email,))
                sql = "INSERT INTO email (email) VALUES (%s)"
                cursor = mydb.cursor()
                cursor.executemany(sql, records)
                mydb.commit()
                print_option("Emails have been Add successfully ", QMessageBox.Information)
                print(records)
        except Exception as error:
            print_option("An error occurred:" + error, QMessageBox.Warning)
    def del_all(self):
        try:
            if list_show == []:
                print_option("There are no emails ", QMessageBox.Information)
            else:
                mycursor = mydb.cursor()
                sql1 = """DELETE FROM email """
                sql2 = """ ALTER TABLE email AUTO_INCREMENT = 1 """
                mycursor.execute(sql1)
                mycursor.execute(sql2)

                mydb.commit()
                self.show_emails.clear()
                print_option("All Emails Delete", QMessageBox.Information)

        except Exception as error:
            print("An error occurred:", error)
            #print_option("Please Select email", QMessageBox.Information)
    def foxSub(self):
        try:
            count = self.show_emails.count()
            if count == 0 or list_show == []:
                print_option("There are no emails", QMessageBox.Warning)
            else:
                for email in list_show:
                    options = webdriver.FirefoxOptions()
                    options.set_preference("browser.privatebrowsing.autostart", True)
                    driver = webdriver.Firefox(options=options)
                    driver.get('https://www.foxnews.com/newsletters')
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item breaking-news']//div[@class='button subscribe']")))
                    submit_button.click()
                    email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='user-input']//input[@placeholder='Type your email']")))
                    email_input.send_keys(email)
                    time.sleep(2)
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                                    "//div[@class='user-input alt']//div[@class='button enter']//a[@href='#'][normalize-space()='Subscribe']")))
                    submit_button.click()
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item breaking-news-fbn']//div[@class='button subscribe']")))
                    submit_button.click()
                    time.sleep(2)
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='user-input alt']//div[@class='button enter']")))
                    submit_button.click()
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                                    "//li[@class='newsletter-item fn-first']//div[@class='info']//div[@class='button subscribe']//a[@href='#'][normalize-space()='Subscribe']")))
                    submit_button.click()
                    time.sleep(2)
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='user-input alt']//div[@class='button enter']")))
                    submit_button.click()
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item fn-elections']//div[@class='button subscribe']")))
                    submit_button.click()
                    time.sleep(2)
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item fn-elections']//div[@class='button enter']")))
                    submit_button.click()
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item fox-411']//div[@class='button subscribe']")))
                    submit_button.click()
                    time.sleep(2)
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item fox-411']//div[@class='button enter']")))
                    submit_button.click()
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item opinion']//div[@class='button subscribe']")))
                    submit_button.click()
                    time.sleep(2)
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item opinion']//div[@class='button enter']")))
                    submit_button.click()
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item lifestyle']//div[@class='button subscribe']")))
                    submit_button.click()
                    time.sleep(2)
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item lifestyle']//div[@class='button enter']")))
                    submit_button.click()
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item fn-health']//div[@class='button subscribe']")))
                    submit_button.click()
                    time.sleep(2)
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='user-input alt']//div[@class='button enter']")))
                    submit_button.click()
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item fn-scitech']//div[@class='button subscribe']")))
                    submit_button.click()
                    time.sleep(2)
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item fn-scitech']//div[@class='button enter']")))
                    submit_button.click()
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item fn-autos']//div[@class='button subscribe']")))
                    submit_button.click()
                    time.sleep(2)
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='user-input alt']//div[@class='button enter']")))
                    submit_button.click()
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//li[@class='newsletter-item foxnation-fbn']//div[@class='button subscribe']")))
                    submit_button.click()
                    time.sleep(2)
                    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='user-input alt']//div[@class='button enter']")))
                    submit_button.click()
                    time.sleep(5)
                    driver.close()
                    list_last_email_sub.append(email)
                print_option("All email  have been successfully subscribe ", QMessageBox.Information)
        except Exception as error:
            print_option("Browsing context has been discarded", QMessageBox.Warning)
            #print(error)
    def test_image(self):
        filepath, _ = QFileDialog.getOpenFileName(None, 'Select File', '','image (*.jpg *.png *.icon *.gif)')
        self.pixmap = QPixmap(filepath)
        self.label_image.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(),self.pixmap.height())
    def insertBLOB(self):
        print("Inserting BLOB into python_employee table")
        try:
            connection = mysql.connector.connect(host="localhost",user="root",password="root",database="mydatabase")
            cursor = connection.cursor()
            sql_insert_blob_query = """ INSERT INTO images
                              (photo) VALUES (%s)"""
            empPicture = convertToBinaryData(photo)
            # Convert data into tuple format
            insert_blob_tuple = (empPicture)
            result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
            connection.commit()
            print("Image and file inserted successfully as a BLOB into python_employee table", result)

        except mysql.connector.Error as error:
            print("Failed inserting BLOB data into MySQL table {}".format(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = View()
    #mainWin = Login()
    mainWin.show()
    sys.exit(app.exec_())

