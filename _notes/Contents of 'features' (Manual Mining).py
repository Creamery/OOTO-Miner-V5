Contents of 'features' (ChiTest parameter)
features = 
[
	{
		'Code': 'b1',
		'Description': 'Gender',
		'Responses':
			[
				{
					'Code': '1',
					'Group': 'a',
					'Description': ' Male'
				},
				{
					'Code': '2',
					'Group': 'b',
					'Description': ' Female'
				}
			]
	},

	{
		'Code': 'b2',
		'Description': 'Age',
		'Responses':
			[
				{
					'Code': '9',
					'Group': 'a',
					'Description': ' 9-11'
				},

				{
					'Code': '10',
					'Group': 'a',
					'Description': ' 9-11'
				},

				{
					'Code': '11',
					'Group': 'a',
					'Description': ' 9-11'
				},

				{
					'Code': '12',
					'Group': 'b',
					'Description': ' 12-14'
				},

				{
					'Code': '13',
					'Group': 'b',
					'Description': ' 12-14'
				},

				{
					'Code': '14',
					'Group': 'b',
					'Description': ' 12-14'
				},

				{
					'Code': '15',
					'Group': 'c',
					'Description': ' 15-17'
				},

				{
					'Code': '16',
					'Group': 'c',
					'Description': ' 15-17'
				},

				{
					'Code': '17',
					'Group': 'c',
					'Description': ' 15-17'
				}
			]
	},

	{
		'Code': 'b3',
		'Description': 'Age Group',
		'Responses':
			[
				{
					'Code': '1',
					'Group': 'a',
					'Description': ' 9-11'
				},

				{
					'Code': '2',
					'Group': 'b',
					'Description': ' 12-14'
				},
				
				{
					'Code': '3',
					'Group': 'c',
					'Description': ' 15-17'
				}
			]
	},

	{<...>}
]

tests = [test, test, <...>]


test = 
	[
		{
			'Datasets':
				[
					{
						'Filter Features':
							[{
								'Selected Responses':
									[
										{'Code': '9', 'Group': 'a', 'Description': ' 9-11'}
									],
								'Code': 'b2',
								'Description': 'Age',
								'Responses':
									[
										{'Code': '9', 'Group': 'a', 'Description': ' 9-11'},
										{'Code': '10', 'Group': 'a', 'Description': ' 9-11'},
										{'Code': '11', 'Group': 'a', 'Description': ' 9-11'},
										{'Code': '12', 'Group': 'b', 'Description': ' 12-14'},
										{'Code': '13', 'Group': 'b', 'Description': ' 12-14'},
										{'Code': '14', 'Group': 'b', 'Description': ' 12-14'},
										{'Code': '15', 'Group': 'c', 'Description': ' 15-17'},
										{'Code': '16', 'Group': 'c', 'Description': ' 15-17'},
										{'Code': '17', 'Group': 'c', 'Description': ' 15-17'}
									]
							}],
						'Data':
							[
								{'s7': 'a', 'b4': 'a', 'b5': 'a', <...>},
								{'s7': '-1', 'b4': 'b', 'b5': 'b', <...>}, 
								{'s7': 'a', 'b4': 'a', 'b5': 'a', <...>},
								<...>
							],
						'Feature':
							{
								'Selected Responses':
									[
										{'Code': '9', 'Group': 'a', 'Description': ' 9-11'}
									],
								'Code': 'b2',
								'Description': 'Age',
								'Responses':
									[
										{'Code': '9', 'Group': 'a', 'Description': ' 9-11'},
										{'Code': '10', 'Group': 'a', 'Description': ' 9-11'},
										{'Code': '11', 'Group': 'a', 'Description': ' 9-11'},
										{'Code': '12', 'Group': 'b', 'Description': ' 12-14'},
										{'Code': '13', 'Group': 'b', 'Description': ' 12-14'},
										{'Code': '14', 'Group': 'b', 'Description': ' 12-14'},
										{'Code': '15', 'Group': 'c', 'Description': ' 15-17'},
										{'Code': '16', 'Group': 'c', 'Description': ' 15-17'},
										{'Code': '17', 'Group': 'c', 'Description': ' 15-17'}
									]
							}
					},

					{
						'Filter Features':
							[{
								'Selected Responses':
									[
										{'Code': '3', 'Group': 'b', 'Description': 'High income'}
									],
								'Code': 'b4',
								'Description': 'Socio-Economic Status',
								'Responses':
									[
										{'Code': '1', 'Group': 'a', 'Description': 'Low income'},
										{'Code': '2', 'Group': 'b', 'Description': 'Middle income'},
										{'Code': '3', 'Group': 'b', 'Description': 'High income'}
									]
							}],
						'Data':
							[
								{'s7': 'b', 'b4': 'b', 'b5': 'a', <...>},
								{'s7': 'b', 'b4': 'b', 'b5': 'a', <...>},
								{'s7': 'a', 'b4': 'b', 'b5': 'b', <...>}
							],
						'Feature':
							{
								'Selected Responses':
									[
										{'Code': '3', 'Group': 'b', 'Description': 'High income'}
									],
								'Code': 'b4',
								'Description': 'Socio-Economic Status',
								'Responses':
									[
										{'Code': '1', 'Group': 'a', 'Description': 'Low income'},
										{'Code': '2', 'Group': 'b', 'Description': 'Middle income'},
										{'Code': '3', 'Group': 'b', 'Description': 'High income'}
									]
							}
					}
				],
			'Type': 'Sample vs Sample'
		}
	]

test['Datasets'][0] = 
	{
		'Filter Features':
			[{
				'Selected Responses':
					[
						{'Code': '9', 'Group': 'a', 'Description': ' 9-11'}
					],
				'Code': 'b2',
				'Description': 'Age',
				'Responses':
					[
						{'Code': '9', 'Group': 'a', 'Description': ' 9-11'},
						{'Code': '10', 'Group': 'a', 'Description': ' 9-11'},
						{'Code': '11', 'Group': 'a', 'Description': ' 9-11'},
						{'Code': '12', 'Group': 'b', 'Description': ' 12-14'},
						{'Code': '13', 'Group': 'b', 'Description': ' 12-14'},
						{'Code': '14', 'Group': 'b', 'Description': ' 12-14'},
						{'Code': '15', 'Group': 'c', 'Description': ' 15-17'},
						{'Code': '16', 'Group': 'c', 'Description': ' 15-17'},
						{'Code': '17', 'Group': 'c', 'Description': ' 15-17'}
					]
			}],
		
		'Data':
			[{
					's7': 'a',
					'b4': 'a',
					<...>
			}],

		'Feature':
			{
				'Selected Responses':
					[{
						'Code': '9',
						'Group': 'a',
						'Description': ' 9-11'
					}],
				'Code': 'b2',
				'Description': 'Age',
				'Responses':
					[
						{'Code': '9', 'Group': 'a', 'Description': ' 9-11'},
						{'Code': '10', 'Group': 'a', 'Description': ' 9-11'},
						{'Code': '11', 'Group': 'a', 'Description': ' 9-11'},
						{'Code': '12', 'Group': 'b', 'Description': ' 12-14'},
						{'Code': '13', 'Group': 'b', 'Description': ' 12-14'},
						{'Code': '14', 'Group': 'b', 'Description': ' 12-14'},
						{'Code': '15', 'Group': 'c', 'Description': ' 15-17'},
						{'Code': '16', 'Group': 'c', 'Description': ' 15-17'},
						{'Code': '17', 'Group': 'c', 'Description': ' 15-17'}
					]
			}
	}




