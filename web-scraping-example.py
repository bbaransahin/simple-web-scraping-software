import mechanicalsoup
import pandas as pd
import pickle

# a basic web-scraping software

def save_data_frame(data_frame):
	#I'm savin data_frame to file named "data" in here
	try:
		save_file = open("data","wb")
	except:
		save_file = open("data","w+")
		save_file.close()
		save_file = open("data","wb")
	finally:
		pickle.dump(data_frame,save_file)
		save_file.close()
	print("data saved to 'data' file")

def get_data_from_website():
	#This part of code is moving to the where is data by mechanicalsoup and get data with using BeautifulSoup
	br = mechanicalsoup.StatefulBrowser()
	print(br.open("https://irpm.org.uk/public/page/members-search"))
	br.select_form('form[name="searchMembers"]')
	br.submit_selected()
	data = br.get_current_page().find_all("td")
	print("got data")
	return data

def organize_data(data):
	#In here I'm organizing the data for creating a frame work
	name_list = []
	company_list = []
	designation_list = []
	qual_list = []
	region_list = []
	a = 0
	while a < len(data):
		name_list.append(data[a].get_text())
		a+=1
		company_list.append(data[a].get_text())
		a+=1
		designation_list.append(data[a].get_text())
		a+=2
		try:
			b=data[a].get_text().index("Qual.: ")
			qual_list.append(data[a].get_text()[b+len("Qual.: "):data[a].get_text().index("Region:")-1])
		except:
			qual_list.append("")
		b = data[a].get_text().index("Region: ")
		region_list.append(data[a].get_text()[b+len("Region: "):len(data[a].get_text())-10])
		a+=1
	data_dict = {"name" : name_list,
		"company" : company_list,
		"designation" : designation_list,
		"qual" : qual_list,
		"region" : region_list}
	print("data is organized")
	return data_dict

def create_data_frame(data_dict):
	#I'm creating frame work in here
	data_frame = pd.DataFrame(data_dict)
	print("created pandas data")
	return data_frame

def main():
	#this is the main loop program starts running here
	data = get_data_from_website()
	data_dict = organize_data(data)
	data_frame = create_data_frame(data_dict)
	save_data_frame(data_frame)
	print("program ended")

main()
