from tableau_dashboard_looper import TableauDashboardLooper

DASHBOARDS = {
    'dashboards': [
        {
            "url": "",
            "update_every": 600,
            "how_long_to_stay": 180,
            "updated_at": ""
        },
        {
            "url": "",
            "update_every": 600,
            "how_long_to_stay": 180,
            "updated_at": ""
        }
    ]
}

def main():
    
    tableau = TableauDashboardLooper(
        username = '-- ADD USERNAME HERE --',
        password = '-- ADD PASSWORD HERE --',
        tableau_login_url = '-- ADD YOUR TABLEAU INSTANCE URL HERE --',
        dashboards=DASHBOARDS
    )

    tableau.start_browser()
    tableau.login_tableau()
    tableau.open_dashboards()
    tableau.loop_through_tabs(refresh=False)

if __name__ == '__main__':
    main()