import requests


def get_domain_dict(df, selection):
    """A partire dal dominio selezionato estraggo il  relativo DataSet
    dei risultati e lo converto in un dizionario"""

    domain_info = {}
    #seleziono il subset rispetto al nome dominio selezionato
    try:
        df_subset = df.loc[df['Domain'].isin(selection)]
    except:
        tmp = []
        tmp.append(str(selection))
        df_subset = df.loc[df['Domain'].isin(tmp)]

    for index, row in df_subset.iterrows():
        for i in range(len(row)):
            if i == 0 or i == 6:
                domain_info['Domain'] = row[i]
                domain_info['Preview'] = get_domain_image_preview(domain_name=row[i])
            elif i == 5:
                domain_info['Sticker'] = row[i]
            elif i == 1:
                domain_info['HTTPS'] = row[i]
            elif i == 2:
                domain_info['Performance'] = row[i]
            elif i == 3:
                domain_info['Trust'] = row[i]

    return domain_info


def get_domain_image_preview(domain_name):
    """Tramite le API di Google Pagespeed ottengo lo screenshot del moninio esaminato"""
    screenshot_encoded=""
    try:

        # seleziono l'url del dominio
        domain_url = "http://www." + str(domain_name)

        # e lo passo a google pagespeed per ottenere l'anteprima in b64
        # api = "https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true&strategy=mobile"
        api = "https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true&strategy=desktop"

        r = requests.get(api, [('url', domain_url)])
        site_data = r.json()
        screenshot_encoded = site_data['screenshot']['data']
        screenshot_encoded = screenshot_encoded.replace("_", "/")
        screenshot_encoded = screenshot_encoded.replace("-", "+")

        screenshot_encoded = "data:image/jpeg;base64," + screenshot_encoded
    except Exception as e:
        screenshot_encoded = "https://rawgit.com/bsab/security-dashboard-wise/wise-turtle/static/img/no_site.png?raw=true"

    return screenshot_encoded
