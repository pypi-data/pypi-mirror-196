"""
  Dave Skura,2023
"""
import sys
from schemawizard_package.schemawizard import schemawiz

def main():
	if len(sys.argv) == 1 or sys.argv[1] == 'mysql_import.py': # no parameters
		print('usage: ')
		print('mysql_import.py [csv_filename] [tablename] [WithTruncate]') 
		print('')
		print('bool WithTruncate = [True,False]')

	elif (len(sys.argv) == 2) : 
		csv_filename = sys.argv[1]
		myexp = dbimport(csv_filename)

	elif (len(sys.argv) == 3) : 
		csv_filename = sys.argv[1]
		tablename = sys.argv[2]

		myexp = dbimport(csv_filename,tablename)

	elif (len(sys.argv) == 4) : 
		csv_filename = sys.argv[1]
		tablename = sys.argv[2]
		WithTruncate = bool(sys.argv[2])

		myexp = dbimport(csv_filename,tablename,WithTruncate)

	else:
		print('Error: Incorrect number of parameters.')
		print('')
		print('usage: ')
		print('mysql_import.py [csv_filename] [tablename] [WithTruncate]') 
		print('')
		print('bool WithTruncate = [True,False]')

class dbimport():
	def __init__(self,csv_filename,tablename='',WithTruncate=False):
		tbl = tablename
		dber = schemawiz()
		if ((tablename != '') and (dber.dbthings.mysql_db.does_table_exist(tablename))):
			dber.justload_mysql_from_csv(csv_filename,tablename,WithTruncate)
		else:
			tbl = dber.createload_mysql_from_csv(csv_filename,tablename)

		print(dber.dbthings.mysql_db.queryone('SELECT COUNT(*) FROM ' + tbl))
		dber.dbthings.mysql_db.close()

		print('mysql_import Done')


if __name__ == '__main__':
	main()

		