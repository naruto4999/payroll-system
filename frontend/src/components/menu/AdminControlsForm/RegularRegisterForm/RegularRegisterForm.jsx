import React, { useState, useEffect } from 'react';
// import authSlice from "./store/slices/auth";
import { useDispatch } from 'react-redux';
import { Link } from 'react-router-dom';
import {
	useGetRegularsQuery,
	useRegularRegisterMutation,
	useDeleteRegularMutation,
	useRegularUpdateMutation,
} from '../../../authentication/api/employeeRegisterApiSlice';
import { Formik } from 'formik';
import { subUserSchema } from './SubUserSchema';
import { useOutletContext } from 'react-router-dom';
import { FaCircleNotch } from 'react-icons/fa';
import ReactModal from 'react-modal';
import PasswordReset from './PasswordReset';
import passwordSchema from './PasswordResetSchema';
import { subUserUpdateSchema } from './SubUserSchema';
import { alertActions } from '../../../authentication/store/slices/alertSlice';

ReactModal.setAppElement('#root');

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const RegularRegisterForm = () => {
	const dispatch = useDispatch();

	const { data: fetchedData, isLoading, isSuccess, isError, error, isFetching } = useGetRegularsQuery();
	// console.log(fetchedData);
	const [
		regularRegister,
		{ isLoading: isRegisteringRegular, isError: errorRegisteringRegular, isSuccess: successRegisteringRegular },
	] = useRegularRegisterMutation(); //use the isLoading later
	const [
		regularUpdate,
		{ isLoading: isUpdatingRegular, isError: errorUpdatingRegular, isSuccess: successUpdatingRegular },
	] = useRegularUpdateMutation();
	const [msg, setMsg] = useState('');
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();
	const [deleteRegular, { isLoading: isDeletingRegular }] = useDeleteRegularMutation();
	const [showPasswordResetModal, setShowPasswordResetModal] = useState(false);
	const [isDisabled, setIsDisabled] = useState(true);

	// console.log(fetchedData);

	// const deleteButtonClicked = async (resetForm) => {
	// 	setMsg('');
	// 	console.log(resetForm);
	// 	resetForm({
	// 		values: {
	// 			email: '',
	// 			password: '',
	// 			passConfirm: '',
	// 			username: '',
	// 			phoneNo: '',
	// 		},
	// 	});
	// 	try {
	// 		const data = await deleteRegular().unwrap();
	// 		console.log(data);
	// 	} catch (err) {
	// 		console.log(err);
	// 	}
	// };
	const changePasswordSubmitHandler = async (values, formikBag) => {
		console.log(values);
		try {
			const data = await regularUpdate({
				...values,
			}).unwrap();
			dispatch(
				alertActions.createAlert({
					message: 'Saved',
					type: 'Success',
					duration: 3000,
				})
			);
		} catch (err) {
			console.log(err);
			let message = 'Error Occurred';
			dispatch(
				alertActions.createAlert({
					message: message,
					type: 'Error',
					duration: 5000,
				})
			);
		}
	};
	const updateButtonClicked = async (values, formikBag) => {
		console.log(values);
		let toSend = { ...values };
		delete toSend.password;
		try {
			const data = await regularUpdate(toSend).unwrap();
			setIsDisabled(true);
			dispatch(
				alertActions.createAlert({
					message: 'Saved',
					type: 'Success',
					duration: 3000,
				})
			);
		} catch (err) {
			console.log(err);
			let message = 'Error Occurred';
			dispatch(
				alertActions.createAlert({
					message: message,
					type: 'Error',
					duration: 5000,
				})
			);
		}
	};

	const createButtonClicked = async (values, formikBag) => {
		// e.preventDefault();
		console.log(values);
		try {
			const data = await regularRegister({
				email: values.email,
				password: values.password,
				username: values.username,
				phoneNo: values.phoneNo,
			}).unwrap();
			console.log(data);
			setMsg(data.detail);
		} catch (err) {
			console.log(err);
			setMsg(err.data.detail);
		}
	};

	useEffect(() => {
		setShowLoadingBar(isRegisteringRegular || isLoading || isDeletingRegular);
	}, [isRegisteringRegular, isLoading, isDeletingRegular]);

	if (isLoading) {
		return (
			<div className="fixed inset-0 z-50 mx-auto my-auto flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium">
				<FaCircleNotch className="mr-2 animate-spin text-white" />
				Processing...
			</div>
		);
	} else {
		return (
			<section className="mx-5 mt-2">
				{/* Formik Implementation */}
				<Formik
					initialValues={
						isSuccess
							? {
									...fetchedData,
									password: 'demo@123',
									passConfirm: '',
							  }
							: {
									email: '',
									password: '',
									passConfirm: '',
									username: '',
									phoneNo: '',
							  }
					}
					validationSchema={isSuccess ? subUserUpdateSchema : subUserSchema}
					onSubmit={isSuccess ? updateButtonClicked : createButtonClicked}
				>
					{({ handleSubmit, handleChange, handleBlur, values, errors, touched, isValid, resetForm }) => {
						console.log(values);
						return (
							<form id="sub-user-form" className="mt-2" onSubmit={handleSubmit}>
								<div className="flex flex-row flex-wrap place-content-between">
									{console.log(errors)}
									<div className="mr-4">
										<h1 className="text-3xl font-medium">Sub User</h1>
										<p className="my-2 text-sm">
											{isSuccess
												? 'Sub user already exists, below are the details.'
												: 'Create Sub User Here'}
										</p>
									</div>
									{isSuccess && (
										<div className="">
											<button
												className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-700 dark:hover:bg-zinc-600"
												type="button"
												onClick={() => {
													setIsDisabled(false);
												}}
											>
												Edit
											</button>
										</div>
									)}
								</div>
								<div className="flex w-full flex-col gap-2">
									<div>
										<label
											htmlFor="username"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											Username
										</label>
										<input
											type="text"
											name="username"
											id="username"
											className={classNames(
												isSuccess && isDisabled
													? 'text-slate-500 dark:text-slate-400'
													: 'text-slate-800 dark:text-slate-200',
												'w-full rounded bg-slate-200 p-2 dark:bg-zinc-800  lg:w-1/3'
											)}
											onChange={handleChange}
											onBlur={handleBlur}
											value={values.username}
											disabled={isSuccess && isDisabled ? true : false}
										/>
										{errors.username && touched.username && (
											<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
												{errors.username}
											</div>
										)}
									</div>
									<div>
										<label
											htmlFor="email"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											Email
										</label>
										<input
											type="text"
											name="email"
											id="email"
											className={classNames(
												isSuccess && isDisabled
													? 'text-slate-500 dark:text-slate-400'
													: 'text-slate-800 dark:text-slate-200',
												'w-full rounded bg-slate-200 p-2 dark:bg-zinc-800  lg:w-1/3'
											)}
											onChange={handleChange}
											onBlur={handleBlur}
											value={values.email}
											disabled={isSuccess && isDisabled ? true : false}
										/>
										{errors.email && touched.email && (
											<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
												{errors.email}
											</div>
										)}
									</div>
									<div>
										<label
											htmlFor="phoneNo"
											className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
										>
											Phone Number
										</label>
										<input
											type="tel"
											name="phoneNo"
											id="phoneNo"
											className={classNames(
												isSuccess && isDisabled
													? 'text-slate-500 dark:text-slate-400'
													: 'text-slate-800 dark:text-slate-200',
												'w-full rounded bg-slate-200 p-2 dark:bg-zinc-800  lg:w-1/3'
											)}
											maxLength="10"
											size="10"
											onChange={handleChange}
											onBlur={handleBlur}
											value={values.phoneNo}
											disabled={isSuccess && isDisabled ? true : false}
										/>
										{errors.phoneNo && touched.phoneNo && (
											<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
												{errors.phoneNo}
											</div>
										)}
									</div>
									{!isSuccess && (
										<div>
											<label
												htmlFor="password"
												className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
											>
												Password
											</label>
											<input
												type="password"
												name="password"
												id="password"
												className="w-full rounded bg-slate-200 p-2 text-slate-500 dark:bg-zinc-800 dark:text-slate-400 lg:w-fit"
												onChange={handleChange}
												onBlur={handleBlur}
												value={values.name}
											/>
											{errors.password && touched.password && (
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													{errors.password}
												</div>
											)}
										</div>
									)}
									{!isSuccess && (
										<div>
											<label
												htmlFor="passConfirm"
												className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
											>
												Confirm Password
											</label>
											<input
												type="password"
												name="passConfirm"
												id="passConfirm"
												className="w-full rounded bg-slate-200 p-2 text-slate-500 dark:bg-zinc-800 dark:text-slate-400 lg:w-fit"
												onChange={handleChange}
												onBlur={handleBlur}
												value={values.name}
											/>
											{errors.passConfirm && touched.passConfirm && (
												<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
													{errors.passConfirm}
												</div>
											)}
										</div>
									)}
									{errorRegisteringRegular || successRegisteringRegular ? (
										<p
											className={classNames(
												errorRegisteringRegular
													? 'text-red-500 dark:text-red-700'
													: 'text-green-500 dark:text-green-700',
												'mt-1 text-sm font-bold'
											)}
										>
											{msg}
										</p>
									) : (
										''
									)}
									<div>
										<button
											form="sub-user-form"
											className="mr-4 w-20 rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
											onClick={handleSubmit}
											type="submit"
											// type="button"
										>
											{isSuccess ? 'Save' : 'Create'}
										</button>
									</div>
									{/* {!isSuccess && (
									<div>
										<button
											className="mt-4 whitespace-nowrap rounded bg-teal-500 py-2 px-6 text-base font-medium hover:bg-teal-600 dark:bg-teal-700 dark:hover:bg-teal-600"
											type="submit"
										>
											Create
										</button>
									</div>
								)} */}
									{/* {isSuccess && (
									<div>
										<button
											className="mt-4 whitespace-nowrap rounded bg-redAccent-500 py-2 px-6 text-base font-medium hover:bg-redAccent-700 dark:bg-redAccent-700 dark:hover:bg-redAccent-500"
											type="button"
											onClick={() => {
												deleteButtonClicked(resetForm);
											}}
										>
											Delete
										</button>
									</div>
								)} */}
								</div>
							</form>
						);
					}}
				</Formik>
				{isSuccess && (
					<button
						className="mt-4 whitespace-nowrap rounded bg-blueAccent-500 py-2 px-6 text-base font-medium hover:bg-blueAccent-600 dark:bg-blueAccent-700 dark:hover:bg-blueAccent-600"
						onClick={() => {
							setShowPasswordResetModal(true);
						}}
					>
						Change Password
					</button>
				)}
				<ReactModal
					className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
					isOpen={showPasswordResetModal}
					onRequestClose={() => {
						setShowPasswordResetModal(false);
					}}
					style={{
						overlay: {
							backgroundColor: 'rgba(0, 0, 0, 0.75)',
						},
					}}
				>
					<Formik
						initialValues={{ password: '', confirmPassword: '' }}
						validationSchema={passwordSchema}
						onSubmit={changePasswordSubmitHandler}
						component={(props) => (
							<PasswordReset
								{...props}
								// displayHeading={
								// 	confirmType == 'resign'
								// 		? 'Resign Employee (All the attendances for this employee after the resignation date will be deleted)'
								// 		: 'Unresign Employee'
								// }
								setShowPasswordResetModal={setShowPasswordResetModal}
								// fullAndFinalEmployeeId={fullAndFinalEmployeeId}
								// globalCompany={globalCompany}
								// generateButtonClicked={generateButtonClicked}
							/>
						)}
					/>
				</ReactModal>
			</section>
		);
	}
};
export default RegularRegisterForm;
