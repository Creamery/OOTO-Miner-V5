            self.findFeature(
                self.entryQuerySetDataA.get(),
                self.listQuerySetDataA,
                self.datasetA,
                self.populationDatasetOriginalA,
                True,
                "Dataset_Feature")




dataset['Feature'] = 
	{
	'Code': 'b1',
	'Description': 'Gender',
	'Responses':
		[
			{'Code': '1', 'Group': 'a', 'Description': ' Male'},
			{'Code': '2', 'Group': 'b', 'Description': ' Female'}
		]
	}


populationDatasetOriginal['Feature'] = dataset['Feature']






getPopulationDataset[KS.FEATURE_LIST] = 
	getPopulationDataset['b1'] = 
		{
			'Description': 'Gender',
			'Responses': OrderedDict(
										[
											('a', OrderedDict	([
																	('Code', ['1']),
																	('Description', [' Male'])
																])
											),

											('b', OrderedDict	([
																	('Code', ['2']),
																	('Description', [' Female'])
																])
											)
										]
									)
		}


	getPopulationDataset['b4'] = 
		{
			'Description': 'Socio-Economic Status',
			'Responses': OrderedDict(
										[
											('a', OrderedDict	([
																	('Code', ['1']),
																	('Description', ['Low income'])
																])
											),

											('b', OrderedDict	([
																	('Code', ['2', '3']),
																	('Description', ['Middle income', 'High income'])
																])
											)
										]
									)
		}

# array of ordered dictionaries
getPopulationDataset[KS.SAMPLES] = 
	[
		OrderedDict	([
						('a1', '3'), ('a2', '3'), ('a3', '2'), ('a4', '5'), ('a5', '2'), ('a6', '4'), ('a7', '2'), ('a8', '3'),
						('b1', '2'), ('b2', '11'), ('b3', '1'), ('b4', '2'), ('b5', '0'),
						('d1', '1'), ('d2', '2'), ('d3', '1'), ('d4', '1'), ('d5', '1'),
						('n1', '2'), ('n2', '1'), ('n3', '1'), ('n4', '4'), ('n5', '3'), ('n6', '1'),
						('p1', '2'), ('p10', '1'), ('p11', '0'), ('p12', '3'), ('p2', '1'), ('p3', '1'), ('p4', '2'), ('p5', '4'), ('p6', '2'), ('p7', '1'), ('p8', '1'), ('p9', '1'),
						('r1', '4'), ('r2', '1'), ('r3', '1'), ('r4', '1'),
						('s1', '4'), ('s2', '3'), ('s3', '3'), ('s4', '1'), ('s5', '2'), ('s6', '2'), ('s7', '2'), ('s8', '2'),
						('u1', '8'), ('u2', '99'), ('u3', '99'), ('u4', '3'),
						('v1', '1'), ('v2', '2'), ('v3', '1'), ('v4', '2')
					]),

		OrderedDict	([
						('a1', '2'), ('a2', '2'), ('a3', '3'), ('a4', '4'), ('a5', '2'), ('a6', '1'), ('a7', '1'), ('a8', '2'),
						('b1', '2'), ('b2', '16'), ('b3', '3'), ('b4', '1'), ('b5', '0'),
						('d1', '0'), ('d2', '2'), ('d3', '1'), ('d4', '1'), ('d5', '1'),
						('n1', '99'), ('n2', '99'), ('n3', '99'), ('n4', '1'), ('n5', '1'), ('n6', '1'),
						('p1', '3'), ('p10', '1'), ('p11', '0'), ('p12', '2'), ('p2', '1'), ('p3', '1'), ('p4', '1'), ('p5', '3'), ('p6', '1'), ('p7', '1'), ('p8', '1'), ('p9', '1'),
						('r1', '2'), ('r2', '1'), ('r3', '1'), ('r4', '0'),
						('s1', '2'), ('s2', '2'), ('s3', '1'), ('s4', '3'), ('s5', '2'), ('s6', '2'), ('s7', '2'), ('s8', '2'),
						('u1', '2'), ('u2', '1'), ('u3', '1'), ('u4', '2'),
						('v1', '1'), ('v2', '1'), ('v3', '2'), ('v4', '1')
					]),

		OrderedDict ([ <...> ])

	]



getPopulationDataset[KS.FILTER_LIST] = 
	[
		{
			'a1': ['1', '2'],
			'b1': ['1']
		}

	]