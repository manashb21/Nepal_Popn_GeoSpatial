import pandas as pd 
import geopandas as gpd 

# data = pd.read_html("https://www.citypopulation.de/php/nepal-mun-admin.php")

# for popn_data in data:
#     print(popn_data)

# #print(type(popn_data))
# popn_data.to_excel(r"G:\Python Projects 2021\Nepal_PopDenMap\popn.xlsx")

popn_data = pd.read_excel(r'G:\Python Projects 2021\Nepal_PopDenMap\popn.xlsx')

popn_data = popn_data[['Name', 'Status', 'PopulationCensus2011-06-22']]

popn_data.rename(columns = {'PopulationCensus2011-06-22':'Population'}, inplace = True)

#filter rows by value
popn_data = popn_data.loc[popn_data['Status']=='District']

#create an empty column
popn_data['Districts2'] = ''

for index, row in popn_data.iterrows():
    if '[' and ']' in row['Name']:
        start_index = row['Name'].find('[')
        end_index = row['Name'].find(']')
        popn_data.loc[index, 'Districts2'] = popn_data.loc[index]['Name'][start_index+1:end_index]
    else:
        popn_data.loc[index, 'Districts2'] = popn_data.loc[index]['Name']
        
popn_data = popn_data