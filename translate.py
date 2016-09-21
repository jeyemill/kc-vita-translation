import os
import json
import xmltodict

# default dirs
xml_dir = os.path.join("Xml", "tables", "master")
en_xml_dir = os.path.join("en", xml_dir)
kc3_trans_dir = os.path.join("kc3-translations", "data", "en")

# maybe kc3 translation should be a submodule, choose language as a argument

def ships(): # translate all ship names
	# open xml
	shipxml = xmltodict.parse(open(os.path.join(en_xml_dir, 'mst_ship.xml'), 'rb'))

	# get KC3 JSON, kanji name as key and translation as value
	shiplist = json.load(open(os.path.join(kc3_trans_dir, 'ships.json'), 'r'))

	# replace all names with corresponding unicode string
	for item in shipxml['mst_ship_data']['mst_ship']:
		if item['Name'] == 'なし': # None
			item['Name'] = 'None'
			print(item['Id'], item['Name'])
			continue

		# 650 運河棲姫 = Canal Princess
		if item['Name'] == "運河棲姫":
			item['Name'] = 'Canal Princess'
			print(item['Id'], item['Name'])
			continue
		
		try:
			# render Kai and Ni to romaji with space separation
			# also render 甲 (corresponds to https://en.wikipedia.org/wiki/Celestial_stem ) as A, B, C, D...
			item['Name'] = item['Name'].replace('改', ' Kai').replace('二', ' Ni')
			
			# since event specifics only start from ID 901, only start checking if it is greater than this
			if int(item['Id']) >= 901:
				events = {"年末": "Year-end", "正月": "New_Year", "梅雨": "Rainy_Season", "夏": "Summer", "秋": "Autumn", "Valentine": "Valentine", "Xmas": "Xmas"} # underscore as scaffolding
				for event in events.keys():
					if item['Name'].find(event) != -1:
						processed = item['Name'].replace(event, event + " ")
						fullname = processed.split()
						fullname[0] = events[event].replace("_", " ")
						translation = shiplist[fullname[1]]
						fullname[1] = translation
						item["Name"] = " ".join(fullname)
						break # name found, no more searching needed
			else:
				# split full name into components
				fullname = item['Name'].split()
				
				# take kanji name (without trailing words) and match to translation
				translation = shiplist[fullname[0]]
				if len(fullname) == 1: # just write base name
					item['Name'] = translation
				else: # add trailing kai and ni with spaces
					fullname[0] = translation
					item['Name'] = " ".join(fullname)
			
		except KeyError: # if name doesn't exist, don't edit
			pass
		
		print(item['Id'], item['Name'])

	# save changes to file
	print("Saving changes shown above to :", en_xml_dir + 'mst_ship.xml')
	with open(os.path.join(en_xml_dir, 'mst_ship.xml'), 'w') as f:
		f.write(xmltodict.unparse(shipxml, pretty=True))

def slot_items():
	# open xml
	itemxml = xmltodict.parse(open(os.path.join(en_xml_dir, 'mst_slotitem.xml'), 'rb'))

	# get KC3 JSON, kanji name as key and translation as value
	itemlist = json.load(open(os.path.join(kc3_trans_dir, 'items.json'), 'r'))

	# replace all names with corresponding unicode string
	for item in itemxml['mst_slotitem_data']['mst_slotitem']:
		# take kanji name (without trailing words) and match to translation
		item['Name'] = itemlist[item['Name']]
		print(item['Id'], item['Name'])
	
	# save changes to file
	print("Saving changes shown above to :", en_xml_dir + 'mst_slotitem.xml')
	with open(os.path.join(en_xml_dir, 'mst_slotitem.xml'), 'w') as f:
		f.write(xmltodict.unparse(itemxml, pretty=True))

# needs to parse from wiki: 
#def quests():
	## open xml
	#xml_fname = 'mst_quest.xml'
	#xml = xmltodict.parse(open(os.path.join(en_xml_dir, xml_fname), 'rb'))

	## get KC3 JSON, id as key and translation as value
	#list_fname = 'quests.json'
	#datalist = json.load(open(os.path.join(kc3_trans_dir, list_fname), 'r'))

	## replace all names with corresponding unicode string
	#for item in xml['mst_quest_data']['mst_quest']:
		## take kanji name (without trailing words) and match to translation
		#item['Name'] = datalist[item['Id']]['Name']
		#item['Details'] = datalist[item['Id']]['Name']
		#print(item['Id'], item['Name'], item['Details'])
	
	## save changes to file
	#print("Saving changes shown above to :", en_xml_dir + xml_fname)
	##with open(os.path.join(en_xml_dir, xml_fname), 'w') as f:
	##	f.write(xmltodict.unparse(xml, pretty=True))
	#print(xmltodict.unparse(xml, pretty=True))

def stype():
	# open xml
	xml_fname = 'mst_stype.xml'
	xml = xmltodict.parse(open(os.path.join(en_xml_dir, xml_fname), 'rb'))

	# get KC3 JSON, id as key and translation as value
	list_fname = 'stype.json'
	datalist = json.load(open(os.path.join(kc3_trans_dir, list_fname), 'r'))

	# replace all names with corresponding unicode string
	for item in xml['mst_stype_data']['mst_stype']:
		# take kanji name (without trailing words) and match to translation
		item['Name'] = datalist[int(item['Id'])]
		print(item['Id'], item['Name'])
	
	# save changes to file
	print("Saving changes shown above to :", os.path.join(en_xml_dir, xml_fname))
	with open(os.path.join(en_xml_dir, xml_fname), 'w') as f:
		f.write(xmltodict.unparse(xml, pretty=True))

def quotes():
	# open xml
	xml_fname = 'mst_shiptext.xml'
	xml = xmltodict.parse(open(os.path.join(en_xml_dir, xml_fname), 'rb'))

	# get KC3 JSON, id as key and translation as value
	list_fname = 'quotes.json'
	datalist = json.load(open(os.path.join(kc3_trans_dir, list_fname), 'r'))
	
	# get original ship name to help
	shipxml_fname = 'mst_ship.xml'
	shipxml = xmltodict.parse(open(os.path.join(en_xml_dir, shipxml_fname), 'rb'))

	# compile a shiphash table by processing shiplist XML
	shiplist = {}
	for item in shipxml['mst_ship_data']['mst_ship']:
		shiplist[item['Id']] = item['Name']

	# replace all names with corresponding unicode string
	for item in xml['mst_shiptext_data']['mst_shiptext']:
		# take kanji name (without trailing words) and match to translation
		item['OrigGetMes'] = item['Getmes']
		item['OrigSinfo'] = item['Sinfo'] # temporarily add original sinfo and getmessage to be sure
		
		try:
			item['Ship'] = shiplist[item['Id']]
		except KeyError:
			item['Ship'] = 'Unknown'
		
		try:
			item['Getmes'] = datalist[item['Id']]['1']
			item['Sinfo'] = datalist[item['Id']]['25']
			print(item['Id'], item['Ship'], '\n', item['Getmes'], '\n', item['Sinfo'], '\n')
		except KeyError: # ignore ship IDs with empty slots
			pass
	
	# save changes to file
	print("Saving changes shown above to :", os.path.join(en_xml_dir, xml_fname))
#	with open(os.path.join(en_xml_dir, xml_fname), 'w') as f:
#		f.write(xmltodict.unparse(xml, pretty=True))

#ships()
#slot_items()
#quests()
#stype()
quotes()
print("Changes compiled. To start over, replace the `Xml/` folder in `en/` with the one from `jp/`.")
