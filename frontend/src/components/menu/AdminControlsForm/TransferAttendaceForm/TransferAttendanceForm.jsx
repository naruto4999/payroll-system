import React, { useState, useMemo } from 'react';
import MonthYearSelector from '../../Reports/forms/MonthYearSelector';
import { useGetEmployeePersonalDetailsQuery } from '../../../authentication/api/employeeEntryApiSlice';
import { useDispatch, useSelector } from 'react-redux';
import { useTransferAttendanceMutation } from '../../../authentication/api/transferAttendanceApiSlice';
import ConfirmationModal from '../../../UI/ConfirmationModal';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import { ConfirmationModalSchema } from '../../Transaction/forms/TimeUpdationForm/TimeUpdationSchema';
import { alertActions } from '../../../authentication/store/slices/alertSlice';

ReactModal.setAppElement('#root');

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const TransferAttendanceForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);

	const {
		data: employeePersonalDetails,
		isLoading: isLoadingEmployeePersonalDetails,
		isSuccess: isSuccessEmployeePersonalDetails,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);

	const [selectedDate, setSelectedDate] = useState({
		year: new Date().getFullYear(),
		month: new Date().getMonth() + 1,
	});

	const [
		transferAttendance,
		{
			isLoading: isTransferringAttendance,
			// isError: errorRegisteringRegular,
			isSuccess: isTransferAttendanceSuccess,
		},
	] = useTransferAttendanceMutation();

	const [showConfirmModal, setShowConfirmModal] = useState(false);

	const earliestMonthAndYear = useMemo(() => {
		let earliestDate = Infinity; // Initialize earliestDate to a very large value
		let earliestMonth = '';
		let earliestYear = '';
		if (employeePersonalDetails) {
			for (const employee of employeePersonalDetails) {
				const dateOfJoining = new Date(employee.dateOfJoining);

				if (dateOfJoining < earliestDate) {
					earliestDate = dateOfJoining;
					earliestMonth = dateOfJoining.getMonth() + 1;
					earliestYear = dateOfJoining.getFullYear();
				}
			}
		}
		return {
			earliestMonth: earliestMonth,
			earliestYear: earliestYear,
		};
	}, [employeePersonalDetails]);

	const transferAttendanceButtonClicked = async (formikBag) => {
		let toSend = {
			company: globalCompany.id,
			month: selectedDate.month,
			year: selectedDate.year,
		};
		console.log(toSend);
		try {
			// setShowLoadingBar(true);
			const startTime = performance.now();
			const data = await transferAttendance(toSend).unwrap();
			const endTime = performance.now(); // Record the end time
			const responseTime = endTime - startTime;
			const responseTimeInSeconds = (responseTime / 1000).toFixed(2);
			dispatch(
				alertActions.createAlert({
					message: `Transferred, Time Taken: ${responseTimeInSeconds} seconds`,
					type: 'Success',
					duration: 5000,
				})
			);
			// setShowLoadingBar(false);
		} catch (err) {
			// setShowLoadingBar(false);
			console.log(err);
			dispatch(
				alertActions.createAlert({
					message: 'Error Occurred',
					type: 'Error',
					duration: 5000,
				})
			);
		}
		// setShowConfirmModal(false);
	};

	return (
		<section className="mx-5 mt-2">
			<div className="flex flex-row flex-wrap place-content-between">
				<div className="mr-4">
					<h1 className="text-3xl font-medium">Transfer Attendance</h1>
					<p className="my-2 text-sm">
						Transfer attendances to Sub User account according to the Over Time Settings defined.
					</p>
				</div>
			</div>
			<section className="flex flex-col gap-4">
				<MonthYearSelector
					setSelectedDate={setSelectedDate}
					selectedDate={selectedDate}
					earliestMonthAndYear={earliestMonthAndYear}
				/>
				<div>
					<button
						className={classNames(
							true ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
							'w-60 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
						)}
						type="submit"
						// disabled={!isValid}
						onClick={() => {
							setShowConfirmModal(true);
						}}
					>
						Transfer Atteandance
					</button>
				</div>
			</section>
			<ReactModal
				className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
				isOpen={showConfirmModal}
				onRequestClose={() => setShowConfirmModal(false || isTransferringAttendance)}
				style={{
					overlay: {
						backgroundColor: 'rgba(0, 0, 0, 0.75)',
					},
				}}
			>
				<Formik
					initialValues={{ userInput: '' }}
					validationSchema={ConfirmationModalSchema}
					onSubmit={transferAttendanceButtonClicked}
					component={(props) => (
						<ConfirmationModal
							{...props}
							displayHeading={'Transfer Attendance'}
							setShowConfirmModal={setShowConfirmModal}
						/>
					)}
				/>
			</ReactModal>
		</section>
	);
};

export default TransferAttendanceForm;
