# Udacity Porfolio: Deploy a Data Dashboard

## Nanodegree: Data Scientist

## Title: COVID-19 in Spain by Regions

## Table of Contents

<li><a href="#installation">Installation</a></li>
<li><a href="#project_motivation">Portfolio Motivation</a></li>
<li><a href="#file_descriptions">File Descriptions</a></li>
<li><a href="#results">Results</a></li>
<li><a href="#acknowledgements">Licensing, Authors, Acknowledgements</a></li>



 
<a id='installation'></a>
## Installation

See the file `requirements.txt`.


<a id='project_motivation'></a>
## Portfolio Motivation

The idea of this portfolio is to develop a dashboard using tools like flask and bootstrap, and publish it in the Heroku platform.
The theme choosen is the coronavirus COVID-19 outbreak. There are a lot of data published these days and this is my first dashboard so I don't mean to be specially insigthful. The objective is to be able to gather in a list of graphs the information I usually consult more in these days.

<a id='file_descriptions'></a>
## File Descriptions

* **Procfile:** A file that specifies to Heroku the commands that are executed by the app on startup. 

* **requirements.txt:** It shows to Heroku the packets that are necessary to import.

* **covapp.py:** To start the web app.

* **wrangling_scripts/wrangle_data.py:** It contains functions to download the data from the [datadista repository](https://github.com/datadista/datasets/tree/master/COVID%2019). It adapts the data gathered to a single dataset and builds the plotly graphs to be showed in the web page.

* **/covapp/**: A packet with the necessary files to deploy the web app.

* **/NoteBook/**: In this directory there is a version of the dashboard made in a notebook. In this version the original data was also downloaded from the datadista repository, but updatings are made directly downloading and reading the pdf published in the [Ministry of Health web page](https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm)



<a id='results'></a>
## Results

The final results can be seen in the Notebook published in this repository or in the web link: https://covid-spain-udacity.herokuapp.com/.


<a id='acknowledgements'></a>
## Licensing, Authors, Acknowledgements

As I mentioned before the data used in the dashboard is downloaded from the [datadista repository](https://github.com/datadista/datasets/tree/master/COVID%2019). I want to thank him his effort to allow us to access to the data in a much easier way than in the official web page.
