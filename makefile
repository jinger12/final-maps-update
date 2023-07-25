.PHONY: data, clean

#this will pull all the census and FCC data
data/df_ffc_tab.csv: 
	mkdir -p data
	python -B src/data_tab.py

#this will make the data for looking at the county level
county_data: 
	python -B src/data_county.py


#maps

countymap: 
	python -B src/map_county_ddi.py

housing_pop: 
	python -B src/map_housing_pop.py

unused: 
	python -B src/map_unused_land_maine.py

infa_se: 
	python -B src/map_infa_se.py

pop: 
	python -B src/map_pop.py

infa: 
	python -B src/map_infa.py	


ddi_tab: data/df_ffc_tab.csv
	python -B src/map_ddi_tab.py

infapop:
	python -B src/infa_and_pop_comp.py

NIA_NBBND:
	python -B src/map_NIA_NBBND.py

computer:
	python -B src/map_computer.py

age:
	python -B src/map_age.py

disability:
	python -B src/map_disability.py

poverty:
	python -B src/map_poverty.py

fcc:
	python -B src/map_fcc.py

#other?

infa_pop: 
	python -B src/map_infa_pop.py	

ddi_county:
	python -B src/map_county_ddi.py
	corrmatrix
# Download the data
# mkdir -p fails quietly if directory already exists
# curl -L follows indirects
# curl -O preserves filename of the source

