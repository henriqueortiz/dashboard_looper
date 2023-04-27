from tableau_dashboard_looper import TableauDashboardLooper

DASHBOARDS = {
    'dashboards': [
        {
            "url": "https://public.tableau.com/views/TwitterAdsAnlaysis/TwitterADCampaigns-2021PerformanceSummary?%3Adisplay_static_image=y&%3AbootstrapWhenNotified=true&%3Aembed=true&%3Alanguage=en-US&:embed=y&:showVizHome=n&:apiID=host0#navType=0&navSrc=Parse",
            "update_every": 600,
            "how_long_to_stay": 180,
            "updated_at": ""
        },
        {
            "url": "https://public.tableau.com/views/SuperstoreSalesOverviewDashboard_16817475061410/ExecOverview?%3Adisplay_static_image=y&%3AbootstrapWhenNotified=true&%3Aembed=true&%3Alanguage=pt-BR&:embed=y&:showVizHome=n&:apiID=host0#navType=0&navSrc=Parse",
            "update_every": 600,
            "how_long_to_stay": 180,
            "updated_at": ""
        }
    ]
}

def main():
    
    tableau = TableauDashboardLooper(
        dashboards=DASHBOARDS
    )

    tableau.start_browser()
    tableau.open_dashboards()
    tableau.loop_through_tabs(refresh=False)

if __name__ == '__main__':
    main()