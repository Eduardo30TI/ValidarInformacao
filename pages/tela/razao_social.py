import streamlit as st
from CNPJ import CNPJ
import pandas as pd
from DownloadXLSX import ExcelDW
from streamlit_js_eval import streamlit_js_eval
import time

class Consultar:

    def __init__(self,titulo):

        self.titulo=titulo

        pass

    def main(self):

        placeholder=st.empty()

        temp_df=pd.DataFrame(columns=['CNPJ'])

        with placeholder.container():

            st.title(self.titulo)
            sidebar=st.sidebar
            data=ExcelDW.DownloadXLSX(temp_df)
            sidebar.download_button('Layout',data=data,file_name='Base de importação.xlsx')

            files=st.file_uploader('Importar arquivo',type=['.xlsx'])

            try:
            
                df=pd.read_excel(files)
                df['CNPJ']=df['CNPJ'].apply(self.FormatarCNPJ)

                bar=st.progress(0)
                texto=st.empty()
                cont=0

                lista=df['CNPJ'].unique().tolist()

                for c in lista:

                    cont+=1

                    perc=float(round(cont/len(lista),4))
                    bar.progress(perc)
                    texto.write(f'{cont} de {len(lista)}')                    

                    try:
                        
                        cnpj=CNPJ(c)
                        json=cnpj.GetDados()

                    
                        temp_dict={'razao_social':'Razão Social','nome_fantasia':'Nome Fantasia'}

                        for k,v in temp_dict.items():

                            nome=json[k]

                            df.loc[df['CNPJ']==c,v]=nome

                            pass

                        pass

                    except:

                        continue

                    #break

                    pass
                
                #df=df.loc[df['Razão Social'].notnull()]

                st.dataframe(df,use_container_width=True)
                    
                data=ExcelDW.DownloadXLSX(df)
                st.download_button('Extrair',data=data,file_name='Base de clientes.xlsx')
                #streamlit_js_eval(js_expression='parent.window.location.reload()')
         
                pass
            
            except:
                
                pass

            pass

        pass


    def FormatarCNPJ(self,val):

        val=str(val)

        for r in [',']:

            val=val.replace(r,'')

            pass

        val=f'0{val}' if len(val)<14 else val

        return val

        pass


    pass