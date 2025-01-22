from connection import conn
import re

def get_all():
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CARTAZES ORDER BY ID DESC")
        dados = cursor.fetchall()
        cursor.close()
        return dados

def get_poster(tmdb):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CARTAZES WHERE TMDB = %s", [tmdb])
        dados = cursor.fetchall()
        cursor.close()

        return dados

def salva(tmdb, imdb, titulo_original, titulo_traduzido, pagina, pasta, data_release, link_imagem, sinopse, cores ):
        if pagina == '':
              pagina = None
        if pasta == '':
              pasta = None

        ano = data_release.year
        sinopse = re.sub(r"\n", "", sinopse)        
        titulo_original = titulo_original.upper()      
        titulo_traduzido = titulo_traduzido.upper()      

        cursor = conn.cursor()
        
        dados = get_poster(tmdb)

        try:
            if(dados):
                    cursor.execute(""" UPDATE CARTAZES SET 
                        imdb = %s,
                        titulo_original = %s,
                        titulo_traduzido = %s,
                        ano = %s,
                        pagina = %s,
                        pasta = %s,
                        data_release = %s,
                        link_imagem = %s,
                        sinopse = %s,
                        cores = %s
                        WHERE TMDB = %s """, [imdb, titulo_original, titulo_traduzido, ano, pagina, pasta, data_release, link_imagem, sinopse, cores, tmdb])
            else:
                    cursor.execute("INSERT INTO CARTAZES (tmdb, imdb, titulo_original, titulo_traduzido, ano, pagina, pasta, data_release, link_imagem, sinopse, cores) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)",
                                   [tmdb, imdb, titulo_original, titulo_traduzido, ano, pagina, pasta, data_release, link_imagem, sinopse, cores])
            cursor.close()
            conn.commit()
            return True
        except (Exception, conn.Error) as error:
            print(error)
            return False
        
def delete(tmdb):
        cursor = conn.cursor()
        try:
                cursor.execute("DELETE FROM CARTAZES WHERE TMDB = %s", [tmdb])
                cursor.close()
                conn.commit()
                return True
        except (Exception, conn.Error) as error:
                print(error)
                return False
        
def graficoAnoPoster():
        cursor = conn.cursor()
        cursor.execute("SELECT coalesce(ANO, 2020) AS ANO, COUNT(*) AS QTDE FROM CARTAZES GROUP BY ANO ORDER BY 1")
        dados = cursor.fetchall()
        cursor.close()
        return dados