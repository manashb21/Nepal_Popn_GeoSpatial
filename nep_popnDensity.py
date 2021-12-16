import pandas as pd 
import geopandas as gpd 
import matplotlib.pyplot as plt

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
        
popn_data = popn_data[['Districts2','Population']]

#renaming the column
popn_data.rename(columns = {'Districts2': 'District'}, inplace = True)

#reading data from the shapefile 
nep_districts = gpd.read_file(r'NPL_adm\NPL_adm3.shp')

nep_districts = nep_districts[['NAME_3','geometry']]

nep_districts.rename(columns ={'NAME_3':'District'}, inplace = True)

#reprojecting to projected coordinate system
nep_districts.to_crs(epsg = 32645, inplace = True)


popn_data.replace('Sindhupalchowk','Sindhupalchok', inplace =True)
popn_data.replace('Chitwan','Chitawan', inplace =True)
popn_data.replace('Tehrathum','Terhathum', inplace =True)
popn_data.replace('Dang Deukhuri','Dang', inplace =True)
popn_data.replace('Tanahun','Tanahu', inplace =True)
popn_data.replace('Kapilvastu','Kapilbastu', inplace =True)

for index, row in nep_districts['District'].iteritems():
    if row in popn_data['District'].tolist():
        pass
    else:
        print('The value ', row, ' is NOT in popn_data list.')
        

nep_districts['Area'] = nep_districts.area/1000000

#Do an attributes join
nep_districts = nep_districts.merge(popn_data, on = 'District')

        
#calculation of population density
nep_districts['PopnDensity (people/sqkm)'] = nep_districts['Population']/nep_districts['Area']

#plotting the density data 
nep_districts.plot(cmap = 'jet', column = 'PopnDensity (people/sqkm)', legend = True, figsize = (10,10))
plt.savefig('Nepal_popnDensity.jpg')
        
        
        
        
        
        
        
        
        
        
        
        