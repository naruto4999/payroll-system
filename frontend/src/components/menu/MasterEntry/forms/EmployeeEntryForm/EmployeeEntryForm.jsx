import React, { useEffect, useMemo, useState, useCallback } from 'react';
import {
	createColumnHelper,
	flexRender,
	getCoreRowModel,
	useReactTable,
	getSortedRowModel,
} from '@tanstack/react-table';
import { FaRegTrashAlt, FaPen, FaAngleUp, FaAngleDown, FaEye } from 'react-icons/fa';
import { useSelector } from 'react-redux';
import {
	useGetEmployeePersonalDetailsQuery,
	useAddEmployeePersonalDetailMutation,
	useAddEmployeeProfessionalDetailMutation,
	useLazyGetSingleEmployeePersonalDetailQuery,
	useUpdateEmployeePersonalDetailMutation,
	useUpdateEmployeeProfessionalDetailMutation,
	useLazyGetSingleEmployeeProfessionalDetailQuery,
	useAddEmployeeSalaryEarningMutation,
	useAddEmployeeSalaryDetailMutation,
	useLazyGetSingleEmployeeSalaryDetailQuery,
	useUpdateEmployeeSalaryDetailMutation,
	useAddEmployeePfEsiDetailMutation,
	useLazyGetSingleEmployeePfEsiDetailQuery,
	useUpdateEmployeePfEsiDetailMutation,
	useAddEmployeeFamilyNomineeDetailMutation,
	useLazyGetEmployeeFamilyNomineeDetailsQuery,
	useUpdateEmployeeFamilyNomineeDetailMutation,
	useDeleteEmployeeFamilyNomineeDetailMutation,
	useDeleteEmployeeMutation,
} from '../../../../authentication/api/employeeEntryApiSlice';
import { useGetEarningsHeadsQuery } from '../../../../authentication/api/earningsHeadEntryApiSlice';
import { useLazyGetEmployeeShiftsQuery } from '../../../../authentication/api/employeeShiftsApiSlice';
import { useOutletContext } from 'react-router-dom';
import ReactModal from 'react-modal';
import { Formik } from 'formik';
import EmployeePersonalDetail from './EmployeePersonalDetail';
import {
	EmployeePersonalDetailSchema,
	EmployeeProfessionalDetailSchema,
	EmployeePfEsiDetailSchema,
	EmployeeFamilyNomineeDetailSchema,
	generateEmployeeSalaryDetailSchema,
} from './EmployeeEntrySchema';
import AddEmployeeNavigationBar from './AddEmployeeNavigationBar';
import EmployeeProfessionalDetail from './EmployeeProfessionalDetail';
import EmployeeSalaryDetail from './EmployeeSalaryDetail';
import EmployeeFamilyNomineeDetail from './EmployeeFamilyNomineeDetail';
import EmployeePfEsiDetail from './EmployeePfEsiDetail';
import * as yup from 'yup';
import { useDispatch } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { useAddEmployeeShiftsMutation } from '../../../../authentication/api/employeeShiftsApiSlice';
import ConfirmationModal from '../../../../UI/ConfirmationModal';
import { ConfirmationModalSchema } from '../../../Transaction/forms/TimeUpdationForm/TimeUpdationSchema';

ReactModal.setAppElement('#root');

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

function getObjectDifferences(obj1, obj2) {
	const diffObj = {};
	if (Object.keys(obj1).length === 0) {
		return obj2;
	}

	for (const key in obj1) {
		console.log('inside the for loop ');
		if (obj1.hasOwnProperty(key) && obj2.hasOwnProperty(key)) {
			console.log('inside the if');
			let value1 = obj1[key];
			let value2 = obj2[key];
			console.log(value1);
			console.log(value2);

			if (value1 === null) {
				obj1[key] = '';
			}

			if (value2 === null) {
				obj2[key] = '';
			}
			if (obj1[key] !== obj2[key]) {
				diffObj[key] = obj2[key];
			}
		}
	}

	return diffObj;
}

const checkNullUndefinedValues = (obj) => {
	for (let key in obj) {
		if (obj[key] === null || obj[key] === undefined) {
			obj[key] = '';
		}
	}
	return obj;
};

const replaceEmptyStringsWithNull = (obj) => {
	for (const key in obj) {
		if (obj.hasOwnProperty(key) && obj[key] === '') {
			obj[key] = null;
		}
	}
	return obj;
};

