import { useRef, useEffect, useState } from 'react';
import { useGetDepartmentsQuery } from '../../../../authentication/api/departmentEntryApiSlice';
import { useGetDesignationsQuery } from '../../../../authentication/api/designationEntryApiSlice';
import { useGetCategoriesQuery } from '../../../../authentication/api/categoryEntryApiSlice';
import { useGetSalaryGradesQuery } from '../../../../authentication/api/salaryGradeEntryApiSlice';
import { useGetShiftsQuery } from '../../../../authentication/api/shiftEntryApiSlice';
import { FaCircleNotch } from 'react-icons/fa6';
import { Field, ErrorMessage } from 'formik';

// import { useGetEmployeeShiftsQuery } from '../../../../authentication/api/employeeShiftsApiSlice';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};
const timeFormat = (time) => {
	const timeParts = time.split(':');
	const formattedTime = `${timeParts[0]}:${timeParts[1]}`;
	return formattedTime;
};

const LoadingSpinner = () => (
	<div>
		<div className="mx-auto flex h-fit w-fit items-center rounded bg-blueAccent-600 p-2 dark:bg-blueAccent-700">
			<FaCircleNotch className="mr-2 animate-spin text-gray-900 dark:text-slate-100" />
			<p className="text-gray-900 dark:text-slate-100">Processing...</p>
		</div>
	</div>
);

