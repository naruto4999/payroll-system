import React, { useEffect, useState } from 'react';
import { useGetSingleEmployeePersonalDetailQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import { useGetSingleEmployeeProfessionalDetailPrefetchQuery } from '../../../../authentication/api/resignationApiSlice';
import { Field, ErrorMessage } from 'formik';

const dateDifference = (date1, date2) => {
	const [year1, month1, day1] = date1.split('-').map(Number);
	const [year2, month2, day2] = date2.split('-').map(Number);

	const date1Obj = new Date(year1, month1 - 1, day1);
	const date2Obj = new Date(year2, month2 - 1, day2);

	const timeDifference = date2Obj - date1Obj;

	const yearsDifference = date2Obj.getFullYear() - date1Obj.getFullYear();
	const monthsDifference = date2Obj.getMonth() - date1Obj.getMonth();
	const daysDifference = date2Obj.getDate() - date1Obj.getDate();

	return {
		years: yearsDifference,
		months: monthsDifference,
		days: daysDifference,
		totalMilliseconds: timeDifference,
	};
};

const FullAndFinal = ({ fullAndFinalEmployeeId, globalCompany }) => {
	const [durationWorked, setDurationWorked] = useState(null);
	const {
		data: employeePersonalDetail,
		isLoadingEmployeePersonalDetail,
		isEmployeePersonalDetailSuccess,
		isEmployeePersonalDetailError,
		errorEmployeePersonalDetail,
	} = useGetSingleEmployeePersonalDetailQuery({ company: globalCompany.id, id: fullAndFinalEmployeeId });
	const {
		data: employeeProfessionalDetail,
		isLoadingEmployeeProfessionalDetail,
		isEmployeeProfessionalDetailSuccess,
		isEmployeeProfessionalDetailError,
		errorEmployeeProfessionalDetail,
	} = useGetSingleEmployeeProfessionalDetailPrefetchQuery({ company: globalCompany.id, id: fullAndFinalEmployeeId });
	if (employeePersonalDetail && employeeProfessionalDetail) {
		console.log(
			dateDifference(employeeProfessionalDetail?.dateOfJoining, employeeProfessionalDetail?.resignationDate)
		);
	}
	useEffect(() => {
		if (employeePersonalDetail && employeeProfessionalDetail) {
			setDurationWorked(
				dateDifference(employeeProfessionalDetail?.dateOfJoining, employeeProfessionalDetail?.resignationDate)
			);
		}
	}, [employeeProfessionalDetail, employeePersonalDetail]);

	if (isLoadingEmployeePersonalDetail || isLoadingEmployeeProfessionalDetail) {
		return (
			<div className="fixed inset-0 z-50 mx-auto my-auto flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium">
				<FaCircleNotch className="mr-2 animate-spin text-white" />
				Processing...
			</div>
		);
	} else {
		return (
			<div className="w-fit">
				<section className="flex flex-col rounded border border-slate-500 p-2">
					<div className="flex h-8 flex-row">
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Paycode:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeePersonalDetail?.paycode}
							</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">ACN:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeePersonalDetail?.attendanceCardNo}
							</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Date of Joining:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeeProfessionalDetail?.dateOfJoining}
							</div>
						</div>
					</div>
					<div className="flex h-8 flex-row">
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Name:</div>
							<div className="w-72 font-medium text-blueAccent-500">{employeePersonalDetail?.name}</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Department:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeeProfessionalDetail?.department?.name}
							</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Resignation Date:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeeProfessionalDetail?.resignationDate}
							</div>
						</div>
					</div>
					<div className="flex h-8 flex-row">
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">F/H Name:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeePersonalDetail?.fatherOrHusbandName}
							</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Designation:</div>
							<div className="w-72 font-medium text-blueAccent-500">
								{employeeProfessionalDetail?.designation?.name}
							</div>
						</div>
						<div className="flex flex-row">
							<div className="w-36 font-medium text-slate-400">Full & Final Date:</div>
							<div className="w-72 text-sm font-medium text-slate-100">
								<Field
									className="block h-7 w-44 rounded border-2 border-gray-800 border-opacity-25 bg-zinc-50  bg-opacity-50 p-1  outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-700 dark:focus:border-opacity-75"
									type="date"
									maxLength={100}
									name="employeeProfessionalDetail.dateOfJoining"
								/>
							</div>
						</div>
					</div>
					<div className="mx-auto flex h-8 flex-row">
						<div className="w-36 font-medium text-slate-400">Working Duration:</div>
						<div className="w-72 font-medium text-yellow-600">
							{durationWorked != null
								? `  ${durationWorked.years} Years, ${durationWorked.months} Months, ${durationWorked.days} Days`
								: ''}
						</div>
					</div>
				</section>
			</div>
		);
	}
};

export default FullAndFinal;
