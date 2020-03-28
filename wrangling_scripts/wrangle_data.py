import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`


def cleandata():
    # get new cases
    df_new_cases = pd.read_csv('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_casos_long.csv')
    df_new_cases = df_new_cases.rename(columns={'fecha': 'date'})

    # get new deaths data
    df_new_deaths = pd.read_csv('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_fallecidos_long.csv')
    df_new_deaths = df_new_deaths.rename(columns={'fecha': 'date'})

    # get new ucis data
    df_new_uci = pd.read_csv('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_uci_long.csv')
    df_new_uci = df_new_uci.rename(columns={'fecha': 'date'})

    # get new hospital data
    df_new_hospital = pd.read_csv('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_hospitalizados_long.csv')
    df_new_hospital = df_new_hospital.rename(columns={'fecha': 'date'})

    # get new healed data
    df_new_healed = pd.read_csv('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_altas_long.csv')
    df_new_healed = df_new_healed.rename(columns={'fecha': 'date'})

    # get icu in 2017 data
    df_new_icu_beds_2017 = pd.read_csv('https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_camas_uci_2017.csv')
    df_new_icu_beds_2017 = df_new_icu_beds_2017.rename(columns={'fecha': 'date'})

    
    # corrections in the type of dates
    df_new_cases.date = df_new_cases.date.apply(lambda x :  pd.to_datetime(x, format='%Y/%m/%d').date())
    df_new_deaths.date = df_new_deaths.date.apply(lambda x :  pd.to_datetime(x, format='%Y/%m/%d').date())
    df_new_uci.date = df_new_uci.date.apply(lambda x :  pd.to_datetime(x, format='%Y/%m/%d').date())
    df_new_hospital.date = df_new_hospital.date.apply(lambda x :  pd.to_datetime(x, format='%Y/%m/%d').date())
    df_new_healed.date = df_new_healed.date.apply(lambda x :  pd.to_datetime(x, format='%Y/%m/%d').date())

    # rename the column total to make a merge
    df_new_cases = df_new_cases.rename(columns={'total':'total_cases'})
    df_new_deaths = df_new_deaths.rename(columns={'total':'total_deaths'})
    df_new_uci = df_new_uci.rename(columns={'total':'total_ucis'})
    df_new_hospital = df_new_hospital.rename(columns={'total':'total_hospital'})
    df_new_healed = df_new_healed.rename(columns={'total':'total_healed'})
    df_new_icu_beds_2017 = df_new_icu_beds_2017.rename(columns={'Total':'total_icu_beds'})

    # add a row with the total icu beds in df_new_icu_beds_2017 for all the regions
    df_new_icu_beds_2017 = df_new_icu_beds_2017.drop(columns= 'CCAA')
    aux = df_new_icu_beds_2017.sum(axis=0)
    aux.cod_ine = 0
    df_new_icu_beds_2017 = df_new_icu_beds_2017.append(aux, ignore_index=True)

    # merge all the datasets
    dataset = pd.merge(df_new_cases, df_new_deaths, how='left', on=['CCAA', 'cod_ine','date'])
    dataset = pd.merge(dataset, df_new_uci, how='left', on=['CCAA', 'cod_ine','date'])
    dataset = pd.merge(dataset, df_new_hospital, how='left', on=['CCAA', 'cod_ine','date'])
    dataset = pd.merge(dataset, df_new_healed, how='left', on=['CCAA', 'cod_ine','date'])
    dataset = pd.merge(dataset, df_new_icu_beds_2017, how='left', on=['cod_ine'])
    dataset = dataset.sort_values(by=['cod_ine', 'date'])
    
    return dataset





def return_figures(panel = 1):
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
    region_list = df.CCAA.unique().tolist()
    if panel == 1:
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
                          legend=dict(x=0.02,
                                      y=1,
                                      traceorder="normal",
                                      font=dict(family="sans-serif",
                                               size=12,
                                               color="black"),
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
                go.Bar(
                x = x_val,
                y = y_val,
                name = region,
                )
            )

       
            layout = dict(title = 'Deaths per Day in: ' + region,
                         xaxis = dict(title = 'Day',
                         autotick=True),
                         showlegend=False,
                         yaxis = dict(title = 'Deaths'),
                         )
                         
            figures.append(dict(data=graph, layout=layout))
    
    elif panel == 2:
        for region in region_list:
            df_region = df[df['CCAA'] == region]
            df_region = df_region[df_region.date >= datetime.strptime('2020-03-21', '%Y-%m-%d').date()]
            graph = []
            x_val = df_region.date.tolist()
            y_val_hosp =  df_region.total_hospital.tolist()    
            y_val_heal =  df_region.total_healed.tolist()
            y_val_ucis =  df_region.total_ucis.tolist()
            y_val_icu_beds =  df_region.total_icu_beds.tolist()
            
            y_val_hosp_1 = [x + y for x, y in zip(y_val_ucis, y_val_hosp)]
            y_val_heal_1 = [x + y for x, y in zip(y_val_heal, y_val_hosp_1)]
            
            
            
            graph.append(
                go.Scatter(
                x = x_val,
                y = y_val_ucis,
                mode = 'lines',
                name = 'ICUs',
                hoverinfo = 'text',
                hovertext = ['ICUs: ' + str(e) for e in y_val_ucis],
                fill = 'tonexty',
                fillcolor = 'orange',
                line = dict(color = ('orange')),
    
                )
            ) 
            
            graph.append(
                go.Scatter(
                x = x_val,
                y = y_val_hosp_1,
                mode = 'lines',
                name = 'Hospital',
                fill = 'tonexty',
                hoverinfo = 'text',
                hovertext = ['Hospital: ' + str(e) for e in y_val_hosp],
                fillcolor = 'royalblue',
                line = dict(color = ('royalblue')),
                    
                )
            )
            
            graph.append(
                go.Scatter(
                x = x_val,
                y = y_val_heal_1,
                mode = 'lines',
                name = 'Healed',
                hoverinfo = 'text',
                hovertext = ['Healed: ' + str(e) for e in y_val_heal],
                fill = 'tonexty',
                fillcolor = 'forestgreen',
                line = dict(color = ('forestgreen')),
    
                )
            )
            
            graph.append(
                go.Scatter(
                x = x_val,
                y = y_val_icu_beds,
                mode = 'lines',
                name = 'ICU Beds 2017',
                hoverinfo = 'text',
                
                hovertext = ['ICU Beds 2017: ' + str(e) for e in y_val_icu_beds],
                line = dict(color = ('red')),
    
                )
            )

   
            layout = dict(title = 'Tocal cases in: ' + region,
                          xaxis = dict(title = 'Day',
                                       autotick=True),
                          yaxis = dict(title = 'Cases'),
                          showlegend=True,
                          legend=dict(x=0.02,
                                      y=1,
                                      traceorder="normal",
                                      font=dict(family="sans-serif",
                                               size=12,
                                               color="black"),
                                      bgcolor="white",
                                      bordercolor="LightBlue",
                                      borderwidth=2
                           
                             )
                        )
                         
            figures.append(dict(data=graph, layout=layout))
    
    return figures