const EmployeeProfessionalDetail = ({
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
	addedEmployeeId,
	employeeShifts,
}) => {
	const { data: fetchedDepartments, isLoading: isLoadingDepartments } = useGetDepartmentsQuery(globalCompany);

	const { data: fetchedDesignations, isLoading: isLoadingDesignations } = useGetDesignationsQuery(globalCompany);

	const { data: fetchedCategories, isLoading: isLoadingCategories } = useGetCategoriesQuery(globalCompany);

	const { data: fetchedSalaryGrades, isLoading: isLoadingSalaryGrade } = useGetSalaryGradesQuery(globalCompany);

	const { data: fetchedShifts, isLoading: isLoadingShifts } = useGetShiftsQuery(globalCompany);

	useEffect(() => {
		setShowLoadingBar(isLoadingDepartments || isLoadingDesignations || isLoadingCategories || isLoadingSalaryGrade);
	}, [isLoadingDepartments, isLoadingDesignations, isLoadingCategories, isLoadingSalaryGrade]);

	// console.log(values);

	console.log(values);
	console.log(employeeShifts);

	// const {
	// 	data: employeeShifts,
	// 	isLoading: isLoadingEmployeeShifts,
	// 	isSuccess: isEmployeeShiftsSuccess,
	// 	isFetching: isFetchingEmployeeShifts,
	// } = useGetEmployeeShiftsQuery(
	// 	{
	// 		employee: values.employeeProfessionalDetail.employee,
	// 		company: globalCompany.id,
	// 		year: new Date(
	// 			values.employeeProfessionalDetail.dateOfJoining
	// 		).getFullYear(),
	// 	},
	// 	{
	// 		skip: !isEditing,
	// 	}
	// );
	const previousExperienceRows = ['first', 'second', 'third'];
	const references = ['first', 'second'];

	useEffect(() => {
		if (values.employeeProfessionalDetail.dateOfJoining !== '') {
			let selectedDate = new Date(values.employeeProfessionalDetail.dateOfJoining);
			selectedDate.setMonth(selectedDate.getMonth() + 6);
			selectedDate.setDate(selectedDate.getDate() - 1);
			setFieldValue('employeeProfessionalDetail.dateOfConfirm', selectedDate.toISOString().slice(0, 10));
		}
	}, [values.employeeProfessionalDetail.dateOfJoining]);

	useEffect(() => {}, []);

	if (isLoadingDepartments || isLoadingDesignations || isLoadingCategories || isLoadingSalaryGrade) {
		return <LoadingSpinner />;
	} else if (!addedEmployeeId && !isEditing) {
		return (
			<div className="mx-auto mt-1 text-xl font-bold text-redAccent-500 dark:text-redAccent-600">
				Please add Personal Details First
			</div>
		);
	} else {
		return (
			<div className="text-gray-900 dark:text-slate-100">
				<form action="" className="flex flex-col justify-center gap-2" onSubmit={handleSubmit}>
					<section className="flex flex-row flex-wrap justify-center gap-10 lg:flex-nowrap">
						<div className="w-fit">
							<label
								htmlFor="employeeProfessionalDetail.dateOfJoining"
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								Date of Joining
							</label>
							<div className="relative">
								<Field
									className={classNames(
										errors?.employeeProfessionalDetail?.dateOfJoining &&
											touched?.employeeProfessionalDetail?.dateOfJoining
											? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
											: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
										'block w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
									)}
									type="date"
									maxLength={100}
									name="employeeProfessionalDetail.dateOfJoining"
								/>
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									<ErrorMessage name="employeeProfessionalDetail.dateOfJoining" />
								</div>
							</div>
							<label
								htmlFor="employeeProfessionalDetail.dateOfConfirm"
								className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								Date of Confirm
							</label>
							<div className="relative">
								<Field
									className={classNames(
										errors?.employeeProfessionalDetail?.dateOfConfirm &&
											touched?.employeeProfessionalDetail?.dateOfConfirm
											? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
											: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
										'block w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
									)}
									type="date"
									maxLength={100}
									name="employeeProfessionalDetail.dateOfConfirm"
								/>
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									<ErrorMessage name="employeeProfessionalDetail.dateOfConfirm" />
								</div>
							</div>

							<label
								className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
								htmlFor="employeeProfessionalDetail.department"
							>
								Department
							</label>
							<Field
								as="select"
								name="employeeProfessionalDetail.department"
								className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
							>
								<option value="">-- Select an option --</option>
								{fetchedDepartments?.map((department) => (
									<option key={department.id} value={department.id}>
										{department.name}
									</option>
								))}
							</Field>

							<label
								className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
								htmlFor="employeeProfessionalDetail.designation"
							>
								Designation
							</label>
							<Field
								className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
								name="employeeProfessionalDetail.designation"
								as="select"
							>
								<option value="">-- Select an option --</option>
								{fetchedDesignations?.map((designation) => (
									<option key={designation.id} value={designation.id}>
										{designation.name}
									</option>
								))}
							</Field>

							<label
								className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
								htmlFor="employeeProfessionalDetail.category"
							>
								Category
							</label>
							<Field
								className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
								name="employeeProfessionalDetail.category"
								as="select"
							>
								<option value="">-- Select an option --</option>
								{fetchedCategories?.map((category) => (
									<option key={category.id} value={category.id}>
										{category.name}
									</option>
								))}
							</Field>
						</div>

						<div className="w-fit">
							<label
								className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
								htmlFor="employeeProfessionalDetail.salaryGrade"
								as="select"
							>
								Salary Grade
							</label>
							<Field
								className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
								name="employeeProfessionalDetail.salaryGrade"
								as="select"
							>
								<option value="">-- Select an option --</option>
								{fetchedSalaryGrades?.map((salaryGrade) => (
									<option key={salaryGrade.id} value={salaryGrade.id}>
										{salaryGrade.name}
									</option>
								))}
							</Field>

							{isEditing && employeeShifts?.length != 0 ? (
								<p className="w-80 font-bold text-redAccent-600 dark:text-redAccent-500">
									Please go to Employee Shifts Entry to make any changes to Shift
								</p>
							) : (
								<>
									<label
										className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
										htmlFor="employeeShift.shift"
									>
										Shift
									</label>
									<Field
										className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
										name="employeeShift.shift"
										as="select"
									>
										<option value="">-- Select an option --</option>

										{fetchedShifts?.map((shift) => (
											<option key={shift.id} value={shift.id}>
												{shift.name}
												{` [${timeFormat(shift.beginningTime)} - ${timeFormat(shift.endTime)}]`}
											</option>
										))}
									</Field>
									<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
										<ErrorMessage name="employeeShift.shift" />
									</div>
								</>
							)}

							<label
								className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
								htmlFor="employeeProfessionalDetail.weeklyOff"
								as="select"
							>
								Weekly Off
							</label>
							<Field
								className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
								name="employeeProfessionalDetail.weeklyOff"
								as="select"
							>
								<option value="no_off">No Off</option>
								<option value="mon">Monday</option>
								<option value="tue">Tuesday</option>
								<option value="wed">Wednesday</option>
								<option value="thu">Thursday</option>
								<option value="fri">Friday</option>
								<option value="sat">Saturday</option>
								<option value="sun">Sunday</option>
							</Field>

							<label
								className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
								htmlFor="employeeProfessionalDetail.extraOff"
							>
								Extra Off
							</label>
							<Field
								className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
								name="employeeProfessionalDetail.extraOff"
								as="select"
							>
								<option value="no_off">No Off</option>
								<option value="mon1">First Monday</option>
								<option value="mon2">Second Monday</option>
								<option value="mon3">Third Monday</option>
								<option value="mon4">Fourth Monday</option>
								<option value="tue1">First Tuesday</option>
								<option value="tue2">Second Tuesday</option>
								<option value="tue3">Third Tuesday</option>
								<option value="tue4">Fourth Tuesday</option>
								<option value="wed1">First Wednesday</option>
								<option value="wed2">Second Wednesday</option>
								<option value="wed3">Third Wednesday</option>
								<option value="wed4">Fourth Wednesday</option>
								<option value="thu1">First Thursday</option>
								<option value="thu2">Second Thursday</option>
								<option value="thu3">Third Thursday</option>
								<option value="thu4">Fourth Thursday</option>
								<option value="fri1">First Friday</option>
								<option value="fri2">Second Friday</option>
								<option value="fri3">Third Friday</option>
								<option value="fri4">Fourth Friday</option>
								<option value="sat1">First Saturday</option>
								<option value="sat2">Second Saturday</option>
								<option value="sat3">Third Saturday</option>
								<option value="sat4">Fourth Saturday</option>
								<option value="sun1">First Sunday</option>
								<option value="sun2">Second Sunday</option>
								<option value="sun3">Third Sunday</option>
								<option value="sun4">Fourth Sunday</option>
							</Field>
						</div>
					</section>
					{console.log(values)}
					{errorMessage && errorMessage.error && (
						<p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">{errorMessage.error}</p>
					)}
					<section className="w-[1000px]">
						<p className="block text-base font-semibold text-black text-opacity-100 dark:text-white dark:text-opacity-70">
							Previous Experiences
						</p>
						<table className="w-full border-collapse text-center text-xs">
							<thead className="sticky top-0 z-20 bg-blueAccent-600 dark:bg-blueAccent-700 dark:bg-opacity-40">
								<tr>
									<th className="w-8 px-1 py-2 font-medium">S/N</th>
									<th className="px-1 py-2 font-medium">Company Name</th>
									<th className="px-1 py-2 font-medium">Designation</th>
									<th className="px-1 py-2 font-medium">From Date</th>
									<th className="px-1 py-2 font-medium">To Date</th>
									<th className="px-1 py-2 font-medium">Salary</th>
									<th className="px-1 py-2 font-medium">Reason For Leaving</th>
								</tr>
							</thead>
							<tbody>
								{/* Row 1 */}
								{previousExperienceRows.map((serial, index) => (
									<tr
										key={index}
										className="hover:bg-zinc-200 dark:hover:bg-zinc-900 dark:focus:bg-teal-800 dark:focus:bg-opacity-50"
									>
										<td className="relative w-8 border border-slate-400 border-opacity-60 p-0 font-normal ">
											{index + 1}
										</td>
										<td className="relative border border-slate-400 border-opacity-60 p-0 font-normal ">
											<Field
												className="custom-number-input h-8 w-full bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
												type="text"
												name={`employeeProfessionalDetail.${serial}PreviousExperienceCompanyName`}
											/>
										</td>
										<td className="relative border border-slate-400 border-opacity-60 p-0 font-normal ">
											<Field
												className="custom-number-input h-8 w-full bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
												type="text"
												name={`employeeProfessionalDetail.${serial}PreviousExperienceDesignation`}
											/>
										</td>
										<td className="relative border border-slate-400 border-opacity-60 p-0 font-normal ">
											<Field
												className="custom-number-input h-8 w-full bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
												type="date"
												name={`employeeProfessionalDetail.${serial}PreviousExperienceFromDate`}
											/>
										</td>
										<td className="relative border border-slate-400 border-opacity-60 p-0 font-normal ">
											<Field
												className="custom-number-input h-8 w-full bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
												type="date"
												name={`employeeProfessionalDetail.${serial}PreviousExperienceToDate`}
											/>
										</td>
										<td className="relative w-20 border border-slate-400 border-opacity-60 p-0 font-normal">
											<Field
												className="custom-number-input h-8 w-full bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
												type="number"
												name={`employeeProfessionalDetail.${serial}PreviousExperienceSalary`}
											/>
										</td>
										<td className="relative border border-slate-400 border-opacity-60 p-0 font-normal ">
											<Field
												className="custom-number-input h-8 w-full bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
												type="text"
												name={`employeeProfessionalDetail.${serial}PreviousExperienceReasonForLeaving`}
											/>
										</td>
									</tr>
								))}
							</tbody>
						</table>

						<p className="block text-base font-semibold text-black text-opacity-100 dark:text-white dark:text-opacity-70">
							References
						</p>
						<table className="w-full border-collapse text-center text-xs">
							<thead className="sticky top-0 z-20 bg-yellow-600 dark:bg-yellow-700 dark:bg-opacity-40">
								<tr>
									<th className="w-8 px-1 py-2 font-medium">S/N</th>
									<th className="px-1 py-2 font-medium">Name</th>
									<th className="px-1 py-2 font-medium">Address</th>
									<th className="px-1 py-2 font-medium">Relation</th>
									<th className="px-1 py-2 font-medium">Phone</th>
								</tr>
							</thead>
							<tbody>
								{/* Row 1 */}
								{references.map((serial, index) => (
									<tr
										key={index}
										className="hover:bg-zinc-200 dark:hover:bg-zinc-900 dark:focus:bg-teal-800 dark:focus:bg-opacity-50"
									>
										<td className="relative w-8 border border-slate-400 border-opacity-60 p-0 font-normal ">
											{index + 1}
										</td>
										<td className="relative border border-slate-400 border-opacity-60 p-0 font-normal ">
											<Field
												className="custom-number-input h-8 w-full bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
												type="text"
												name={`employeeProfessionalDetail.${serial}ReferenceName`}
											/>
										</td>
										<td className="relative border border-slate-400 border-opacity-60 p-0 font-normal ">
											<Field
												className="custom-number-input h-8 w-full bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
												type="text"
												name={`employeeProfessionalDetail.${serial}ReferenceAddress`}
											/>
										</td>
										<td className="relative w-36 border border-slate-400 border-opacity-60 p-0 font-normal">
											<Field
												className="custom-number-input h-8 w-full bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
												type="text"
												name={`employeeProfessionalDetail.${serial}ReferenceRelation`}
											/>
										</td>
										<td className="relative w-32 border border-slate-400 border-opacity-60 p-0 font-normal ">
											<Field
												className="custom-number-input h-8 w-full bg-zinc-50 bg-transparent p-1 outline-none transition focus:border-opacity-100  dark:focus:border-opacity-75"
												type="number"
												name={`employeeProfessionalDetail.${serial}ReferencePhone`}
											/>
										</td>
									</tr>
								))}
							</tbody>
						</table>
					</section>

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
export default EmployeeProfessionalDetail;
