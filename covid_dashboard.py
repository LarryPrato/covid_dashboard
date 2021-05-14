import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

pip install --upgrade pip

st.set_page_config(page_title="Covid Dashboard", layout="wide")
st.markdown('<style>body{background-color: #edf7ef;}</style>',unsafe_allow_html=True)

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
    return df

df_orig= load_data()
df_orig['cases_per_100k'] = df_orig['total_cases']/df_orig['population']*100000
df_orig['daily_new_cases_per_100k'] = round(df_orig['new_cases']/df_orig['population']*100000,0)
df_orig['daily_new_cases_per_100k_sma'] = round(df_orig.daily_new_cases_per_100k.rolling(14).mean(),0)
df_orig['daily_new_deaths_per_100k'] = round(df_orig['new_deaths']/df_orig['population']*100000,0)
df_orig['daily_new_deaths_per_100k_sma'] = round(df_orig.daily_new_deaths_per_100k.rolling(14).mean(),3)
df = df_orig.set_index('date')
df['cases_per_100k'] = df['total_cases']/df['population']*100000
df['deaths_per_100k'] = df['total_deaths']/df['population']*100000
df['daily_new_cases_per_100k'] = df['new_cases']/df['population']*100000
df['fatal_rate'] = df['total_deaths']/df['total_cases']
df['vacinated_perc'] = round(df.people_vaccinated/df.population, 4)
df['new_cases_MA14'] = round(df.new_cases.rolling(14).mean(), 0)
df = df.round({'cases_per_100k':1, 'deaths_per_100k':1, 'fatal_rate':2})


#list of all countries
countries = df.location.unique().tolist()
countries = pd.DataFrame(countries)
col_rename = {0 : "country"}
countries = countries.rename(columns = col_rename)

#last_date
last_date = df.last_valid_index()

#summarizing by country
df_country_summ = df.groupby(['location']).last()
#reseting country as index
df_country_summ = df_country_summ.reset_index()

data_sum = df_country_summ.copy() # deleting NaN

data_sum['cases_per_100k'] = data_sum['total_cases']/data_sum['population']*100000
data_sum['deaths_per_100k'] = data_sum['total_deaths']/data_sum['population']*100000
data_sum['fatal_rate'] = data_sum['total_deaths']/data_sum['total_cases']
data_sum = data_sum.round({'cases_per_100k':1, 'deaths_per_100k':1, 'fatal_rate':2 })
data_sum['deaths_per_100k'] = data_sum['deaths_per_100k'].fillna(0) # countries with 0 deaths
data_sum=data_sum[data_sum['continent'].notna()]
data_sum=data_sum[data_sum['total_cases'].notna()]

###Header#####################################################################################
st.info('# ** COVID STACTISTICS **   ')
st.markdown('**	 Updated: **'+ last_date)
st.markdown('***')

###Global summary############################################################################
summ_glob_cases_per_100k = round(data_sum.total_cases.sum()/data_sum.population.sum()*100000,0)
summ_glob_deaths_per_100k = round(data_sum.total_deaths.sum()/data_sum.population.sum()*100000,0)
summ_glob_total_cases = round(data_sum.total_cases.sum(),0)
summ_glob_total_deaths = round(data_sum.total_deaths.sum(),0)
summ_glob_max_cases_per_100k = data_sum['cases_per_100k'].max()
summ_glob_max_deaths_per_100k = data_sum['deaths_per_100k'].max()
#st.write(summ_glob_max_cases_per_100k)
#st.write(summ_glob_max_deaths_per_100k)

