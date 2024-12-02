import streamlit as st
from streamlit_modal import Modal

import sql
import pandas as pd
from st_aggrid import AgGrid, ColumnsAutoSizeMode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
import requests as rq
import datetime
from dateutil import parser

import altair as alt

st.set_page_config(
    page_title="Coleção de Posters de Jornal",
    page_icon="🧊",
    layout="wide"
)

st.subheader("Coleção de Posters", divider='rainbow')

modal = Modal(
    "Cadastro",
    key="demo-modal",

    # Optional
    padding=15,  # default value = 20
    # max_width=744  # default value = 744
)
open_modal = st.button("Novo Cadastro")
if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
            colinicio, colinicio2, colinicio3 = st.columns((2, 6, 0.1))
            with colinicio:
                tmdb = st.text_input('TMDB')
            if tmdb:
                dados_filme = sql.get_poster(tmdb)
                if dados_filme:

                    #st.write(dados_filme)
                    with colinicio2:
                        st.caption("")
                        st.error('Poster já cadastrado')
                        vIMDB = dados_filme[0][2]
                        vTitulo_original = dados_filme[0][3].upper()
                        vTitulo_traduzido = dados_filme[0][4].upper()
                        vPagina = dados_filme[0][6]
                        vPasta = dados_filme[0][7]
                        ano = int(dados_filme[0][8][0:4])
                        mes = int(dados_filme[0][8][5:7])
                        dia = int(dados_filme[0][8][8:])
                        vLink = dados_filme[0][9]
                        vSinopse = dados_filme[0][10]
                        vColorido = 1 if dados_filme[0][11] == "Cores" else 0
                        bMostraCampos = True
                else:
                    with colinicio2:
                        st.caption("")
                        resposta = rq.get(f'https://api.themoviedb.org/3/movie/{tmdb}?api_key=2b0120b7e901bbe70b631b2273fe28c9&language=pt-BR&include_adult=false')
                        if resposta.status_code == 200:
                            st.success('Novo Cadastro')
                            dados_filme = resposta.json()
                            #st.write(dados_filme)
                            vIMDB = dados_filme['imdb_id']
                            vTitulo_original = dados_filme['original_title'].upper()
                            vTitulo_traduzido = dados_filme['title'].upper()
                            ano = int(dados_filme['release_date'][0:4])
                            mes = int(dados_filme['release_date'][5:7])
                            dia = int(dados_filme['release_date'][8:])
                            vPagina = "-1"
                            vPasta = "-1"
                            vLink = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{dados_filme['poster_path']}"
                            vSinopse = dados_filme['overview']
                            vColorido = 0
                            bMostraCampos = True
                        else:
                            bMostraCampos = False

                if bMostraCampos:
                    col1, col2 = st.columns([15,10])
                    with col1:
                        titulo_original = st.text_input('Título Original', value=vTitulo_original)
                        titulo_traduzido = st.text_input('Título Traduzido', value=vTitulo_traduzido)
                        col3, col4, col5, col6 = st.columns([8,9,5,5])
                        with col3:
                            imdb = st.text_input('IMDB', value=vIMDB)
                        with col4:
                            data_release = st.date_input('Data Release', datetime.date(ano, mes, dia), format="DD/MM/YYYY")
                        with col5:
                            pasta = st.text_input('Pasta', value=vPasta)
                        with col6:
                            pagina = st.text_input('Pagina', value=vPagina)
                        cores = st.radio('Cor', ['Preto Branco', 'Cores'], index=vColorido, horizontal=True)
                        link_imagem = st.text_input('Link Imagem', value=vLink)
                    with col2:
                        st.image(link_imagem, width=250)
                    sinopse = st.text_area('Sinopse', value=vSinopse, height=150)

                    # pegando as capinhas
                    resposta = rq.get(f'https://api.themoviedb.org/3/movie/{tmdb}/images?api_key=2b0120b7e901bbe70b631b2273fe28c9')
                    if resposta.status_code == 200:
                            imagens = resposta.json()
                            jpgs = imagens['posters']
                            
                            # Exibindo os posters horizontalmente com colunas
                            st.subheader("Posters Disponíveis (Alternativa)")

                            # Defina um tamanho maior para as colunas
                            num_colunas = 5  # Defina quantas colunas você quer por linha
                            cols = st.columns(num_colunas)

                            # Adiciona as imagens nas colunas com espaçamento e largura ajustada
                            for i, jpg in enumerate(jpgs):
                                img_url = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{jpg['file_path']}"
                                
                                # Use um espaçamento e ajuste a largura da imagem
                                with cols[i % num_colunas]:  # Adiciona a imagem na coluna correspondente
                                    st.image(img_url, width=150)  # Aumente a largura da imagem

                            # Se você quiser adicionar uma nova linha após cada conjunto de imagens
                            if len(jpgs) > num_colunas:
                                st.write("") 
                    st.divider()

                    # pegando o elento
                    resposta = rq.get(f'https://api.themoviedb.org/3/movie/{tmdb}/credits?api_key=2b0120b7e901bbe70b631b2273fe28c9')
                    if resposta.status_code == 200:
                            imagens = resposta.json()
                            cast = imagens['cast']
                            
                            # Exibindo os elenco horizontalmente com colunas
                            st.subheader("Elenco Principal")

                            # Defina um tamanho maior para as colunas
                            num_colunas = 8  # Defina quantas colunas você quer por linha
                            cols = st.columns(num_colunas)

                            # carrego todos os posters não nulos num vetor
                            atores_com_imagem = [ator for ator in cast if ator.get('profile_path')]

                            # varro o vetor e mostro as imagens
                            for i, ator in enumerate(atores_com_imagem):
                                img_url = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{ator['profile_path']}"
                                
                                # Usa um espaçamento e ajusta a largura da imagem
                                with cols[i % num_colunas]:  # Adiciona a imagem na coluna correspondente
                                    st.image(img_url, width=90)  # Ajusta a largura da imagem
                                    #st.write(ator['name'])  # Exibe o nome do ator abaixo da imagem
                                    st.markdown(f"<p style='font-size:10px;  text-align: center;'>{ator['name']}</p>", unsafe_allow_html=True)

                            # Se você quiser adicionar uma nova linha após cada conjunto de imagens
                            if len(cast) > num_colunas:
                                st.write("") 
                    st.divider()


                    # ate aqui

                    #Botoes
                    colbotoes = st.columns((2,2,10),gap="small")
                    with colbotoes[0]:
                        if st.button('Salvar', type="primary"):
                                if sql.salva(tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse, cores):
                                    with colbotoes[2]:                        
                                        st.success('Poster Atualizado com Sucesso!')
                                        modal.close()
                                else:
                                    with colbotoes[2]:                        
                                        st.error('Ops deu erro')
                    with colbotoes[1]:
                        if st.button('Excluir', type="secondary"):
                                if sql.delete(tmdb):
                                    with colbotoes[2]:
                                        # st.success('Poster excluido com Sucesso!')
                                        modal.close()
                                else:
                                    with colbotoes[2]:
                                        st.error('Ops deu erro')
                else:
                    with colinicio2:
                        st.info('Filme não encontrado')




