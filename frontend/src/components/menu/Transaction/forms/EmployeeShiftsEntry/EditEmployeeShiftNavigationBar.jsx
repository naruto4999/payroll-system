import React from 'react';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const EditEmployeeShiftNavigationBar = ({
	editEmployeeShiftPopover,
	editEmployeeShiftsPopoverHandler,
	isEditing,
	updateEmployeeId,
}) => {
	return (
		// <h1>HI</h1>
		<div className=" mx-auto mt-6 flex h-10 w-fit flex-row justify-center gap-8 md:mt-0">
			<button
				onClick={() => {
					editEmployeeShiftsPopoverHandler('dayWiseShiftEdit');
				}}
				className={classNames(
					editEmployeeShiftPopover.dayWiseShiftEdit
						? 'text-opacity-100 dark:text-opacity-100'
						: 'text-opacity-50 dark:text-opacity-50',
					'text-lg font-semibold text-gray-900  transition-all dark:text-slate-100 md:text-xl'
				)}
			>
				Day Wise Shift
				<div
					className={classNames(
						editEmployeeShiftPopover.dayWiseShiftEdit
							? ''
							: 'hidden',
						'mt-2 h-1 dark:bg-blueAccent-600 '
					)}
				></div>
			</button>

			<button
				onClick={() => {
					editEmployeeShiftsPopoverHandler('permanentShiftEdit');
				}}
				className={classNames(
					editEmployeeShiftPopover.permanentShiftEdit
						? 'text-opacity-100 dark:text-opacity-100'
						: 'text-opacity-50 dark:text-opacity-50',
					'text-lg font-semibold text-gray-900  transition-all dark:text-slate-100 md:text-xl'
				)}
			>
				Permanent Shift
				<div
					className={classNames(
						editEmployeeShiftPopover.permanentShiftEdit
							? ''
							: 'hidden',
						'mt-2 h-1 dark:bg-blueAccent-600 '
					)}
				></div>
			</button>
		</div>
	);
};

export default EditEmployeeShiftNavigationBar;