with st.beta_container():
	#st.header('Global summary')
	st.markdown( "<span style='color: #1e6777; font-size:2.1em'>Global summary</span>", unsafe_allow_html= True)
	#Cards metrics
	col1, col2, col3, col4 = st.beta_columns([1,1,1,1])
	with col1:
	   fig = go.Figure(go.Indicator(
	   	mode = "number",
    	value = summ_glob_total_cases,
    	title = {"text": "Total confirmed cases", "font" : {"size":20, 'color': "#1e6777", 'family': "Arial"} },
    	number = {"font" : {"size":28, 'color': "#1e6777", 'family': "Arial"}, "valueformat": "#,##0"},
    	align = "center",
    	domain = {'x': [0, 1], 'y': [0, 1]}))
	   fig.update_layout(autosize=False,
	   	width=290,
    	height=120,
    	margin=dict(
    		l=20,
    		r=20,
        	b=20,
        	t=20,
        	pad=4),
    	paper_bgcolor = "#d5e9eb")
	   st.plotly_chart(fig)

	with col2:
	   fig = go.Figure(go.Indicator(
	   	mode = "number",
    	value = summ_glob_total_deaths,
    	title = {"text": "Total deaths", "font" : {"size":20, 'color': "#1e6777", 'family': "Arial"} },
    	number = {"font" : {"size":28, 'color': "#1e6777", 'family': "Arial"}, "valueformat": "#,##0"},
    	align = "center",
    	domain = {'x': [0, 1], 'y': [0, 1]}))
	   fig.update_layout(autosize=False,
	   	width=290,
    	height=120,
    	margin=dict(
    		l=20,
    		r=20,
        	b=20,
        	t=20,
        	pad=4),
    	paper_bgcolor = "#d5e9eb")
	   st.plotly_chart(fig)

	with col3:
	   fig = go.Figure(go.Indicator(
	   	mode = "number",
    	value = summ_glob_cases_per_100k,
    	title = {"text": "Total cases per 100,000 people", "font" : {"size":20, 'color': "#1e6777", 'family': "Arial"} },
    	number = {"font" : {"size":28, 'color': "#1e6777", 'family': "Arial"}, "valueformat": "#,##0"},
    	align = "center",
    	domain = {'x': [0, 1], 'y': [0, 1]}))
	   fig.update_layout(autosize=False,
	   	width=290,
    	height=120,
    	margin=dict(
    		l=20,
    		r=20,
        	b=20,
        	t=20,
        	pad=4),
    	paper_bgcolor = "#d5e9eb")
	   st.plotly_chart(fig)

	with col4:
	   fig = go.Figure(go.Indicator(
	   	mode = "number",
    	value = summ_glob_deaths_per_100k,
    	title = {"text": "Total deaths per 100,000 people", "font" : {"size":20, 'color': "#1e6777", 'family': "Arial"} },
    	number = {"font" : {"size":28, 'color': "#1e6777", 'family': "Arial"}, "valueformat": "#,##0"},
    	align = "center"))
	   fig.update_layout(autosize=False,
	   	width=290,
    	height=120,
    	margin=dict(
    		l=20,
    		r=20,
        	b=20,
        	t=20,
        	pad=4),
    	paper_bgcolor = "#d5e9eb")
	   st.plotly_chart(fig)

#Treemap#####################################################################
with st.beta_container():
	col1, col2, col3 = st.beta_columns([1,5,2])	
	with col1:
		st.write(' ')
	with col2:
		fig = px.treemap(data_sum, path=['continent', 'location'], values='total_cases',
	                  color='cases_per_100k',
	                  color_continuous_scale='ice_r', width=1030, height=625,
	                  color_continuous_midpoint=np.average(data_sum['cases_per_100k'], weights=data_sum['cases_per_100k']))
		fig.update_layout(
	    	title_text='Total confirmed cases',
	    	paper_bgcolor="#edf7ef",    
		    title={'y':0.95,
		        'x':0.5,
		        'xanchor': 'center',
		        'yanchor': 'top',
		        'font' : {"size":22, 'color': "#1E6777", 'family': "Arial"}
		        })
		st.plotly_chart(fig)
	with col3:
		st.write(' ')

#Choropleth map##############################################################################
with st.beta_container():
	col1, col2, col3 = st.beta_columns([1,8,1])	
	with col1:
		st.write(' ')

	with col2:
		#st.header('Cases per 100k')
		fig = go.Figure(data=go.Choropleth(
		    locations = data_sum['iso_code'],
		    z = data_sum['cases_per_100k'],
		    text = data_sum['location'],
		    colorscale = 'PuBu',
		    autocolorscale=False,
		    reversescale=False,
		    marker_line_color='darkgray',
		    marker_line_width=0.5,
		    colorbar_tickprefix = '',
		    colorbar_title = '',
		))

		fig.update_layout(
		    title_text='Cases per 100k',
		    paper_bgcolor="#edf7ef", # background
		    autosize=False,
		    width=1030,
		    height=625,
		    margin=dict(l=5, r=5, b=5, t=30),
		    geo=dict(
		    	showframe=False,
		        showcoastlines=False,
		        resolution=50,
		        showocean=True, oceancolor="#092834",#141d1f",
		        projection_type='equirectangular'
		        
		    ),    
		    title={
		        'text': "Cases per 100,000 people",
		        'y':0.9,
		        'x':0.5,
		        'xanchor': 'center',
		        'yanchor': 'top',
		        'font' : {"size":22, 'color': "#1E6777", 'family': "Arial"}
		        }
		)
		st.plotly_chart(fig)
	with col3:
		st.write(' ')

