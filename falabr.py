import requests
from datetime import date
import shutil
import os
import time
import zipfile
import pandas as pd
import re

header_pedidos = ['IdPedido',
                'ProtocoloPedido',
                'Esfera',
                'UF',
                'Municipio',
                'OrgaoDestinatario',
                'Situacao',
                'DataRegistro',
                'PrazoAtendimento',
                'FoiProrrogado',
                'FoiReencaminhado',
                'FormaResposta',
                'OrigemSolicitacao',
                'IdSolicitante',
                'AssuntoPedido',
                'SubAssuntoPedido',
                'Tag',
                'DataResposta',
                'Decisao',
                'EspecificacaoDecisao']

header_recursos = ['IdRecurso',
                'IdRecursoPrecedente',
                'IdPedido',
                'IdSolicitante',
                'ProtocoloPedido',
                'Esfera',
                'UF',
                'Municipio',
                'OrgaoDestinatario',
                'Instancia',
                'Situacao',
                'DataRegistro',
                'PrazoAtendimento',
                'OrigemSolicitacao',
                'TipoRecurso',
                'DataResposta',
                'TipoResposta']

header_solicitante = ['IdSolicitante',
                    'TipoDemandante',
                    'DataNascimento',
                    'Genero',
                    'Escolaridade',
                    'Profissao',
                    'TipoPessoaJuridica',
                    'Pais',
                    'UF',
                    'Municipio']

ANO_INICIO=2012
PREFIXO_ACESSO = "Pedidos"
PREFIXO_RECURSO = "Recursos_Reclamacoes"
NOME_ARQUIVO_BASE = "{prefixo}_{formato_arquivo}_{ano}.zip"
URL_BASE = "https://dadosabertos-download.cgu.gov.br/FalaBR/Arquivos_FalaBR/{nome_arquivo}"

NOME_ARQUIVO_FILTRADO = 'Arquivos_{formato_arquivo}_{ano}.zip'
URL_FILTRADOS = "https://dadosabertos-download.cgu.gov.br/FalaBR/Arquivos_FalaBR_Filtrado/{nome_arquivo}"


