import React from 'react';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const AddEmployeeNavigationBar = ({
	addEmployeePopover,
	editEmployeePopover,
	editEmployeePopoverHandler,
	isEditing,
	updateEmployeeId,
}) => {
	console.log(updateEmployeeId);
	return (
		// <h1>HI</h1>
		<div className=" mx-auto mt-6 flex h-10 w-fit flex-row justify-center gap-8 md:mt-0">
			<button
				onClick={() => {
					isEditing
						? editEmployeePopoverHandler({
								popoverName: 'editEmployeePersonalDetail',
								id: updateEmployeeId,
						  })
						: null;
				}}
				className={classNames(
					addEmployeePopover.addEmployeePersonalDetail ||
						editEmployeePopover.editEmployeePersonalDetail
						? 'text-opacity-100 dark:text-opacity-100'
						: 'text-opacity-50 dark:text-opacity-50',
					'text-sm font-semibold text-gray-900  transition-all dark:text-slate-100 md:text-xl'
				)}
			>
				Personal
				<div
					className={classNames(
						addEmployeePopover.addEmployeePersonalDetail ||
							editEmployeePopover.editEmployeePersonalDetail
							? ''
							: 'hidden',
						'mt-2 h-1 dark:bg-blueAccent-600 '
					)}
				></div>
			</button>

			<button
				onClick={() => {
					if (isEditing) {
						editEmployeePopoverHandler({
							popoverName: 'editEmployeeProfessionalDetail',
							id: updateEmployeeId,
						});
						// getSingleEmployeeProfessionalDetail({globalCompany, id: updateEmployeeId})
					}
				}}
				className={classNames(
					addEmployeePopover.addEmployeeProfessionalDetail ||
						editEmployeePopover.editEmployeeProfessionalDetail
						? 'text-opacity-100 dark:text-opacity-100'
						: 'text-opacity-50 dark:text-opacity-50',
					'text-sm font-semibold text-gray-900  transition-all dark:text-slate-100 md:text-xl'
				)}
			>
				Professional
				<div
					className={classNames(
						addEmployeePopover.addEmployeeProfessionalDetail ||
							editEmployeePopover.editEmployeeProfessionalDetail
							? ''
							: 'hidden',
						'mt-2 h-1 dark:bg-blueAccent-600 '
					)}
				></div>
			</button>
			<button
				onClick={() => {
					if (isEditing) {
						editEmployeePopoverHandler({
							popoverName: 'editEmployeeSalaryDetail',
							id: updateEmployeeId,
						});
						// getSingleEmployeeProfessionalDetail({globalCompany, id: updateEmployeeId})
					}
				}}
				className={classNames(
					addEmployeePopover.addEmployeeSalaryDetail ||
						editEmployeePopover.editEmployeeSalaryDetail
						? 'text-opacity-100 dark:text-opacity-100'
						: 'text-opacity-50 dark:text-opacity-50',
					'text-sm font-semibold text-gray-900  transition-all dark:text-slate-100 md:text-xl'
				)}
			>
				Salary
				<div
					className={classNames(
						addEmployeePopover.addEmployeeSalaryDetail ||
							editEmployeePopover.editEmployeeSalaryDetail
							? ''
							: 'hidden',
						'mt-2 h-1 dark:bg-blueAccent-600 '
					)}
				></div>
			</button>
			<button
				onClick={() => {
					if (isEditing) {
						editEmployeePopoverHandler({
							popoverName: 'editEmployeePfEsiDetail',
							id: updateEmployeeId,
						});
					}
				}}
				className={classNames(
					addEmployeePopover.addEmployeePfEsiDetail ||
						editEmployeePopover.editEmployeePfEsiDetail
						? 'text-opacity-100 dark:text-opacity-100'
						: 'text-opacity-50 dark:text-opacity-50',
					'text-sm font-semibold text-gray-900  transition-all dark:text-slate-100 md:text-xl'
				)}
			>
				ESI & PF
				<div
					className={classNames(
						addEmployeePopover.addEmployeePfEsiDetail ||
							editEmployeePopover.editEmployeePfEsiDetail
							? ''
							: 'hidden',
						'mt-2 h-1 dark:bg-blueAccent-600 '
					)}
				></div>
			</button>
			<button
				onClick={() => {
					if (isEditing) {
						editEmployeePopoverHandler({
							popoverName: 'editEmployeeFamilyNomineeDetail',
							id: updateEmployeeId,
						});
					}
				}}
				className={classNames(
					addEmployeePopover.addEmployeeFamilyNomineeDetail ||
						editEmployeePopover.editEmployeeFamilyNomineeDetail
						? 'text-opacity-100 dark:text-opacity-100'
						: 'text-opacity-50 dark:text-opacity-50',
					'text-sm font-semibold text-gray-900  transition-all dark:text-slate-100 md:text-xl'
				)}
			>
				Family/Nominee
				<div
					className={classNames(
						addEmployeePopover.addEmployeeFamilyNomineeDetail ||
							editEmployeePopover.editEmployeeFamilyNomineeDetail
							? ''
							: 'hidden',
						'mt-2 h-1 dark:bg-blueAccent-600 '
					)}
				></div>
			</button>
		</div>
	);
};

export default AddEmployeeNavigationBar;
