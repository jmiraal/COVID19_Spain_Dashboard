import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`


def cleandata():
    # get new cases
    df_new_cases = pd.read_csv('data/ccaa_covid19_casos_long.csv') 

    # get new deads
    df_new_deaths = pd.read_csv('data/ccaa_covid19_fallecidos_long.csv') 

    # get new ucis
    df_new_uci = pd.read_csv('data/ccaa_covid19_uci_long.csv')

    # corrections in the type of dates
    df_new_cases.date = df_new_cases.date.apply(lambda x :  pd.to_datetime(x, format='%Y/%m/%d').date())
    df_new_cases = df_new_cases.rename(columns={'total':'total_cases'})
    df_new_deaths.date = df_new_deaths.date.apply(lambda x :  pd.to_datetime(x, format='%Y/%m/%d').date())
    df_new_deaths = df_new_deaths.rename(columns={'total':'total_deaths'})
    df_new_uci.date = df_new_uci.date.apply(lambda x :  pd.to_datetime(x, format='%Y/%m/%d').date())
    df_new_uci = df_new_uci.rename(columns={'total':'total_ucis'})

    dataset = pd.merge(df_new_cases, df_new_deaths, how='left', on=['CCAA', 'cod_ine','date'])
    dataset = pd.merge(dataset, df_new_uci, how='left', on=['CCAA', 'cod_ine','date'])
    
    return dataset





def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    
    
    figures = []
    df = cleandata()
    #df.sort_values(['CCAA', 'date'], ascending=False, inplace=True)
    region_list = df.CCAA.unique().tolist()
    
    for region in region_list:
        df_region = df[df['CCAA'] == region]
        graph = []
        x_val = df_region.date.tolist()
        y_val =  df_region.total_cases.tolist()
        graph.append(
            go.Scatter(
            x = x_val,
            y = y_val,
            mode = 'lines',
            name = 'Total Cases'
            )
        )
        
        if df_region.total_cases.max() >= 10:
            date_reference = df_region[df_region.total_cases >= 10].head(1).date.values[0]
        else:
            date_reference_str = '2020-03-08'
            date_reference = datetime.strptime(date_reference_str, '%Y-%m-%d').date()
    
        # the number of cases the day of reference
        value_reference = df_region[df_region.date == date_reference].total_cases.values[0]
    
        # last day of the graph and number of days since the day of reference
        date_line_2 = df_region.date.max()
        max_limit = date_line_2 - date_reference
    
        # first day of the graph and number of days to the day of reference
        date_line_1 = df_region.date.min()
        min_limit = date_reference - date_line_1
    
        # extrapolation of the number of cases for the blue line
        value_line_3_1 = value_reference / (2 ** (min_limit.days/3))
        value_line_3_2 = value_reference * (2 ** (max_limit.days/3))
    
        # extrapolation of the number of cases for the blue line
        value_line_4_1 = value_reference / (2 ** (min_limit.days/7))
        value_line_4_2 = value_reference * (2 ** (max_limit.days/7))
    
        # extrapolation of the number of cases for the blue line
        value_line_2_1 = value_reference / (2 ** (min_limit.days/2))
        value_line_2_2 = value_reference * (2 ** (max_limit.days/2))
        
        
        graph.append(
            go.Scatter(
            x = [date_line_1, date_line_2],
            y = [value_line_3_1, value_line_3_2],
            mode = 'lines',
            opacity = 0.5,
            name = 'Double 3 Days',
            line = dict(color = ('Purple'))       
            )
         )
        
        graph.append(
             go.Scatter(
             x = [date_line_1, date_line_2],
             y = [value_line_4_1, value_line_4_2],
             mode = 'lines',
             opacity = 0.5,
             name = 'Double 7 Days',
             line = dict(color = ('MediumPurple'))
                         
             )
           )
            
        graph.append(
              go.Scatter(
              x = [date_line_1, date_line_2],
              y = [value_line_2_1, value_line_2_2],
              mode = 'lines',
              opacity = 0.5,
              name = 'Double 2 Days',
              line = dict(color = ('MediumPurple'))
                         
              )
          )        
        
         
        
        
   
       
        layout = dict(title = 'Tocal cases in: ' + region,
                          xaxis = dict(title = 'Day',
                                       autotick=True),
                          yaxis = dict(title = 'Cases (Log Sacale)', 
                                       type="log"),
                          showlegend=True,
                      legend=dict(
                                   x=0.02,
                                   y=1,
                                   traceorder="normal",
                                   font=dict(
                                             family="sans-serif",
                                             size=12,
                                             color="black"
                                             ),
                                   bgcolor="white",
                                   bordercolor="LightBlue",
                                   borderwidth=2
                           
                          )
                     )
                         
        figures.append(dict(data=graph, layout=layout))
        
        graph = []
        x_val = df_region.date.tolist()
        y_val = df_region.total_deaths.diff(periods=1).tolist()
        graph.append(
            go.Scatter(
            x = x_val,
            y = y_val,
            type = 'bar',
            name = region
            )
        )

       
        layout = dict(title = 'Deaths per Day in: ' + region,
                      xaxis = dict(title = 'Day',
                      autotick=True),
                      showlegend=False,
                      yaxis = dict(title = 'Deaths'),
                      )
                         
        figures.append(dict(data=graph, layout=layout))
    
    return figures