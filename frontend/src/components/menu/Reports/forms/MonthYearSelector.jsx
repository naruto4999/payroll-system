import React, { useMemo } from 'react';

const MonthYearSelector = React.memo(({ setSelectedDate, selectedDate, earliestMonthAndYear }) => {
	const months = [
		'January',
		'February',
		'March',
		'April',
		'May',
		'June',
		'July',
		'August',
		'September',
		'October',
		'November',
		'December',
	];

	const optionsForYear = useMemo(() => {
		if (earliestMonthAndYear) {
			const options = [];
			for (let i = earliestMonthAndYear.earliestYear; i <= new Date().getFullYear(); i++) {
				options.push(
					<option key={i} value={i}>
						{i}
					</option>
				);
			}
			return options;
		}
	}, [earliestMonthAndYear]);
	return (
		<div>
			<label
				htmlFor="year"
				className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
			>
				Month and Year :
			</label>

			<select
				name="month"
				id="month"
				value={selectedDate.month}
				onChange={(e) => {
					setSelectedDate((prevValue) => ({ ...prevValue, month: e.target.value }));
				}}
				className="my-1 mr-2 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
			>
				{months.map((month, index) => {
					return (
						<option key={index} value={index + 1}>
							{month}
						</option>
					);
				})}
			</select>
			<select
				name="year"
				id="year"
				onChange={(e) => {
					setSelectedDate((prevValue) => ({ ...prevValue, year: e.target.value }));
				}}
				value={selectedDate.year}
				className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
			>
				{optionsForYear}
			</select>
		</div>
	);
});

export default MonthYearSelector;
