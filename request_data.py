from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import json
import pandas_gbq
import numpy as np
import requests
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import dash_html_components as html
from pandas.tseries.offsets import BDay


personal_cred = json.loads('{"type":"service_account","project_id":"tr-data-workbench","private_key_id":"1c715a521ff59da097178dd1ab3433ec419b84af","private_key":"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2+XxOal6ShiEH\\ngEXk7fDvJikzPQBBGF78ULXZ6dF2exLAcVsjJfRLASx21QVS7U20up4y2tWZ1bE8\\n8lloLkJstxJsTLIAx/9+Xwj6ur6kTsUxPYD5FwQGtsE7V7W1JgsiNvRBwFc2azHU\\n+sgkF31oA44kcwBbi7ltpP11dORQOJ+ldQpFq7KnUtL/POTbTfKlBlcrrX3Rkm7c\\n/9pFcR5FEQ8ApYagsdFgYHGSay8YLkOZjHNgIpW4ybAXI5OnbIxO3T1PeZDbjpEB\\nvoFieRZ2/IuiGjVNhE2WkTgz5QMwBapoYwtRDTpUlAb5eRfSRpRvKTgFAnQpLbAm\\nPi38IbFRAgMBAAECggEAIw3V8kHvn1uh/UlmWo75Px/M+duAbngoTmd6B2cDsZKv\\ni33MC4ZMcIgniBaUgAglgG/WOgDxthiZ7YayeUKPiDtkhKoG2h52xLOZSUu4lUrf\\n/Wh+inoN0+l0SJWroqpIrMPhdK1QKAVOVTK8YCm95Uz1EOeVVHSG0EoxIq0DxphX\\ngGDcDTS372SFoI8CQxFw7CTOQCe7zwgcgJlQekmwhZm8yyCVEYzo5xlo4XciLE33\\njLpdgWjjM7YVwqh94IiK2hXmt30mY3ioVt+r0iNxe4xR2wBSOXnLGRvDGb0hPBOu\\nkbvcV+MZHcEkYjOM70+ZvM6BbIH8SCcuopVOrbFSCQKBgQDh8OOXTYrh1IIlQynj\\n/4JZzuppcX5uffkMVQqX4gZOOp2d2NIme2e0S6ix059G554jPx8bbpXor4hEeKxr\\nSjSe3mk5wqRzYXptqXoo17QPZmvpVi+2RfdnGUFhhZLJbwhEHmqLXJMe7W0e5At9\\nzyIVnzK3DheTRjIPS6pUxn2LpQKBgQDPUT5iQj0IKINSEnjKj1IJAd7Vbxwwraag\\njTOuHTFHByHi5Asdy62gF+HIRUkA9tPNUCmqhocBYAw0VpPGCRAEd3ENHXKQrMax\\nSROcbsT+mm6ymgEK2B/GPtydCjY7PPMHTmrCxsPV1koq147Ain9Ru649IOQdCv98\\ne9lm3YnPPQKBgCDbwo2PhmIfYKoAoYf58cAT2n1pNwTkpyKG/5plEZuw5Jk/Hhjg\\nm41Z73elGiXaq2He3SxFIeIMHRowHosf6JUuLUlsKDRreb2XByAHdrVCpPDzSs8M\\nT9Wbk6mWHmnTDvWxIrePyAmYZ+U1LwKl7AQO+fYrQ3x0mfUlgOkBUOLNAoGAWzZh\\nfhWqiIZakKdz4ZsA+tmJ0tnZy0j7gLPfQwGxBpEKxaqTgX51W3RmcBibsALo2PIm\\nAtLBX0eE1xooVf7yvyRV5vFH0INTv/ho2nCZ13LWtVmwj7ba8/wAUE+H4LRGMLa9\\nngiZbOGlLAg+1FObBLjQRjDMbELEeV58HhfmY/kCgYEAkxcuBL0gLq06JoLtDSC6\\n7Bfp/Fj4IV6OChAYN60SFU8VnDoopV6sA+5CiZbWzu2ob+Agh/i7PQQxSs1s1tR1\\nsauVB8DUXUqAztSfKdymKXWafpUnTmwXzsd849Z75Y0Er/HwLsgB30GDhQ+BVnKJ\\n4Ih5xzWVb6ofozTA8IdHh2E=\\n-----END PRIVATE KEY-----\\n","client_email":"s4s8bso2qk5cvv8e5ts8ajhmsq8b0e@tr-data-workbench.iam.gserviceaccount.com","client_id":"113639508953850221246","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/s4s8bso2qk5cvv8e5ts8ajhmsq8b0e%40tr-data-workbench.iam.gserviceaccount.com"}') # your personal key for Tick History on BigQuery
proj = u'tr-data-workbench'
cred = service_account.Credentials.from_service_account_info(personal_cred)


