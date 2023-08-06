import irsviz23.total_points_graph as totalpoints

import pandas as pd

from bokeh.models import Select
import bokeh.io as io
import bokeh.models as models
import bokeh.plotting as plotting
import bokeh.resources as resources
import pandas as pd
from bokeh.models import ColumnDataSource, Div
import math
from bokeh.io import output_notebook
import bokeh.palettes
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, Toggle, TableColumn, DataTable
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap, dodge
import math
from bokeh.layouts import column, row, grid, gridplot

class OneTeam:

    def __init__(self, manager, plotting_measures):
        self.layout = None
        self.manager = manager
        self.matches = self.manager.get_data()['matches']
        self.select = None
        self.plotting_measures = plotting_measures
        self.toggle = None

        self.points_tasks_list = ['auto_charge_station',
                                  'auto_cone_low',
                                  'auto_cone_mid',
                                  'auto_cone_up',
                                  'auto_cube_low',
                                  'auto_cube_mid',
                                  'auto_cube_up',
                                  'auto_left_community',
                                  'endgame_charge_station',
                                  'tele_cone_low', 
                                  'tele_cone_mid', 
                                  'tele_cone_up',
                                  'tele_cube_low', 
                                  'tele_cube_mid', 
                                        'tele_cube_up']
        self.point_tasks = {'auto_cone_low':3,
                                    'auto_cone_mid':4,
                                    'auto_cone_up':6,
                                    'auto_cube_low':3,
                                    'auto_cube_mid':4,
                                    'auto_cube_up':6,
                                    'auto_left_community':3,
                                    'tele_cone_low':2, 
                                    'tele_cone_mid':3, 
                                    'tele_cone_up':5,
                                    'tele_cube_low':2, 
                                    'tele_cube_mid':3,
                                    'tele_cube_up':5}
        self.charge_points_auto = {'docked':8,'engaged':12,'not_attempt':0,'attempt':0}
        self.charge_points_endgame = {'docked': 6,'engaged':10,'parked': 2,'not_attempt':0,'attempt':0}

    def refresh(self):
        self._callback("value", self.select.value, self.select.value)

    def _callback(self, attr, old, new):
        plot = self.graph_plot()
        self.layout.children[0] = plot

    def _togglecallback(self, attr, old, new):
        plot = self.graph_plot()
        self.layout.children[0] = plot

    def get_layout(self):
        measures = self.manager.get_data()['measures']
        team_list = sorted(measures['team'].unique())
        if 1318 in team_list:
            initial = "1318"
        else:
            initial = str(team_list[0])
        self.select = Select(title="Choose Team:", value=initial, options=[str(x) for x in team_list])
        self.select.on_change("value", self._callback)

        self.toggle = Toggle(label="On", name= "Qualitative Visibility")
        self.toggle.on_change("active", self._togglecallback)

        self.layout = column(self.graph_plot(), self.select)
        return self.layout

    def prepare_data(self):
        measures = self.manager.get_data()['measures']
        qual = self.manager.get_data().get('qualitative')
        ranking = self.manager.get_data().get('rankingpoints')

        team = int(self.select.value)

        rank_drop = None
        if ranking is not None:
            rankteam = ranking[ranking['team'] == team]
            rank_drop = rankteam.drop(['team', 'match'], axis=1)

        team_df = measures[measures['team'] == team].copy()
        avg_defense = team_df[team_df['task'] == 'defense']['hit'].sum() / len(team_df[team_df['task'] == 'defense']['hit'])
        avg_defended_ag = team_df[team_df['task'] == 'defended_against']['hit'].sum() / len(team_df[team_df['task'] == 'defended_against']['hit'])

        per_sust = "None"
        per_charge = "None"
        if rank_drop is not None:
            if len(rank_drop) > 0: 
                per_sust = rank_drop[rank_drop['rp_type'] == 'sust']['points'].sum() / len(rankteam['match'].unique()) * 100
                per_charge = rank_drop[rank_drop['rp_type'] == 'charge']['points'].sum() / len(rankteam['match'].unique()) * 100

        full_comment = ""
        pit_scouting = pd.DataFrame(data=[], columns=[0, 1])
        penalty_table = pd.DataFrame(data=[], columns=["match", "team", "comment", "penalty"])
        if qual is not None:
            qual = qual[qual['team'] == team]
            qual['penalty'] = qual['penalty'].replace('none', np.nan)
            
            penalty_table = qual[qual['penalty'].notna()]
            pit = qual[qual['match'] == "none"].copy()
            
            if not pit.empty:
                pit_scouting = pd.concat([pit['penalty'], pit['comment'].str.split(':', expand=True)], axis=1)
            qual = qual[qual['match'] != "none"]

            qual['comment'] = qual['comment'].replace("none", np.nan)
            qual['comment'] = qual['comment'].dropna()
            full_comment = qual['comment'].str.cat(sep ="\n")

        stats = {"percent_sust": per_sust, "percent_charge": per_charge, "average_defense": avg_defense,
                                    "comments": full_comment, "average_defended": avg_defended_ag}

        team_df['phase_task'] = team_df['phase'] + "_" + team_df['task']

        # converting hit to points for non-charge station tasks
        point_df = team_df[team_df['phase_task'].isin(self.point_tasks.keys())].copy()
        point_df['point_of_task'] = point_df['phase_task'].map(self.point_tasks)
        point_df['hit'] = point_df['hit'] * point_df['point_of_task']

        # filtering to charge station tasks 
        charge_station_auto = team_df[team_df['phase_task'] == 'auto_charge_station'].copy()
        charge_station_end = team_df[team_df['phase_task'] == 'endgame_charge_station'].copy()

        # converting hit to points for charge station tasks
        charge_station_auto['point_of_task'] = charge_station_auto['cat'].map(self.charge_points_auto)
        charge_station_auto['hit'] = charge_station_auto['point_of_task']
        charge_station_end['point_of_task'] = charge_station_end['cat'].map(self.charge_points_endgame)
        charge_station_end['hit'] = charge_station_end['point_of_task']

        full_df = pd.concat([point_df, charge_station_auto, charge_station_end])
        full_df = full_df.drop(['team', 'phase', 'task', 'miss', 'cat', 'measure_type', 'point_of_task'], axis=1)
        match_df = full_df.pivot(index='match', columns="phase_task")
        match_df.columns = match_df.columns.droplevel(0)

        if not match_df.empty:
            match_df['auto_cone'] = match_df['auto_cone_low'] + match_df['auto_cone_mid'] + match_df['auto_cone_up']
            match_df['auto_cube'] = match_df['auto_cube_low'] + match_df['auto_cube_mid'] + match_df['auto_cube_up']
            match_df['tele_cone'] = match_df['tele_cone_low'] + match_df['tele_cone_mid'] + match_df['tele_cone_up']
            match_df['tele_cube'] = match_df['tele_cube_low'] + match_df['tele_cube_mid'] + match_df['tele_cube_up']

        match_df = match_df.reset_index()
        match_df['match'] = match_df['match'].astype(str)
        match_df = match_df.fillna(0)
        return match_df, stats, pit_scouting, penalty_table

    def graph_plot(self):
        filter_df, stats, pit_scouting, penalty_table = self.prepare_data()
        filter_df = ColumnDataSource(filter_df)

        plot = plotting.figure(x_range = filter_df.data['match'],
                                x_axis_label="Match",
                                y_axis_label="Average Points",
                                title= "Team " + self.select.value + " Points",
                                tools = "hover",
                                tooltips = "$name: @$name",
                                width=900, height=600)

        vbar = plot.vbar_stack(self.plotting_measures,
                                x = "match",
                                color = bokeh.palettes.Paired[len(self.plotting_measures)],
                                width = 0.9,
                                source = filter_df)   

        legend_items = [(lbl, [glyph]) for lbl, glyph in zip(self.plotting_measures, vbar)]
        legend = models.Legend(items = legend_items, location = "top_right")
        plot.add_layout(legend, 'right')

        full_comment = "Qualitative Comments: \n" + stats["comments"] 

        comment = Div(text=f" <pre>{full_comment} </pre>", width=200, height=500)

        fin_stats = "Statistics: \n"
        for i in stats.keys():
            if i != "comments":
                fin_stats += i + ": " + str(stats[i]) + "\n"
        
        stats = Div(text=f" <pre>{fin_stats} </pre>", width=300, height=100)

        pit_scouting = pit_scouting.rename(columns={0: "0", 1: "1"})


        pit_scout_cs = ColumnDataSource(pit_scouting)
        columns_pit = [
                            TableColumn(field="0", title="Skill/Category"),
                            TableColumn(field="1", title="Comment")
                        ]
 
        pen_scout_cs = ColumnDataSource(penalty_table)
        columns_pen = [
                        TableColumn(field="match", title="Match"),
                        TableColumn(field="team", title="Team"),
                        TableColumn(field="penalty", title="Penalty"),
                        TableColumn(field="comment", title="Comment")
                    ]

        pit_table = DataTable(columns=columns_pit, source=pit_scout_cs, width = 900)
        pen_scout_cs = DataTable(columns=columns_pen, source=pen_scout_cs)
        
        datatab = row(pit_table, pen_scout_cs)
        if self.toggle.active is True:
            return column(row(plot, stats, column(comment, self.toggle)), datatab)
        else:
            return column(row(plot, stats, self.toggle), datatab)



