# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_valid_file_name(base_file_name, file_path):
    fileName, fileExtension = os.path.splitext(file_path)
    return (fileName == base_file_name)

def evalute_https_score(file_pshtt_csv):
    """ classifica il dominio rispetto ai parametri HTTPS"""

    #seleziono solo le colonne interessanti per il calcolo
    columns = ['Domain',
               'Base Domain',
               'Canonical URL',
               'Domain Supports HTTPS',
               'Domain Enforces HTTPS',
               'Domain Uses Strong HSTS']

    #controllo che il file di input sia un file pshtt.csv
    _file_check_name = 'pshtt.csv'
    if not check_valid_file_name(_file_check_name, file_pshtt_csv):
        return False

    try:
        # Scan domains and return data based on HTTPS best practices
        pshtt = pd.read_csv(file_pshtt_csv,
                            usecols=columns)
    except IOError as e:
        logger.error('Cannot load csv security file', exc_info=False)
        return False
    except Exception as ge: #generic
        logger.error('Exception:' + str(ge), exc_info=False)
        return False

    # associo uno score rispetto ai boolean contenuti nelle rispettive colonne selezionate
    pshtt[['Domain Supports HTTPS']] *= 5
    pshtt[['Domain Enforces HTTPS', ]] *= 3.5
    pshtt[['Domain Uses Strong HSTS']] *= 6.5

    # eseguo la somma degli score per ottenere un valore di score totale rispetto all'uso di HTTPS
    pshtt.loc[:, 'HTTPS Score'] = pshtt['Domain Supports HTTPS'] + \
                                  pshtt['Domain Enforces HTTPS'] + \
                                  pshtt['Domain Uses Strong HSTS']

    # ..inifne creo il dataframe degli score per HTTPS
    df_score_https = pd.DataFrame(pshtt, columns=['Domain', 'HTTPS Score'])

    return df_score_https, pshtt


def evalute_performance_score(file_pageload_csv):
    """ classifica il dominio rispetto ai parametri di Performance
    letti dal file csv "Pageload.csv"""

    # seleziono solo le colonne interessanti per il calcolo
    #in questo caso quelle che riguardano il caricamento del DOM
    columns = ['Domain',
               'domContentLoaded',
               'domComplete']

    #controllo che il file di input sia un file pageload.csv
    _file_check_name = 'pageload.csv'
    if not check_valid_file_name(_file_check_name, file_pageload_csv):
        return False

    # Scan domains and return web performance metrics collector
    try:
        pageload = pd.read_csv(file_pageload_csv,
                               usecols=columns)
    except IOError as e:
        logger.error('Cannot load csv performance file', exc_info=False)
        return False
    except Exception as ge: #generic
        logger.error('Exception:' + str(ge), exc_info=False)
        return False

    # eseguo la somma degli score per ottenere un valore di score totale rispetto all'uso di HTTPS
    pageload.loc[:, 'Performance Score'] = (pageload['domContentLoaded'] + \
                                            pageload['domComplete'])/2
    pageload['Performance Score'] = pageload['Performance Score'].replace(np.nan, 0.01)
    pageload['Performance Score'] = pageload['Performance Score'].replace(0, 0.01)

    pageload['Performance Score'] = pd.cut(pageload['Performance Score'],
                                           bins=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500, np.inf],
                                           labels=False) + 5

    # Creo il dataframe degli score per HTTPS
    df_score_performance = pd.DataFrame(pageload, columns=['Domain', 'Performance Score'])
    return df_score_performance, pageload


