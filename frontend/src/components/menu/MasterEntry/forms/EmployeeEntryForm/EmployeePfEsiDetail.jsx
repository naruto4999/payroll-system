import { useRef, useEffect, useState } from 'react';
import { FaUserPlus } from 'react-icons/fa6';
import { FaCircleNotch } from 'react-icons/fa6';
import { Field, ErrorMessage } from 'formik';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};
const timeFormat = (time) => {
	const timeParts = time.split(':');
	const formattedTime = `${timeParts[0]}:${timeParts[1]}`;
	return formattedTime;
};
const EmployeePfEsiDetail = ({
	handleSubmit,
	handleChange,
	handleBlur,
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
}) => {
	console.log(values);
	// console.log(errors)
	useEffect(() => {
		if (values.pfLimitIgnoreEmployee === false) {
			setFieldValue('pfLimitIgnoreEmployeeValue', '');
		}
		if (values.pfPercentIgnoreEmployee === false) {
			setFieldValue('pfPercentIgnoreEmployeeValue', '');
		}
		if (values.pfLimitIgnoreEmployer === false) {
			setFieldValue('pfLimitIgnoreEmployerValue', '');
		}
		if (values.pfPercentIgnoreEmployer === false) {
			setFieldValue('pfPercentIgnoreEmployerValue', '');
		}
	}, [
		values.pfLimitIgnoreEmployee,
		values.pfPercentIgnoreEmployee,
		values.pfLimitIgnoreEmployer,
		values.pfPercentIgnoreEmployer,
	]);

	if (!addedEmployeeId && !isEditing) {
		return (
			<div className="mx-auto mt-1 text-xl font-bold text-redAccent-500 dark:text-redAccent-600">
				Please add Personal Details First
			</div>
		);
	} else {
		return (
			<div className="text-gray-900 dark:text-slate-100">
				{/* <h1 className="font-medium text-2xl mb-2">Add Employee</h1> */}
				<form action="" className="flex flex-col justify-center gap-2" onSubmit={handleSubmit}>
					<section className="flex flex-row flex-wrap justify-center gap-10 lg:flex-nowrap">
						<div className="w-fit">
							<label className="my-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
								PF Allow:
								<Field
									type="checkbox"
									name="pfAllow"
									className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
								/>
							</label>
							<div>
								<label
									className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
									htmlFor={'pfNumber'}
								>
									PF Number
								</label>
								<Field
									className={classNames(
										errors.pfNumber && touched.pfNumber
											? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
											: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
										'block w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
									)}
									type="text"
									maxLength={50}
									name={'pfNumber'}
								/>
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									<ErrorMessage name="pfNumber" />
								</div>
							</div>

							<div>
								<label className="mt-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
									PF Limit Ignore Employee:
									<Field
										type="checkbox"
										name="pfLimitIgnoreEmployee"
										className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
									/>
								</label>
								<Field
									className={classNames(
										errors.pfLimitIgnoreEmployeeValue && touched.pfLimitIgnoreEmployeeValue
											? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
											: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
										'custom-number-input block w-full rounded  border-2   bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
									)}
									type="number"
									name={'pfLimitIgnoreEmployeeValue'}
									disabled={!values.pfLimitIgnoreEmployee}
								/>
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									<ErrorMessage name="pfLimitIgnoreEmployeeValue" />
								</div>
							</div>

							<div>
								<label className="mt-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
									PF % Ignore Employee:
									<Field
										type="checkbox"
										name="pfPercentIgnoreEmployee"
										className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
									/>
								</label>
								<Field
									className={classNames(
										errors.pfPercentIgnoreEmployeeValue && touched.pfPercentIgnoreEmployeeValue
											? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
											: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
										'custom-number-input block w-full rounded  border-2   bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
									)}
									type="number"
									maxLength={5}
									name={'pfPercentIgnoreEmployeeValue'}
									disabled={!values.pfPercentIgnoreEmployee}
								/>
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									<ErrorMessage name="pfPercentIgnoreEmployeeValue" />
								</div>
							</div>

							<div>
								<label className="mt-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
									PF Limit Ignore Employer:
									<Field
										type="checkbox"
										name="pfLimitIgnoreEmployer"
										className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
									/>
								</label>
								<Field
									className={classNames(
										errors.pfLimitIgnoreEmployerValue && touched.pfLimitIgnoreEmployerValue
											? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
											: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
										'custom-number-input block w-full rounded  border-2   bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
									)}
									type="number"
									name={'pfLimitIgnoreEmployerValue'}
									disabled={!values.pfLimitIgnoreEmployer}
								/>
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									<ErrorMessage name="pfLimitIgnoreEmployerValue" />
								</div>
							</div>

							<div>
								<label className="mt-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
									PF % Ignore Employer:
									<Field
										type="checkbox"
										name="pfPercentIgnoreEmployer"
										className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
									/>
								</label>
								<Field
									className={classNames(
										errors.pfPercentIgnoreEmployerValue && touched.pfPercentIgnoreEmployerValue
											? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
											: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
										'custom-number-input block w-full rounded  border-2   bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
									)}
									type="number"
									maxLength={5}
									name={'pfPercentIgnoreEmployerValue'}
									disabled={!values.pfPercentIgnoreEmployer}
								/>
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									<ErrorMessage name="pfPercentIgnoreEmployerValue" />
								</div>
							</div>

							<div>
								<label
									className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
									htmlFor={'vpfAmount'}
								>
									VPF
								</label>
								<Field
									className={classNames(
										errors.vpfAmount && touched.vpfAmount
											? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
											: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
										'custom-number-input block w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
									)}
									type="number"
									name={'vpfAmount'}
								/>
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									<ErrorMessage name="vpfAmount" />
								</div>
							</div>
						</div>

						<div className="w-fit">
							{/* <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block my-2">
                                Bonus Exg.:
                                <Field
                                    type="checkbox"
                                    name="salaryDetail.bonusExg"
                                    className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                                />
                            </label> */}

							<div>
								<label className="my-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
									ESI Allow:
									<Field
										type="checkbox"
										name="esiAllow"
										className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
									/>
								</label>
							</div>
							<div>
								<label
									className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
									htmlFor={'esiNumber'}
								>
									ESI Number
								</label>
								<Field
									className={classNames(
										errors.esiNumber && touched.esiNumber
											? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
											: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
										'block w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
									)}
									type="text"
									maxLength={30}
									name={'esiNumber'}
								/>
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									<ErrorMessage name="esiNumber" />
								</div>
							</div>

							<div>
								<label
									className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
									htmlFor={'esiDispensary'}
								>
									ESI Dispensary
								</label>
								<Field
									className={classNames(
										errors.esiDispensary && touched.esiDispensary
											? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
											: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
										'block w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
									)}
									type="text"
									maxLength={100}
									name={'esiDispensary'}
								/>
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									<ErrorMessage name="esiDispensary" />
								</div>
							</div>

							<div>
								<label className="my-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
									ESI on Overtime:
									<Field
										type="checkbox"
										name="esiOnOt"
										className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
									/>
								</label>
							</div>

							<div>
								<label
									className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
									htmlFor={'uanNumber'}
								>
									UAN Number
								</label>
								<Field
									className={classNames(
										errors.uanNumber && touched.uanNumber
											? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
											: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
										'block w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
									)}
									type="text"
									maxLength={50}
									name={'uanNumber'}
								/>
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									<ErrorMessage name="uanNumber" />
								</div>
							</div>
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
export default EmployeePfEsiDetail;
