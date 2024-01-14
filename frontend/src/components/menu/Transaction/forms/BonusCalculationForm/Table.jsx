import React, { useEffect } from 'react';
import { Field, ErrorMessage, FieldArray } from 'formik';
import { FaCircleNotch } from 'react-icons/fa';
import TableHeader from './TableHeader';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const Table = ({
	handleChange,
	values,
	isValid,
	handleSubmit,
	isSubmitting,
	selectedDate,
	setFieldValue,
	categorizedBonusCalculations,
	initialValues,

	calculations,
	categories,
}) => {
	console.log(initialValues);

	useEffect(() => {
		if (!isSubmitting) {
			if (categories !== undefined) {
				categories.forEach((category) => {
					// initialValues[category.id] = {};
					let updatedValues = {};

					const startDate = new Date(Date.UTC(selectedDate.year, calculations.bonusStartMonth - 1, 1));
					let currentDate = startDate;

					for (let i = 0; i < 12; i++) {
						let year = currentDate.getFullYear();
						let month = currentDate.getMonth() + 1;
						let day = currentDate.getDate();
						if (
							categorizedBonusCalculations?.[category.id]?.[
								`${year}-${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day}`
							]
						) {
							updatedValues[`${year}-${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day}`] =
								categorizedBonusCalculations[category.id][
									`${year}-${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day}`
								];
						} else {
							updatedValues[`${year}-${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day}`] = 0;
						}

						// Move to the next month
						currentDate.setMonth(currentDate.getMonth() + 1);
					}
					setFieldValue(`bonusCalculationsMonthWise.${category.id}`, updatedValues);
				});
			}
		}
	}, [
		categorizedBonusCalculations != undefined
			? Object.keys(categorizedBonusCalculations)
					.map((item) => item.date)
					.join(',')
			: '',
		parseInt(selectedDate.year),
	]);
	console.log('yes rerendering');
	console.log(values);

	return (
		<form id="" className="mt-2" onSubmit={handleSubmit}>
			<table className="w-full border-collapse text-center text-xs">
				<TableHeader bonusStartMonth={calculations.bonusStartMonth} year={selectedDate.year} />

				<tbody>
					{Object.keys(values.bonusCalculationsMonthWise).map((category, index) => {
						if (category == 'bonusPercentage') {
							return false;
						}
						const categoryObject = categories.find((element) => element.id === parseInt(category));

						console.log(category);
						return (
							<tr
								key={index}
								className="h-10 hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50"
							>
								<td className="relative w-8 border border-slate-400 border-opacity-60 p-0 font-normal text-blueAccent-500">
									{category}
								</td>
								<td className="relative w-8 border border-slate-400 border-opacity-60 p-0 font-normal text-blueAccent-500">
									{categoryObject ? categoryObject.name : 'N/A'}
								</td>
								{Object.keys(values.bonusCalculationsMonthWise?.[category]).map((month, index) => {
									return (
										<td
											className="relative w-20 border border-slate-400 border-opacity-60 p-0 font-normal"
											key={month}
										>
											<Field
												className="custom-number-input h-8 w-full bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
												type="number"
												name={`bonusCalculationsMonthWise.${category}.${month}`}
											/>
										</td>
									);
								})}
							</tr>
						);
					})}
				</tbody>
			</table>
			<div className="mt-4">
				<label
					htmlFor="bonusPercentage"
					className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
				>
					Bonus % :
				</label>
				<Field
					className="custom-number-input w-14 rounded border-2 border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
					type="number"
					name="bonusPercentage"
					id="bonusPercentage"
				/>
			</div>
			<div>
				<button
					className="mt-4 whitespace-nowrap rounded bg-teal-500 py-2 px-6 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
					type="submit"
				>
					{'Update'}
				</button>
			</div>
		</form>
	);
};

export default Table;