#Bubble map####################################################################################
with st.beta_container():
	col1, col2, col3 = st.beta_columns([1,8,1])	
	with col1:
		st.write(' ')

	with col2:
		fig = px.scatter_geo(data_sum, locations="iso_code",
			hover_name="location", size="deaths_per_100k", 
			width=900, height=600)
		fig.update_geos(
		    visible=False, resolution=50,
		    showcountries=True, countrycolor="#bbc7c6",
		    showocean=True, oceancolor="#092834")
		fig.update_layout(paper_bgcolor="#edf7ef",
			margin=dict(l=5, r=5, b=5, t=30),
			title={
		        'text': "Deaths per 100,000 people",
		        'y':0.9,
		        'x':0.5,
		        'xanchor': 'center',
		        'yanchor': 'top',
		        'font' : {"size":22, 'color': "#1E6777", 'family': "Arial"}
		        })
		fig.update_traces(marker=dict(color="#C86D38"))
		st.plotly_chart(fig)
	with col3:
		st.write(' ')	

#Global vacination info##########################################################################
df_vaccination = df_orig[["date", "location", "people_vaccinated", "population"]].copy()
df_vaccination = df_vaccination.dropna()
df_vaccination = df_vaccination.drop_duplicates('location', keep = 'last')
df_vaccination['perc_vacc'] = round(df_vaccination.people_vaccinated/df_vaccination.population, 4)
perc_world_pop_vac = df_vaccination['perc_vacc'].iloc[-2]*100
#st.write(df_vaccination)
#st.write(perc_world_pop_vac)

with st.beta_container():
	col1, col2, col3 = st.beta_columns([1,5,1])	
	with col1:
		st.write(' ')

	with col2:
		st.markdown( "<span style='color: #1e6777; font-size:1.5em'>World population vacinated (%)</span>", unsafe_allow_html= True)
		fig = go.Figure(go.Indicator(
    		mode = "gauge", value = perc_world_pop_vac,
    		domain = {'x': [0, 1], 'y': [0, 1]},
    		gauge = {
		        'shape': "bullet",
		        'axis': {'range': [None, 100]},
		        'bgcolor': "white",
		        'steps': [
		            {'range': [0, 100], 'color': "#092834"}],
		        'bar': {'color': "#636efa", 'thickness': 0.75}}))
		fig.update_layout(height = 90, width=900,  paper_bgcolor ="#edf7ef", plot_bgcolor="#092834", 
			margin=dict(l=5, r=80, b=25, t=5))

		st.plotly_chart(fig)

	with col3:
		st.write(' ')
		st.write(' ')
		st.write(' ')
		st.write(' ')
		st.write(' ')
		perc_world_pop_vac = round(perc_world_pop_vac, 4)
		st.markdown(perc_world_pop_vac)


###Subplots ########################################################################
data_sum.vacinated_perc.fillna(value = 0, inplace = True)
df_top20_cases_per_100k = data_sum.sort_values('cases_per_100k', ascending = False).head(20)
df_top20_cases_per_100k = df_top20_cases_per_100k[["location", "cases_per_100k", "vacinated_perc"]].copy()
df_top20_cases_per_100k.set_index('location')

df_top_vacinated = data_sum.sort_values('vacinated_perc', ascending = False).head(20)
df_top_vacinated = df_top_vacinated[["location", "cases_per_100k", "deaths_per_100k", "vacinated_perc"]].copy()
df_top_vacinated.set_index('location')

# Data
tops = df_top20_cases_per_100k.location
cases_ = df_top20_cases_per_100k.cases_per_100k
vacinates = df_top20_cases_per_100k.vacinated_perc