############################################################
##################### PAGINA INICIAL #######################
############################################################

#custom_css = {".ag-header-cell-text": {"font-size": "20px", 'text-overflow': 'revert;', 'font-weight': 1700}, ".ag-theme-streamlit": {'transform': "scale(0.8)", "transform-origin": '0 0'}}

cell_renderer =  JsCode("""
        class UrlCellRenderer {
        init(params) {
            this.eGui = document.createElement('a');
            this.eGui.innerText = 'Imagem';
            this.eGui.setAttribute('href', params.value);
            this.eGui.setAttribute('style', "text-decoration:none");
            this.eGui.setAttribute('target', "_blank");
        }
        getGui() {
            return this.eGui;
        }
    }
    """)
cell_renderer_tmdb =  JsCode("""
        class UrlCellRenderer {
        init(params) {
            this.eGui = document.createElement('a');
            this.eGui.innerText = 'Link TMDB';
            this.eGui.setAttribute('href', params.value);
            this.eGui.setAttribute('style', "text-decoration:none");
            this.eGui.setAttribute('target', "_blank");
        }
        getGui() {
            return this.eGui;
        }
    }
    """)
cell_renderer_imdb =  JsCode("""
    class UrlCellRenderer {
        init(params) {
        this.eGui = document.createElement('a');
        this.eGui.innerText = 'Link IMDB';
        this.eGui.setAttribute('href', params.value);
        this.eGui.setAttribute('style', "text-decoration:none");
        this.eGui.setAttribute('target', "_blank");
        }
        getGui() {
            return this.eGui;
        }
    }
    """)


