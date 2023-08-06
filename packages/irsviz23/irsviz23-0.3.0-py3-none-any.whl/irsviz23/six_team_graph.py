import irsviz23.total_points_graph as totalpoints

import pandas as pd

from bokeh.models import Select
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
from bokeh.models import ColumnDataSource, Span
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap, dodge
import math
from bokeh.layouts import column, row, grid, gridplot

class SixTeam:
    def __init__(self, manager, plotting_measures):
        self.layout = None
        self.manager = manager
        self.matches = self.manager.get_data()['matches']
        self.select = None
        self.plotting_measures = plotting_measures

    def _callback(self, attr, old, new):
        plot = self.graph_plot()
        self.layout.children[0] = plot

    def refresh(self):
        self._callback("value", self.select.value, self.select.value)

    def get_layout(self):
        self.select = Select(title="Choose Match:", value="1", options=[str(x) for x in sorted(self.matches.match.unique())])
        self.select.on_change("value", self._callback)
        self.layout = column(self.graph_plot(), self.select)
        return self.layout
    
    def prepare_data(self):
        main_totalpointgraph = totalpoints.TotalPointsGraph(self.manager, self.plotting_measures)
        df = main_totalpointgraph.prepare_data()
        
        df['total_points'] = df[self.plotting_measures].to_numpy().sum(axis=1)
        mtch = sorted(self.matches['match'].unique())
        match_list = list()  
        for match_number in mtch:
            new_match_item = self.matches.loc[self.matches.match == match_number, "team"].to_list()
            match_list.append(new_match_item)

        print(match_list[int(self.select.value) - 1])
        ind=[df.index[df['team']==i].tolist() for i in [str(x) for x in match_list[int(self.select.value) - 1]]]
        flat_ind=[item for sublist in ind for item in sublist]
        filter_df = df.reindex(flat_ind)
        filter_df['team'] = filter_df['team'].astype(int)
        filter_df = filter_df.merge(self.matches[(self.matches['team'].isin(match_list[int(self.select.value) - 1])) 
                                    & (self.matches['match'] == (int(self.select.value)))], how="outer")
        filter_df['team'] = filter_df['team'].astype(str)
        return filter_df

    def graph_plot(self):
        filter_df = self.prepare_data()
        print(filter_df)

        blue_filter_df = filter_df.iloc[:3]
        red_filter_df = filter_df.iloc[-3:]

        average_blue = blue_filter_df['total_points'].sum()/3
        average_red = red_filter_df['total_points'].sum()/3

        filtered_blue = ColumnDataSource(blue_filter_df)
        filtered_red = ColumnDataSource(red_filter_df)

        plot_blue = plotting.figure(x_range = filtered_blue.data['team'],
                                x_axis_label="Team",
                                y_axis_label="Average Points",
                                title= "Blue Alliance Points",
                                tools = "hover",
                                tooltips = "@team $name: @$name",
                                width=650, height=600)

        plot_red = plotting.figure(x_range = filtered_red.data['team'],
                                y_range=plot_blue.y_range,
                                x_axis_label="Team",
                                title= "Red Alliance Points",
                                tools = "hover",
                                tooltips = "@team $name: @$name",
                                width=650, height=600)

        vbar_blue = plot_blue.vbar_stack(self.plotting_measures,
                                x = "team",
                                color = bokeh.palettes.Blues[len(self.plotting_measures)],
                                width = 0.9,
                                source = filtered_blue)
    
        vbar_red = plot_red.vbar_stack(self.plotting_measures,
                                x = "team",
                                color = bokeh.palettes.Reds[len(self.plotting_measures)],
                                width = 0.9,
                                source = filtered_red)

        dst_start = Span(location=average_blue, dimension='width',
                         line_color='black', line_width=3)
        plot_blue.add_layout(dst_start)

        dst_end = Span(location=average_red, dimension='width',
                         line_color='black', line_width=3)
        plot_red.add_layout(dst_end)

        legend_items = [(lbl, [glyph]) for lbl, glyph in zip(self.plotting_measures, vbar_red)]
        legend = models.Legend(items = legend_items, location = "top_right")
        plot_red.add_layout(legend, 'right')

        legend_items = [(lbl, [glyph]) for lbl, glyph in zip(self.plotting_measures, vbar_blue)]
        legend = models.Legend(items = legend_items, location = "top_right")
        plot_blue.add_layout(legend, 'left')

        plot_blue.xaxis.major_label_orientation = math.pi/4
        plot_red.xaxis.major_label_orientation = math.pi/4
        return row(plot_blue, plot_red)
        