with st.beta_container():
	st.write(' ')
	st.markdown( "<span style='color: #1e6777; font-size:1.5em'>Cases per 100,000 people vs. Population Vacinated (%)</span>", unsafe_allow_html= True)
	col1, col2, col3, col4 = st.beta_columns([5,1,5,1])	

	with col1:
		# Data
		df_top20_cases_per_100k = df_top20_cases_per_100k.sort_values('cases_per_100k', ascending = True)
		tops = df_top20_cases_per_100k.location
		cases_ = df_top20_cases_per_100k.cases_per_100k
		vacinates = df_top20_cases_per_100k.vacinated_perc*100

		fig, axes = plt.subplots(ncols=2, sharey=True)
		axes[0].barh(tops, cases_, align='center', color='#092834')
		axes[0].set(title='Cases per 100,000 people')
		axes[1].barh(tops, vacinates, align='center', color='#636efa')
		axes[1].set(title='Population vacinated (%)')
		axes[1].xaxis.set_major_locator(plt.MaxNLocator(7))

		axes[0].invert_xaxis()
		axes[0].yaxis.tick_left()

		for ax in axes.flat:
		    ax.margins(0.04)
		    ax.grid(False)
		    ax.set_facecolor('#edf7ef')

		fig.patch.set_facecolor('#edf7ef')
		fig.tight_layout()
		fig.set_figheight(10)
		fig.set_figwidth(7)
		st.pyplot(plt)

	with col2:
		st.write(' ')

	with col3:
		# Data
		df_top_vacinated = df_top_vacinated.sort_values('vacinated_perc', ascending = True)
		tops = df_top_vacinated.location
		cases_ = df_top_vacinated.cases_per_100k
		vacinates = df_top_vacinated.vacinated_perc*100

		fig, axes = plt.subplots(ncols=2, sharey=True)
		axes[0].barh(tops, cases_, align='center', color='#092834')
		axes[0].set(title='Cases per 100,000 people')
		axes[1].barh(tops, vacinates, align='center', color='#636efa')
		axes[1].set(title='Population vacinated (%)')
		axes[1].xaxis.set_major_locator(plt.MaxNLocator(7))

		axes[0].invert_xaxis()
		axes[0].yaxis.tick_left()

		for ax in axes.flat:
		    ax.margins(0.04)
		    ax.grid(False)
		    ax.set_facecolor('#edf7ef')

		fig.patch.set_facecolor('#edf7ef')
		fig.tight_layout()
		fig.set_figheight(10)
		fig.set_figwidth(7)
		fig = plt.gcf() 
		st.pyplot(fig)

	with col4:
		st.write(' ')