def busca_lai_por_anos(anos, tipo_dados='acesso', localizacao='./', formato_arquivo='csv'):
    """
    anos: Lista de anos para download.
    tipo_dados: Se o arquivo é de acesso ou recurso
    localizacao: Onde salvar os arquivos
    formato_arquivo: formatos xml|csv
    """
    if tipo_dados.lower() == "acesso":
        prefix = PREFIXO_ACESSO
    else:
        prefix = PREFIXO_RECURSO

    for year in anos:
        nome_arquivo = NOME_ARQUIVO_BASE.format(prefixo=prefix, formato_arquivo=formato_arquivo, ano=str(year))
        url = URL_BASE.format(nome_arquivo=nome_arquivo)
        try:
            response = requests.get(url, stream=True)
            with open(os.path.join(localizacao, nome_arquivo), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            print(f"Arquivo {nome_arquivo} baixado de {url}")
        except Exception as e:
            print(e)
            print(f"Error baixando arquivo {nome_arquivo} da url {url}")

        time.sleep(2)


def unzip_arquivos(de='zips', diretorio_destino='csvs'):
    # https://stackoverflow.com/questions/3451111/unzipping-files-in-python

    pattern = re.compile(".*\.zip")
    files = os.listdir(de)
    for file in files:
        if os.path.isfile(os.path.join(de, file)) and pattern.match(file.lower()) != None:
            arquivo = os.path.join(de, file)
            with zipfile.ZipFile(arquivo, "r") as arquivo_zip:
                print(f'descompactando {arquivo}')
                arquivo_zip.extractall(diretorio_destino)


def busca_textos_por_anos(anos, localizacao='./', formato_arquivo='csv'):
    """
    anos: Lista de anos para download.
    localizacao: Onde salvar os arquivos
    formato_arquivo: formatos xml|csv
    """

    for year in anos:
        nome_arquivo = NOME_ARQUIVO_FILTRADO.format(formato_arquivo=formato_arquivo, ano=str(year))
        url = URL_FILTRADOS.format(nome_arquivo=nome_arquivo)
        try:
            response = requests.get(url, stream=True)
            with open(os.path.join(localizacao, nome_arquivo), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            print(f"Arquivo {nome_arquivo} baixado de {url}")
        except Exception as e:
            print(e)
            print(f"Error baixando arquivo {nome_arquivo} da url {url}")

        time.sleep(2)


class Pedidos:

    @staticmethod
    def carrega_arquivos_csv_df(diretorio, header_pedidos, parse_dates=None):
        pattern = re.compile(".*\_pedidos\_.*\.csv")
        df = pd.DataFrame()
        files = os.listdir(diretorio)
        if parse_dates is None:
            parse_dates = ['DataRegistro', 'PrazoAtendimento', 'DataResposta']

        for file in files:
            if os.path.isfile(os.path.join(diretorio, file)) and pattern.match(file.lower()) != None:
                print(f"Carregando {file}")
                df = pd.concat([df, pd.read_csv(os.path.join(diretorio, file), names=header_pedidos, sep=';',
                                                encoding='utf-16', parse_dates=parse_dates, dayfirst=True, engine='c',
                                                low_memory=False)], axis=0)
                print(
                    f'Carregado, memória utilizada após carga: {round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)}MB')
        return df

    @staticmethod
    def carrega_arquivos_xml_df(diretorio, header_pedidos, parse_dates):
        pattern = re.compile(".*\_pedidos\_.*\.xml")
        df = pd.DataFrame()
        files = os.listdir(diretorio)
        for file in files:
            if os.path.isfile(os.path.join(diretorio, file)) and pattern.match(file.lower()) != None:
                print(f"Carregando {file}")
                df = pd.concat([df, pd.read_xml(os.path.join(diretorio, file), names=header_pedidos, encoding='utf-16',
                                                parse_dates=parse_dates, dayfirst=True, engine='c', low_memory=False)])
                print(
                    f'Carregado, memória utilizada após carga: {round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)}MB')
        return df


class Recursos:

    @staticmethod
    def carrega_arquivos_csv_df(diretorio, header_recursos, parse_dates=None):
        pattern = re.compile(".*\_recursos\_.*\.csv")
        df = pd.DataFrame()
        files = os.listdir(diretorio)
        if parse_dates is None:
            parse_dates = ['DataRegistro', 'PrazoAtendimento', 'DataResposta']

        for file in files:
            if os.path.isfile(os.path.join(diretorio, file)) and pattern.match(file.lower()) != None:
                print(f"Carregando {file}")
                df = pd.concat([df, pd.read_csv(os.path.join(diretorio, file), names=header_recursos, sep=';',
                                                encoding='utf-16', parse_dates=parse_dates, dayfirst=True, engine='c',
                                                low_memory=False)], axis=0)
                print(
                    f'Carregado, memória utilizada após carga: {round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)}MB')
        return df

    @staticmethod
    def carrega_arquivos_xml_df(diretorio, header_recursos, parse_dates):
        pattern = re.compile(".*\_recursos\_.*\.xml")
        df = pd.DataFrame()
        files = os.listdir(diretorio)
        for file in files:
            if os.path.isfile(os.path.join(diretorio, file)) and pattern.match(file.lower()) != None:
                print(f"Carregando {file}")
                df = pd.concat([df, pd.read_xml(os.path.join(diretorio, file), names=header_recursos, encoding='utf-16',
                                                parse_dates=parse_dates, dayfirst=True, engine='c', low_memory=False)])
                print(
                    f'Carregado, memória utilizada após carga: {round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)}MB')
        return df


class Solicitantes:

    @staticmethod
    def carrega_arquivos_csv_df(diretorio, header_solicitante, parse_dates=None):
        pattern = re.compile(".*\_solicitantes\_.*\.csv")
        df = pd.DataFrame()
        files = os.listdir(diretorio)

        if parse_dates is None:
            parse_dates = ['DataNascimento']

        for file in files:
            if os.path.isfile(os.path.join(diretorio, file)) and pattern.match(file.lower()) != None:
                print(f"Carregando {file}")
                df = pd.concat([df, pd.read_csv(os.path.join(diretorio, file), names=header_solicitante, sep=';',
                                                encoding='utf-16', parse_dates=parse_dates, dayfirst=True, engine='c',
                                                low_memory=False)], axis=0)
                print(
                    f'Carregado, memória utilizada após carga: {round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)}MB')
        return df

    @staticmethod
    def carrega_arquivos_xml_df(diretorio, header_solicitante, parse_dates):
        pattern = re.compile(".*\_solicitantes\_.*\.xml")
        df = pd.DataFrame()
        files = os.listdir(diretorio)
        for file in files:
            if os.path.isfile(os.path.join(diretorio, file)) and pattern.match(file.lower()) != None:
                print(f"Carregando {file}")
                df = pd.concat([df,
                                pd.read_xml(os.path.join(diretorio, file), names=header_solicitante, encoding='utf-16',
                                            parse_dates=parse_dates, dayfirst=True, engine='c', low_memory=False)])
                print(
                    f'Carregado, memória utilizada após carga: {round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)}MB')
        return df

# anos = range(ANO_INICIO, int(date.today().strftime("%Y"))+1)
# list(anos)

# busca_lai_por_anos(anos, 'acesso', 'zips_lai_rel', 'csv')

# busca_lai_por_anos(anos, 'recurso', 'zips_lai_rel', 'csv')

# unzip_arquivos(de='zips_lai_rel', diretorio_destino='csvs_rel')

# %%time
# df = Pedidos.carrega_arquivos_csv_df('csvs_rel', header_pedidos=header_pedidos)

# df.to_pickle('dados/pedidos_relatorio.pkl')
# df.to_csv('dados/pedidos_relatorio.csv', index=False)

# %%time
# df = Recursos.carrega_arquivos_csv_df('csvs_rel', header_recursos=header_recursos)

# df.to_pickle('dados/recursos_relatorio.pkl')
# df.to_csv('dados/recursos_relatorio.csv', index=False)

pedido_header_txts = ['IdPedido',
                'ProtocoloPedido',
                'Esfera',
                'OrgaoDestinatario',
                'Situacao',
                'DataRegistro',
                'ResumoSolicitacao',
                'DetalhamentoSolicitacao',
                'PrazoAtendimento',
                'FoiProrrogado',
                'FoiReencaminhado',
                'FormaResposta',
                'OrigemSolicitacao',
                'IdSolicitante',
                'AssuntoPedido',
                'SubAssuntoPedido',
                'Tag',
                'DataResposta',
                'Resposta',
                'Decisao',
                'EspecificacaoDecisao']

recurso_header_txts = ['IdRecurso',
                'IdRecursoPrecedente',
                'DescRecurso',
                'IdPedido',
                'IdSolicitante',
                'ProtocoloPedido',
                'OrgaoDestinatario',
                'Instancia',
                'Situacao',
                'DataRegistro',
                'PrazoAtendimento',
                'OrigemSolicitacao',
                'TipoRecurso',
                'DataResposta',
                'RespostaRecurso',
                'TipoResposta']


solicitante_header_txts = ['IdSolicitante',
                'TipoDemandante',
                'DataNascimento',
                'Genero',
                'Escolaridade',
                'Profissao',
                'TipoPessoaJuridica',
                'Pais',
                'UF',
                'Municipio']

anos = range(2015, int(date.today().strftime("%Y"))+1)
list(anos)

busca_textos_por_anos(anos, localizacao='zips_lai_txts', formato_arquivo='csv')

unzip_arquivos(de='zips_lai_txts', diretorio_destino='csvs_txts')

# %%time
df = Pedidos.carrega_arquivos_csv_df('csvs_txts', header_pedidos=pedido_header_txts)

df.to_pickle('dados/pedidos_textos.pkl')
df.to_csv('dados/pedidos_textos.csv', index=False)

# %%time
df = Recursos.carrega_arquivos_csv_df('csvs_txts', header_recursos=recurso_header_txts)

df.to_pickle('dados/recursos_texto.pkl')
df.to_csv('dados/recursos_texto.csv', index=False)

# %%time
df = Solicitantes.carrega_arquivos_csv_df('csvs_txts', header_solicitante=solicitante_header_txts)

df.to_csv('dados/solicitantes_texto.csv', index=False)
df.to_pickle('dados/solicitantes_texto.pkl')