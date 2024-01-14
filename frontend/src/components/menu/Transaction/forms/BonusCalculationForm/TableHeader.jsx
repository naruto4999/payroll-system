import React, { useMemo } from 'react';

const TableHeader = ({ bonusStartMonth, year }) => {
	const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

	// Calculate the "To:" month
	const toMonth = (bonusStartMonth + 11) % 12;
	const toMonthName = months[toMonth === 0 ? 11 : toMonth - 1];

	// Generate header columns dynamically for the next 12 months
	const headerColumns = [];
	for (let i = 0; i < 12; i++) {
		const currentMonth = (bonusStartMonth + i) % 12;
		const currentMonthName = months[currentMonth === 0 ? 11 : currentMonth - 1];
		const currentYear = parseInt(year) + Math.floor((bonusStartMonth + i - 1) / 12); // Adjusting year for each iteration
		const header = `${currentMonthName}-${currentYear}`;
		headerColumns.push(
			<th key={i} className="px-1 py-2 font-medium">
				{header}
			</th>
		);
	}

	return (
		<thead className="sticky top-0 z-20 bg-blueAccent-600 dark:bg-blueAccent-700 dark:bg-opacity-40">
			<tr>
				<th className="w-8 px-1 py-2 font-medium">Cat. ID</th>
				<th className="px-1 py-2 font-medium">Category Name</th>
				{headerColumns}
			</tr>
		</thead>
	);
};

export default TableHeader;