####Summary by country##############################################################
with st.beta_container():
	#st.header('Summary by country')
	st.markdown( "<span style='color: #1e6777; font-size:2.1em'>Country summary</span>", unsafe_allow_html= True)	
	country_selected  = st.selectbox(' Select country', countries)

	df_summ_by_country = df[df.location==country_selected]
	df_summ_by_country['people_vaccinated'] = df_summ_by_country['people_vaccinated'].fillna(method= 'ffill')# fill na values with previous valid value
	
	summ_total_cases = df_summ_by_country.total_cases[-1]
	
	summ_total_deaths = df_summ_by_country.total_deaths[-1]
	
	summ_cases_per_100k = df_summ_by_country.cases_per_100k[-1]
	
	summ_deaths_per_100k = df_summ_by_country.deaths_per_100k[-1]
	
	summ_people_vaccinated = round(df_summ_by_country.people_vaccinated[-1]/df_summ_by_country.population[-1], 3) #people_vaccinated

	df_summ_by_country.vacinated_perc.fillna(method= 'ffill', inplace = True)
	perc_people_vacc_by_country = df_summ_by_country['vacinated_perc'].iloc[-1]*100

	#st.dataframe(start_vacc_by_country)
	#st.write(country_selected)
	#st.write(perc_people_vacc_by_country)

	#row 1 - Cards   ###############
	col1, col2, col3, col4 = st.beta_columns([1,1,1,1])
	with col1:
	   fig = go.Figure(go.Indicator(
	   	mode = "number",
    	value = summ_total_cases,
    	title = {"text": "Total confirmed cases", "font" : {"size":20, 'color': "#1E6777", 'family': "Arial"} },
    	number = {"font" : {"size":28, 'color': "#1E6777", 'family': "Arial"}, "valueformat": "#,##0"},
    	align = "center",
    	domain = {'x': [0, 1], 'y': [0, 1]}))
	   fig.update_layout(autosize=False,
	   	width=290,
    	height=120,
    	margin=dict(
    		l=20,
    		r=20,
        	b=20,
        	t=20,
        	pad=4),
    	paper_bgcolor = "#d5e9eb")
	   st.plotly_chart(fig)

	with col3:
	   fig = go.Figure(go.Indicator(
	   	mode = "number",
    	value = summ_total_deaths,
    	title = {"text": "Total deaths", "font" : {"size":20, 'color': "#1E6777", 'family': "Arial"} },
    	number = {"font" : {"size":28, 'color': "#1E6777", 'family': "Arial"}, "valueformat": "#,##0"},
    	align = "center",
    	domain = {'x': [0, 1], 'y': [0, 1]}))
	   fig.update_layout(autosize=False,
	   	width=290,
    	height=120,
    	margin=dict(
    		l=20,
    		r=20,
        	b=20,
        	t=20,
        	pad=4),
    	paper_bgcolor = "#d5e9eb")
	   st.plotly_chart(fig)

	with col2:
	   fig = go.Figure(go.Indicator(
	   	mode = "number",
    	value = summ_cases_per_100k, #round(data_sum.total_cases.sum()/data_sum.population.sum()*100000,0),
    	title = {"text": "Total cases per 100,000 people", "font" : {"size":20, 'color': "#1E6777", 'family': "Arial"} },
    	number = {"font" : {"size":28, 'color': "#1E6777", 'family': "Arial"}, "valueformat": "#,##0"},
    	align = "center",
    	domain = {'x': [0, 1], 'y': [0, 1]}))
	   fig.update_layout(autosize=False,
	   	width=290,
    	height=120,
    	margin=dict(
    		l=20,
    		r=20,
        	b=20,
        	t=20,
        	pad=4),
    	paper_bgcolor = "#d5e9eb")
	   st.plotly_chart(fig)

	with col4:
	   fig = go.Figure(go.Indicator(
	   	mode = "number",
    	value = summ_deaths_per_100k,
    	title = {"text": "Total deaths per 100,000 people", "font" : {"size":20, 'color': "#1E6777", 'family': "Arial"} },
    	number = {"font" : {"size":28, 'color': "#1E6777", 'family': "Arial"}, "valueformat": "#,##0"},
    	align = "center"))
	   fig.update_layout(autosize=False,
	   	width=290,
    	height=120,
    	margin=dict(
    		l=20,
    		r=20,
        	b=20,
        	t=20,
        	pad=4),
    	paper_bgcolor = "#d5e9eb")
	   st.plotly_chart(fig)

	   #row 2 - Gaugemeters  ###############
	col1, col2, col3, col4, col5 = st.beta_columns([1,4,1,4,1])
	with col1:
	   st.write(" ")

	with col2:
	   fig = go.Figure(go.Indicator(
	   		mode = "gauge+number",
			value = summ_cases_per_100k,
			domain = {'x': [0, 1], 'y': [0, 1]},
			title = {'text': "Cases per 100,000 people", 'font': {'size': 20, 'color': '#1E6777'}},
    		number = {"font" : {"size":30, 'color': "#C86D38", 'family': "Arial"}, "valueformat": "#,##0"},
			gauge = {
			    'axis': {'range': [None, summ_glob_max_cases_per_100k], 'tickwidth': 1, 'tickcolor': "darkblue"},
			    'bar': {'color': 'rgba(200,109,56, 0.6)', 'thickness': 0.75},
			    'bgcolor': "#1A3E4C",
			    'borderwidth': 0,
			    'bordercolor': "gray",
			    'steps': [
			        {'range': [0, summ_glob_cases_per_100k], 'color': '#E4F1F6'},
			        {'range': [summ_glob_cases_per_100k, summ_glob_max_cases_per_100k], 'color': '#347B98'}],
			    'threshold': {
			        'line': {'color': "white", 'width': 2},
			        'thickness': 0.1,
			        'value': summ_glob_max_cases_per_100k}}))
	   fig.update_layout(paper_bgcolor = "#edf7ef", font = {'color': "darkblue", 'family': "Arial"}, height= 220, width=330, 
	   	margin=dict(
    		l=5,
    		r=10,
        	b=40,
        	t=45,
        	pad=10))
	   fig.update_yaxes(automargin=True)
	   st.plotly_chart(fig)

	with col3:
	   st.write(" ")

	with col4:
	   fig = go.Figure(go.Indicator(
	   		mode = "gauge+number",
			value = summ_deaths_per_100k,
			domain = {'x': [0, 1], 'y': [0, 1]},
			title = {'text': "Deaths per 100,000 people", 'font': {'size': 20, 'color': '#1E6777'}},
    		number = {"font" : {"size":30, 'color': "#C86D38", 'family': "Arial"}, "valueformat": "#,##0"},
			gauge = {
			    'axis': {'range': [None, summ_glob_max_deaths_per_100k], 'tickwidth': 1, 'tickcolor': "darkblue"},
			    'bar': {'color': 'rgba(200,109,56, 0.7)', 'thickness': 0.75},
			    'bgcolor': "#1A3E4C",
			    'borderwidth': 0,
			    'bordercolor': "gray",
			    'steps': [
			        {'range': [0, summ_glob_deaths_per_100k], 'color': '#E4F1F6'},
			        {'range': [summ_glob_deaths_per_100k, summ_glob_max_deaths_per_100k], 'color': '#347B98'}],
			    'threshold': {
			        'line': {'color': "white", 'width': 2},
			        'thickness': 0.1,
			        'value': summ_glob_max_deaths_per_100k}}))
	   fig.update_layout(paper_bgcolor = "#edf7ef", font = {'color': "darkblue", 'family': "Arial"}, height= 220, width=330, 
	   	margin=dict(
    		l=5,
    		r=10,
        	b=40,
        	t=45,
        	pad=10))
	   st.plotly_chart(fig)

	with col5:
		st.write(" ")

