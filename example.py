from dashboard_looper import BrowserHandler

DASHBOARDS = {
    'dashboards': [
        {
            "type": "Tableau",
            "url": "https://public.tableau.com/views/TwitterAdsAnlaysis/TwitterADCampaigns-2021PerformanceSummary?%3Adisplay_static_image=y&%3AbootstrapWhenNotified=true&%3Aembed=true&%3Alanguage=en-US&:embed=y&:showVizHome=n&:apiID=host0#navType=0&navSrc=Parse",
            "update_every": 0,
            "how_long_to_stay": 10,
            "updated_at": ""
        },
        {   
            "type": "Tableau",
            "url": "https://public.tableau.com/views/SuperstoreSalesOverviewDashboard_16817475061410/ExecOverview?%3Adisplay_static_image=y&%3AbootstrapWhenNotified=true&%3Aembed=true&%3Alanguage=pt-BR&:embed=y&:showVizHome=n&:apiID=host0#navType=0&navSrc=Parse",
            "update_every": 0,
            "how_long_to_stay": 10,
            "updated_at": ""
        },
        {   
            "type": "Looker",
            "url": "https://lookerstudio.google.com/reporting/17Yq6eVJSSEM1mCtkB9lnZ2bjOROZBBU1/page/QzYj",
            "update_every": 0,
            "how_long_to_stay": 10,
            "updated_at": ""
        }
    ]
}


def main():
    chrome = BrowserHandler(dashboards=DASHBOARDS)
    chrome.start_browser()
    chrome.login('Tableau')
    chrome.login('Looker')
    chrome.open_dashboards()
    chrome.loop_through_tabs(refresh=False)

if __name__ == '__main__':
    main()