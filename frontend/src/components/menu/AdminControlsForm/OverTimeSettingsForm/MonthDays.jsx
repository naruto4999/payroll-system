import React from 'react';
import { Field, ErrorMessage, FieldArray, Formik } from 'formik';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const MonthDays = ({ element, index }) => {
	return (
		<div
			className={classNames(
				Number.isInteger(element.maxOtHrs) && element.maxOtHrs > 0 ? 'bg-redAccent-700 bg-opacity-50' : '',
				'group relative flex h-20 flex-col rounded-sm border hover:bg-teal-700 hover:bg-opacity-50 dark:border-slate-400 dark:border-opacity-30'
			)}
		>
			<div className="flex h-1/2 w-full flex-col justify-center">
				<p className="mx-auto h-fit w-fit text-blueAccent-400">{element.day}</p>
			</div>
			<div className="flex h-1/2 w-full flex-col rounded">
				<Field
					className="custom-number-input h-full rounded border-slate-200 border-opacity-40 bg-zinc-800 p-1 text-center outline-none transition focus:border-opacity-100 group-hover:border dark:focus:border-opacity-75"
					type="number"
					name={`dayArray[${index}].maxOtHrs`}
				/>
			</div>
		</div>
	);
};

export default MonthDays;
