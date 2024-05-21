import streamlit as st
import sql
import pandas as pd
from st_aggrid import AgGrid, ColumnsAutoSizeMode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
import requests as rq
import datetime
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Coleção de Posters de Jornal",
    page_icon="🧊",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.subheader("Coleção de Posters", divider='rainbow')

# Pagina Inicial
def page1():
    if st.button("Novo"):
            st.session_state.page = 2

    total_linhas_pagina_ag_grid = 30
    ano = []
    tmdb = []
    imdb = []
    titulo_original = []
    titulo_traduzido = []
    pagina = []
    pasta = []
    link_imagem = []
    link_tmdb = []
    link_imdb = []

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

    dados = sql.get_all()
    # st.write(dados)

    for linha in dados:
        tmdb.append(linha[1])
        imdb.append(linha[2])
        titulo_original.append(linha[3])
        titulo_traduzido.append(linha[4])
        ano.append(linha[5])
        pagina.append(linha[6])
        pasta.append(linha[7])
        link_imagem.append(linha[9])
        link_tmdb.append(f"https://www.themoviedb.org/movie/{linha[1]}")
        link_imdb.append(f"https://www.imdb.com/title/{linha[2]}")

    df=pd.DataFrame({
        "Ano":ano,
        "TMDB":tmdb,
        "Título Original":titulo_original,
        "Título Traduzido":titulo_traduzido,
        "Pasta":pasta,
        "Página":pagina,
        "Imagem":link_imagem,
        "Link TMDB":link_tmdb,
        "Link IMDB":link_imdb,
    })
        #"IMDB":imdb,

    gb = GridOptionsBuilder.from_dataframe(df, theme='streamlit')
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=total_linhas_pagina_ag_grid)
    gb.configure_column('Ano', minWidth=70, maxWidth=70)
    gb.configure_column('TMDB', minWidth=80, maxWidth=100, editable=True)
    gb.configure_column('Título Original', minWidth=600, maxWidth=620, editable=True)
    gb.configure_column('Título Traduzido', minWidth=600, maxWidth=600, editable=True)
    #gb.configure_column('IMDB', minWidth=100,maxWidth=100)
    gb.configure_column('Página', minWidth=50, maxWidth=80)
    gb.configure_column('Pasta', minWidth=50, maxWidth=70)
    gb.configure_column('Imagem', cellRenderer=cell_renderer, minWidth=90, maxWidth=90)
    gb.configure_column('Link TMDB', cellRenderer=cell_renderer_tmdb, minWidth=120,maxWidth=100)
    gb.configure_column('Link IMDB', cellRenderer=cell_renderer_imdb, minWidth=120,maxWidth=100)
    gridoption = gb.build()

    col1, col2, col3 = st.columns([30,200,30])
    with col2:
        AgGrid(df,
                gridOptions=gridoption,
                #custom_css=custom_css,
                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, 
                updateMode=GridUpdateMode.VALUE_CHANGED,
                allow_unsafe_jscode=True
                )
        
# Pagina de Cadastro
def page2():
#    if (st.session_state.page == 2):
    if st.button("Home"):
        st.session_state.page = 1

    bPodeExcluir = False
    direita, centro, esquerda = st.columns([50,50,50], gap="small")
    with centro:
        colinicio, colinicio2 = st.columns((1, 5))
        with colinicio:
            tmdb = st.text_input('TMDB')
        if tmdb:
            dados_filme = sql.get_poster(tmdb)
            if dados_filme:
                bPodeExcluir = True

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
                        vPagina = ""
                        vPasta = ""
                        vLink = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{dados_filme['poster_path']}"
                        vSinopse = dados_filme['overview']
                        vColorido = 0
                        bMostraCampos = True
                    else:
                        bMostraCampos = False

            if bMostraCampos:
                col1 = st.columns(2)
                with col1[0]:
                    titulo_original = st.text_input('Título Original', value=vTitulo_original)
                    titulo_traduzido = st.text_input('Título Traduzido', value=vTitulo_traduzido)
#                    col3, col4, col5, col6 = st.columns(4)
#                    with col3:
                    imdb = st.text_input('IMDB', value=vIMDB)
#                    with col4:
                    data_release = st.date_input('Data Release', datetime.date(ano, mes, dia), format="DD/MM/YYYY")
#                    with col5:
                    pasta = st.text_input('Pasta', value=vPasta)
#                    with col6:
                    pagina = st.text_input('Pagina', value=vPagina)
                    cores = st.radio('Cor', ['Preto Branco', 'Cores'], index=vColorido, horizontal=True)
                    link_imagem = st.text_input('Link Imagem', value=vLink)
                with col1[1]:
                    st.image(link_imagem, width=380)
                sinopse = st.text_area('Sinopse', value=vSinopse, height=150)

                # pegando as capinhas
                resposta = rq.get(f'https://api.themoviedb.org/3/movie/{tmdb}/images?api_key=2b0120b7e901bbe70b631b2273fe28c9')
                if resposta.status_code == 200:
                        imagens = resposta.json()
                        jpgs = imagens['posters']

                        div = """ 
                            <style>
                                .table_wrapper{
                                display: block;
                                overflow-x: auto;
                                white-space: nowrap;
                                }
                            </style>
                        """
                        st.markdown(div, unsafe_allow_html=True)

                        colunas = ''
                        for jpg in jpgs:
                            colunas = colunas + f"""<td><img width="100px" src="https://image.tmdb.org/t/p/w600_and_h900_bestv2{jpg['file_path']}"></td>"""

                        tabela = "<nav aria-label='breadcrumb'><ol class='breadcrumb''><label>Posters Disponíveis</label><div class='table_wrapper'><table><tr>" + colunas + "</tr></table></div></ol></nav>"

                        st.markdown(tabela, unsafe_allow_html=True)
                st.divider()
                # ate aqui

                #Botoes
                colbotoes = st.columns((2,2,10),gap="small")
                with colbotoes[0]:
                    if st.button('Atualizar', type="primary"):
                            if sql.salva(tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse, cores):
                                with colbotoes[2]:                        
                                    st.success('Poster Atualizado com Sucesso!')
                            else:
                                with colbotoes[2]:                        
                                    st.error('Ops deu erro')
                with colbotoes[1]:
                    if bPodeExcluir:
                        if st.button('Deletar', type="secondary"):
                                if sql.delete(tmdb):
                                    with colbotoes[2]:                        
                                        st.success('Poster deletado com Sucesso!')
                                else:
                                    with colbotoes[2]:                        
                                        st.error('Ops deu erro')
            else:
                with colinicio2:
                    st.info('Filme não encontrado')


def app():
    if st.session_state.page == 1:
        page1()
    elif st.session_state.page == 2:
        page2()

if __name__ == "__main__":
    
    if "page" not in st.session_state:
        st.session_state.page = 1
    app()