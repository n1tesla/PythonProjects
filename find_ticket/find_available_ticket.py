from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



from datetime import datetime
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play


from playsound import playsound

# song = AudioSegment.from_mp3("music1.mp3")

#numberların type error olup olmadığını kontrol et. gmail'de two step authentication varsa uygulama şifresi oluşturman gerekiyor.
#https://support.google.com/accounts/answer/185833?hl=tr
#gidiş sefer tablo numaraları önemli
#
PATH="chromedriver.exe"
driver=webdriver.Chrome(PATH)
driver.implicitly_wait(3)
import smtplib, ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "tnakyol1@gmail.com"
receiver_email = "tnakyol1@gmail.com"
password = 'pvwioejicbcuzemr'   #google uygulama şifreleri

while True:
    driver.get('https://ebilet.tcddtasimacilik.gov.tr/view/eybis/tnmGenel/tcddWebContent.jsf')

    nereden=driver.find_element(By.XPATH,'//*[@id="nereden"]')
    nereden.clear()
    nereden.send_keys('Ankara Gar')
    #'Ankara Gar'

    nereye=driver.find_element(By.XPATH,'//*[@id="nereye"]')
    nereye.clear()
    nereye.send_keys('Gebze')

    driver.find_element(By.XPATH,'//*[@id="trCalGid_input"]').clear()

    tarih=driver.find_element(By.XPATH,'//*[@id="trCalGid_input"]')
    tarih.click()
    tarih.send_keys('20.01.2023')
    kapat=driver.find_element(By.XPATH,'//*[@id="ui-datepicker-div"]/div[2]/button[2]')
    kapat.click()

    searchbutton=driver.find_element(By.XPATH,'//*[@id="btnSeferSorgula"]')
    searchbutton.click()

    try:
        # number2=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"mainTabView:gidisSeferTablosu:2:j_idt109:0:somVagonTipiGidis1_label"))) #saat 10
        # number3=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"mainTabView:gidisSeferTablosu:3:j_idt109:0:somVagonTipiGidis1_label")))
        # number4 =WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"mainTabView:gidisSeferTablosu:4:j_idt109:0:somVagonTipiGidis1_label")))
        number3=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"mainTabView:gidisSeferTablosu:3:j_idt109:0:somVagonTipiGidis1_label"))) #saat 12:40
        number4=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"mainTabView:gidisSeferTablosu:4:j_idt109:0:somVagonTipiGidis1_label"))) # 17
        number5=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"mainTabView:gidisSeferTablosu:5:j_idt109:0:somVagonTipiGidis1_label")))
        #number6=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"mainTabView:gidisSeferTablosu:6:j_idt109:0:somVagonTipiGidis1_label")))
        #number7=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"mainTabView:gidisSeferTablosu:7:j_idt109:0:somVagonTipiGidis1_label")))

        # number6=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"mainTabView:gidisSeferTablosu:14:j_idt109:0:somVagonTipiGidis1_label")))
        # print(f"number2:  {number2.text}")
        # print(f"number3: {number3.text}")
        # print(f"number4: {number4.text}")
        print(f"number5: {number3.text}")
        print(f"number6: {number4.text}")
        print(f"number7: {number5.text}")
        #print(f"number8: {number6.text}")
        #print(f"number9: {number7.text}")
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        if(number3.text!="2+2 Pulman (Ekonomi) (1)") or (number4.text!="2+2 Pulman (Ekonomi) (1)") or (number5.text!="2+2 Pulman (Ekonomi) (1)"):
            print("********************************************")
#(number6.text!="2+2 Pulman (Ekonomi) (0)" or (number7.text!="2+2 Pulman (Ekonomi) (0)")
            message = f"""\
            Subject: Hi there
            
            I found a available ticket """
            print('playing sound using  pydub')
            # play(song)
            playsound("music.mp3")
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
                #server.sendmail(sender_email,"eceulas21@gmail.com",message)
                server.sendmail(sender_email, "tnakyol@hotmail.com", message)
                server.sendmail(sender_email,"akyol.tunahann@gmail.com",message)

    except:
        time.sleep(3)
    time.sleep(3)

#driver.quit()


