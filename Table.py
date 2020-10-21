
__author__ = ["Candy Espulgar"]
__copyright__ = "Copyright 2019 - TE3D House, Copyright 2020 - Liverpool Hope University"
__credits__ = ["Arnulfo Azcarraga, Neil Buckley"]
__version__ = "3.0"

'''
	A script used by the original Manual Mining system.
	[Candy]
'''

class Table(object):

	def __init__(self, groups, keys, head):
		self.rows = []

		header = [head]
		header = header + keys
		self.rows.append(header)


		for i  in range(0,len(groups)):
			row = [i]

			for k in keys:
				if k not in groups[i]:
					row.append(str(0))
				else:
					row.append(str(len(groups[i][k])))
			self.rows.append(row)


	def getPrintable(self, rowList):
		for row in self.rows:
			rowLine = []
			for e in row:
				rowLine.append(e)
				# print ('rowLine e ' + str(e))
			rowList.append(rowLine)
		rowList.append("***********")