id=[]
tmdb = []
imdb = []
titulo_original = []
titulo_traduzido = []
ano = []
pagina = []
pasta = []
data_release = []
link_imagem = []
link_tmdb = []
link_imdb = []
dados = sql.get_all()
# st.write(dados)
for linha in dados:
    id.append(linha[0])
    tmdb.append(linha[1])
    imdb.append(linha[2])
    titulo_original.append(linha[3])
    titulo_traduzido.append(linha[4])
    ano.append(linha[5])
    pagina.append(linha[6])
    pasta.append(linha[7])
    ano2 = ano
    if linha[8] is not None:
        ano2, mes, dia = linha[8].split('-')
    data_release.append( f"{dia}-{mes}-{ano2}")
    link_imagem.append(linha[9])
    link_tmdb.append(f"https://www.themoviedb.org/movie/{linha[1]}")
    link_imdb.append(f"https://www.imdb.com/title/{linha[2]}")

df=pd.DataFrame({
    "ID":id,
    "Ano":ano,
    "TMDB":tmdb,
    "IMDB":imdb,
    "Título Original":titulo_original,
    "Título Traduzido":titulo_traduzido,
    "Data Release":data_release,
    "Página":pagina,
    "Pasta":pasta,
    "Imagem":link_imagem,
    "Link TMDB":link_tmdb,
    "Link IMDB":link_imdb,
})
    #"IMDB":imdb,

gb = GridOptionsBuilder.from_dataframe(df, theme='streamlit')
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=100)
gb.configure_column('Ano')
gb.configure_column('TMDB', editable=True)
gb.configure_column('IMDB', editable=True)
gb.configure_column('Título Original', minWidth=600, maxWidth=620, editable=True)
gb.configure_column('Título Traduzido', minWidth=600, maxWidth=600, editable=True)
gb.configure_column('Página')
gb.configure_column('Pasta')
gb.configure_column('Data Release')
gb.configure_column('Imagem', cellRenderer=cell_renderer)
gb.configure_column('Link TMDB', cellRenderer=cell_renderer_tmdb, minWidth=120,maxWidth=100)
gb.configure_column('Link IMDB', cellRenderer=cell_renderer_imdb, minWidth=120,maxWidth=100)
gridoption = gb.build()

#col1, col2, col3 = st.columns([30,200,30])
#with col2:
AgGrid(df,
        gridOptions=gridoption,
        #custom_css=custom_css,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW, 
        updateMode=GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True
        )
    




############################################################
######################### GRAFICO ##########################
############################################################
dados = sql.graficoAnoPoster()
ano = []
quantidade = []

i = 0
for dado in dados:
    ano.append(dados[i][0])
    quantidade.append(dados[i][1])
    i += 1

source = pd.DataFrame({
    'Ano': ano,
    'Quantidade': quantidade
})

bar_chart = alt.Chart(source).mark_bar().encode(
    x='Ano:O',
    y='Quantidade',
    color=alt.condition(
        alt.datum.Ano == 2020,  # If the year is 1810 this test returns True,
        alt.value('red'),     # which sets the bar orange.
        alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
    )
).properties(
    title='Quantidade por Ano',
    width=600, 
    height=500
)

st.altair_chart(bar_chart, use_container_width=True)