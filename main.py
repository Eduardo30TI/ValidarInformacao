from Acentos import Acentuacao
from CEP import CEP
from DownloadXLSX import ExcelDW
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options  import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import warnings
import time
import streamlit as st
from pages.tela import*

warnings.filterwarnings('error')

def Main():

    lista=['Consultar CNPJ','Google Telefone']

    sidebar=st.sidebar
    sidebar.title('Menu')
    sidebar.text('Consultar lista de contato pelo Google')
    sidebar.markdown('----')

    val=sidebar.selectbox('Telas',options=lista)

    if val=='Consultar CNPJ':

        tela=Consultar(val)
        tela.main()

        pass

    elif val=='Google Telefone':

        tela=GS(val)
        tela.main()

        pass

    pass


if __name__=='__main__':

    Main()

    pass