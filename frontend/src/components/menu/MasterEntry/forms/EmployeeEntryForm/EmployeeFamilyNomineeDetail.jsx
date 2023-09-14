import { useRef, useEffect, useState } from 'react';
import { FaUserPlus } from 'react-icons/fa6';
import { FaPlus } from 'react-icons/fa6';
import { Field, ErrorMessage, FieldArray } from 'formik';
import {
	useLazyGetSingleEmployeePfEsiDetailQuery,
	useGetSingleEmployeePfEsiDetailQuery,
} from '../../../../authentication/api/employeeEntryApiSlice';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const EmployeeFamilyNomineeDetail = ({
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
	familyNomineeDetailInitailValues,
	updateEmployeeId,
	singleEmployeePfEsiDetail,
}) => {
	let employeeId = addedEmployeeId;
	if (isEditing) {
		employeeId = updateEmployeeId;
	}

	console.log(values);

	const useNomineeShare = (fieldName, nomineeFieldName) => {
		const previousNomineeRef = useRef([]);

		useEffect(() => {
			const hasNomineeChanged = values.familyNomineeDetail.some(
				(detail, index) => detail[fieldName] !== previousNomineeRef.current[index]
			);

			if (hasNomineeChanged) {
				const count = values.familyNomineeDetail.reduce(
					(accumulator, detail) => (detail[fieldName] ? accumulator + 1 : accumulator),
					0
				);
				const divisionResult = count > 0 ? (100 / count).toFixed(2) : '0.00';
				values.familyNomineeDetail.forEach((detail, index) => {
					if (detail[fieldName]) {
						setFieldValue(`familyNomineeDetail.${index}.${nomineeFieldName}`, parseFloat(divisionResult));
					} else {
						setFieldValue(`familyNomineeDetail.${index}.${nomineeFieldName}`, '');
					}
				});
			}

			// Update the previousNomineeRef with the current nominee values
			previousNomineeRef.current = values.familyNomineeDetail.map((detail) => detail[fieldName]);
		}, [values.familyNomineeDetail]);
	};

	// Usage
	useNomineeShare('isFaNominee', 'faNomineeShare');
	useNomineeShare('isGratuityNominee', 'gratuityNomineeShare');
	useNomineeShare('isEsiNominee', 'esiNomineeShare');
	useNomineeShare('isPfNominee', 'pfNomineeShare');

	useEffect(() => {
		values.familyNomineeDetail.forEach((detail, index) => {
			if (!detail.pfBenefits && detail.isPfNominee) {
				setFieldValue(`familyNomineeDetail.${index}.isPfNominee`, false);
			}
			if (!detail.esiBenefit && detail.isEsiNominee) {
				setFieldValue(`familyNomineeDetail.${index}.isEsiNominee`, false);
			}
		});
	}, [values.familyNomineeDetail]);

	if (!addedEmployeeId && !isEditing) {
		return (
			<div className="mx-auto mt-1 text-xl font-bold text-redAccent-500 dark:text-redAccent-600">
				Please add Personal Details First
			</div>
		);
	} else if (singleEmployeePfEsiDetail === null) {
		return (
			<div className="mx-auto mt-1 text-xl font-bold text-redAccent-500 dark:text-redAccent-600">
				Please add PF and ESI Details First
			</div>
		);
	} else {
		return (
			<div className="text-gray-900 dark:text-slate-100">
				{/* <h1 className="font-medium text-2xl mb-2">Add Employee</h1> */}
				<form action="" className="flex flex-col justify-center gap-2" onSubmit={handleSubmit}>
					<section className="flex flex-row flex-wrap justify-center gap-10 lg:flex-nowrap">
						<div className="w-fit">
							<FieldArray
								name="familyNomineeDetail"
								render={(arrayHelpers) => {
									return (
										<div>
											{values.familyNomineeDetail?.map((member, index) => (
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
																htmlFor={`familyNomineeDetail.${index}.name`}
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
															>
																Name
															</label>
															<Field
																className={classNames(
																	errors.familyNomineeDetail?.[index]?.name &&
																		touched.familyNomineeDetail?.[index]?.name
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'min-w-32 block rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="text"
																name={`familyNomineeDetail.${index}.name`}
																maxLength={100}
															/>
															<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
																<ErrorMessage
																	name={`familyNomineeDetail.${index}.name`}
																/>
															</div>
														</div>

														<div>
															<label
																htmlFor={`familyNomineeDetail.${index}.address`}
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
															>
																Address
															</label>
															<Field
																className={classNames(
																	errors.familyNomineeDetail?.[index]?.address &&
																		touched.familyNomineeDetail?.[index]?.address
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'min-w-32 block rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="text"
																name={`familyNomineeDetail.${index}.address`}
															/>
															<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
																<ErrorMessage
																	name={`familyNomineeDetail.${index}.address`}
																/>
															</div>
														</div>

														<div>
															<label
																htmlFor={`familyNomineeDetail.${index}.dob`}
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
															>
																DOB
															</label>
															<Field
																className={classNames(
																	errors.familyNomineeDetail?.[index]?.dob &&
																		touched.familyNomineeDetail?.[index]?.dob
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'block w-[132px] rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="date"
																name={`familyNomineeDetail.${index}.dob`}
															/>
															<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
																<ErrorMessage
																	name={`familyNomineeDetail.${index}.dob`}
																/>
															</div>
														</div>

														<div>
															<label
																htmlFor={`familyNomineeDetail.${index}.relation`}
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
															>
																Relation
															</label>
															<Field
																as="select"
																name={`familyNomineeDetail.${index}.relation`}
																className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
															>
																<option value="Father">Father</option>
																<option value="Mother">Mother</option>
																<option value="Wife">Wife</option>
																<option value="Son">Son</option>
																<option value="Brother">Brother</option>
																<option value="Sister">Sister</option>
																<option value="Daughter">Daughter</option>
																<option value="Husband">Husband</option>
															</Field>
															<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
																<ErrorMessage
																	name={`familyNomineeDetail.${index}.relation`}
																/>
															</div>
														</div>

														<div>
															<label
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
																htmlFor={`familyNomineeDetail.${index}.residing`}
															>
																Residing?
															</label>
															<Field
																type="checkbox"
																name={`familyNomineeDetail.${index}.residing`}
																className="mx-auto mt-2 block h-4 w-4 rounded accent-teal-600"
															/>
														</div>

														<div>
															<label
																className="mt-1 block text-center text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
																htmlFor={`familyNomineeDetail.${index}.esiBenefit`}
															>
																Esi
															</label>
															<Field
																type="checkbox"
																name={`familyNomineeDetail.${index}.esiBenefit`}
																className="mx-auto mt-2 block h-4 w-4 rounded accent-teal-600"
																disabled={!singleEmployeePfEsiDetail.esiAllow}
															/>
															{!singleEmployeePfEsiDetail.esiAllow && (
																<p className="mt-1 text-xs font-bold text-blueAccent-500 dark:text-blueAccent-600">
																	ESI is not allowed
																</p>
															)}
														</div>

														<div>
															<label
																className="mt-1 block text-center text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
																htmlFor={`familyNomineeDetail.${index}.pfBenefits`}
															>
																Pf
															</label>
															<Field
																type="checkbox"
																name={`familyNomineeDetail.${index}.pfBenefits`}
																className="mx-auto mt-2 block h-4 w-4 rounded accent-teal-600"
																disabled={!singleEmployeePfEsiDetail.pfAllow}
															/>
															{!singleEmployeePfEsiDetail.pfAllow && (
																<p className="mt-1 text-xs font-bold text-blueAccent-500 dark:text-blueAccent-600">
																	Pf is not allowed
																</p>
															)}
														</div>

														<div>
															<label
																className="mx-2 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
																htmlFor={`familyNomineeDetail.${index}.isEsiNominee`}
															>
																Esi Nominee
															</label>
															<Field
																type="checkbox"
																name={`familyNomineeDetail.${index}.isEsiNominee`}
																className="mx-auto mt-2 block h-4 w-4 rounded accent-teal-600"
																disabled={!singleEmployeePfEsiDetail.esiAllow}
															/>
															{!singleEmployeePfEsiDetail.esiAllow && (
																<p className="mt-1 text-xs font-bold text-blueAccent-500 dark:text-blueAccent-600">
																	ESI is not allowed
																</p>
															)}
														</div>

														<div>
															<label
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
																htmlFor={`familyNomineeDetail.${index}.esiNomineeShare`}
															>
																Esi %
															</label>
															<Field
																className={classNames(
																	errors.familyNomineeDetail?.[index]
																		?.esiNomineeShare &&
																		touched.familyNomineeDetail?.[index]
																			?.esiNomineeShare
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'custom-number-input block w-20 rounded  border-2   bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="number"
																maxLength={5}
																name={`familyNomineeDetail.${index}.esiNomineeShare`}
																disabled={
																	!values.familyNomineeDetail[index].isEsiNominee
																}
															/>
															{errors?.familyNomineeDetail?.[index]?.esiNomineeShare && (
																<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
																	{
																		errors?.familyNomineeDetail?.[index]
																			?.esiNomineeShare
																	}
																</div>
															)}
															{errorMessage[index]?.esiNomineeShare && (
																<p className="mt-1 w-20 text-xs font-bold text-red-500 dark:text-red-700">
																	{errorMessage[index].esiNomineeShare}
																</p>
															)}
														</div>

														<div>
															<label
																className="mx-2 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
																htmlFor={`familyNomineeDetail.${index}.isPfNominee`}
															>
																Pf Nominee
															</label>
															<Field
																type="checkbox"
																name={`familyNomineeDetail.${index}.isPfNominee`}
																className="mx-auto mt-2 block h-4 w-4 rounded accent-teal-600"
																disabled={
																	!singleEmployeePfEsiDetail.pfAllow ||
																	!values.familyNomineeDetail[index].pfBenefits
																}
															/>
															{!singleEmployeePfEsiDetail.pfAllow && (
																<p className="mt-1 text-xs font-bold text-blueAccent-500 dark:text-blueAccent-600">
																	Pf is not allowed
																</p>
															)}
														</div>

														<div>
															<label
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
																htmlFor={`familyNomineeDetail.${index}.pfNomineeShare`}
															>
																Pf %
															</label>
															<Field
																className={classNames(
																	errors.familyNomineeDetail?.[index]
																		?.pfNomineeShare &&
																		touched.familyNomineeDetail?.[index]
																			?.pfNomineeShare
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'custom-number-input block w-20 rounded  border-2   bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="number"
																maxLength={5}
																name={`familyNomineeDetail.${index}.pfNomineeShare`}
																disabled={
																	!values.familyNomineeDetail[index].isPfNominee
																}
															/>
															{errors?.familyNomineeDetail?.[index]?.pfNomineeShare && (
																<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
																	{
																		errors?.familyNomineeDetail?.[index]
																			?.pfNomineeShare
																	}
																</div>
															)}
															{errorMessage[index]?.pfNomineeShare && (
																<p className="mt-1 w-20 text-xs font-bold text-red-500 dark:text-red-700">
																	{errorMessage[index].pfNomineeShare}
																</p>
															)}
														</div>

														<div>
															<label
																className="mx-2 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
																htmlFor={`familyNomineeDetail.${index}.isFaNominee`}
															>
																FA Nominee
															</label>
															<Field
																type="checkbox"
																name={`familyNomineeDetail.${index}.isFaNominee`}
																className="mx-auto mt-2 block h-4 w-4 rounded accent-teal-600"
															/>
														</div>

														<div>
															<label
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
																htmlFor={`familyNomineeDetail.${index}.faNomineeShare`}
															>
																FA %
															</label>
															<Field
																className={classNames(
																	errors.familyNomineeDetail?.[index]
																		?.faNomineeShare &&
																		touched.familyNomineeDetail?.[index]
																			?.faNomineeShare
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'custom-number-input block w-20 rounded  border-2   bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="number"
																maxLength={5}
																name={`familyNomineeDetail.${index}.faNomineeShare`}
																disabled={
																	!values.familyNomineeDetail[index].isFaNominee
																}
															/>
															{errors?.familyNomineeDetail?.[index]?.faNomineeShare && (
																<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
																	{
																		errors?.familyNomineeDetail?.[index]
																			?.faNomineeShare
																	}
																</div>
															)}
															{errorMessage[index]?.faNomineeShare && (
																<p className="mt-1 w-20 text-xs font-bold text-red-500 dark:text-red-700">
																	{errorMessage[index].faNomineeShare}
																</p>
															)}
														</div>

														<div>
															<label
																className="mx-2 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
																htmlFor={`familyNomineeDetail.${index}.isGratuityNominee`}
															>
																Gratuity Nominee
															</label>
															<Field
																type="checkbox"
																name={`familyNomineeDetail.${index}.isGratuityNominee`}
																className="mx-auto mt-2 block h-4 w-4 rounded accent-teal-600"
															/>
														</div>

														<div>
															<label
																className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
																htmlFor={`familyNomineeDetail.${index}.gratuityNomineeShare`}
															>
																Gratuity %
															</label>
															<Field
																className={classNames(
																	errors.familyNomineeDetail?.[index]
																		?.gratuityNomineeShare &&
																		touched.familyNomineeDetail?.[index]
																			?.gratuityNomineeShare
																		? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
																		: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
																	'custom-number-input block w-20 rounded  border-2   bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
																)}
																type="number"
																maxLength={5}
																name={`familyNomineeDetail.${index}.gratuityNomineeShare`}
																disabled={
																	!values.familyNomineeDetail[index].isGratuityNominee
																}
															/>
															{errors?.familyNomineeDetail?.[index]
																?.gratuityNomineeShare && (
																<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
																	{
																		errors?.familyNomineeDetail?.[index]
																			?.gratuityNomineeShare
																	}
																</div>
															)}
															{errorMessage[index]?.gratuityNomineeShare && (
																<p className="mt-1 w-20 text-xs font-bold text-red-500 dark:text-red-700">
																	{errorMessage[index].gratuityNomineeShare}
																</p>
															)}
														</div>
													</div>
												</div>
											))}
											<div>
												<button
													onClick={() =>
														arrayHelpers.insert(
															values.familyNomineeDetail.length + 1,
															familyNomineeDetailInitailValues
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
							// disabled={!isValid}
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
export default EmployeeFamilyNomineeDetail;