def evalute_trust_score(file_trust_csv):
    """ classifica il dominio rispetto ai parametri di affidabilita'
    letti dal file csv "trust.csv"""

    # seleziono solo le colonne interessanti per il calcolo
    # in questo caso quelle che riguardano i protocolli MX, SPF, DMARC
    columns = ['Domain',
               'MX Record',
               'Valid SPF',
               'Valid DMARC']

    # controllo che il file di input sia un file trustymail.csv
    _file_check_name = 'trustymail.csv'
    if not check_valid_file_name(_file_check_name, file_trust_csv):
        return False

    # Scan domains and return web performance metrics collector
    try:
        df_trust_performance = pd.read_csv(file_trust_csv, usecols=columns)
    except IOError as e:
        logger.error('Cannot load csv trust file', exc_info=False)
        return False
    except Exception as ge:  # generic
        logger.error('Exception:' + str(ge), exc_info=False)
        return False

    # associo uno score rispetto ai boolean contenuti nelle rispettive colonne selezionate
    df_trust_performance[['MX Record']] *= 5
    df_trust_performance[['Valid SPF', ]] *= 5
    df_trust_performance[['Valid DMARC']] *= 5

    # eseguo la somma degli score per ottenere un valore di score totale rispetto all'uso dei protocolli
    df_trust_performance.loc[:, 'Trust Score'] = (df_trust_performance['MX Record'] +
                                                  df_trust_performance['Valid SPF'] +
                                                  df_trust_performance['Valid DMARC'])

    # Creo il dataframe degli score per TRUST
    df_score_performance = pd.DataFrame(df_trust_performance, columns=['Domain', 'Trust Score'])

    return df_score_performance, df_trust_performance


def merge_df_results(df_score_https, df_score_performance, df_trust_performance):
    """Unisce i risultati dei dataframe precedenti in un unico dataframe
    di risultati
    """

    # df_score_https + df_score_performance
    df_res_partial = df_score_https.merge(df_score_performance, on='Domain', how='outer')

    # df_res_partial + df_trust_performance
    df_res = df_res_partial.merge(df_trust_performance, on='Domain', how='outer')
    df_res['Performance Score'] = df_res['Performance Score'].replace(np.nan, 0.01)

    df_res.loc[:, 'Tot Score'] = ((df_res['HTTPS Score'] + \
                                  df_res['Performance Score'] +
                                  df_res['Trust Score'])/3)*300

    #assegno un bollino allo score
    df_res.loc[:, 'Sticker'] = '/static/img/CircleF.png'
    df_res['Sticker'] = np.where(df_res['Tot Score'] >= 1500, '/static/img/CircleA.png',
                                 np.where(df_res['Tot Score'] >= 1200, '/static/img/CircleB.png',
                                          np.where(df_res['Tot Score'] >= 900, '/static/img/CircleC.png',
                                                   np.where(df_res['Tot Score'] >= 600, '/static/img/CircleD.png',
                                                            np.where(df_res['Tot Score'] >= 300, '/static/img/CircleE.png',
                                                                     '/static/img/CircleF.png')))))

    return df_res

def perform_classification(dict_data):
    """
    Questa procedura esegue l'mport dei csv ottenuti dall'utility domain-scan
    e classifica ogni dominio rispetto ai parametri di sicurezza, performance
    e affidabilità.
    """

    # 1) Importo il csv relativo al test HTTPS (pshtt scanner)
    # e calcolo un punteggio finale associato ad ogni dominio analizzato
    # in scala da 0 a 15
    df_score_https, df_https = evalute_https_score(dict_data['HTTPS'])

    # 2) Importo il csv relativo al test sulle performance (pageload scanner)
    # e calcolo un punteggio finale associato ad ogni dominio analizzato
    # in scala da 0 a 15
    df_score_performance, df_perf = evalute_performance_score(dict_data['PERFORMANCE'])

    #3) Importo il csv relativo al test sull'affidabilita' (trustymail scanner)
    # e calcolo un punteggio finale associato ad ogni dominio analizzato
    # in scala da 0 a 15
    df_score_trust, df_trust = evalute_trust_score(dict_data['TRUST'])

    # 4) Unifico i risultati in unico DataFrame definendo un punteggio finale
    # in scala da 0 a 1500
    df_result = merge_df_results(df_score_https, df_score_performance, df_score_trust)

    #Lista dei domini da visualizzare nella combobox di ricerca
    search_domain_list = [{'label': i, 'value': i} for i in df_result['Domain'].tolist()]

    return dict(dataframe_all_result=df_result,
                dataframe_https=df_https,
                dataframe_perf=df_perf,
                dataframe_trust=df_trust,
                search_domain_list=search_domain_list)
