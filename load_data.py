import io
import sys

import get_dynasties
import get_chars
import get_provs
import get_titles
import get_religion
import get_culture
import get_traits
import get_bloodline

import sqlite3
import re
import zipfile
import tempfile
import os

def load_data(filename):
	# connect and get a cursor
	conn = sqlite3.connect('ck2-db.db')
	cur = conn.cursor()

	# create the tables
	with open("ck2_make_table.sql") as f:
		cur.executescript(f.read())

	#read in religion and culture
	print('Preloading religion...')
	get_religion.get_religion(cur)
	print('Preloading culture...')
	get_culture.get_culture(cur)
	print('Preloading traits...')
	get_traits.get_traits(cur)

	temp_dir = None
	with io.open(filename, "rb") as f:
		label = f.read(2) # Get byte object
		if label == b"PK": # I don't know if the beginning is just PK or PK3
			print("This file is a zip-compressed file, unpacking...")
			with zipfile.ZipFile(filename, 'r') as zip_ref:
				temp_dir = tempfile.TemporaryDirectory(prefix="ck2db-unpacked-")
				zip_ref.extractall(temp_dir.name)
			filename=os.path.join(temp_dir.name, os.path.basename(filename))
		elif label == b"CK": # If PK3, then we should check CK2
			print("Reading CK2 file...")
		else: # Ironman mode files???
			print("Unknown file type, exiting...")
			quit()

	# parse the file and fill the tables with data
	with io.open(filename, encoding="cp1252") as f:
		print('Getting metadata...')
		get_metadata(f, cur)
		print('Getting dynasties...')
		get_dynasties.get_dynasties(f, cur)
		print('Getting characters...')
		get_chars.get_chars(f, cur)
		print('Getting religions...')
		get_religion.get_heresies(f, cur)
		print('Getting provinces...')
		get_provs.get_provs(f, cur)
		# Handle case for no dlc?
		print("Getting bloodlines...")
		get_bloodline.get_bloodlines(f, cur) # order matters because we don't rewind the file in each separate parser
		print("Getting titles...")
		get_titles.get_titles(f, cur)

	# commit changes made and disconnect from database
	conn.commit()
	cur.close()
	conn.close()

	print("All done!")


def get_metadata(file, cur):
	while True:
		date_re = re.match("^date=\"(.+)\"", file.readline().strip())
		if(date_re != None):
			break

	while True:
		id_re = re.match("^id=(.+)", file.readline().strip())
		if(id_re != None):
			break

	id = int(id_re[1])
	date = get_chars.make_date(date_re[1])
	cur.execute("INSERT INTO Metadata VALUES(?, ?)", [id, date])


if __name__=='__main__':
	file_name = "Leon1067_02_12.ck2"
	if len(sys.argv) > 1:
		file_name = sys.argv[1]
	load_data(file_name)
