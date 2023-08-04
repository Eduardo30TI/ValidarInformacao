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
import pandas as pd

warnings.filterwarnings('error')

link='https://www.google.com.br/'

class GS:


    def __init__(self,titulo):

        self.titulo=titulo

        pass

    def main(self):

        placeholder=st.empty()

        temp_df=pd.DataFrame(columns=['CNPJ','Razão Social','Nome Fantasia'])
        colunas=temp_df.columns.tolist()

        with placeholder.container():

            st.title(self.titulo)
            sidebar=st.sidebar
            data=ExcelDW.DownloadXLSX(temp_df)
            sidebar.download_button('Download',data=data,file_name='Base de importação.xlsx')
            
            files=st.file_uploader('Importar arquivo',type=['.xlsx'],accept_multiple_files=True)

            for f in files:

                df=pd.read_excel(f)

                if df.columns.tolist()!=colunas:

                    continue          
                
                temp_df=pd.concat([temp_df,df],axis=0,ignore_index=True)

                pass
            
            temp_df.drop_duplicates(inplace=True)
            lista=temp_df.columns.tolist()

            if len(temp_df)>0:

                val=st.selectbox('Filtro',options=lista)
                lista=temp_df[val].unique().tolist()
            
                btn=st.button('Enviar')

                if btn==True:
                    
                    espera=5

                    service=Service(GeckoDriverManager().install())

                    excel=pd.DataFrame(columns=['Razão Social','Endereço','Telefone','CEP'])
                    opcao=Options()
                    opcao.add_argument('--headless')
                    
                    with webdriver.Firefox(service=service,options=opcao) as driver:

                        driver.maximize_window()

                        bar=st.progress(0)
                        cont=0
                        
                        for n in lista:

                            cont+=1
                            perc=float(round(cont/len(lista),4))
                            bar.progress(perc)

                            try:

                                driver.get(link)

                                campo=WebDriverWait(driver,timeout=espera).until(lambda d: d.find_element(By.ID,'APjFqb'))
                                campo.send_keys(n)
                                time.sleep(2)
                                campo.send_keys(Keys.ENTER)

                                #kp-wp-tab-overview
                                WebDriverWait(driver,timeout=espera).until(lambda d: d.find_element(By.ID,'kp-wp-tab-overview'))

                                page=BeautifulSoup(driver.page_source,'html.parser')

                                div=page.select_one('div#kp-wp-tab-overview')
                                elements=div.select_one('div.B03h3d.V14nKc.i8qq8b.ptcLIOszQJu__wholepage-card.wp-ms')

                                endereco=elements.select_one('div.QsDR1c').get_text()
                                endereco=endereco[len('Endereço:'):].strip()
                                cep=endereco.split()[-1]

                                telefone=elements.select_one('span.LrzXr.zdqRlf.kno-fv').get_text()

                                excel.loc[len(excel)]=[n,endereco,telefone,cep]
                                                       
                                pass

                            except:

                                continue

                            #break

                            pass

                        pass

                    #lista de clientes

                    st.dataframe(excel,use_container_width=True)
                    data=ExcelDW.DownloadXLSX(excel)

                    st.download_button('Extrair',data=data,file_name='Lista de Telefone.xlsx')

                    pass

                pass

            pass

        pass

    pass