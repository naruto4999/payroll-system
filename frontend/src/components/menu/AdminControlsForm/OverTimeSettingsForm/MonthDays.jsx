import React from 'react';

const MonthDays = ({ element }) => {
	return (
		<div className="relative h-20 rounded-sm border dark:border-slate-400 dark:border-opacity-30">
			{element.day}
		</div>
	);
};

export default MonthDays;
