import { useRef, useEffect, useState } from 'react';
import { FaUserPlus } from 'react-icons/fa6';
import { Field, ErrorMessage, FieldArray } from 'formik';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const EmployeePersonalDetail = ({
	handleSubmit,
	handleChange,
	handleBlur,
	values,
	errors,
	cancelButtonClicked,
	isValid,
	touched,
	errorMessage,
	setErrorMessage,
	setFieldValue,
	isEditing,
	dirty,
}) => {
	// const inputRef = useRef(null);
	// console.log(errors);
	const [sameAsLocal, setSameAsLocal] = useState(false);
	// useEffect(() => {
	//     inputRef.current.focus();
	// }, []);

	useEffect(() => {
		if (sameAsLocal) {
			setFieldValue('permanentAddress', values.localAddress);
			setFieldValue('permanentDistrict', values.localDistrict);
			setFieldValue('permanentStateOrUnionTerritory', values.localStateOrUnionTerritory);
			setFieldValue('permanentPincode', values.localPincode);
		}
	}, [
		sameAsLocal,
		values.localAddress,
		values.localDistrict,
		values.localStateOrUnionTerritory,
		values.localPincode,
	]);

	console.log(values);

	const handleSameAsLocal = (event) => {
		setSameAsLocal(event.target.checked);
	};

	return (
		<div className="text-gray-900 dark:text-slate-100">
			<form
				action=""
				className="flex flex-col justify-center gap-2"
				onSubmit={handleSubmit}
				// encType="multipart/form-data"
			>
				<section className="flex flex-col justify-center">
					<label className="mx-auto flex h-24 w-24 flex-row items-center justify-center rounded-full border-2 border-zinc-700 hover:cursor-pointer dark:border-slate-50 dark:hover:bg-blueAccent-700">
						{values.photo === '' || values.photo === null || values.photo === undefined ? (
							<FaUserPlus className="h-14 w-14" />
						) : (
							<img
								id="previewImage"
								src={
									typeof values.photo == 'string'
										? `${import.meta.env.VITE_MEDIA_URL}${values.photo}`
										: URL.createObjectURL(values.photo)
								}
								alt="Preview"
								className="mx-auto h-24 w-24 rounded-full object-contain"
							/>
						)}
						<input
							className="hidden"
							type="file"
							name="photo"
							id="photo"
							accept="image/*"
							onBlur={handleBlur}
							onChange={(e) => {
								setFieldValue('photo', e.currentTarget.files[0]);

								// Display the image preview
								const reader = new FileReader();
								reader.onload = (event) => {
									const previewImage = document.getElementById('previewImage');
									previewImage.src = event.target.result;
								};
								reader.readAsDataURL(e.currentTarget.files[0]);
							}}
						/>
					</label>
					{errors.photo && (
						<div className="mx-auto mt-1 text-xs font-bold text-red-500 dark:text-red-700">
							{errors.photo}
						</div>
					)}
				</section>
				<section className="flex flex-row flex-wrap justify-center gap-4 lg:flex-nowrap">
					<div className="w-full">
						<label
							htmlFor="paycode"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Paycode
							<span className="text-redAccent-500 dark:text-redAccent-600 ">*</span>
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.paycode && touched.paycode
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								id="paycode"
								name="paycode"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.paycode}
							/>
							{errors.paycode && touched.paycode && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.paycode}
								</div>
							)}
							{errorMessage && errorMessage.paycode && (
								<p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errorMessage.paycode}
								</p>
							)}
						</div>

						<label
							htmlFor="attendanceCardNo"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Attendance Card Number
							<span className="text-redAccent-500 dark:text-redAccent-600 ">*</span>
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.attendanceCardNo && touched.attendanceCardNo
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="attendanceCardNo"
								name="attendanceCardNo"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.attendanceCardNo}
							/>
							{errors.attendanceCardNo && touched.attendanceCardNo && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.attendanceCardNo}
								</div>
							)}
							{errorMessage && errorMessage.attendanceCardNo && (
								<p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errorMessage.attendanceCardNo}
								</p>
							)}
						</div>

						<label
							htmlFor="name"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Employee Name
							<span className="text-redAccent-500 dark:text-redAccent-600 ">*</span>
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.name && touched.name
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								maxLength={100}
								id="name"
								name="name"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.name}
							/>
							{errors.name && touched.name && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.name}
								</div>
							)}
						</div>

						<label
							htmlFor="fatherOrHusbandName"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Father's/Husband's name
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.fatherOrHusbandName && touched.fatherOrHusbandName
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								id="fatherOrHusbandName"
								name="fatherOrHusbandName"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.fatherOrHusbandName}
							/>
							{errors.fatherOrHusbandName && touched.fatherOrHusbandName && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.fatherOrHusbandName}
								</div>
							)}
						</div>

						<label
							htmlFor="motherName"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Mother's Name
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.motherName && touched.motherName
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								id="motherName"
								name="motherName"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.motherName}
							/>
							{errors.motherName && touched.motherName && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.motherName}
								</div>
							)}
						</div>

						<label
							htmlFor="wifeName"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Wife's Name
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.wifeName && touched.wifeName
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								id="wifeName"
								name="wifeName"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.wifeName}
							/>
							{errors.wifeName && touched.wifeName && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.wifeName}
								</div>
							)}
						</div>

						<label
							htmlFor="dob"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Date of Birth
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.dob && touched.dob
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="date"
								id="dob"
								name="dob"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.dob}
							/>
							{errors.dob && touched.dob && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.dob}
								</div>
							)}
						</div>

						<label
							htmlFor="phoneNumber"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Phone Number
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.phoneNumber && touched.phoneNumber
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="tel"
								pattern="[0-9]{10}"
								maxLength="10"
								id="phoneNumber"
								name="phoneNumber"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.phoneNumber}
							/>
							{errors.phoneNumber && touched.phoneNumber && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.phoneNumber}
								</div>
							)}
						</div>
					</div>

					<div className="w-full">
						<label
							htmlFor="alternatePhoneNumber"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Alternate Phone Number
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.alternatePhoneNumber && touched.alternatePhoneNumber
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="tel"
								pattern="[0-9]{10}"
								maxLength="10"
								id="alternatePhoneNumber"
								name="alternatePhoneNumber"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.alternatePhoneNumber}
							/>
							{errors.alternatePhoneNumber && touched.alternatePhoneNumber && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.alternatePhoneNumber}
								</div>
							)}
						</div>

						<label
							htmlFor="religion"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Religion
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.religion && touched.religion
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								maxLength={50}
								id="religion"
								name="religion"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.religion}
							/>
							{errors.religion && touched.religion && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.religion}
								</div>
							)}
						</div>

						<label
							htmlFor="email"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Email
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.email && touched.email
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="email"
								maxLength={150}
								id="email"
								name="email"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.email}
							/>
							{errors.email && touched.email && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.email}
								</div>
							)}
						</div>

						<br />
						<label className="my-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
							Handicapped:
							<Field
								type="checkbox"
								name="handicapped"
								className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
							/>
						</label>

						{/* <br /> */}

						<label
							className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							htmlFor="gender"
						>
							Gender
						</label>
						<select
							className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
							name="gender"
							id="gender"
							onChange={handleChange}
							value={values.gender}
						>
							<option value="">-- Select an option --</option>
							<option value="M">Male</option>
							<option value="F">Female</option>
							<option value="O">Others</option>
						</select>

						<label
							className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							htmlFor="maritalStatus"
						>
							Marital Status
						</label>
						<select
							className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
							name="maritalStatus"
							id="maritalStatus"
							onChange={handleChange}
						>
							<option value="">-- Select an option --</option>
							<option value="S">Single</option>
							<option value="M">Married</option>
							<option value="D">Divorced</option>
							<option value="W">Widowed</option>
						</select>

						<label
							className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							htmlFor="bloodGroup"
						>
							Blood Group
						</label>
						<select
							className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
							name="bloodGroup"
							id="bloodGroup"
							onChange={handleChange}
							value={values.bloodGroup}
						>
							<option value="">-- Select an option --</option>
							<option value="A+">A+</option>
							<option value="A-">A-</option>
							<option value="B+">B+</option>
							<option value="B-">B-</option>
							<option value="AB+">AB+</option>
							<option value="AB-">AB-</option>
							<option value="O+">O+</option>
							<option value="O-">O-</option>
						</select>
					</div>

					<div className="w-full">
						<label
							htmlFor="panNumber"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Pan Number
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.panNumber && touched.panNumber
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								maxLength={10}
								id="panNumber"
								name="panNumber"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.panNumber}
							/>
							{errors.panNumber && touched.panNumber && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.panNumber}
								</div>
							)}
						</div>

						<label
							htmlFor="drivingLicence"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Driving Licence
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.drivingLicence && touched.drivingLicence
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								maxLength={16}
								id="drivingLicence"
								name="drivingLicence"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.drivingLicence}
							/>
							{errors.drivingLicence && touched.drivingLicence && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.drivingLicence}
								</div>
							)}
						</div>

						<label
							htmlFor="passport"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Passport
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.passport && touched.passport
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								maxLength={8}
								id="passport"
								name="passport"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.passport}
							/>
							{errors.passport && touched.passport && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.passport}
								</div>
							)}
						</div>

						<label
							htmlFor="aadhaar"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Aadhaar
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.aadhaar && touched.aadhaar
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								maxLength={12}
								id="aadhaar"
								name="aadhaar"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.aadhaar}
							/>
							{errors.aadhaar && touched.aadhaar && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.aadhaar}
								</div>
							)}
						</div>
						<label
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							htmlFor="educationQualification"
						>
							Educational Qualification
						</label>
						<select
							className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
							name="educationQualification"
							id="educationQualification"
							onChange={handleChange}
							value={values.educationQualification}
						>
							<option value="">-- Select an option --</option>
							<option value="0">No Qualification</option>
							<option value="1">1st class</option>
							<option value="2">2nd class</option>
							<option value="3">3rd class</option>
							<option value="4">4th class</option>
							<option value="5">5th class</option>
							<option value="6">6th class</option>
							<option value="7">7th class</option>
							<option value="8">8th class</option>
							<option value="9">9th class</option>
							<option value="10">10th class</option>
							<option value="11">11th class</option>
							<option value="12">12th class</option>
							<option value="G">Graduate</option>
							<option value="PG">Post Graduate</option>
						</select>

						<label
							htmlFor="technicalQualification"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Technical Qualification
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.technicalQualification && touched.technicalQualification
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								id="technicalQualification"
								maxLength={50}
								name="technicalQualification"
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.technicalQualification}
							/>
							{errors.technicalQualification && touched.technicalQualification && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.technicalQualification}
								</div>
							)}
						</div>

						<label
							htmlFor="localAddress"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Local Address
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.localAddress && touched.localAddress
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								id="localAddress"
								name="localAddress"
								maxLength={250}
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.localAddress}
							/>
							{errors.localAddress && touched.localAddress && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.localAddress}
								</div>
							)}
						</div>
					</div>

					<div className="w-full">
						<label
							htmlFor="localDistrict"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Local District
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.localDistrict && touched.localDistrict
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								id="localDistrict"
								name="localDistrict"
								maxLength={30}
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.localDistrict}
							/>
							{errors.localDistrict && touched.localDistrict && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.localDistrict}
								</div>
							)}
						</div>

						<label
							className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							htmlFor="localStateOrUnionTerritory"
						>
							Local State or UT
						</label>
						<select
							className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
							name="localStateOrUnionTerritory"
							id="localStateOrUnionTerritory"
							onChange={handleChange}
							value={values.localStateOrUnionTerritory}
						>
							<option value="">-- Select an option --</option>
							<option value="AP">Andhra Pradesh</option>
							<option value="AR">Arunachal Pradesh</option>
							<option value="AS">Assam</option>
							<option value="BR">Bihar</option>
							<option value="CT">Chhattisgarh</option>
							<option value="GA">Goa</option>
							<option value="GJ">Gujarat</option>
							<option value="HR">Haryana</option>
							<option value="HP">Himachal Pradesh</option>
							<option value="JH">Jharkhand</option>
							<option value="KA">Karnataka</option>
							<option value="KL">Kerala</option>
							<option value="MP">Madhya Pradesh</option>
							<option value="MH">Maharashtra</option>
							<option value="MN">Manipur</option>
							<option value="ML">Meghalaya</option>
							<option value="MZ">Mizoram</option>
							<option value="NL">Nagaland</option>
							<option value="OR">Odisha</option>
							<option value="PB">Punjab</option>
							<option value="RJ">Rajasthan</option>
							<option value="SK">Sikkim</option>
							<option value="TN">Tamil Nadu</option>
							<option value="TG">Telangana</option>
							<option value="TR">Tripura</option>
							<option value="UP">Uttar Pradesh</option>
							<option value="UK">Uttarakhand</option>
							<option value="WB">West Bengal</option>
							<option value="JK">Jammu and Kashmir</option>
							<option value="AN">Andaman and Nicobar Islands</option>
							<option value="CH">Chandigarh</option>
							<option value="DN">Dadra and Nagar Haveli</option>
							<option value="DD">Daman and Diu</option>
							<option value="DL">Delhi</option>
							<option value="LD">Lakshadweep</option>
							<option value="PY">Puducherry</option>
						</select>

						<label
							htmlFor="localPincode"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Local Pin Code
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.localPincode && touched.localPincode
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								id="localPincode"
								name="localPincode"
								maxLength={6}
								onChange={handleChange}
								onBlur={handleBlur}
								value={values.localPincode}
							/>
							{errors.localPincode && touched.localPincode && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.localPincode}
								</div>
							)}
						</div>

						<br />
						<label className="my-2 block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
							Permanent and local same?
							<input
								type="checkbox"
								id="sameAsPermanent"
								name="sameAsPermanent"
								checked={sameAsLocal}
								onChange={handleSameAsLocal}
								className="mx-4 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
							/>
						</label>
						<label
							htmlFor="permanentAddress"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Permanent Address
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.permanentAddress && touched.permanentAddress
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								id="permanentAddress"
								name="permanentAddress"
								disabled={sameAsLocal}
								maxLength={250}
								onChange={handleChange}
								onBlur={handleBlur}
								value={sameAsLocal ? values.localAddress : values.permanentAddress}
							/>
							{errors.permanentAddress && touched.permanentAddress && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.permanentAddress}
								</div>
							)}
						</div>

						<label
							htmlFor="permanentDistrict"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Permanent District
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.permanentDistrict && touched.permanentDistrict
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'w-full rounded border-2 bg-zinc-50  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="text"
								id="permanentDistrict"
								name="permanentDistrict"
								disabled={sameAsLocal}
								value={sameAsLocal ? values.localDistrict : values.permanentDistrict}
								maxLength={30}
								onChange={handleChange}
								onBlur={handleBlur}
							/>
							{errors.permanentDistrict && touched.permanentDistrict && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.permanentDistrict}
								</div>
							)}
						</div>

						<label
							className="block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							htmlFor="permanentStateOrUnionTerritory"
						>
							Permanent State or UT
						</label>
						<select
							className="my-1 block rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
							name="permanentStateOrUnionTerritory"
							id="permanentStateOrUnionTerritory"
							onChange={handleChange}
							value={
								sameAsLocal ? values.localStateOrUnionTerritory : values.permanentStateOrUnionTerritory
							}
							disabled={sameAsLocal}
						>
							<option value="">-- Select an option --</option>
							<option value="AP">Andhra Pradesh</option>
							<option value="AR">Arunachal Pradesh</option>
							<option value="AS">Assam</option>
							<option value="BR">Bihar</option>
							<option value="CT">Chhattisgarh</option>
							<option value="GA">Goa</option>
							<option value="GJ">Gujarat</option>
							<option value="HR">Haryana</option>
							<option value="HP">Himachal Pradesh</option>
							<option value="JH">Jharkhand</option>
							<option value="KA">Karnataka</option>
							<option value="KL">Kerala</option>
							<option value="MP">Madhya Pradesh</option>
							<option value="MH">Maharashtra</option>
							<option value="MN">Manipur</option>
							<option value="ML">Meghalaya</option>
							<option value="MZ">Mizoram</option>
							<option value="NL">Nagaland</option>
							<option value="OR">Odisha</option>
							<option value="PB">Punjab</option>
							<option value="RJ">Rajasthan</option>
							<option value="SK">Sikkim</option>
							<option value="TN">Tamil Nadu</option>
							<option value="TG">Telangana</option>
							<option value="TR">Tripura</option>
							<option value="UP">Uttar Pradesh</option>
							<option value="UK">Uttarakhand</option>
							<option value="WB">West Bengal</option>
							<option value="JK">Jammu and Kashmir</option>
							<option value="AN">Andaman and Nicobar Islands</option>
							<option value="CH">Chandigarh</option>
							<option value="DN">Dadra and Nagar Haveli</option>
							<option value="DD">Daman and Diu</option>
							<option value="DL">Delhi</option>
							<option value="LD">Lakshadweep</option>
							<option value="PY">Puducherry</option>
						</select>

						<label
							htmlFor="permanentPincode"
							className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
						>
							Permanent Pin Code
						</label>
						<div className="relative">
							<input
								className={classNames(
									errors.permanentPincode && touched.permanentPincode
										? 'border-red-500 border-opacity-100 dark:border-red-700 dark:border-opacity-75'
										: 'border-gray-800 border-opacity-25 dark:border-slate-100 dark:border-opacity-25',
									'custom-number-input w-full rounded border-2  bg-zinc-50   bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:bg-zinc-700 dark:focus:border-opacity-75'
								)}
								type="number"
								id="permanentPincode"
								name="permanentPincode"
								maxLength={6}
								onChange={handleChange}
								onBlur={handleBlur}
								disabled={sameAsLocal}
								value={sameAsLocal ? values.localPincode : values.permanentPincode}
							/>
							{errors.permanentPincode && touched.permanentPincode && (
								<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
									{errors.permanentPincode}
								</div>
							)}
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
};
export default EmployeePersonalDetail;
