import React, { useEffect } from 'react';
import { Field, ErrorMessage, FieldArray } from 'formik';
import { FaCircleNotch } from 'react-icons/fa';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};
const FilterOptions = ({
	handleChange,
	values,
	pfEsiFilter,
	isValid,
	handleSubmit,
	isSubmitting,
	selectedDate,
	setFieldValue,
	setPfEsiFilter,
}) => {
	// console.log(values);
	// useEffect(() => {
	// 	setFieldValue('filters.monthFromDate', 1);
	// 	setFieldValue('filters.monthToDate', new Date(selectedDate.year, selectedDate.month, 0).getDate());
	// }, [selectedDate.month]);
	const handleRadioChange = (event) => {
		setPfEsiFilter(event.target.value);
		if (event.target.value == 'pfAllow') {
			setFieldValue('reportType', 'pf_statement');
		} else if (event.target.value == 'esiAllow') {
			setFieldValue('reportType', 'esi_statement');
		}
	};
	console.log(values);

	return (
		<div className="flex flex-col gap-2">
			{/* <div>
				<label>
					<input
						type="radio"
						name="pfEsiFilter"
						value="pfAllow"
						checked={pfEsiFilter === 'pfAllow'}
						onChange={handleRadioChange}
					/>
					PF
				</label>
				<label>
					<input
						type="radio"
						name="pfEsiFilter"
						value="esiAllow"
						checked={pfEsiFilter === 'esiAllow'}
						onChange={handleRadioChange}
					/>
					ESI
				</label>
			</div> */}
			<div className="grid w-full grid-cols-2 gap-2 rounded-xl bg-zinc-700 p-1">
				<div>
					<input
						type="radio"
						name="pfEsiFilter"
						id="pfAllow"
						value="pfAllow"
						className="peer hidden"
						checked={pfEsiFilter === 'pfAllow'}
						onChange={handleRadioChange}
					/>
					<label
						htmlFor="pfAllow"
						className="block cursor-pointer select-none rounded-xl p-1 text-center peer-checked:bg-teal-600 peer-checked:font-bold peer-checked:text-white"
					>
						PF
					</label>
				</div>

				<div>
					<input
						type="radio"
						name="pfEsiFilter"
						id="esiAllow"
						value="esiAllow"
						className="peer hidden"
						checked={pfEsiFilter === 'esiAllow'}
						onChange={handleRadioChange}
					/>
					<label
						htmlFor="esiAllow"
						className="block cursor-pointer select-none rounded-xl p-1 text-center peer-checked:bg-teal-600 peer-checked:font-bold peer-checked:text-white"
					>
						ESI
					</label>
				</div>
			</div>
			<div>
				<label
					htmlFor="reportType"
					className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
				>
					Report Type :
				</label>
				<Field
					as="select"
					id="reportType"
					className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
					name="reportType"
				>
					{pfEsiFilter == 'pfAllow' && <option value="pf_statement">PF Statement</option>}
					{pfEsiFilter == 'esiAllow' && <option value="esi_statement">ESI Statement</option>}
				</Field>
			</div>
			{/* {(values.reportType == 'present_report' || values.reportType == 'overtime_sheet_daily') && (
				<div>
					<label
						htmlFor="filters.date"
						className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
					>
						Date :
					</label>
					<Field
						className="custom-number-input w-14 rounded border-2 border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
						type="number"
						name="filters.date"
						id="filters.date"
					/>
				</div>
			)} */}
			<div>
				<label
					htmlFor="sortBy"
					className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
				>
					Sort By :
				</label>
				<Field
					as="select"
					id="sortBy"
					className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
					name="filters.sortBy"
				>
					<option value="paycode">Paycode</option>
					<option value="attendance_card_no">Attendance Card No.</option>
					<option value="employee_name">Employee Name</option>
				</Field>
			</div>
			<div>
				<label
					htmlFor="format"
					className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
				>
					Format :
				</label>
				<Field
					as="select"
					id="format"
					className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
					name="filters.format"
				>
					<option value="xlsx">MS Excel</option>
					<option value="txt">Notepad / Txt File</option>
				</Field>
			</div>
			{/* <div>
				<label
					htmlFor="groupBy"
					className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
				>
					Group By :
				</label>
				<Field
					as="select"
					id="groupBy"
					className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
					name="filters.groupBy"
				>
					<option value="none">None</option>
					<option value="department">Department</option>
				</Field>
			</div> */}
			{/* <div>
				<label
					htmlFor="resignationFilter"
					className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
				>
					Resignation Filter :
				</label>
				<Field
					as="select"
					id="resignationFilter"
					className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
					name="filters.resignationFilter"
				>
					<option value="all">All</option>
					<option value="without_resigned">Without Resigned Employees</option>
					<option value="only_resigned">Only Resigned Employees</option>
				</Field>
			</div> */}

			<section>
				<div className="mt-4 mb-2 flex w-fit flex-row gap-4">
					<button
						className={classNames(
							isValid ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
							'h-10 w-fit rounded bg-teal-500 p-2 px-4 text-base font-medium dark:bg-teal-700'
						)}
						type="submit"
						disabled={!isValid}
						onClick={handleSubmit}
					>
						Generate
						{isSubmitting && (
							<FaCircleNotch className="my-auto ml-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
						)}
					</button>
				</div>
			</section>
		</div>
	);
};

export default FilterOptions;
