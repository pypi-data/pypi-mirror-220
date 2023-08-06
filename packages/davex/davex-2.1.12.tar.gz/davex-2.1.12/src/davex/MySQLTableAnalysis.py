"""
  Dave Skura

	Connect to MySQL
	Connect to local sqlite_db
	read table details
	calc metrics 
	load metrics to table in sqlite cache tables

"""
from sqlitedave_package.sqlitedave import sqlite_db 
from mysqldave_package.mysqldave import mysql_db 
from schemawizard_package.schemawizard import schemawiz

import logging
import sys

class runner():

	def __init__(self,cache_prefix='',selected_schema='%',selected_table=''):

		self.cache_schemas_tablename = cache_prefix.lower() + "_schemas"
		self.cache_tblcounts_tablename = cache_prefix.lower() + "_table_counts"

		self.metrics_table_name = cache_prefix.lower() + 'table_metrics'
		self.metrics_tablehdr_name = cache_prefix.lower() + 'table_comments'
		self.sqlite = sqlite_db()
		
		self.db = mysql_db(cache_prefix.lower().replace('_','')) 

		self.connect()
		self.build_metrics_table(self.sqlite)
		if selected_schema != '':
			self.sqlite.execute('DELETE FROM ' + self.metrics_table_name + " WHERE schema_name='" + selected_schema + "' and table_name = '" + selected_table + "'")
		else:
			self.sqlite.execute('DELETE FROM ' + self.metrics_table_name)

		comment_sql = """
			SELECT table_comment 
			FROM information_Schema.tables 
			WHERE upper(table_schema)=upper('world') and upper(table_name)=upper('city')
		"""
		comment_sql = comment_sql.replace('world',selected_schema)
		comment_sql = comment_sql.replace('city',selected_table)

		table_comment = self.db.queryone(comment_sql)
		
		self.table_comment_insert(self.sqlite,selected_schema,selected_table,table_comment)

		col_list_sql = """
			SELECT column_name,a.column_comment
			FROM INFORMATION_SCHEMA.COLUMNS a
			WHERE upper(table_schema)=upper('world') and upper(table_name)=upper('city')
			ORDER BY ordinal_position
		"""
		col_list_sql = col_list_sql.replace('world',selected_schema)
		col_list_sql = col_list_sql.replace('city',selected_table)

		data = self.db.query(col_list_sql)
		for row in data:
			col_name = row[0]
			col_comment = str(row[1].decode('ASCII'))
			if col_comment.find("'") > -1:
				col_comment = col_comment.replace("'",'`')

			#-- schema_name, table_name,field_name
			# ,sample_data,distinct_values,indexes,ddl_comments 

			sql = """

				SELECT
				'world' as schemaname,
				'city' as tablename,
				'CountryCode' as field_name,
				sample_data,
				distinct_values,
				indexes
				FROM 
				(SELECT count(DISTINCT CountryCode) as distinct_values FROM world.city) distinct_counter
				LEFT JOIN (
						SELECT concat('[ ',CountryCode
								,' ][ ', coalesce(LEAD(CountryCode,1) OVER (ORDER BY CountryCode),'') 
								,' ][ ', coalesce(LEAD(CountryCode,2) OVER (ORDER BY CountryCode),'') 
								,' ]') as sample_data 
						FROM 
								(SELECT DISTINCT CountryCode FROM world.city) dist_qry
						ORDER BY CountryCode
						limit 1
						) sampling ON (1=1)
				LEFT JOIN (				
				SELECT
					concat(coalesce(INDEX_NAME,'')
					,'; ',coalesce(LEAD(INDEX_NAME,1) OVER (ORDER BY INDEX_NAME))
					,'; ',coalesce(LEAD(INDEX_NAME,2) OVER (ORDER BY INDEX_NAME))
					,'; ',coalesce(LEAD(INDEX_NAME,3) OVER (ORDER BY INDEX_NAME))
					,'; ',coalesce(LEAD(INDEX_NAME,4) OVER (ORDER BY INDEX_NAME))
					) as indexes
					FROM INFORMATION_SCHEMA.STATISTICS
					WHERE TABLE_SCHEMA= 'world' 
									and TABLE_NAME = 'city'
									and COLUMN_NAME = 'CountryCode'
					) indexqry ON (1=1)        
			"""

			sql = sql.replace('world',selected_schema)
			sql = sql.replace('city',selected_table)
			sql = sql.replace('CountryCode',col_name)
			#print(sql)
			#sys.exit(0)
			metric_data = self.db.query(sql)			
			for onerow in metric_data:
				"""
				print('schema_name		= ', selected_schema)
				print('table_name			= ', selected_table)
				print('field_name			= ', col_name)
				"""
				sample_data		= onerow[3]
				distinct_values= onerow[4]
				indexes				= onerow[5]
				ddl_comments 	= col_comment
				
				self.metric_insert(self.sqlite,selected_schema,selected_table,col_name,sample_data,distinct_values,indexes,ddl_comments )
			
		print('Analaysis completed. ' + self.metrics_table_name + ' updated with stats from ' + selected_schema + '.' + selected_table)

		self.disconnect()

	def build_metrics_table(self,sqlite):
		if not sqlite.does_table_exist(self.metrics_tablehdr_name):
			logging.info('table ' + self.metrics_tablehdr_name + ' does not exist.  Creating it.')
			csql = "CREATE TABLE " + self.metrics_tablehdr_name + """ (
				schema_name text,
				table_name text,
				row_counts int,
				table_comments text
				)
			"""
			sqlite.execute(csql)

		if not sqlite.does_table_exist(self.metrics_table_name):
			logging.info('table ' + self.metrics_table_name + ' does not exist.  Creating it.')
			csql = "CREATE TABLE " + self.metrics_table_name + """ (
				schema_name text,
				table_name text,
				field_name text,
				sample_data text,
				distinct_values int,
				indexes text,
				field_comments text
				)
			"""
			sqlite.execute(csql)

	def table_comment_insert(self,sqlite,schema_name,table_name,table_comments):
		dsql = 'DELETE FROM ' + self.metrics_tablehdr_name 
		dsql += " WHERE schema_name ='" + schema_name + "' and table_name='" + table_name + "';"
		sqlite.execute(dsql)

		qry = """
			SELECT coalesce(counts,0)
			FROM """ + self.cache_tblcounts_tablename + """
			WHERE table_schema='world' and table_name='city'
		"""
		row_counts = 0
		qry = qry.replace('world',schema_name)
		qry = qry.replace('city',table_name)
		try:
			row_counts = sqlite.queryone(qry)
			if not row_counts:
				row_counts = 0
		except:
			qry = """
				SELECT count(*)
				FROM world.city
			"""
			qry = qry.replace('world',schema_name)
			qry = qry.replace('city',table_name)
			row_counts = self.db.queryone(qry)
			if not row_counts:
				row_counts = 0


		isql = 'INSERT INTO ' + self.metrics_tablehdr_name + ' (schema_name,table_name,row_counts,table_comments) VALUES ('
		isql += "'" + schema_name + "',"
		isql += "'" + table_name + "',"
		isql += "" + str(row_counts) + ","
		isql += "'" + table_comments + "');"
		sqlite.execute(isql)

	def metric_insert(self,sqlite,schema_name,table_name,field_name,sample_data,distinct_values,indexes,field_comments ):

		sample_data_cln = sample_data
		if str(sample_data).find("'") > -1:
			sample_data_cln = sample_data.replace("'",'`')

		dsql = 'DELETE FROM ' + self.metrics_table_name 
		dsql += " WHERE schema_name ='" + schema_name + "' and table_name='" + table_name + "' and field_name='" + field_name + "';"
		sqlite.execute(dsql)

		isql = 'INSERT INTO ' + self.metrics_table_name + ' (schema_name,table_name,field_name,sample_data,distinct_values,indexes,field_comments) VALUES ('
		isql += "'" + schema_name + "',"
		isql += "'" + table_name + "',"
		isql += "'" + field_name + "',"
		isql += "'" + str(sample_data_cln) + "',"
		isql += "" + str(distinct_values) + ","
		isql += "'" + str(indexes) + "',"
		isql += "'" + str(field_comments) + "' "
		isql += ');'
		sqlite.execute(isql)

	def connect(self):
		self.db.connect()
		logging.info('Connected to ' + self.db.db_conn_dets.dbconnectionstr())
		self.sqlite.connect()
		logging.info('Connected to ' + self.sqlite.db_conn_dets.dbconnectionstr())

	def disconnect(self):
		self.sqlite.close()
		self.db.close()

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	logging.info(" Starting Table Analysis") # 
	runner('Demo_','world','city')