### Map for selected country##############################################################

with st.beta_container():
	col1, col2, col3 = st.beta_columns([1,3,1])
	with col1:
		st.write(" ")

	with col2:
		dfp = df[df['location']==country_selected]
		fig = px.line(x=dfp.index, y=dfp.new_cases_MA14, template="plotly_dark", color=px.Constant("Moving average 14 days"),
			labels=dict(x=" ", y="Daily cases"))		
		fig.add_bar(x=dfp.index, y=dfp.new_cases, name= country_selected)		
		fig.update_layout(title={'text':"Daily confirmed cases", 'x': 0.5},  plot_bgcolor="#092834", paper_bgcolor = "#092834", 
			height= 480, width=800, showlegend=True, margin=dict(l=20, r=10, b=10,t=40, pad=0), 
			legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, title= ''))
		fig.update_xaxes( ticks="inside",  title_font=dict(size=14, family='Courier', color='white'))
		fig.update_yaxes(showline=True, linewidth=1, linecolor='white', zeroline=True, zerolinewidth=1, zerolinecolor='white', title_font=dict(size=14, family='Courier', color='white'))
		fig.update_traces(marker_color='white')
		st.plotly_chart(fig)

	with col3:
		st.write(" ")

### Info vacination
with st.beta_container():
	col1, col2, col3 = st.beta_columns([1,3,1])
	with col1:
		st.write(" ")

	with col2:
		st.write(" ")
		st.markdown( "<span style='color: #1E6777; font-size:1.5em'>Country population vacinated (%)</span>", unsafe_allow_html= True)
		fig = go.Figure(go.Indicator(
    		mode = "gauge", value = perc_people_vacc_by_country,
    		domain = {'x': [0, 1], 'y': [0, 1]},
    		gauge = {
		        'shape': "bullet",
		        'axis': {'range': [None, 100]},
		        'bgcolor': "white",
		        'steps': [
		            {'range': [0, 100], 'color': "#092834"}],
		        'bar': {'color': "#636efa", 'thickness': 0.60}}))
		fig.update_layout(height = 68, width=650, paper_bgcolor ="#edf7ef", plot_bgcolor="#092834", 
			margin=dict(l=5, r=10, b=20, t=0))

		st.plotly_chart(fig)

	with col3:
		st.write(" ")
		st.write(" ")
		st.write(" ")
		st.write(" ")
		st.write(" ")
		perc_people_vacc_by_country = round(perc_people_vacc_by_country, 4)
		st.markdown(perc_people_vacc_by_country)

### Country selection

