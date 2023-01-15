from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, chromedriver_binary
from configparser import ConfigParser




def search_ticket(start_point,destination,date,webDriver):
    sefer_listesi=list()
    number_of_expeditions=int(input('Kaa tane sefer sorgulanacak? Senin icin uygun olan sefer sayini gir: '))
    print(f"{number_of_expeditions} sefer icin tek tek hangi sefer numaraları senin icin uygun bunlari gir!")

    for i in range(0,number_of_expeditions):
        sefer=input(f"Sefer numarasını sıfırdan baslayarak girin!!: ")

        sefer_listesi.append(sefer)



    while True:
        webDriver.implicitly_wait(1)
        webDriver.get("https://ebilet.tcddtasimacilik.gov.tr/view/eybis/tnmGenel/tcddWebContent.jsf")



        xpath_start_point=webDriver.find_element(By.XPATH,'//*[@id="nereden"]')
        xpath_start_point.clear()
        xpath_start_point.send_keys(start_point) #where do you want to go

        xpath_destination=webDriver.find_element(By.XPATH,'//*[@id="nereye"]')
        xpath_destination.clear()
        xpath_destination.send_keys(destination)

        webDriver.find_element(By.XPATH,'//*[@id="trCalGid_input"]').clear()

        xpath_date=webDriver.find_element(By.XPATH,'//*[@id="trCalGid_input"]')
        xpath_date.click()
        xpath_date.send_keys(date)

        close_pop_up=webDriver.find_element(By.XPATH,'//*[@id="ui-datepicker-div"]/div[2]/button[2]')
        close_pop_up.click()

        searchbutton = webDriver.find_element(By.XPATH, '//*[@id="btnSeferSorgula"]')
        searchbutton.click()

        try:
            for sefer in sefer_listesi:
                vagon_tipi = f"mainTabView:gidisSeferTablosu:{sefer}:j_idt109:0:somVagonTipiGidis1_label"
                empty_seat=vagon_tipi[-2]
                sec_butonu=webDriver.find_element(By.XPATH,f'//*[@id="mainTabView:gidisSeferTablosu:{sefer}:j_idt117"]')
                sec_butonu.click()
                devam_butonu=webDriver.find_element(By.XPATH,'// *[ @ id = "mainTabView:btnDevam44"]')
                devam_butonu.click()
                count_vagon=0
                try:
                    count_empty_seat=0
                    while True:

                        # vagon_butonu=webDriver.find_element(By.XPATH,'mainTabView:j_idt206:3:gidisVagonlariGost')
                        seat=webDriver.find_elements(By.CLASS_NAME,'ui-wagon-item-checkbox')
                        for i in seat:
                            seat_number=i.get_attribute('value')
                            if seat_number!='9h':
                                i.click()
                                gender=webDriver.find_element(By.XPATH,'//*[@id="j_idt547"]')
                                gender.click()
                            print(i.text)
                        # for elem in webDriver.find_element(By.NAME,'checkbox'):
                        #     print(elem.text)
                        #     count_empty_seat+=1
                        # print(count_empty_seat)

                        # select by value
                        # // *[ @ id = "mainTabView:j_idt214"] / table / tbody / tr[1] / td[16] / div / div / input
                except Exception as e:
                    print(f"Vagon Butonu Error:  {e}")

        except Exception as e:
            print(f"Sefer Error: {e}")
        # for elem in webDriver.find_elements_by_xpath('.//span[@class = "seferSorguTableBuyuk"]')
        #         // *[ @ id = "mainTabView:gidisSeferTablosu_data"] / tr[2] / td[1] / span


# <input type="checkbox" style="z-index:3" class="ui-wagon-item-checkbox" name="7c_selection" value="7c">
# # mainTabView\:j_idt214 > table > tbody > tr:nth-child(2) > td:nth-child(19) > div > div > input
#
# // *[ @ id = "mainTabView:j_idt214"] / table / tbody / tr[2] / td[19] / div / div / input


if __name__=='__main__':
    config = ConfigParser()
    config.read('config.txt')
    start_point = config.get('LOCATION', 'start')
    destination = config.get('LOCATION', 'destination')
    date = config.get('LOCATION', 'date')

    wd = wd.Chrome()

    search_ticket(start_point,destination,date,wd)
