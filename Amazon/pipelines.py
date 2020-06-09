from scrapy import signals
from scrapy.exporters import CsvItemExporter
import os
import pandas as pd
import csv

class AmazonPipeline(object):
	def __init__(self):
		self.delete_csv()
		self.make_csv()
	
	def make_csv(self):
		self.df = pd.DataFrame()

	def delete_csv(self):
		if os.path.exists('items.csv'):
			os.remove('items.csv')

	def output_csv(self,item):
		self.df['Titles'] = pd.Series(list(item.values())[0])
		self.df['Prices'] = pd.Series(list(item.values())[1])
		self.df['Reviews'] = pd.Series(list(item.values())[2])
		with open('items.csv','a') as f:
			self.df.to_csv('items.csv',index=False, mode='a',header=f.tell()==0)

	def process_item(self, item, spider):
		self.output_csv(item)
		return item