with st.beta_container():
	col1, col2, col3 = st.beta_columns([1,3,1])
	with col1:
		st.write(" ")

	with col2:
		st.write(' ')
		st.markdown( "<span style='color: #1e6777; font-size:1.5em'>Evolution of cases per 100,000 people for countries selection</span>", unsafe_allow_html= True)
		options = "Brazil"
		options = st.multiselect(
			' Select countries to compare', countries)
		fig = go.Figure()
		for c in options:
		    dfp = df_orig[df_orig['location']==c].pivot(index='date', columns='location', values='cases_per_100k') 
		    fig.add_traces(go.Scatter(x=dfp.index, y=dfp[c], mode='lines', name = c))
		    fig.update_layout(title={'text':"Cases per 100,000 people for selected countries ", 'x': 0.5}, plot_bgcolor="#092834", paper_bgcolor = "#092834", height= 480, width=800, template="plotly_dark",
				margin=dict(l=20, b=10, t=40, pad=0), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01 ))
		fig.update_yaxes(showline=True, linewidth=1, linecolor='white', zeroline=True, zerolinewidth=1, zerolinecolor='white', title_font=dict(size=14, family='Courier', color='white'))
		st.plotly_chart(fig)
		
		#####Daily new cases per 100K
		fig = go.Figure()
		for c in options:
		    dfp = df_orig[df_orig['location']==c].pivot(index='date', columns='location', values='daily_new_cases_per_100k_sma') 
		    fig.add_traces(go.Scatter(x=dfp.index, y=dfp[c], mode='lines', name = c))
		    fig.update_layout(title={'text':"Daily new cases per 100,000 people for selected countries (sma14)", 'x': 0.5}, plot_bgcolor="#092834", paper_bgcolor = "#092834", height= 480, width=800, template="plotly_dark",
				margin=dict(l=20, b=10, t=40, pad=0), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01 ))
		fig.update_yaxes(showline=True, linewidth=1, linecolor='white', zeroline=True, zerolinewidth=1, zerolinecolor='white', title_font=dict(size=14, family='Courier', color='white'))
		st.plotly_chart(fig)
		#####
		
		#####Daily new deaths per 100K
		fig = go.Figure()
		for c in options:
		    dfp = df_orig[df_orig['location']==c].pivot(index='date', columns='location', values='daily_new_deaths_per_100k_sma') 
		    fig.add_traces(go.Scatter(x=dfp.index, y=dfp[c], mode='lines', name = c))
		    fig.update_layout(title={'text':"Daily new deaths per 100,000 people for selected countries (sma14)", 'x': 0.5}, plot_bgcolor="#092834", paper_bgcolor = "#092834", height= 480, width=800, template="plotly_dark",
				margin=dict(l=20, b=10, t=40, pad=0), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01 ))
		fig.update_yaxes(showline=True, linewidth=1, linecolor='white', zeroline=True, zerolinewidth=1, zerolinecolor='white', title_font=dict(size=14, family='Courier', color='white'))
		st.plotly_chart(fig)
		#####
		
	with col3:
		st.write(" ")

	
st.markdown('***')

####Some interesting views##############################################################
with st.beta_container():
	st.markdown( "<span style='color: #1e6777; font-size:2.1em'>Some interesting views</span>", unsafe_allow_html= True)
	st.write(" ")
	st.write(" ")
	col1, col2 = st.beta_columns([1,1])	
	with col1:
		fig = px.scatter(data_sum, x="cases_per_100k", y="deaths_per_100k", color="location", template="plotly_dark",
			labels=dict(cases_per_100k="Cases per 100,000 people", deaths_per_100k="Deaths per 100,000 peolpe", location = "country"))
		fig.update_layout(title={'text':"Cases vs Deaths by country (per 100,000 people)", 'x': 0.5},  plot_bgcolor="#092834", paper_bgcolor = "#092834", height= 320, width=550, showlegend=False,
			margin=dict(l=10, r=10, b=10,t=40))
		fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white',ticks="inside",  title_font=dict(size=14, family='Courier', color='white'))
		fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white', title_font=dict(size=14, family='Courier', color='white'))
		st.plotly_chart(fig)


	with col2:
		fig = px.scatter(data_sum, x="cases_per_100k", y="fatal_rate", color="location", template="plotly_dark",
			labels=dict(cases_per_100k="Cases per 100,000 people", fatal_rate="Fatal rate", location = "country"))
		fig.update_layout(title={'text':"Cases per 100,000 vs Fatal rate by country", 'x': 0.5},  plot_bgcolor="#092834", paper_bgcolor = "#092834", height= 320, width=550, showlegend=False,
			margin=dict(l=20, r=10, b=10,t=40, pad=0))
		fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white',ticks="inside",  title_font=dict(size=14, family='Courier', color='white'))
		fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white', title_font=dict(size=14, family='Courier', color='white'))

		st.plotly_chart(fig)

with st.beta_container():
	st.write(" ")
	st.write(" ")
	col1, col2 = st.beta_columns([1,1])	
	with col1:
		fig = px.scatter(data_sum, y="cases_per_100k", x="gdp_per_capita", color="location", size= 'population', template="plotly_dark",
			labels=dict(cases_per_100k="Cases per 100,000 people", gdp_per_capita="GDP per capita", location = "country"))
		fig.update_layout(title={'text':"Cases per 100,000 people vs GDP per capita by country", 'x': 0.5},  plot_bgcolor="#092834", paper_bgcolor = "#092834", height= 320, width=550, showlegend=False,
			margin=dict(l=10, r=10, b=10,t=40))
		fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white',ticks="inside",  title_font=dict(size=14, family='Courier', color='white'))
		fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white', title_font=dict(size=14, family='Courier', color='white'))
		st.plotly_chart(fig)


	with col2:
		fig = px.scatter(data_sum, y="deaths_per_100k", x="gdp_per_capita", color="location", size= 'population', template="plotly_dark",
			labels=dict(cases_per_100k="Cases per 100,000 people", gdp_per_capita="GDP per capita", location = "country"))
		fig.update_layout(title={'text':"Deaths per 100,000 people vs GDP per capita by country", 'x': 0.5},  plot_bgcolor="#092834", paper_bgcolor = "#092834", height= 320, width=550, showlegend=False,
			margin=dict(l=20, r=10, b=10,t=40))
		fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white',ticks="inside",  title_font=dict(size=14, family='Courier', color='white'))
		fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='white', title_font=dict(size=14, family='Courier', color='white'))

		st.plotly_chart(fig)

