import React from 'react';

const DateSelector = ({ date, setDate, id, name }) => {
	return (
		<input
			type="date"
			id={id}
			name={name}
			value={date.toISOString().split('T')[0]}
			className="inline w-32 rounded border-2 border-gray-800 border-opacity-25 bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-700 dark:focus:border-opacity-75"
			onChange={(event) => {
				const newDate = new Date(event.target.value);
				if (!isNaN(newDate)) {
					setDate(newDate);
				}
			}}
		/>
	);
};

export default DateSelector;
