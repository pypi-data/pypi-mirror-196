import argparse
import pathlib
import sys

from bokeh.plotting import curdoc, figure
from bokeh.models import TabPanel, Tabs, Div
from bokeh.layouts import column, row, grid, gridplot

import irsviz23.data as data
import irsviz23.total_points_graph as totalpoints
import irsviz23.six_team_graph as sixteam
import irsviz23.one_team as oneteam


def run_server(args):
    """Runs visualization app on Bokeh server"""
    print(args)

    manager = data.Manager(args.json, args.ip)

    div = Div(text="""<h1>Welcome to the IRS 1318 Scouting Homepage!</h1>""")

    main_plot_list = [
        "auto_cone",
        "auto_cube",
        "tele_cone",
        "tele_cube",
        "auto_charge_station",
        "endgame_charge_station",
        "auto_left_community",
    ]

    auto_plot_list = [
        "auto_charge_station",
        "auto_cone_low",
        "auto_cone_mid",
        "auto_cone_up",
        "auto_cube_low",
        "auto_cube_mid",
        "auto_cube_up",
        "auto_left_community",
    ]

    tele_plot_list = [
        "endgame_charge_station",
        "tele_cone_low",
        "tele_cone_mid",
        "tele_cone_up",
        "tele_cube_low",
        "tele_cube_mid",
        "tele_cube_up",
    ]

    try:
        main_totalpointgraph = totalpoints.TotalPointsGraph(manager, main_plot_list)
        auto_totalpointgraph = totalpoints.TotalPointsGraph(manager, auto_plot_list)
        tele_totalpointsgraph = totalpoints.TotalPointsGraph(manager, tele_plot_list)

        tab_main = TabPanel(child=main_totalpointgraph.get_layout(), title="Main Plot")
        tab_auto = TabPanel(child=auto_totalpointgraph.get_layout(), title="Auto Plot")
        tab_tele = TabPanel(child=tele_totalpointsgraph.get_layout(), title="Tele Plot")
        tab2 = TabPanel(
            child=Tabs(tabs=[tab_main, tab_auto, tab_tele]), title="Total Points Plot"
        )
    except BaseException as err:
        tab2 = TabPanel(
            child=Div(text=f"<code>{err}</code>"), title="Total Points Plot"
        )

    try:
        main_six_team = sixteam.SixTeam(manager, main_plot_list)
        auto_six_team = sixteam.SixTeam(manager, auto_plot_list)
        tele_six_team = sixteam.SixTeam(manager, tele_plot_list)

        six_main = TabPanel(child=main_six_team.get_layout(), title="Main Six Plot")
        six_auto = TabPanel(child=auto_six_team.get_layout(), title="Auto Six Plot")
        six_tele = TabPanel(child=tele_six_team.get_layout(), title="Tele Six Plot")

        six_team_chart = TabPanel(
            child=Tabs(tabs=[six_main, six_auto, six_tele]), title="Six Team Plot"
        )
    except BaseException as err:
        six_team_chart = TabPanel(
            child=Div(text=f"<code>{err}</code>"), title="Six Team Plot"
        )

    try:
        main_one_team = oneteam.OneTeam(manager, main_plot_list)
        auto_one_team = oneteam.OneTeam(manager, auto_plot_list)
        tele_one_team = oneteam.OneTeam(manager, tele_plot_list)

        main_onet = TabPanel(
            child=main_one_team.get_layout(), title="Main One Team Plot"
        )
        auto_onet = TabPanel(
            child=auto_one_team.get_layout(), title="Auto One Team Plot"
        )
        tele_onet = TabPanel(
            child=tele_one_team.get_layout(), title="Tele One Team Plot"
        )

        one_team_chart = TabPanel(
            child=Tabs(tabs=[main_onet, auto_onet, tele_onet]), title="One Team Plot"
        )
    except BaseException as err:
        one_team_chart = TabPanel(
            child=Div(text=f"<code>{err}</code>"), title="One Team Plot"
        )

    try:
        refreshclass = data.RefreshData(
            [
                main_totalpointgraph,
                auto_totalpointgraph,
                tele_totalpointsgraph,
                main_six_team,
                auto_six_team,
                tele_six_team,
                main_one_team,
                auto_one_team,
                tele_one_team,
            ],
            manager,
        )
        tab8 = TabPanel(child=refreshclass.get_layout(), title="Refresh Data")
    except:
        tab8 = TabPanel(child=Div(text=f"<code>{err}</code>"), title="Refresh Data")

    return column(div, Tabs(tabs=[tab2, six_team_chart, one_team_chart, tab8]))
    curdoc().add_root(column)


def create_parser():
    """Creates object that interprets visualizer's command line arguments"""
    parser = argparse.ArgumentParser(
        description= "IRS Scouting Visualizer"
    )
    parser.add_argument("-i", "--ip", help="Scouting server's ip address")
    parser.add_argument("-j", "--json", type=pathlib.Path, 
                        help="Path to json data file")
    parser.add_argument("-d", "--debug", action="store_true", 
                        help="Run in dev mode, disabling error catching")
    parser.add_argument("-o", "--online", action="store_true",
                        help="Run on an online hosting service, disables refresh tab")
    parser.add_argument("-t", "--tabs", 
                        choices=["total_points", "six_team", "one_team", "refresh"],
                        help="Switch between tabs")
    return parser

parser = create_parser()
args = parser.parse_args()
column_layout = run_server(args)
curdoc().add_root(column_layout)