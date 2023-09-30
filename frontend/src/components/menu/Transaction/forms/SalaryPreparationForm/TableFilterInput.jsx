import { useEffect, useRef } from 'react';

const TableFilterInput = ({ globalFilter, setGlobalFilter }) => {
	return (
		<div>
			<input
				type="text"
				value={globalFilter ?? ''}
				onChange={(event) => setGlobalFilter(event.target.value)}
				className="w-full rounded border-2 border-gray-800  border-opacity-25   bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-700 dark:focus:border-opacity-75"
				placeholder="Search all columns..."
			/>
		</div>
	);
};
export default TableFilterInput;