const EmployeeEntryForm = () => {
	const globalCompany = useSelector((state) => state.globalCompany);
	const dispatch = useDispatch();
	const [showConfirmModal, setShowConfirmModal] = useState(false);
	const [employeeToDelete, setEmployeeToDelete] = useState(null);

	const dispatchAlert = (type) => {
		if (type === 'Success') {
			dispatch(
				alertActions.createAlert({
					message: 'Saved',
					type: type,
					duration: 3000,
				})
			);
		} else if (type === 'Error') {
			dispatch(
				alertActions.createAlert({
					message: 'Error Occurred',
					type: type,
					duration: 5000,
				})
			);
		}
	};

	const [
		getSingleEmployeePersonalDetail,
		{
			data: {
				user: PersonalDetailUser,
				company: PersonalDetailCompany,
				isActive: PersonalDetailIsActive,
				createdAt: PersonalDetailCreatedAt,
				...singleEmployeePersonalDetail
			} = {},
			isLoading: isLoadingSingleEmployeePersonalDetail,
		} = {},
		// lastPromiseInfo,
	] = useLazyGetSingleEmployeePersonalDetailQuery();

	const [
		getEmployeeFamilyNomineeDetail,
		{ data: employeeFamilyNomineeDetail, isLoading: isLoadingEmployeeFamilyNomineeDetail },
		// lastPromiseInfo,
	] = useLazyGetEmployeeFamilyNomineeDetailsQuery();

	const [
		getSingleEmployeeSalaryDetail,
		{
			data: { user: SalaryDetailUser, company: SalaryDetailCompany, ...singleEmployeeSalaryDetail } = {},
			isLoading: isLoadingSingleEmployeeSalaryDetail,
			isSuccess: isSingleEmployeeSalaryDetailSuccess,
		} = {},
		// lastPromiseInfo,
	] = useLazyGetSingleEmployeeSalaryDetailQuery();

	const [
		getEmployeeShifts,
		{ data: employeeShifts, isLoading: isLoadingemployeeShifts, isSuccess: isemployeeShiftsSuccess } = {},
		// lastPromiseInfo,
	] = useLazyGetEmployeeShiftsQuery();

	const [
		getSingleEmployeeProfessionalDetail,
		{
			data: {
				user: ProfessionalDetailUser,
				company: ProfessionalDetailCompany,
				...singleEmployeeProfessionalDetail
			} = {},
			isLoading: isLoadingSingleEmployeeProfessionalDetail,
			isSuccess: isSingleEmployeeProfessionalDetailSuccess,
		} = {},
		// lastPromiseInfo,
	] = useLazyGetSingleEmployeeProfessionalDetailQuery();

	const [
		getSingleEmployeePfEsiDetail,
		{
			data: { company: PfEsiDetailDetailCompany, ...singleEmployeePfEsiDetail } = {},
			isSuccess: getSingleEmployeePfEsiDetailIsSuccess,
			isLoading: isLoadingSingleEmployeePfEsiDetail,
		} = {},
		// lastPromiseInfo,
	] = useLazyGetSingleEmployeePfEsiDetailQuery();

	const {
		data: fetchedData,
		isLoading,
		isSuccess,
		isError,
		error,
		isFetching,
		refetch,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);
	// console.log(fetchedData);

	const [addEmployeePersonalDetail, { isLoading: isAddingEmployeePersonalDetail }] =
		useAddEmployeePersonalDetailMutation();

	const [addEmployeePfEsiDetail, { isLoading: isAddingEmployeePfEsiDetail }] = useAddEmployeePfEsiDetailMutation();
	const [addEmployeeProfessionalDetail, { isLoading: isAddingEmployeeProfessionalDetail }] =
		useAddEmployeeProfessionalDetailMutation();
	const [addEmployeeSalaryDetail, { isLoading: isAddingEmployeeSalaryDetail }] = useAddEmployeeSalaryDetailMutation();

	const [addEmployeeShifts, { isLoading: isAddingEmoloyeeShifts }] = useAddEmployeeShiftsMutation();

	const [addEmployeeFamilyNomineeDetail, { isLoading: isAddingEmployeeFamilyNomineeDetail }] =
		useAddEmployeeFamilyNomineeDetailMutation();

	const [
		updateEmployeePersonalDetail,
		{ isLoading: isUpdatingEmployeePersonalDetail, isSuccess: isUpdateEmployeePersonalDetailSuccess },
	] = useUpdateEmployeePersonalDetailMutation();

	const [
		updateEmployeeFamilyNomineeDetail,
		{ isLoading: isUpdatingEmployeeFamilyNomineeDetail, isSuccess: isUpdateEmployeeFamilyNomineeDetaiSuccess },
	] = useUpdateEmployeeFamilyNomineeDetailMutation();

	const [
		updateEmployeeSalaryDetail,
		{ isLoading: isUpdatingEmployeeSalaryDetail, isSuccess: isUpdateEmployeeSalaryDetailSuccess },
	] = useUpdateEmployeeSalaryDetailMutation();

	const [updateEmployeePfEsiDetail, { isLoading: isUpdatingEmployeePfEsiDetail }] =
		useUpdateEmployeePfEsiDetailMutation();

	const [updateEmployeeProfessionalDetail, { isLoading: isUpdatingEmployeeProfessionalDetail }] =
		useUpdateEmployeeProfessionalDetailMutation();
	const {
		data: fetchedEarningsHeads,
		isLoading: isLoadingEarningsHeads,
		isSuccess: EarningsHeadsSuccess,
	} = useGetEarningsHeadsQuery(globalCompany);
	const [addEmployeeSalaryEarning, { isLoading: isAddingEmployeeSalaryEarning }] =
		useAddEmployeeSalaryEarningMutation();

	const [deleteEmployeeFamilyNomineeDetail, { isLoading: isDeletingEmployeeFamilyNomineeDetail }] =
		useDeleteEmployeeFamilyNomineeDetailMutation();

	const [deleteEmployee, { isLoading: isDeletingEmployee }] = useDeleteEmployeeMutation();

	let earningHeadInitialValues = {};
	if (EarningsHeadsSuccess) {
		fetchedEarningsHeads.forEach((earningHead) => {
			earningHeadInitialValues[earningHead.name] = 0;
		});
	}

	const familyNomineeDetailInitailValues = {
		name: '',
		address: '',
		dob: '',
		relation: 'Father',
		residing: false,
		esiBenefit: false,
		pfBenefits: false,
		isEsiNominee: false,
		esiNomineeShare: '',
		isPfNominee: false,
		pfNomineeShare: '',
		isFaNominee: false,
		faNomineeShare: '',
		isGratuityNominee: false,
		gratuityNomineeShare: '',
	};

	const employeePfEsiDetailInitialValues = {
		pfAllow: false,
		pfNumber: '',
		pfLimitIgnoreEmployee: false,
		pfLimitIgnoreEmployeeValue: '',
		pfLimitIgnoreEmployer: false,
		pfLimitIgnoreEmployerValue: '',
		uanNumber: '',
		esiAllow: false,
		esiNumber: '',
		esiDispensary: '',
		esiOnOt: false,
		vpfAmount: 0,
	};

	const [addEmployeePopover, setAddEmployeePopover] = useState({
		addEmployeePersonalDetail: false,
		addEmployeeProfessionalDetail: false,
		addEmployeeSalaryDetail: false,
		addEmployeePfEsiDetail: false,
		addEmployeeFamilyNomineeDetail: false,
	});
	const [editEmployeePopover, setEditEmployeePopover] = useState({
		editEmployeePersonalDetail: false,
		editEmployeeProfessionalDetail: false,
		editEmployeeSalaryDetail: false,
		editEmployeePfEsiDetail: false,
		editEmployeeFamilyNomineeDetail: false,
	});
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const [updateEmployeeId, setUpdateEmployeeId] = useState(null);
	const [addedEmployeeId, setAddedEmployeeId] = useState(null);
	// const [msg, setMsg] = useState("");
	const [errorMessage, setErrorMessage] = useState('');

	const addEmployeePopoverHandler = (popoverName) => {
		setAddEmployeePopover((prevState) => {
			const updatedState = {};
			Object.keys(prevState).forEach((key) => {
				updatedState[key] = key === popoverName;
			});
			return updatedState;
		});
	};

	const currentDate = new Date();
	const formattedDate = currentDate.toISOString().split('T')[0];

	const editEmployeeProfessionalDetailInitialValues = {
		employeeProfessionalDetail: {
			dateOfJoining: formattedDate,
			dateOfConfirm: '',
			department: '',
			designation: '',
			category: '',
			salaryGrade: '',
			weeklyOff: 'sun',
			extraOff: 'no_off',
			// Previous Experience Row 1
			firstPreviousExperienceCompanyName: '',
			firstPreviousExperienceFromDate: '',
			firstPreviousExperienceToDate: '',
			firstPreviousExperienceDesignation: '',
			firstPreviousExperienceReasonForLeaving: '',
			firstPreviousExperienceSalary: '',
			// Previous Experience Row 2
			secondPreviousExperienceCompanyName: '',
			secondPreviousExperienceFromDate: '',
			secondPreviousExperienceToDate: '',
			secondPreviousExperienceDesignation: '',
			secondPreviousExperienceReasonForLeaving: '',
			secondPreviousExperienceSalary: '',
			// Previous Experience Row 3
			thirdPreviousExperienceCompanyName: '',
			thirdPreviousExperienceFromDate: '',
			thirdPreviousExperienceToDate: '',
			thirdPreviousExperienceDesignation: '',
			thirdPreviousExperienceReasonForLeaving: '',
			thirdPreviousExperienceSalary: '',
			// References Row 1
			firstReferenceName: '',
			firstReferenceAddress: '',
			firstReferenceRelation: '',
			firstReferencePhone: '',
			// References Row 2
			secondReferenceName: '',
			secondReferenceAddress: '',
			secondReferenceRelation: '',
			secondReferencePhone: '',
		},
		employeeShift: {
			shift: '',
		},
	};

	const editEmployeePopoverStateUpdater = (popoverName) => {
		setEditEmployeePopover((prevState) => {
			const updatedState = {};
			Object.keys(prevState).forEach((key) => {
				updatedState[key] = key === popoverName;
			});
			return updatedState;
		});
	};
	const editEmployeePopoverHandler = async ({ popoverName, id }) => {
		setUpdateEmployeeId(id);

		try {
			switch (popoverName) {
				case 'editEmployeePersonalDetail':
					const personalData = await getSingleEmployeePersonalDetail(
						{ id: id, company: globalCompany.id },
						true
					).unwrap();
					editEmployeePopoverStateUpdater(popoverName);
					break;

				case 'editEmployeeProfessionalDetail':
					// const employeeShiftsData = await getEmployeeShifts(
					// 	{
					// 		company: globalCompany.id,
					// 		employee: id,
					// 		year: new Date().getFullYear(),
					// 	},
					// 	true
					// );
					// const professionalData = await getSingleEmployeeProfessionalDetail(
					// 	{ id: id, company: globalCompany.id },
					// 	true
					// ).unwrap();
					// console.log(professionalData);

					await Promise.all([
						getEmployeeShifts(
							{
								company: globalCompany.id,
								employee: id,
								year: new Date().getFullYear(),
							},
							true
						).unwrap(),
						getSingleEmployeeProfessionalDetail({ id: id, company: globalCompany.id }, true).unwrap(),
					]);
					editEmployeePopoverStateUpdater(popoverName);

					break;

				case 'editEmployeeSalaryDetail':
					const currentDate = new Date();
					const currentYear = currentDate.getFullYear();
					await Promise.all([
						getSingleEmployeeProfessionalDetail({ id: id, company: globalCompany.id }, true).unwrap(),
						getSingleEmployeeSalaryDetail(
							{
								id: id,
								company: globalCompany.id,
							},
							true
						).unwrap(),
					]);
					editEmployeePopoverStateUpdater(popoverName);
					break;

				case 'editEmployeePfEsiDetail':
					const pfEsiData = await getSingleEmployeePfEsiDetail(
						{
							id: id,
							company: globalCompany.id,
						},
						true
					).unwrap();
					editEmployeePopoverStateUpdater(popoverName);
					break;

				case 'editEmployeeFamilyNomineeDetail':
					const [personalDetail, pfEsiDetail, nomineeData] = await Promise.all([
						getSingleEmployeePersonalDetail(
							{
								id: id,
								company: globalCompany.id,
							},
							true
						).unwrap(),
						getSingleEmployeePfEsiDetail(
							{
								id: id,
								company: globalCompany.id,
							},
							true
						).unwrap(),
						getEmployeeFamilyNomineeDetail(
							{
								id: id,
								company: globalCompany.id,
							},
							true
						).unwrap(),
					]);

					editEmployeePopoverStateUpdater(popoverName);
					break;

				default:
					console.log('Unknown popoverName:', popoverName);
			}
		} catch (err) {
			console.log(err);
			if (err.status !== 404) {
				// cancelButtonClicked(true);
				dispatchAlert('Error');
			}
		}
		editEmployeePopoverStateUpdater(popoverName);
	};

	const cancelButtonClicked = useCallback((isEditing) => {
		if (isEditing) {
			setUpdateEmployeeId(null);
			setEditEmployeePopover({
				editEmployeePersonalDetail: false,
				editEmployeeProfessionalDetail: false,
				editEmployeeSalaryDetail: false,
				editEmployeePfEsiDetail: false,
				editEmployeeFamilyNomineeDetail: false,
			});
		} else {
			setAddedEmployeeId(null);
			setAddEmployeePopover({
				addEmployeePersonalDetail: false,
				addEmployeeProfessionalDetail: false,
				addEmployeeSalaryDetail: false,
				addEmployeePfEsiDetail: false,
				addEmployeeFamilyNomineeDetail: false,
			});
		}
		setErrorMessage('');
	}, []);

	const addPersonalDetailButtonClicked = useCallback(async (values, formikBag) => {
		console.log(values);
		const formData = new FormData();
		for (const key in values) {
			if (values.hasOwnProperty(key)) {
				formData.append(key, values[key]);
			}
		}
		formData.append('company', globalCompany.id);

		try {
			const data = await addEmployeePersonalDetail({
				formData,
			}).unwrap();
			setErrorMessage('');
			setAddedEmployeeId(data.id);
			formikBag.resetForm();
			dispatchAlert('Success');
			addEmployeePopoverHandler('addEmployeeProfessionalDetail');
		} catch (err) {
			if (err.status === 400) {
				setErrorMessage(err.data.error);
			}
			dispatchAlert('Error');
		}
	}, []);

	const addProfessionalDetailButtonClicked = useCallback(
		async (values, formikBag) => {
			let employeeId = addedEmployeeId;
			if (updateEmployeeId !== null) {
				employeeId = updateEmployeeId;
			}

			try {
				const addEmployeeProfessionalDetailPromise = await addEmployeeProfessionalDetail({
					professionalDetail: replaceEmptyStringsWithNull({
						...values.employeeProfessionalDetail,
						employee: employeeId,
						company: globalCompany.id,
					}),
					...values.employeeShift,
				}).unwrap();
				setErrorMessage('');
				dispatchAlert('Success');

				if (updateEmployeeId === null) {
					try {
						const data = await getSingleEmployeeProfessionalDetail({
							id: employeeId,
							company: globalCompany.id,
						}).unwrap();
					} catch (err) {
						console.log(err);
					}
					formikBag.resetForm();
					addEmployeePopoverHandler('addEmployeeSalaryDetail');
				} else {
					editEmployeePopoverHandler({
						popoverName: 'editEmployeeProfessionalDetail',
						id: updateEmployeeId,
					});
				}
			} catch (err) {
				console.log(err);
				dispatchAlert('Error');
				if (err.status === 400) {
					console.log(err.data.error);
					setErrorMessage(err.data.error);
				}
			}
		},
		[addedEmployeeId, updateEmployeeId]
	);

	const updatePersonalDetailButtonClicked = async (values, formikBag) => {
		// console.log(formikBag);
		// console.log(values);
		console.log(singleEmployeePersonalDetail);
		const differences = getObjectDifferences(singleEmployeePersonalDetail, values);
		console.log(differences);
		if (Object.keys(differences).length !== 0) {
			console.log('in if fucking whatever');
			const formData = new FormData();
			for (const key in differences) {
				if (differences.hasOwnProperty(key)) {
					formData.append(key, differences[key]);
				}
			}
			formData.append('company', globalCompany.id);
			formData.append('id', values.id);
			// console.log(globalCompany.id)

			try {
				const data = await updateEmployeePersonalDetail({
					formData,
					id: values.id,
					globalCompany: globalCompany.id,
				}).unwrap();
				console.log(data);
				setErrorMessage('');
				dispatchAlert('Success');

				try {
					const data = await getSingleEmployeePersonalDetail(
						{
							id: updateEmployeeId,
							company: globalCompany.id,
						},
						true
					).unwrap();

					console.log(updateEmployeeId);
				} catch (err) {
					console.log(err);
				}
			} catch (err) {
				dispatchAlert('Error');
				console.log(err);
				if (err.status === 400) {
					console.log(err.data.error);
					setErrorMessage(err.data.error);
				} else {
					console.log(err);
				}
			}
		} else {
			setErrorMessage('');
		}
	};

	console.log(singleEmployeeProfessionalDetail);

	const updateProfessionalDetailButtonClicked = async (values, formikBag) => {
		const differences = getObjectDifferences(singleEmployeeProfessionalDetail, values.employeeProfessionalDetail);
		if (Object.keys(differences).length !== 0) {
			console.log('in if fucking whatever');

			try {
				const data = await updateEmployeeProfessionalDetail({
					...differences,
					employee: updateEmployeeId,
					globalCompany: globalCompany.id,
				}).unwrap();
				console.log(data);
				setErrorMessage('');
				dispatchAlert('Success');

				try {
					console.log('yo getting the professional detail here');
					const data = await getSingleEmployeeProfessionalDetail({
						id: updateEmployeeId,
						company: globalCompany.id,
					}).unwrap();
					console.log(data);
				} catch (err) {
					console.log(err);
				}
			} catch (err) {
				dispatchAlert('Error');
				if (err.status === 400) {
					console.log(err.data.error);
					setErrorMessage(err.data.error);
				} else {
					console.log(err);
				}
			}
		}
	};

	const addSalaryDetailButtonClicked = async (values, formikBag) => {
		console.log(values);

		console.log(updateEmployeeId);
		let employeeId = addedEmployeeId;
		if (updateEmployeeId !== null) {
			employeeId = updateEmployeeId;
		}

		const monthofJoining = isSingleEmployeeProfessionalDetailSuccess
			? parseInt(singleEmployeeProfessionalDetail.dateOfJoining.split('-')[1])
			: '';
		const from_date = `${values.year}-${monthofJoining}-01`;
		const to_date = `${values.year}-12-01`;

		const toSend = {
			employeeEarnings: [],
			company: globalCompany.id,
			employee: employeeId,
		};

		console.log(singleEmployeeProfessionalDetail.dateOfJoining);
		console.log(from_date);
		for (const key in values.earningsHead) {
			console.log(key);
			for (let i = 0; i < fetchedEarningsHeads.length; i++) {
				if (fetchedEarningsHeads[i].name === key) {
					let obj = {
						employee: employeeId,
						earnings_head: fetchedEarningsHeads[i].id,
						value: values.earningsHead[key],
						company: globalCompany.id,
						from_date,
						to_date,
					};
					toSend.employeeEarnings.push(obj);
					console.log(obj);
				}
			}
		}
		console.log(toSend);

		const salaryDetail = {
			...values.salaryDetail,
			company: globalCompany.id,
			employee: employeeId,
		};
		try {
			await Promise.all([
				addEmployeeSalaryEarning(toSend).unwrap(),
				addEmployeeSalaryDetail(salaryDetail).unwrap(),
			]);
			console.log('Both requests completed successfully');
			dispatchAlert('Success');
			setErrorMessage('');
			if (updateEmployeeId === null) {
				formikBag.resetForm();
				addEmployeePopoverHandler('addEmployeePfEsiDetail');
			} else {
				editEmployeePopoverHandler({
					popoverName: 'editEmployeeSalaryDetail',
					id: updateEmployeeId,
				});
			}
		} catch (err) {
			dispatchAlert('Error');
			console.log(err);
			if (err.status === 400) {
				console.log(err.data.overtimeRate);
				setErrorMessage(err.data);
			}
		}
	};

	const addPfEsiDetailButtonClicked = useCallback(
		async (values, formikBag) => {
			console.log(values);
			console.log('ksldjflksdjfd');

			let employeeId = addedEmployeeId;
			if (updateEmployeeId !== null) {
				employeeId = updateEmployeeId;
			}

			try {
				const data = await addEmployeePfEsiDetail({
					...values,
					pfLimitIgnoreEmployerValue:
						values.pfLimitIgnoreEmployerValue !== '' ? values.pfLimitIgnoreEmployerValue : null,
					pfLimitIgnoreEmployeeValue:
						values.pfLimitIgnoreEmployeeValue !== '' ? values.pfLimitIgnoreEmployeeValue : null,
					employee: employeeId,
					company: globalCompany.id,
				}).unwrap();
				console.log(data);
				dispatchAlert('Success');
				setErrorMessage('');

				if (updateEmployeeId === null) {
					formikBag.resetForm();
					try {
						const [personalDetailData, pfEsiDetailData] = await Promise.all([
							getSingleEmployeePersonalDetail(
								{
									id: employeeId,
									company: globalCompany.id,
								},
								true
							).unwrap(),
							getSingleEmployeePfEsiDetail(
								{
									id: employeeId,
									company: globalCompany.id,
								},
								true
							).unwrap(),
						]);
						addEmployeePopoverHandler('addEmployeeFamilyNomineeDetail');
					} catch (err) {
						// Handle errors if needed
						console.log('Error:', err);
					}
				}
			} catch (err) {
				console.log(err);
				dispatchAlert('Error');
				if (err.status === 400) {
					console.log(err.data.error);
					setErrorMessage(err.data.error);
				}
			}
		},
		[addedEmployeeId, updateEmployeeId]
	);

	const addFamilyNomineeDetailButtonClicked = useCallback(
		async (values, formikBag) => {
			console.log(values);
			let employeeId = addedEmployeeId;
			if (updateEmployeeId !== null) {
				employeeId = updateEmployeeId;
			}
			let toSend = JSON.parse(JSON.stringify(values));
			for (let i = 0; i < values.familyNomineeDetail.length; i++) {
				if (values.familyNomineeDetail[i].dob === '') {
					toSend.familyNomineeDetail[i].dob = null;
				}
				toSend.familyNomineeDetail[i].employee = employeeId;
				toSend.familyNomineeDetail[i].company = globalCompany.id;
			}
			console.log(toSend);
			try {
				const data = await addEmployeeFamilyNomineeDetail(toSend).unwrap();
				console.log(data);
				dispatchAlert('Success');
				setErrorMessage('');
			} catch (err) {
				console.log(err);
				dispatchAlert('Error');
				if (err.status === 400) {
					console.log(err.data);
					setErrorMessage(err.data);
				}
			}
		},
		[addedEmployeeId, updateEmployeeId]
	);

	const updatePfEsiDetailButtonClicked = async (values, formikBag) => {
		console.log(values);
		const differences = getObjectDifferences(singleEmployeePfEsiDetail, values);
		// console.log(differences);
		if (Object.keys(differences).length !== 0) {
			const differencesWithNulls = replaceEmptyStringsWithNull(differences);
			try {
				const data = await updateEmployeePfEsiDetail({
					...differencesWithNulls,
					employee: updateEmployeeId,
					globalCompany: globalCompany.id,
				}).unwrap();
				console.log(data);
				setErrorMessage('');
				dispatchAlert('Success');
				try {
					const data = await getSingleEmployeePfEsiDetail(
						{
							id: updateEmployeeId,
							company: globalCompany.id,
						},
						true
					).unwrap();
					console.log(data);

					console.log(updateEmployeeId);
				} catch (err) {
					console.log(err);
				}
			} catch (err) {
				dispatchAlert('Error');
				if (err.status === 400) {
					console.log(err.data.error);
					setErrorMessage(err.data.error);
				} else {
					console.log(err);
				}
			}
		}
	};

	const updateSalaryDetailButtonClicked = async (values, formikBag) => {
		console.log(values);
		console.log('askldjsakldjaslkdj');
		const salaryDetail = {
			...values.salaryDetail,
			company: globalCompany.id,
			employee: updateEmployeeId,
		};
		try {
			const data = await updateEmployeeSalaryDetail(salaryDetail).unwrap();

			console.log('Requests completed successfully');
			dispatchAlert('Success');

			try {
				const data = await getSingleEmployeeSalaryDetail(
					{
						id: updateEmployeeId,
						company: globalCompany.id,
					},
					true
				).unwrap();
				console.log(data);
			} catch (err) {
				console.log(err);
			}
		} catch (err) {
			dispatchAlert('Error');
			if (err.status === 400) {
				console.log(err.data.error);
				setErrorMessage(err.data.error);
			} else {
				console.log(err);
			}
		}
	};

	const updateFamilyNomineeDetailButtonClicked = async (values, formikBag) => {
		console.log(values);
		const arrayWithId = [];
		const arrayWithoutId = [];

		values.familyNomineeDetail.forEach((obj) => {
			if (obj.hasOwnProperty('id')) {
				arrayWithId.push({
					...obj,
					dob: obj.dob === '' ? null : obj.dob,
				});
			} else {
				arrayWithoutId.push({ ...obj });
			}
		});
		let toSend = { familyNomineeDetail: arrayWithoutId };
		for (let i = 0; i < arrayWithoutId.length; i++) {
			toSend.familyNomineeDetail[i].employee = updateEmployeeId;
			toSend.familyNomineeDetail[i].company = globalCompany.id;
			if (toSend.familyNomineeDetail[i].dob === '') {
				toSend.familyNomineeDetail[i].dob = null;
			}
		}
		console.log(toSend);

		let toSendUpdate = {
			globalCompany: globalCompany.id,
			employee: updateEmployeeId,
			familyNomineeDetail: arrayWithId,
		};

		const newArray = employeeFamilyNomineeDetail.filter(
			(obj) => obj.id && !arrayWithId.some((item) => item.id === obj.id)
		);
		console.log(newArray);

		try {
			let addEmployeePromise = null;
			if (toSend.familyNomineeDetail.length != 0) {
				const addEmployeePromise = addEmployeeFamilyNomineeDetail(toSend).unwrap();
			}
			const updateEmployeePromise = updateEmployeeFamilyNomineeDetail(toSendUpdate).unwrap();
			const deletePromises = newArray.map((obj) =>
				deleteEmployeeFamilyNomineeDetail({
					id: obj.id,
					company: globalCompany.id,
					employee: updateEmployeeId,
				})
			);

			const [addEmployeeData, updateEmployeeData, ...deleteResponses] = await Promise.all([
				addEmployeePromise,
				updateEmployeePromise,
				...deletePromises,
			]);

			console.log(addEmployeeData);
			console.log(updateEmployeeData);
			console.log(deleteResponses);

			setErrorMessage('');
			dispatchAlert('Success');
		} catch (err) {
			dispatchAlert('Error');
			console.log(err);
			if (err.status === 400) {
				console.log(err.data);
				setErrorMessage(err.data);
			} else {
				console.log(err);
			}
		}
	};

	const deleteButtonClicked = async (formikBag) => {
		console.log(employeeToDelete);
		try {
			const data = await deleteEmployee({ company: globalCompany.id, id: employeeToDelete }).unwrap();
			dispatch(
				alertActions.createAlert({
					message: `Deleted Successfully`,
					type: 'Success',
					duration: 3000,
				})
			);
		} catch (err) {
			console.log(err);
			dispatch(
				alertActions.createAlert({
					message: 'Error Occurred',
					type: 'Error',
					duration: 5000,
				})
			);
		}
		setShowConfirmModal(false);
		setEmployeeToDelete(null);
		// setShowConfirmModal(true);

		// deleteShift({ id: id, company: globalCompany.id });
	};

	console.log(
		isUpdateEmployeeFamilyNomineeDetaiSuccess,
		isUpdatingEmployeeSalaryDetail,
		isUpdateEmployeePersonalDetailSuccess
	);

	const columnHelper = createColumnHelper();

	const columns = [
		columnHelper.accessor('paycode', {
			header: () => 'Paycode',
			cell: (props) => props.renderValue(),
			//   footer: props => props.column.id,
		}),
		columnHelper.accessor('attendanceCardNo', {
			header: () => 'ACN',
			cell: (props) => props.renderValue(),
			//   footer: props => props.column.id,
		}),

		columnHelper.accessor('name', {
			header: () => 'Employee Name',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.accessor('dateOfJoining', {
			header: () => 'DOJ',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.accessor('resignationDate', {
			header: () => 'Resign Date',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.accessor('designation', {
			header: () => 'Designation',
			cell: (props) => props.renderValue(),
			//   footer: info => info.column.id,
		}),
		columnHelper.display({
			id: 'actions',
			header: () => 'Actions',
			cell: (props) => (
				<div className="flex justify-center gap-4">
					<div
						className="rounded bg-redAccent-500 p-1.5 hover:bg-redAccent-700 dark:bg-redAccent-700 dark:hover:bg-redAccent-500"
						onClick={() => {
							setEmployeeToDelete(props.row.original.id);
							setShowConfirmModal(true);
						}}
					>
						<FaRegTrashAlt className="h-4 text-white" />
					</div>
					<div
						className="rounded bg-teal-600 p-1.5 hover:bg-teal-700 dark:bg-teal-700 dark:hover:bg-teal-600"
						onClick={() => {
							editEmployeePopoverHandler({
								id: props.row.original.id,
								popoverName: 'editEmployeePersonalDetail',
							});
						}}
					>
						<FaPen className="h-4 text-white" />
					</div>
					{/* <div
                        className="p-1.5 dark:bg-blueAccent-600 rounded bg-blueAccent-600 dark:hover:bg-blueAccent-500 hover:bg-blueAccent-700"
                        onClick={() =>
                            viewEmployeePopoverHandler(props.row.original)
                        }
                    >
                        <FaEye className="h-4" />
                    </div> */}
				</div>
			),
		}),
	];

	const data = useMemo(() => (fetchedData ? [...fetchedData] : []), [fetchedData]);

	const table = useReactTable({
		data,
		columns,
		initialState: {
			sorting: [{ id: 'name', desc: false }],
		},
		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
		enableSortingRemoval: false,
	});

	useEffect(() => {
		// Add more for adding, editing and deleting later on
		setShowLoadingBar(
			isLoading ||
				isAddingEmployeePersonalDetail ||
				isAddingEmployeeProfessionalDetail ||
				isUpdatingEmployeePersonalDetail ||
				isUpdatingEmployeePfEsiDetail ||
				isUpdatingEmployeeProfessionalDetail ||
				isLoadingEarningsHeads ||
				isAddingEmployeeSalaryEarning ||
				isDeletingEmployeeFamilyNomineeDetail ||
				isLoadingSingleEmployeePersonalDetail ||
				isLoadingEmployeeFamilyNomineeDetail ||
				isLoadingSingleEmployeeSalaryDetail ||
				isLoadingSingleEmployeeProfessionalDetail ||
				isLoadingSingleEmployeePfEsiDetail ||
				isAddingEmployeePfEsiDetail ||
				isAddingEmployeeSalaryDetail ||
				isAddingEmployeeFamilyNomineeDetail ||
				isUpdatingEmployeeFamilyNomineeDetail ||
				isUpdatingEmployeeSalaryDetail
		);
	}, [
		isLoading,
		isAddingEmployeePersonalDetail,
		isAddingEmployeeProfessionalDetail,
		isUpdatingEmployeePersonalDetail,
		isUpdatingEmployeePfEsiDetail,
		isUpdatingEmployeeProfessionalDetail,
		isLoadingEarningsHeads,
		isAddingEmployeeSalaryEarning,
		isDeletingEmployeeFamilyNomineeDetail,
		isLoadingSingleEmployeePersonalDetail,
		isLoadingEmployeeFamilyNomineeDetail,
		isLoadingSingleEmployeeSalaryDetail,
		isLoadingSingleEmployeeProfessionalDetail,
		isLoadingSingleEmployeePfEsiDetail,
		isAddingEmployeePfEsiDetail,
		isAddingEmployeeSalaryDetail,
		isAddingEmployeeFamilyNomineeDetail,
		isUpdatingEmployeeFamilyNomineeDetail,
		isUpdatingEmployeeSalaryDetail,
	]);
	if (globalCompany.id == null) {
		return (
			<section className="flex flex-col items-center">
				<h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
					Please Select a Company First
				</h4>
			</section>
		);
	}
	if (isLoading) {
		return <div></div>;
	} else {
		return (
			<>
				<section className="mx-5 mt-2">
					<div className="flex flex-row flex-wrap place-content-between">
						<div className="mr-4">
							<h1 className="text-3xl font-medium">Employees</h1>
							<p className="my-2 text-sm">Add and manage employees here</p>
						</div>
						<button
							className="my-auto whitespace-nowrap rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
							onClick={() => addEmployeePopoverHandler('addEmployeePersonalDetail')}
						>
							Add Employee
						</button>
					</div>
					<div className="scrollbar mx-auto max-h-[80dvh] max-w-6xl overflow-y-auto rounded border border-black border-opacity-50 shadow-md lg:max-h-[84dvh]">
						<table className="w-full border-collapse text-center text-sm">
							<thead className="sticky top-0 bg-blueAccent-600 dark:bg-blueAccent-700">
								{table.getHeaderGroups().map((headerGroup) => (
									<tr key={headerGroup.id}>
										{headerGroup.headers.map((header) => (
											<th key={header.id} scope="col" className="px-4 py-4 font-medium">
												{header.isPlaceholder ? null : (
													<div className="">
														<div
															{...{
																className: header.column.getCanSort()
																	? 'cursor-pointer select-none flex flex-row justify-center'
																	: '',
																onClick: header.column.getToggleSortingHandler(),
															}}
														>
															{flexRender(
																header.column.columnDef.header,
																header.getContext()
															)}

															{/* {console.log(
                                                            header.column.getIsSorted()
                                                        )} */}
															{header.column.getCanSort() ? (
																<div className="relative pl-2">
																	<FaAngleUp
																		className={classNames(
																			header.column.getIsSorted() == 'asc'
																				? 'text-teal-700'
																				: '',
																			'absolute -translate-y-2 text-lg'
																		)}
																	/>
																	<FaAngleDown
																		className={classNames(
																			header.column.getIsSorted() == 'desc'
																				? 'text-teal-700'
																				: '',
																			'absolute translate-y-2 text-lg'
																		)}
																	/>
																</div>
															) : (
																''
															)}
														</div>
													</div>
												)}
											</th>
										))}
									</tr>
								))}
							</thead>
							<tbody className="max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50">
								{table.getRowModel().rows.map((row) => (
									<tr
										className={`hover:bg-zinc-200 dark:hover:bg-zinc-800 ${
											row.original.resignationDate ? 'text-redAccent-500' : ''
										}`}
										key={row.id}
									>
										{row.getVisibleCells().map((cell) => (
											<td className="px-4 py-4 font-normal" key={cell.id}>
												<div className="text-sm">
													<div className="font-medium">
														{flexRender(cell.column.columnDef.cell, cell.getContext())}
													</div>
												</div>
											</td>
										))}
									</tr>
								))}
							</tbody>
						</table>
					</div>

					{/* For Adding */}
					<ReactModal
						className="items-left scrollbar fixed inset-0 mx-2 my-auto flex h-fit max-h-[100dvh] w-fit flex-col gap-4 overflow-y-scroll rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-[1100px]"
						isOpen={
							addEmployeePopover.addEmployeePersonalDetail ||
							addEmployeePopover.addEmployeeProfessionalDetail ||
							addEmployeePopover.addEmployeeSalaryDetail ||
							addEmployeePopover.addEmployeePfEsiDetail ||
							addEmployeePopover.addEmployeeFamilyNomineeDetail
						}
						onRequestClose={() => cancelButtonClicked(false)}
						style={{
							overlay: {
								backgroundColor: 'rgba(0, 0, 0, 0.75)',
							},
						}}
					>
						<>
							<AddEmployeeNavigationBar
								addEmployeePopover={addEmployeePopover}
								addEmployeePopoverHandler={addEmployeePopoverHandler}
								editEmployeePopover={editEmployeePopover}
								editEmployeePopoverHandler={editEmployeePopoverHandler}
								isEditing={false}
								updateEmployeeId={updateEmployeeId}
								getSingleEmployeeProfessionalDetail={getSingleEmployeeProfessionalDetail}
								globalCompany={globalCompany.id}
							/>
							{addEmployeePopover.addEmployeePersonalDetail && (
								<Formik
									initialValues={{
										photo: '',

										// 1st column
										paycode: '',
										attendanceCardNo: '',
										name: '',
										fatherOrHusbandName: '',
										motherName: '',
										wifeName: '',
										dob: '',
										phoneNumber: '',

										// 2nd column
										alternatePhoneNumber: '',
										religion: '',
										email: '',
										handicapped: false,
										gender: '',
										maritalStatus: '',
										bloodGroup: '',
										nationality: 'Indian',

										// 3rd column
										panNumber: '',
										drivingLicence: '',
										passport: '',
										aadhaar: '',
										educationQualification: '',
										technicalQualification: '',
										localAddress: '',

										// 4th column
										localDistrict: '',
										localStateOrUnionTerritory: '',
										localPincode: '',
										permanentAddress: '',
										permanentDistrict: '',
										permanentStateOrUnionTerritory: '',
										permanentPincode: '',
									}}
									validationSchema={EmployeePersonalDetailSchema}
									onSubmit={addPersonalDetailButtonClicked}
									component={(props) => (
										<>
											<EmployeePersonalDetail
												{...props}
												errorMessage={errorMessage}
												setErrorMessage={setErrorMessage}
												cancelButtonClicked={cancelButtonClicked}
												isEditing={false}
											/>
										</>
									)}
								/>
							)}

							{addEmployeePopover.addEmployeeProfessionalDetail && (
								<Formik
									initialValues={editEmployeeProfessionalDetailInitialValues}
									validationSchema={EmployeeProfessionalDetailSchema(false)}
									onSubmit={addProfessionalDetailButtonClicked}
									component={(props) => (
										<>
											<EmployeeProfessionalDetail
												{...props}
												errorMessage={errorMessage}
												setErrorMessage={setErrorMessage}
												globalCompany={globalCompany}
												setShowLoadingBar={setShowLoadingBar}
												isEditing={false}
												cancelButtonClicked={cancelButtonClicked}
												addedEmployeeId={addedEmployeeId}
											/>
										</>
									)}
								/>
							)}

							{addEmployeePopover.addEmployeeSalaryDetail && (
								<Formik
									initialValues={{
										earningsHead: {
											...earningHeadInitialValues,
										},
										year: isSingleEmployeeProfessionalDetailSuccess
											? parseInt(singleEmployeeProfessionalDetail.dateOfJoining.split('-')[0])
											: '',
										salaryDetail: {
											overtimeType: 'no_overtime',
											overtimeRate: '',
											salaryMode: 'monthly',
											paymentMode: 'bank_transfer',
											bankName: '',
											accountNumber: '',
											ifcs: '',
											labourWellfareFund: false,
											lateDeduction: false,
											bonusAllow: false,
											bonusExg: false,
										},
									}}
									validationSchema={generateEmployeeSalaryDetailSchema(earningHeadInitialValues)}
									onSubmit={addSalaryDetailButtonClicked}
									component={(props) => (
										<>
											<EmployeeSalaryDetail
												{...props}
												errorMessage={errorMessage}
												setErrorMessage={setErrorMessage}
												// setAddEmployeePopover={
												//     setAddEmployeePopover
												// }
												globalCompany={globalCompany}
												setShowLoadingBar={setShowLoadingBar}
												isEditing={false}
												cancelButtonClicked={cancelButtonClicked}
												addedEmployeeId={addedEmployeeId}
												singleEmployeeProfessionalDetail={
													isSingleEmployeeProfessionalDetailSuccess
														? singleEmployeeProfessionalDetail
														: null
												}
												isSingleEmployeeProfessionalDetailSuccess={
													isSingleEmployeeProfessionalDetailSuccess
												}
											/>
										</>
									)}
								/>
							)}

							{addEmployeePopover.addEmployeePfEsiDetail && (
								<Formik
									initialValues={employeePfEsiDetailInitialValues}
									validationSchema={EmployeePfEsiDetailSchema}
									onSubmit={addPfEsiDetailButtonClicked}
									component={(props) => (
										<>
											<EmployeePfEsiDetail
												{...props}
												errorMessage={errorMessage}
												setErrorMessage={setErrorMessage}
												// setAddEmployeePopover={
												//     setAddEmployeePopover
												// }
												globalCompany={globalCompany}
												setShowLoadingBar={setShowLoadingBar}
												isEditing={false}
												cancelButtonClicked={cancelButtonClicked}
												addedEmployeeId={addedEmployeeId}
											/>
										</>
									)}
								/>
							)}
							{addEmployeePopover.addEmployeeFamilyNomineeDetail && (
								<Formik
									initialValues={{
										familyNomineeDetail: [
											{
												...familyNomineeDetailInitailValues,
												address:
													singleEmployeePersonalDetail.localAddress +
													' ' +
													singleEmployeePersonalDetail.localDistrict +
													' ' +
													singleEmployeePersonalDetail.localStateOrUnionTerritory,
											},
										],
									}}
									validationSchema={EmployeeFamilyNomineeDetailSchema}
									onSubmit={addFamilyNomineeDetailButtonClicked}
									component={(props) => (
										<>
											<EmployeeFamilyNomineeDetail
												{...props}
												errorMessage={errorMessage}
												setErrorMessage={setErrorMessage}
												globalCompany={globalCompany}
												setShowLoadingBar={setShowLoadingBar}
												isEditing={false}
												cancelButtonClicked={cancelButtonClicked}
												addedEmployeeId={addedEmployeeId}
												familyNomineeDetailInitailValues={{
													...familyNomineeDetailInitailValues,
													address:
														singleEmployeePersonalDetail.localAddress +
														' ' +
														singleEmployeePersonalDetail.localDistrict +
														' ' +
														singleEmployeePersonalDetail.localStateOrUnionTerritory,
												}}
												singleEmployeePfEsiDetail={
													getSingleEmployeePfEsiDetailIsSuccess
														? singleEmployeePfEsiDetail
														: null
												}
											/>
										</>
									)}
								/>
							)}
						</>
					</ReactModal>

					{/* For Editing */}
					<ReactModal
						className="items-left scrollbar fixed inset-0 mx-2 my-auto flex h-fit max-h-[100dvh] w-fit flex-col gap-4 overflow-y-scroll rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-[1100px]"
						isOpen={
							editEmployeePopover.editEmployeePersonalDetail ||
							editEmployeePopover.editEmployeeProfessionalDetail ||
							editEmployeePopover.editEmployeeSalaryDetail ||
							editEmployeePopover.editEmployeePfEsiDetail ||
							editEmployeePopover.editEmployeeFamilyNomineeDetail
						}
						onRequestClose={() => cancelButtonClicked(true)}
						style={{
							overlay: {
								backgroundColor: 'rgba(0, 0, 0, 0.75)',
							},
						}}
					>
						<>
							<AddEmployeeNavigationBar
								addEmployeePopover={addEmployeePopover}
								addEmployeePopoverHandler={addEmployeePopoverHandler}
								editEmployeePopover={editEmployeePopover}
								editEmployeePopoverHandler={editEmployeePopoverHandler}
								isEditing={true}
								updateEmployeeId={updateEmployeeId}
								getSingleEmployeeProfessionalDetail={getSingleEmployeeProfessionalDetail}
								globalCompany={globalCompany.id}
							/>
							{editEmployeePopover.editEmployeePersonalDetail && (
								<Formik
									initialValues={
										singleEmployeePersonalDetail !== undefined
											? checkNullUndefinedValues(singleEmployeePersonalDetail)
											: {}
									}
									validationSchema={EmployeePersonalDetailSchema}
									onSubmit={updatePersonalDetailButtonClicked}
									component={(props) => (
										<>
											<EmployeePersonalDetail
												{...props}
												errorMessage={errorMessage}
												setErrorMessage={setErrorMessage}
												cancelButtonClicked={cancelButtonClicked}
												isEditing={true}
											/>
										</>
									)}
								/>
							)}

							{editEmployeePopover.editEmployeeProfessionalDetail && (
								<Formik
									initialValues={
										isSingleEmployeeProfessionalDetailSuccess
											? {
													employeeProfessionalDetail: checkNullUndefinedValues(
														singleEmployeeProfessionalDetail
													),
											  }
											: editEmployeeProfessionalDetailInitialValues
									}
									validationSchema={
										isSingleEmployeeProfessionalDetailSuccess
											? EmployeeProfessionalDetailSchema(true)
											: EmployeeProfessionalDetailSchema(false)
									}
									onSubmit={
										isSingleEmployeeProfessionalDetailSuccess
											? updateProfessionalDetailButtonClicked
											: addProfessionalDetailButtonClicked
									}
									component={(props) => (
										<>
											<EmployeeProfessionalDetail
												{...props}
												errorMessage={errorMessage}
												setErrorMessage={setErrorMessage}
												// setEditEmployeePopover={
												//     setEditEmployeePopover
												// }
												globalCompany={globalCompany}
												setShowLoadingBar={setShowLoadingBar}
												isEditing={true}
												cancelButtonClicked={cancelButtonClicked}
												employeeShifts={employeeShifts}
											/>
										</>
									)}
								/>
							)}

							{editEmployeePopover.editEmployeeSalaryDetail && (
								<Formik
									initialValues={
										isSingleEmployeeSalaryDetailSuccess
											? {
													earningsHead: {
														//   ...editEarningHeadInitialValues,
													},
													year: isSingleEmployeeProfessionalDetailSuccess
														? parseInt(
																singleEmployeeProfessionalDetail.dateOfJoining.split(
																	'-'
																)[0]
														  )
														: null,
													salaryDetail: {
														...singleEmployeeSalaryDetail,
													},
											  }
											: {
													earningsHead: {
														...earningHeadInitialValues,
													},
													year: isSingleEmployeeProfessionalDetailSuccess
														? parseInt(
																singleEmployeeProfessionalDetail.dateOfJoining.split(
																	'-'
																)[0]
														  )
														: '',
													salaryDetail: {
														overtimeType: 'no_overtime',
														overtimeRate: '',
														salaryMode: 'monthly',
														paymentMode: 'bank_transfer',
														bankName: '',
														accountNumber: '',
														ifcs: '',
														labourWellfareFund: false,
														lateDeduction: false,
														bonusAllow: false,
														bonusExg: false,
													},
											  }
									}
									validationSchema={generateEmployeeSalaryDetailSchema(null)}
									onSubmit={
										isSingleEmployeeSalaryDetailSuccess
											? updateSalaryDetailButtonClicked
											: addSalaryDetailButtonClicked
									}
									component={(props) => (
										<>
											<EmployeeSalaryDetail
												{...props}
												errorMessage={errorMessage}
												setErrorMessage={setErrorMessage}
												globalCompany={globalCompany}
												setShowLoadingBar={setShowLoadingBar}
												isEditing={true}
												cancelButtonClicked={cancelButtonClicked}
												singleEmployeeProfessionalDetail={
													isSingleEmployeeProfessionalDetailSuccess
														? singleEmployeeProfessionalDetail
														: null
												}
												updateEmployeeId={updateEmployeeId}
												isSingleEmployeeSalaryDetailSuccess={
													isSingleEmployeeSalaryDetailSuccess
												}
												isSingleEmployeeProfessionalDetailSuccess={
													isSingleEmployeeProfessionalDetailSuccess
												}
											/>
										</>
									)}
								/>
							)}
							{editEmployeePopover.editEmployeePfEsiDetail && (
								<Formik
									initialValues={
										getSingleEmployeePfEsiDetailIsSuccess
											? checkNullUndefinedValues(singleEmployeePfEsiDetail)
											: {}
									}
									validationSchema={EmployeePfEsiDetailSchema}
									onSubmit={
										// Object.keys(singleEmployeePfEsiDetail).length !== 0
										getSingleEmployeePfEsiDetailIsSuccess
											? updatePfEsiDetailButtonClicked
											: addPfEsiDetailButtonClicked
									}
									component={(props) => (
										<>
											<EmployeePfEsiDetail
												{...props}
												errorMessage={errorMessage}
												setErrorMessage={setErrorMessage}
												globalCompany={globalCompany}
												setShowLoadingBar={setShowLoadingBar}
												isEditing={true}
												cancelButtonClicked={cancelButtonClicked}
											/>
										</>
									)}
								/>
							)}

							{editEmployeePopover.editEmployeeFamilyNomineeDetail && (
								<Formik
									initialValues={{
										familyNomineeDetail: employeeFamilyNomineeDetail.map((obj) => {
											const modifiedObj = {
												...obj,
											}; // Create a shallow copy of the object
											return checkNullUndefinedValues(modifiedObj); // Apply the modification function to the copied object
										}),
									}}
									validationSchema={EmployeeFamilyNomineeDetailSchema}
									onSubmit={
										getSingleEmployeePfEsiDetailIsSuccess
											? updateFamilyNomineeDetailButtonClicked
											: addFamilyNomineeDetailButtonClicked
									}
									component={(props) => (
										<>
											<EmployeeFamilyNomineeDetail
												{...props}
												errorMessage={errorMessage}
												setErrorMessage={setErrorMessage}
												globalCompany={globalCompany}
												setShowLoadingBar={setShowLoadingBar}
												isEditing={true}
												cancelButtonClicked={cancelButtonClicked}
												familyNomineeDetailInitailValues={{
													...familyNomineeDetailInitailValues,
													address:
														singleEmployeePersonalDetail.localAddress +
														' ' +
														singleEmployeePersonalDetail.localDistrict +
														' ' +
														singleEmployeePersonalDetail.localStateOrUnionTerritory,
												}}
												updateEmployeeId={updateEmployeeId}
												singleEmployeePfEsiDetail={
													getSingleEmployeePfEsiDetailIsSuccess
														? singleEmployeePfEsiDetail
														: null
												}
											/>
										</>
									)}
								/>
							)}
						</>
					</ReactModal>

					<ReactModal
						className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
						isOpen={showConfirmModal}
						onRequestClose={() => {
							setShowConfirmModal(false);
							setEmployeeToDelete(null);
						}}
						style={{
							overlay: {
								backgroundColor: 'rgba(0, 0, 0, 0.75)',
							},
						}}
					>
						<Formik
							initialValues={{ userInput: '' }}
							validationSchema={ConfirmationModalSchema}
							onSubmit={deleteButtonClicked}
							component={(props) => (
								<ConfirmationModal
									{...props}
									displayHeading={'Delete Employee (Keep in mind this is irreversible)'}
									setShowConfirmModal={setShowConfirmModal}
								/>
							)}
						/>
					</ReactModal>
				</section>
			</>
		);
	}
};

export default EmployeeEntryForm;
