import pandas as pd

import bokeh.io as io
import bokeh.models as models
import bokeh.plotting as plotting
import bokeh.resources as resources
import pandas as pd
from bokeh.models import ColumnDataSource
import math
from bokeh.io import output_notebook
import bokeh.palettes
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource, CheckboxGroup
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap, dodge
import math
from bokeh.layouts import column, row, grid, gridplot

class TotalPointsGraph:
    def __init__(self, manager, stack_list):
        self.layout = None
        self.manager = manager
        self.checkbox = None
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
        self.charge_points_end = {'docked': 6,'engaged':10,'parked': 2,'not_attempt':0,'attempt':0}
        self.stack_list = stack_list
    

    def refresh(self):
        self._callback("active", self.checkbox.active, self.checkbox.active)

    def get_layout(self):
        self.checkbox = CheckboxGroup(labels=self.stack_list,active=[i for i in range(0, len(self.stack_list))])
        self.checkbox.on_change("active", self._callback)
        self.layout = row(self.graph_plot(), self.checkbox)
        return self.layout

    def _callback(self, attr, old, new):
        if len(new) < 3:
            self.checkbox.update(value=old)
        else:
            plot = self.graph_plot() 
            self.layout.children[0] = plot

    def prepare_data(self):
        measures = self.manager.get_data()['measures']
        measures['phase_task'] = measures['phase'] + "_" + measures['task']
        teams = measures['team'].unique()

        all_teams = []
        for team in teams:
            # filter to only one team 
            team_measure = measures[measures['team'] == team]
            
            # empty list that will contain all the averages 
            team_averages = [] 
            team_averages.append(team)
            
            for task in self.point_tasks.keys():
                avg_sum = team_measure[team_measure['phase_task'] == task]["hit"].sum() * self.point_tasks[task]
                avg = avg_sum / (len(team_measure[team_measure['phase_task'] == task]['hit'])) 
                avg = round(avg,1) 
                team_averages.append(avg)
                                                
            for task in ["auto_charge_station", "endgame_charge_station"]: 
                charge_station_measure = team_measure[team_measure['phase_task'] == task]
                if task == 'auto_charge_station':
                    charge_station_measure = charge_station_measure.assign(cat=lambda df: df.cat.map(self.charge_points_auto))
                elif task == "endgame_charge_station":
                    charge_station_measure = charge_station_measure.assign(cat=lambda df: df.cat.map(self.charge_points_end))
                avg_sum = charge_station_measure[charge_station_measure['phase_task'] == task]["cat"].sum()
                avg = avg_sum / (len(charge_station_measure[charge_station_measure['phase_task'] == task]['cat'])) 
                avg = round(avg,1) 
                team_averages.append(avg)
            
            all_teams.append(team_averages)
        columns = ['team'] + list(self.point_tasks.keys()) + ["auto_charge_station", "endgame_charge_station"]

        df = pd.DataFrame(all_teams, columns=columns)
        df = df.sort_values('team')
        df['team'] = df['team'].astype(str)
        df['auto_cone'] = df['auto_cone_low'] + df['auto_cone_mid'] + df['auto_cone_up']
        df['auto_cube'] = df['auto_cube_low'] + df['auto_cube_mid'] + df['auto_cube_up']
        df['tele_cone'] = df['tele_cone_low'] + df['tele_cone_mid'] + df['tele_cone_up']
        df['tele_cube'] = df['tele_cube_low'] + df['tele_cube_mid'] + df['tele_cube_up']
        return df
        
    def graph_plot(self):
        df = self.prepare_data()
        filtered = ColumnDataSource(df)
        tasks = [self.stack_list[x] for x in self.checkbox.active]
        plot = plotting.figure(x_range = filtered.data['team'],
                    x_axis_label="Team",
                    y_axis_label="Average Points",
                    title= "Points",
                    tools = "hover", 
                    tooltips = "@team $name: @$name",
                    width=1200, height=600)

        vbar = plot.vbar_stack(tasks,
                                x = "team", 
                                color = bokeh.palettes.Paired[len(tasks)], 
                                width = 0.9,
                                source = filtered)

        legend_items = [(lbl, [glyph]) for lbl, glyph in zip(tasks, vbar)]
        legend = models.Legend(items = legend_items, location = "top_right")
        plot.add_layout(legend, "right")

        plot.xaxis.major_label_orientation = math.pi/4
        
        return plot       
        