with st.beta_container():
	st.write(" ")
	st.write(" ")
	col1, col2 = st.beta_columns([1,1])	
	with col1:
		fig = px.scatter(data_sum, y="cases_per_100k", x="median_age", color="location", size='population', template="plotly_dark",
			labels=dict(cases_per_100k="Cases per 100,000 people", median_age="Median age", location = "country"))
		fig.update_layout(title={'text':"Cases per 100,000 people vs Median age by country", 'x': 0.5},  plot_bgcolor="#092834", paper_bgcolor = "#092834", height= 320, width=550, showlegend=False,
			margin=dict(l=10, r=10, b=10,t=40))
		fig.update_xaxes(ticks="inside",  title_font=dict(size=14, family='Courier', color='white'))
		fig.update_yaxes(showline=True, linewidth=1, linecolor='white', zeroline=True, zerolinewidth=1, zerolinecolor='white', ticks="outside", tickwidth=1, tickcolor='#283442', ticklen=20, title_font=dict(size=14, family='Courier', color='white'))
		st.plotly_chart(fig)


	with col2:
		fig = px.scatter(data_sum, y="cases_per_100k", x="life_expectancy", color="location", size= 'population', template="plotly_dark",
			labels=dict(cases_per_100k="Cases per 100,000 people", life_expectancy="Life expectancy", location = "country"))
		fig.update_layout(title={'text':"Cases per 100,000 people vs Life expectancy by country", 'x': 0.5},  plot_bgcolor="#092834", paper_bgcolor = "#092834", height= 320, width=550, showlegend=False,
			margin=dict(l=20, r=10, b=10,t=40))
		fig.update_xaxes(ticks="inside",  title_font=dict(size=14, family='Courier', color='white'))
		fig.update_yaxes(showline=True, linewidth=1, linecolor='white', zeroline=True, zerolinewidth=1, zerolinecolor='white', ticks="outside", tickwidth=1, tickcolor='#283442', ticklen=20, title_font=dict(size=14, family='Courier', color='white'))
		st.plotly_chart(fig)


st.write(" ")
st.write(" ")

### Correlation Matriz ########################################################################################

df_corr = data_sum[['location', 'cases_per_100k', 'deaths_per_100k', 'fatal_rate', 'population_density', 'median_age',
                   'aged_65_older', 'gdp_per_capita', 'extreme_poverty', 'cardiovasc_death_rate', 'diabetes_prevalence',
                   'life_expectancy', 'human_development_index']]

st.write(" ")
st.write(" ")

with st.beta_container():
	col1, col2, col3 = st.beta_columns([1,3,1])
	with col1:
		st.write(" ")

	with col2:
		#st.markdown( "<span style='color: #1e6777; font-size:2.1em'>Correlation matrix</span>", unsafe_allow_html= True)
		corr = df_corr.corr()
		fig = go.Figure(data=go.Heatmap(
		                   z=corr[['cases_per_100k', 'deaths_per_100k', 'fatal_rate']],
		                   x=['cases_per_100k', 'deaths_per_100k', 'fatal_rate'],
		                   y=['cases_per_100k', 'deaths_per_100k', 'fatal_rate', 'population_density', 'median_age',
		                   'aged_65_older', 'gdp_per_capita', 'extreme_poverty', 'cardiovasc_death_rate', 'diabetes_prevalence',
		                   'life_expectancy', 'human_development_index'],
		                   hoverongaps = False, colorscale='ice_r'))
		fig.update_layout(title_text='Correlation matrix',
		title={'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font' : {"size":22, 'color': "#1E6777", 'family': "Arial"}},
			paper_bgcolor="#edf7ef", height=500, width=800, margin=dict(l=20, r=20, b=20, t=80))
		st.plotly_chart(fig)
						
	with col3:
		st.write(" ")

st.write(" ")
st.markdown('***')
st.markdown( "<span style='color: rgba(40,52,66,0.5); font-size:0.8em'>by: larryprato@gmail.com</span>", unsafe_allow_html= True)
