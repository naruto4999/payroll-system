import React, { useRef, useEffect, useState, useMemo } from 'react';
import { FaUserPlus } from 'react-icons/fa6';
import { FaCircleNotch } from 'react-icons/fa6';
import { Field, ErrorMessage } from 'formik';
import { useGetSingleEmployeeSalaryEarningQuery } from '../../../../authentication/api/employeeEntryApiSlice';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};
const isDateWithinRange = (date, fromDate, toDate) => {
	return date >= fromDate && date <= toDate;
};
const timeFormat = (time) => {
	const timeParts = time.split(':');
	const formattedTime = `${timeParts[0]}:${timeParts[1]}`;
	return formattedTime;
};
const EditSalary = React.memo(
	({
		handleSubmit,
		handleChange,
		handleBlur,
		values,
		errors,
		isValid,
		touched,
		setFieldValue,
		globalCompany,
		cancelButtonClicked,
		isEditing,
		dirty,
		initialValues,
		addedEmployeeId,
		yearOfJoining,
		fetchedEarningsHeads,
		updateEmployeeSalaryId,
		firstRender,
		setFirstRender,
		monthOfJoining,
	}) => {
		const {
			data: singleEmployeeSalaryEarning,
			isLoading: isLoadingSingleEmployeeSalaryEarning,
			isSuccess: isSingleEmployeeSalaryEarningSuccess,
			isFetching: isFetchingSingleEmployeeSalaryEarning,
		} = useGetSingleEmployeeSalaryEarningQuery(
			{
				id: updateEmployeeSalaryId,
				company: globalCompany.id,
				year: values.year,
			},
			{
				skip: updateEmployeeSalaryId === null,
			}
		);

		const currentDate = new Date();
		const futureYear = currentDate.getFullYear() + 1;

		console.log(values.year);
		console.log(monthOfJoining);
		console.log(yearOfJoining);
		console.log(values);

		const options = [];

		for (let i = yearOfJoining; i <= currentDate.getFullYear(); i++) {
			options.push(
				<option key={i} value={i}>
					{i}
				</option>
			);
		}

		const months = [
			'01',
			'02',
			'03',
			'04',
			'05',
			'06',
			'07',
			'08',
			'09',
			'10',
			'11',
			'12',
		];

		const data = useMemo(
			() =>
				singleEmployeeSalaryEarning
					? [...singleEmployeeSalaryEarning]
					: [],
			[singleEmployeeSalaryEarning]
		);
		console.log(data);

		const prevSingleEmployeeSalaryEarningRef = useRef(
			firstRender ? null : singleEmployeeSalaryEarning
		);
		useEffect(() => {
			setFirstRender(false);
			if (
				prevSingleEmployeeSalaryEarningRef.current !==
				singleEmployeeSalaryEarning
			) {
				if (
					isSingleEmployeeSalaryEarningSuccess == true &&
					data.length != 0
				) {
					const initialValues = {
						year: values.year,
						earnings: {},
						sameValue: {
							'01': false,
							'02': false,
							'03': false,
							'04': false,
							'05': false,
							'06': false,
							'07': false,
							'08': false,
							'09': false,
							10: false,
							11: false,
							12: false,
						},
					};

					// Iterate through each object in fetchedEarningsHeads
					fetchedEarningsHeads.forEach((item) => {
						// const monthInitialValues = {};
						const months = [
							'01',
							'02',
							'03',
							'04',
							'05',
							'06',
							'07',
							'08',
							'09',
							'10',
							'11',
							'12',
						];

						// Set initial value for each month ('01' to '12')
						months.forEach((month) => {
							singleEmployeeSalaryEarning.forEach(
								(salaryEarning) => {
									if (
										item.name ===
										salaryEarning.earningsHead.name
									) {
										let fromDate = new Date(
											salaryEarning.fromDate
										);
										let toDate = new Date(
											salaryEarning.toDate
										);
										let formik_field_date_representation =
											new Date(
												`${values.year}-${month}-01`
											);
										if (
											isDateWithinRange(
												formik_field_date_representation,
												fromDate,
												toDate
											)
										) {
											setFieldValue(
												`earnings.${item.name}.${month}`,
												salaryEarning.value
											);
										} else if (
											formik_field_date_representation <
											new Date(
												`${yearOfJoining}-${monthOfJoining}-01`
											)
										) {
											setFieldValue(
												`earnings.${item.name}.${month}`,
												''
											);
										}
									}
								}
							);
						});

						// Assign the monthInitialValues object to the 'name' key
						// initialValues.earnings[item.name] = monthInitialValues;
					});
				}
			}
			prevSingleEmployeeSalaryEarningRef.current =
				singleEmployeeSalaryEarning;
		}, [singleEmployeeSalaryEarning]);
		// console.log(singleEmployeeSalaryEarning);
		// console.log(prevSingleEmployeeSalaryEarningRef);

		useEffect(() => {
			for (const month in values.sameValue) {
				setFieldValue(`sameValue.${month}`, false);
			}
		}, [values.year]);

		useEffect(() => {
			// Sync up earnings values based on sameValue checkboxes for each earning head
			for (const earningHead in values.earnings) {
				const sameValueMonths = [];
				for (const month in values.sameValue) {
					if (values.sameValue[month]) {
						sameValueMonths.push(month);
					}
				}
				sameValueMonths.sort();

				if (sameValueMonths.length > 1) {
					const selectedMonthValue =
						values.earnings[earningHead][sameValueMonths[0]];
					sameValueMonths.forEach((month) => {
						setFieldValue(
							`earnings.${earningHead}.${month}`,
							selectedMonthValue
						);
					});
				}
			}
		}, [values.sameValue]);

		if (singleEmployeeSalaryEarning?.length === 0) {
			return (
				<>
					<div className="mx-auto font-bold text-redAccent-500 dark:text-redAccent-600">
						{
							'Please First Create a Salary for this employee in (Employee Entry -> Salary Details)'
						}
					</div>
				</>
			);
		} else {
			return (
				<div className="text-gray-900 dark:text-slate-100">
					{/* <h1 className="font-medium text-2xl mb-2">Add Employee</h1> */}
					<form
						action=""
						className="flex flex-col justify-center gap-2"
						onSubmit={handleSubmit}
					>
						<section>
							<label
								htmlFor="year"
								className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								Salary for year
							</label>
							<Field
								as="select"
								name="year"
								className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
							>
								{options}
							</Field>
							{isFetchingSingleEmployeeSalaryEarning && (
								<FaCircleNotch className="ml-2 inline animate-spin text-amber-700 dark:text-amber-600 " />
							)}

							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="year" />
							</div>
						</section>
						<section className="flex flex-row flex-wrap justify-center gap-10 lg:flex-nowrap">
							<div className="w-fit">
								<div className="mt-9">
									<h3 className="my-4 text-xl">January</h3>
									<h3 className="my-4 text-xl">February</h3>
									<h3 className="my-4 text-xl">March</h3>
									<h3 className="my-4 text-xl">April</h3>
									<h3 className="my-4 text-xl">May</h3>
									<h3 className="my-4 text-xl">June</h3>
									<h3 className="my-4 text-xl">July</h3>
									<h3 className="my-4 text-xl">August</h3>
									<h3 className="my-4 text-xl">September</h3>
									<h3 className="my-4 text-xl">October</h3>
									<h3 className="my-4 text-xl">November</h3>
									<h3 className="my-4 text-xl">December</h3>
								</div>
							</div>

							{Object.keys(values?.earnings).map((key) => (
								<div className="w-fit" key={key}>
									<h3 className="font-b text-xl text-blueAccent-600 dark:text-blueAccent-500">
										{key}
									</h3>

									{months.map((month, index) => (
										<div
											className="relative my-2"
											key={index}
										>
											{console.log(
												values.year == yearOfJoining &&
													parseInt(month) <
														monthOfJoining
											)}
											<Field
												className={classNames(
													errors[key]?.[month] &&
														touched[key]?.[month]
														? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
														: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
													'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
												)}
												type="number"
												name={`earnings.${key}.${month}`}
												disabled={
													values.year ==
														yearOfJoining &&
													parseInt(month) <
														monthOfJoining
												}
											/>
											<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
												<ErrorMessage
													name={`earnings.${key}.${month}`}
												/>
											</div>
										</div>
									))}
								</div>
							))}

							<div className="w-fit">
								<div className="mb-5">
									<h2 className="text-base font-medium text-amber-700 dark:text-amber-600">
										Same
									</h2>
								</div>

								{months.map((month, index) => (
									<div key={index} className="my-5">
										<Field
											type="checkbox"
											name={`sameValue.${month}`}
											className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
											disabled={
												values.year == yearOfJoining &&
												parseInt(month) <
													parseInt(monthOfJoining)
											}
										/>
									</div>
								))}
							</div>
						</section>
						{/* {errorMessage && errorMessage.error && (
                            <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                {errorMessage.error}
                            </p>
                        )} */}

						<section className="mt-4 mb-2 flex flex-row gap-4">
							<button
								className={classNames(
									isValid
										? 'hover:bg-teal-600  dark:hover:bg-teal-600'
										: 'opacity-40',
									'w-20 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
								)}
								type="submit"
								disabled={!isValid}
								onClick={handleSubmit}
							>
								Update
							</button>
							<button
								type="button"
								className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
								// onClick={() => {
								//     cancelButtonClicked(isEditing);
								//     setErrorMessage("");
								// }}
							>
								Cancel
							</button>
						</section>
					</form>
				</div>
			);
		}
	}
);
export default EditSalary;
