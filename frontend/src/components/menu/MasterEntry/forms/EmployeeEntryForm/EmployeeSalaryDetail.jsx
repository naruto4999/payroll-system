import { useRef, useEffect, useState } from 'react';
import { FaUserPlus } from 'react-icons/fa6';
import { FaCircleNotch } from 'react-icons/fa6';
import { Field, ErrorMessage } from 'formik';
// import { useLazyGetSingleEmployeeSalaryEarningQuery } from "../../../../authentication/api/employeeEntryApiSlice";

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};
const timeFormat = (time) => {
	const timeParts = time.split(':');
	const formattedTime = `${timeParts[0]}:${timeParts[1]}`;
	return formattedTime;
};
const EmployeeSalaryDetail = ({
	handleSubmit,
	values,
	errors,
	isValid,
	touched,
	errorMessage,
	setErrorMessage,
	setFieldValue,
	globalCompany,
	setShowLoadingBar,
	cancelButtonClicked,
	isEditing,
	dirty,
	initialValues,
	addedEmployeeId,
	fromDateMostRecentYear,
	toDateSmallestYear,
	updateEmployeeId,
	isSingleEmployeeSalaryDetailSuccess,
	isSingleEmployeeProfessionalDetailSuccess,
}) => {
	console.log(errors);
	console.log(values.year);
	console.log(values);
	console.log(isSingleEmployeeProfessionalDetailSuccess);

	useEffect(() => {
		if (values.salaryDetail.overtimeType !== 'no_overtime' && values.salaryDetail.overtimeRate === '') {
			setFieldValue('salaryDetail.overtimeRate', 'S');
		} else if (values.salaryDetail.overtimeType === 'no_overtime') {
			setFieldValue('salaryDetail.overtimeRate', '');
		}
	}, [values.salaryDetail.overtimeType]);
	if (!addedEmployeeId && !isEditing) {
		return (
			<div className="mx-auto mt-1 text-xl font-bold text-redAccent-500 dark:text-redAccent-600">
				Please add Personal Details First
			</div>
		);
	} else if (!isSingleEmployeeProfessionalDetailSuccess || values.year === null) {
		return (
			<div className="mx-auto mt-1 text-xl font-bold text-redAccent-500 dark:text-redAccent-600">
				Please add Professional Details First
			</div>
		);
	} else {
		return (
			<div className="text-gray-900 dark:text-slate-100">
				{/* <h1 className="font-medium text-2xl mb-2">Add Employee</h1> */}
				<form action="" className="flex flex-col justify-center gap-2" onSubmit={handleSubmit}>
					<section className="flex flex-row flex-wrap justify-center gap-10 lg:flex-nowrap">
						<div className="w-fit">
							<label
								htmlFor="year"
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								Salary for year
							</label>
							<p>{values.year ? values.year : "Coundn't get Joining Date"}</p>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="year" />
							</div>
							{(!isEditing || !isSingleEmployeeSalaryDetailSuccess) &&
								Object.keys(initialValues.earningsHead).map((key) => (
									<div key={key}>
										<label
											htmlFor={key}
											className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
										>
											{key}
										</label>
										<div className="relative">
											<Field
												className={classNames(
													errors.earningsHead?.[key] && touched.earningsHead?.[key]
														? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
														: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
													'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
												)}
												type="number"
												name={`earningsHead.${key}`}
											/>
											<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
												<ErrorMessage name={`earningsHead.${key}`} />
											</div>
										</div>
									</div>
								))}

							{isEditing && isSingleEmployeeSalaryDetailSuccess && (
								<p className="w-80 font-bold text-redAccent-600 dark:text-redAccent-500">
									Please go to Employee Salary to make any changes to Salary since it already exists
								</p>
							)}
						</div>

						<div className="w-fit">
							<label
								htmlFor={'salaryDetail.overtimeType'}
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								Overtime Type
							</label>
							<Field
								as="select"
								name="salaryDetail.overtimeType"
								className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
							>
								<option value="no_overtime">No Overtime</option>
								<option value="all_days">All Days</option>
								<option value="holiday_weekly_off">Holiday/Weekly Off</option>
							</Field>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name={'salaryDetail.overtimeType'} />
							</div>

							<label
								htmlFor={'salaryDetail.overtimeRate'}
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								Overtime Rate
							</label>
							{values.salaryDetail.overtimeType !== 'no_overtime' ? (
								<Field
									as="select"
									name="salaryDetail.overtimeRate"
									className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
								>
									<option value="S">Single</option>
									<option value="D">Double</option>
								</Field>
							) : (
								<div className="mt-1 text-xs font-bold text-blueAccent-500 dark:text-blueAccent-700">
									No overtime is allowed
								</div>
							)}
							{errorMessage && errorMessage.overtimeRate && (
								<p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errorMessage.overtimeRate}
								</p>
							)}
							{console.log(errorMessage)}
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name={'salaryDetail.overtimeRate'} />
							</div>

							<label
								htmlFor={'salaryDetail.salaryMode'}
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								Salary Mode
							</label>
							<Field
								as="select"
								name="salaryDetail.salaryMode"
								className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
							>
								<option value="monthly">Monthly</option>
								<option value="daily">Daily</option>
								<option value="piece_rate">Piece Rate</option>
							</Field>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name={'salaryDetail.salaryMode'} />
							</div>

							<label
								htmlFor={'salaryDetail.paymentMode'}
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								Payment Mode
							</label>
							<Field
								as="select"
								name="salaryDetail.paymentMode"
								className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
							>
								<option value="bank_transfer">Bank Transfer</option>
								<option value="cheque">Cheque</option>
								<option value="cash">Cash</option>
								<option value="rtgs">RTGS</option>
								<option value="neft">NEFT</option>
							</Field>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name={'salaryDetail.paymentMode'} />
							</div>

							<label
								htmlFor="salaryDetail.bankName"
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								Bank Name
							</label>
							<Field
								className={classNames(
									errors.salaryDetail?.bankName && touched.salaryDetail?.bankName
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								name="salaryDetail.bankName"
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="salaryDetail.bankName" />
							</div>

							<label
								htmlFor="salaryDetail.accountNumber"
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								Account Number
							</label>
							<Field
								className={classNames(
									errors.salaryDetail?.accountNumber && touched.salaryDetail?.accountNumber
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								name="salaryDetail.accountNumber"
								maxLength={30}
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="salaryDetail.accountNumber" />
							</div>

							<label
								htmlFor="salaryDetail.ifcs"
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								IFSC
							</label>
							<Field
								className={classNames(
									errors.salaryDetail?.ifcs && touched.salaryDetail?.ifcs
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								name="salaryDetail.ifcs"
								maxLength={25}
							/>
							<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
								<ErrorMessage name="salaryDetail.ifcs" />
							</div>
						</div>

						<div className="w-fit">
							<label className="my-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
								Labour Welfare Fund:
								<Field
									type="checkbox"
									name="salaryDetail.labourWellfareFund"
									className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
								/>
							</label>

							<label className="my-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
								Late Deduction:
								<Field
									type="checkbox"
									name="salaryDetail.lateDeduction"
									className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
								/>
							</label>

							<label className="my-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
								Bonus Allow:
								<Field
									type="checkbox"
									name="salaryDetail.bonusAllow"
									className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
								/>
							</label>

							<label className="my-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
								Bonus Exg.:
								<Field
									type="checkbox"
									name="salaryDetail.bonusExg"
									className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
								/>
							</label>
						</div>
					</section>
					{errorMessage && errorMessage.error && (
						<p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">{errorMessage.error}</p>
					)}

					<section className="mt-4 mb-2 flex flex-row gap-4">
						<button
							className={classNames(
								isValid ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
								'w-20 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
							)}
							type="submit"
							disabled={!isValid}
							onClick={handleSubmit}
						>
							{isEditing ? 'Update' : 'Add'}
						</button>
						<button
							type="button"
							className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
							onClick={() => {
								cancelButtonClicked(isEditing);
								setErrorMessage('');
							}}
						>
							Cancel
						</button>
					</section>
				</form>
			</div>
		);
	}
};
export default EmployeeSalaryDetail;