def getTRtickdata(ticker_list ,start_date="2018-10-01", end_date="2018-12-31"):

    part_query1 = """SELECT 
      RIC, Date_Time, Bid_Price, Bid_Size, Ask_Price, Ask_Size, Price, Volume, Type 
    FROM
      `tr-data-workbench.Futures.L1_Q4_2018`
    WHERE 
        Type in ("Trade", "Quote")
        AND
        Date_Time between
    """

    date_range = pd.date_range(start=start_date, end=end_date, freq=BDay())

    for ric in ticker_list:
        part_query2 = " AND RIC=" + "'" + ric + "'" + " ORDER BY Date_Time"

        for i in range(int(np.ceil(len(date_range)/5))-1):

            if i != int( np.ceil(len(date_range)/5))-2:
                start = date_range[(0+i*5)]
                end = date_range[(0+(i+1)*5)]
            else:
                start = date_range[(0+i*5)]
                end = date_range[len(date_range)]

            file_name = os.getcwd() + "/TickData" + ric + "_" + str(start.date()) + "_" + str(end.date()) + ".json"
            if os.path.exists(file_name):
                next
            else:
                query = part_query1 + "'" + str(start.date()) + " 8:00:00" + "'" + "and" + "'" + str(end.date()) + " 16:00:00" + "'" + part_query2
                df = pandas_gbq.read_gbq(query, project_id=proj, credentials=cred, dialect='standard')
                with open(file_name, "+w") as f:
                    f.write(df.to_json())
                del df


def loadTRtickdata(ticker, target_date, start_date="2018-10-01", end_date="2018-12-31"):
    date_range = pd.date_range(start=start_date, end=end_date, freq=BDay())

    for i in range(int(np.ceil(len(date_range)/5))-1):

        if i != int(np.ceil(len(date_range)/5))-2:
            this_date_range = date_range[(0+i*5):(0+(i+1)*5)]
        else:
            this_date_range=date_range[(0+i*5):len(date_range)]

        filename = os.getcwd() + "/TickData" + ticker + "_" + str(date_range[(0+i*5)].date()) + "_" + str(date_range[(0+(i+1)*5)].date()) + ".json"
        if target_date in this_date_range:
            try:
                df = pd.read_json(filename)
                df.sort_index(inplace=True)
                df['t'] = pd.to_datetime(df.Date_Time)
                df.set_index('t', drop=True, inplace=True)
                df = df.tz_localize(None)
                df = df.loc[df.index.normalize()==target_date]
            except:
                print("file {0}, doesn't exist".format(filename))

            return df


def get_data_request(ric, start_date, end_date, fields="BID"):

    RESOURCE_ENDPOINT = "https://dsa-stg-edp-api.fr-nonprod.aws.thomsonreuters.com/data/historical-pricing/beta1/views/summaries/"+ ric
    access_token = 'T1IcOXrbT89HlDos9q9uG3YlBxK4nPY31HQLTllT'
    requestData = {
        "interval": "P1D",
        "start": start_date,
        "end": end_date,
        "fields": fields #BID,ASK,OPEN_PRC,HIGH_1,LOW_1,TRDPRC_1,NUM_MOVES,TRNOVR_UNS
    };

    dResp = requests.get(RESOURCE_ENDPOINT, headers={"X-api-key": access_token}, params=requestData)

    if dResp.status_code!=200:
        print("Unable to get data. Code %s, Message: %s" %(dResp.status_code, dResp.text))
    else:
        print("Data access successful " + "for ", ric)
        jResp = json.loads(dResp.text)
        return jResp


def load_TRHistdata(tickerList, startDate, endDate, fn):

    if os.path.exists(fn):
        final_df = pd.read_json(fn)
        return final_df
    else:
        df_list = []
        for ticker in tickerList:
            jResp = get_data_request(ticker, startDate, endDate)

            if jResp is not None:
                try:
                    data = jResp[0]['data']
                    headers = jResp[0]['headers']
                    names = [headers[x]['name'] for x in range(len(headers))]
                    close_price = pd.DataFrame(data, columns=names )
                    close_price.columns = ['DATE', ticker.replace("=", "")]
                    close_price.set_index("DATE", inplace=True)
                    df_list.append(close_price)
                except:
                    next

        final_df = pd.concat(df_list, axis=1, join="outer", sort=False)
        final_df.sort_index(inplace=True)

        with open(fn, "+w") as f:
            f.write(final_df.to_json())

        return final_df


def double_axis_plotter(df, colnames_1, colnames_2):

    fig, ax1 = plt.subplots(figsize=(10,7))

    ax1.plot(df[colnames_1])
    ax1.set_ylabel(colnames_1)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    ax2 = ax1.twinx()
    ax2.plot(df[colnames_2], 'r-')
    ax2.set_ylabel(colnames_2, color="r")

    fig.autofmt_xdate()


def generate_table(dataframe, max_rows=20):

    return html.Table(
        [html.Tr([html.Th(col) for col in dataframe.columns]
         for i in range(min(len(dataframe), max_rows)))]
    )