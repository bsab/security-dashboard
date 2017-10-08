import pandas as pd
import numpy as np


def evalute_https_score(file_pshtt_csv):
    """
    return a Dataframe score for HTTPS
    :return:
    """

    #seleziono solo le colonne interessanti per il calcolo
    columns = ['Domain',
               'Base Domain',
               'Canonical URL',
               'Domain Supports HTTPS',
               'Domain Enforces HTTPS',
               'Domain Uses Strong HSTS']

    # Scan domains and return data based on HTTPS best practices
    pshtt = pd.read_csv(file_pshtt_csv,
                        usecols=columns)

    # associo uno score rispetto ai boolean contenuti nelle rispettive colonne selezionate
    pshtt[['Domain Supports HTTPS']] *= 5
    pshtt[['Domain Enforces HTTPS', ]] *= 3.5
    pshtt[['Domain Uses Strong HSTS']] *= 6.5

    # eseguo la somma degli score per ottenere un valore di score totale rispetto all'uso di HTTPS
    pshtt.loc[:, 'HTTPS Score'] = pshtt['Domain Supports HTTPS'] + \
                                  pshtt['Domain Enforces HTTPS'] + \
                                  pshtt['Domain Uses Strong HSTS']

    # Creo il dataframe degli score per HTTPS
    df_score_https = pd.DataFrame(pshtt, columns=['Domain', 'HTTPS Score'])

    return df_score_https


def evalute_performance_score(file_pageload_csv):
    """
    return a Dataframe score for performance domain
    :return:
    """

    # seleziono solo le colonne interessanti per il calcolo
    #in questo caso quelle che riguardano il caricamento del DOM
    columns = ['Domain',
               'domContentLoaded',
               'domComplete']

    # Scan domains and return web performance metrics collector
    pageload = pd.read_csv(file_pageload_csv,
                           usecols=columns)

    # eseguo la somma degli score per ottenere un valore di score totale rispetto all'uso di HTTPS
    pageload.loc[:, 'Performance Score'] = (pageload['domContentLoaded'] + \
                                            pageload['domComplete'])/2
    pageload['Performance Score'] = pageload['Performance Score'].replace(np.nan, 0.01)
    pageload['Performance Score'] = pageload['Performance Score'].replace(0, 0.01)

    pageload['Performance Score'] = pd.cut(pageload['Performance Score'],
                                           bins=[0, 500, 1000, 1500, 2000, 2500, 3000, 3500, np.inf],
                                           labels=False) + 5

    #print("-----------pageload---------------")
    #print(pageload)

    # Creo il dataframe degli score per HTTPS
    df_score_performance = pd.DataFrame(pageload, columns=['Domain', 'Performance Score'])

    print("-----------PERFORMANCE---------------")
    print(df_score_performance)
    df_score_performance.to_csv("df_score_performance.csv", index=False)

    return df_score_performance


def evalute_trust_score(file_trust_csv):
    """
    return a Dataframe score for trust domain
    :return:
    """

    # seleziono solo le colonne interessanti per il calcolo
    # in questo caso quelle che riguardano i protocolli MX, SPF, DMARC
    columns = ['Domain',
               'MX Record',
               'Valid SPF',
               'Valid DMARC']

    # Scan domains and return web performance metrics collector
    df_trust_performance = pd.read_csv(file_trust_csv, usecols=columns)

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

    return df_score_performance


def merge_df_results(df_score_https, df_score_performance, df_trust_performance):

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

    df_res.to_csv("df_results.csv", index=False)

    print("-----------RESULT---------------")
    print(df_res)

    return df_res
