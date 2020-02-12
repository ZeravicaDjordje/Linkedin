try:
    import pip
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    from pyvirtualdisplay import Display
    from skrol import scrolls_bottom, scrolls_top, scrolls
    import sql_linkedin as sql
except Exception as e:
    print('Install librery', e)
    module = str(e)[17:]
    module = module[0:len(module)-1]
    pip_return = pip.main(['install', module])
    if pip_return == 1:
        print("Can't install python library", module)

class Login(object):
    '''Login class is main class that has four methods '''
    
    def start_display(self):
        ''' Making virutal display where your browser will be (put it in variable)'''
        display = Display(visible=0, size=(1366, 768))
        display.start()
        return display
    
    def start_browser(self, url, goo_fire='firefox'):
        ''' Starting web-driver browser, you have to 
        accepting two atributes object and url(url-login page)'''
        if goo_fire.lower() == 'firefox':
            browser = webdriver.Firefox()
            browser.get(url)
        else:
            browser = webdriver.Chrome()
            browser.get(url)
        return browser

    def login(self, e_mail, passw, browser):
        ''' These is acctualy login method accepting 4 parramaters 
        object, mail, password, browser'''
        email = browser.find_element_by_id('login-email')
        password = browser.find_element_by_id('login-password')
        email.send_keys(e_mail)
        password.send_keys(passw)
        sign_in = browser.find_element_by_id('login-submit')
        sign_in.click()
        time.sleep(5)

    def stop_display(self, disp):
        ''' These method will only work if display is on, accepting display as paramter '''
        return disp.stop()

    
class MyNetwork(Login):
        
    def connection_my(self, browser, number = 0):
        my_connection = browser.find_element_by_id('mynetwork-nav-item')
        my_connection.click()
        time.sleep(10)
        scrolls_bottom(number, browser)

    
    def all_connections(self, browser, number = 0):
        see_all = browser.find_element_by_link_text('See all')
        see_all.click()
        time.sleep(7)
        scrolls_bottom(int(number), browser, stop='')
        time.sleep(5)

        
    def connect_people(self, browser):
        connect = browser.find_elements_by_tag_name("span")
        for connection in connect:
            
            try:
                if 'Connect' == connection.text:
                    print('Click on:',connection.text)
                    connection.click()
                    print("Connect")
                    time.sleep(1)
                    
            except Exception as e:
                print(e)

class Messages(MyNetwork):
    '''These class is for sending message to all your connection or some of it'''

    def message(self, browser):
        all_message = browser.find_elements_by_tag_name("span")
        
        for mesg in all_message:
            
            try:
                
                if 'Message' == mesg.text:
                    print('Send a message to: ', all_message[all_message.index(mesg)+1])
                    mesg.click()
                    time.sleep(0.5)
                    
            except Exception as e:
                print(e)


class Endorsment(Messages):
    
    def connection_number(self, browser):
        ''' Use when in my network '''
        number = browser.find_element_by_tag_name('h3')
        return number.text.replace(',','')
        
    def endorsment(self, browser, number=1000):
        end = 1
        n = number
        num = 0
        while end:
            if num > 10:
                break
            scrolls(number, browser)
            time.sleep(5)
            more_skills = browser.find_elements_by_tag_name('span')
            print(more_skills)
            for div in more_skills:
                try:
                    if 'more skills' in div.text.lower():
                        print('Click on %r' % div.text)
                        div.click()
                        end = 0
                        break
                except Exception as e:
                    print(e)
            number += n
            num += 1
        time.sleep(3)
        skills = browser.find_elements_by_class_name('pv-skill-entity__endorse-actions.ember-view')
        print(skills)
        for skill in skills:
            skill.click()
            print('Click on skill')
            time.sleep(0.5)
    
    
    def connection(self, browser, job_d, sql, sql_data, sql_info, cursor, connect, people=100):
        number_of_people = 0
        if type(job_d) != type([]):
            print('You have to forward list type, not %r type' % type(job_d))
        job_descript = browser.find_elements_by_class_name('mn-person-info__link.ember-view')
       for descrpt in job_descript:
            # end = 0
            link = descrpt.get_attribute('href')
            job_company = descrpt.text.split('\n')[3].split(' at ')
            name_surname = descrpt.text.split('\n')[1]
            print('Job company',job_company, 'Name_surname',name_surname)
            try:
                job = job_company[0]
                company = job_company[1]
            except:
                job = ''
                company = ''
                print('Except')
         for data in sql_data:
                if name_surname == data[1] and company == data[2] and job == data[3]:
                    print('In database skipping',(name_surname, company, job))
                    break
                print('Link click')
                sql.insert_data(cursor, (name_surname, company, job), sql_info)
                descrpt.send_keys(Keys.CONTROL + Keys.RETURN)
                print('Click on', name_surname)
                time.sleep(3)
                browser.switch_to.window(browser.window_handles[1])
                time.sleep(3)
                self.endorsment(browser)
                number_of_people += 1
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                time.sleep(2)
                break
        sql.save_data(connect)
 
