import React, { useEffect } from 'react';
import { Field, ErrorMessage, FieldArray } from 'formik';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const EditAdvance = React.memo(
	({
		globalCompany,
		handleSubmit,
		values,
		errors,
		setFieldValue,
		cancelButtonClicked,
		updateEmployeeId,
		isValid,
	}) => {
		const advanceInitialValues = {
			principal: 0,
			date: '',
			emi: 0,
			tenureMonths: '',
			repaidAmount: '',
		};
		const calculateTenureInMonths = (principal, emi) => {
			let months = Math.floor(principal / emi);
			if (principal % emi != 0) {
				months += 1;
			}
			return months;
		};
		console.log(values);

		useEffect(() => {
			// Loop through the updatedAdvanceDetails array and calculate/set tenureMonths for each object
			values.employeeAdvanceDetails.map((details, index) => {
				console.log(index);
				if (details.principal != 0 && details.emi != 0) {
					console.log(details.principal);
					console.log(details.emi);
					const tenureMonths = calculateTenureInMonths(parseInt(details.principal), parseFloat(details.emi));
					const years = Math.floor(tenureMonths / 12);
					const months = tenureMonths % 12;
					const formattedTenure =
						tenureMonths >= 12 ? `${years} Years and ${months} Months` : `${months} Months`;
					console.log(formattedTenure);
					setFieldValue(`employeeAdvanceDetails.${index}.tenureMonths`, formattedTenure);
				} else {
					setFieldValue(`employeeAdvanceDetails.${index}.tenureMonths`, '');
				}

				// Format the tenureMonths as "x Years and y Months"

				// Update the detail object with the calculated tenureMonths
				//   return {
				//     ...detail,
				//     tenureMonths: formattedTenure,
				//   };
			});

			// Update the state with the updatedAdvanceDetails
			// setUpdatedAdvanceDetails(updatedDetails);
		}, [values.employeeAdvanceDetails]); // Empty dependency array t
		return (
			<div className="text-gray-900 dark:text-slate-100">
				{/* <h1 className="font-medium text-2xl mb-2">Add Employee</h1> */}
				<form action="" className="flex flex-col justify-center gap-2" onSubmit={handleSubmit}>
					<section className="flex flex-row flex-wrap justify-center gap-10 lg:flex-nowrap">
						<div className="w-fit">
							<FieldArray
								name="employeeAdvanceDetails"
								render={(arrayHelpers) => {
									return (
										<div>
											{values.employeeAdvanceDetails.map((member, index) => (
												<div
													key={index}
													className="my-1 flex flex-row flex-wrap gap-1 rounded border-2 border-gray-800 border-opacity-25 p-2 dark:border-slate-100 dark:border-opacity-25"
												>
													<div className="flex w-full flex-row justify-between">
														<div className="mr-2 text-blueAccent-500 dark:text-blueAccent-600">{`${
															index + 1
														}`}</div>
														<div>
															<button
																type="button"
																className="inline-flex items-center justify-center rounded-md bg-redAccent-500 p-2 hover:bg-redAccent-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 dark:bg-redAccent-700 dark:hover:bg-redAccent-600"
																onClick={() => arrayHelpers.remove(index)}
															>
																<svg
																	className="h-4 w-4"
																	xmlns="http://www.w3.org/2000/svg"
																	fill="none"
																	viewBox="0 0 24 24"
																	stroke="currentColor"
																	aria-hidden="true"
																>
																	<path
																		strokeLinecap="round"
																		strokeLinejoin="round"
																		strokeWidth="2"
																		d="M6 18L18 6M6 6l12 12"
																	/>
																</svg>
															</button>
														</div>
													</div>
													<div className="flex flex-row flex-wrap gap-1">
														<div>
															<label
																htmlFor={`employeeAdvanceDetails.${index}.principal`}
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
															>
																Principal*
															</label>
															<Field
																className={classNames(
																	errors.employeeAdvanceDetails?.[index]?.principal &&
																		touched.employeeAdvanceDetails?.[index]
																			?.principal
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'min-w-32 block rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="number"
																name={`employeeAdvanceDetails.${index}.principal`}
															/>
														</div>

														<div>
															<label
																htmlFor={`employeeAdvanceDetails.${index}.emi`}
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
															>
																EMI*
															</label>
															<Field
																className={classNames(
																	errors.employeeAdvanceDetails?.[index]?.emi &&
																		touched.employeeAdvanceDetails?.[index]?.emi
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'min-w-32 block rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="number"
																name={`employeeAdvanceDetails.${index}.emi`}
															/>
														</div>

														<div>
															<label
																htmlFor={`employeeAdvanceDetails.${index}.tenureMonths`}
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
															>
																Tenure
															</label>
															<Field
																className={classNames(
																	errors.employeeAdvanceDetails?.[index]
																		?.tenureMonths &&
																		touched.employeeAdvanceDetails?.[index]
																			?.tenureMonths
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'min-w-32 block rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="text"
																// value={'asd'}
																name={`employeeAdvanceDetails.${index}.tenureMonths`}
																disabled={true}
															/>
														</div>

														<div>
															<label
																htmlFor={`employeeAdvanceDetails.${index}.date`}
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
															>
																Date*
															</label>
															<Field
																className={classNames(
																	errors.employeeAdvanceDetails?.[index]?.date &&
																		touched.employeeAdvanceDetails?.[index]?.date
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'min-w-32 block rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="date"
																name={`employeeAdvanceDetails.${index}.date`}
															/>
														</div>

														<div>
															<label
																htmlFor={`employeeAdvanceDetails.${index}.repaidAmount`}
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
															>
																Repaid Amount
															</label>
															<Field
																className={classNames(
																	errors.employeeAdvanceDetails?.[index]
																		?.repaidAmount &&
																		touched.employeeAdvanceDetails?.[index]
																			?.repaidAmount
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'min-w-32 block rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="number"
																name={`employeeAdvanceDetails.${index}.repaidAmount`}
																disabled={true}
															/>
														</div>
													</div>
												</div>
											))}
											<div>
												<button
													onClick={() =>
														arrayHelpers.insert(
															values.employeeAdvanceDetails.length + 1,
															advanceInitialValues
														)
													}
													className="inline-flex items-center justify-center rounded-md bg-teal-500 p-2 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500 dark:bg-teal-700 dark:hover:bg-teal-600"
													type="button"
												>
													<svg
														className="h-4 w-4"
														xmlns="http://www.w3.org/2000/svg"
														fill="none"
														viewBox="0 0 24 24"
														stroke="currentColor"
														aria-hidden="true"
													>
														<path
															strokeLinecap="round"
															strokeLinejoin="round"
															strokeWidth="2"
															d="M5 12h14M12 5v14"
														/>
													</svg>
												</button>
											</div>
										</div>
									);
								}}
							/>
						</div>
					</section>
					<section className="mt-4 mb-2 flex flex-row gap-4">
						<button
							className={classNames(
								isValid ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
								'w-20 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
							)}
							type="submit"
							// disabled={!isValid}
							onClick={handleSubmit}
						>
							Update
						</button>
						<button
							type="button"
							className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
							onClick={() => {
								cancelButtonClicked(isEditing);
								// setErrorMessage('');
							}}
						>
							Cancel
						</button>
					</section>
				</form>
			</div>
		);
	}
);

export default EditAdvance;
