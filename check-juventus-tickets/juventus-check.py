from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import os


def init_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    return webdriver.Chrome(executable_path='../settings/chromedriver',
                            chrome_options=chrome_options
                            )


url = "https://sport.ticketone.it/46542/90600124/juventus-vs-roma--iv-di-finale-coppa-italia?ctsaffiliate=ITT"
chrome_browser = init_browser()
while True:
    try:
        chrome_browser.get(url)
        time.sleep(8)
        # se lo slide (quello per mostrare solo i biglietti disponibili) non è cliccato
        if chrome_browser.find_element_by_xpath("//input[@aria-checked='false']"):
            chrome_browser.find_element_by_class_name("mat-slide-toggle-bar").click()
        time.sleep(0.4)
        # verifico se non ci sono biglietti (in caso contrario viene lanciata l'eccezione perche non viene trovato l'elemento)
        chrome_browser.find_element_by_xpath('//div[normalize-space()="La tua ricerca non ha prodotti risultati."]')
    except NoSuchElementException as e:
        list_of_available_tickets = chrome_browser.find_elements_by_css_selector(
            'div.card__inner.best-seats.align-middle.ng-star-inserted')

        useful_ticket = False
        for ticket in list_of_available_tickets:
            ticket_name = ticket.find_element_by_css_selector(
                'b.button-link--small--list__text').text  # prendo il nome del ticket

            if ticket_name != 'TRIBUNA LAT. NORD 2 LIVELLO' and ticket_name != 'TRIBUNA EST LATERALE 2^ ANELLO':  # verifico che il ticket name sia qualcosa a cui sono interessato
                useful_ticket = True

        if useful_ticket:
            print("Biglietti trovati")
            os.system('say "There are some tickets"')

    print("...")
    time.sleep(50)
