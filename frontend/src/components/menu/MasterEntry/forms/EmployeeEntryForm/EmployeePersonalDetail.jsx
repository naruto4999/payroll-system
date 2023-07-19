import { useRef, useEffect, useState } from "react";
import { FaUserPlus } from "react-icons/fa6";
import { Field, ErrorMessage, FieldArray } from "formik";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const EmployeePersonalDetail = ({
    handleSubmit,
    handleChange,
    handleBlur,
    values,
    errors,
    // setAddEmployeePopover,
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
            setFieldValue("permanentAddress", values.localAddress);
            setFieldValue("permanentDistrict", values.localDistrict);
            setFieldValue(
                "permanentStateOrUnionTerritory",
                values.localStateOrUnionTerritory
            );
            setFieldValue("permanentPincode", values.localPincode);
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
                className="flex flex-col gap-2 justify-center"
                onSubmit={handleSubmit}
                // encType="multipart/form-data"
            >
                <section className="flex flex-col justify-center">
                    <label className="dark:border-slate-50 border-zinc-700 dark:hover:bg-blueAccent-700 hover:cursor-pointer border-2 h-24 w-24 mx-auto rounded-full flex flex-row justify-center items-center">
                        {values.photo === "" ||
                        values.photo === null ||
                        values.photo === undefined ? (
                            <FaUserPlus className="h-14 w-14" />
                        ) : (
                            <img
                                id="previewImage"
                                src={
                                    typeof values.photo == "string"
                                        ? values.photo
                                        : URL.createObjectURL(values.photo)
                                }
                                alt="Preview"
                                className="h-24 w-24 mx-auto rounded-full object-contain"
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
                                setFieldValue(
                                    "photo",
                                    e.currentTarget.files[0]
                                );

                                // Display the image preview
                                const reader = new FileReader();
                                reader.onload = (event) => {
                                    const previewImage =
                                        document.getElementById("previewImage");
                                    previewImage.src = event.target.result;
                                };
                                reader.readAsDataURL(e.currentTarget.files[0]);
                            }}
                        />
                    </label>
                    {errors.photo && (
                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold mx-auto">
                            {errors.photo}
                        </div>
                    )}
                </section>
                <section className="flex flex-row justify-center gap-4 flex-wrap lg:flex-nowrap">
                    <div className="w-full">
                        <label
                            htmlFor="paycode"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Paycode
                            <span className="dark:text-redAccent-600 text-redAccent-500 ">
                                *
                            </span>
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.paycode && touched.paycode
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
                                )}
                                type="number"
                                id="paycode"
                                name="paycode"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.paycode}
                            />
                            {errors.paycode && touched.paycode && (
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.paycode}
                                </div>
                            )}
                            {errorMessage && errorMessage.paycode && (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errorMessage.paycode}
                                </p>
                            )}
                        </div>

                        <label
                            htmlFor="attendanceCardNo"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Attendance Card Number
                            <span className="dark:text-redAccent-600 text-redAccent-500 ">
                                *
                            </span>
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.attendanceCardNo &&
                                        touched.attendanceCardNo
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
                                )}
                                type="number"
                                id="attendanceCardNo"
                                name="attendanceCardNo"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.attendanceCardNo}
                            />
                            {errors.attendanceCardNo &&
                                touched.attendanceCardNo && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.attendanceCardNo}
                                    </div>
                                )}
                            {errorMessage && errorMessage.attendanceCardNo && (
                                <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errorMessage.attendanceCardNo}
                                </p>
                            )}
                        </div>

                        <label
                            htmlFor="name"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Employee Name
                            <span className="dark:text-redAccent-600 text-redAccent-500 ">
                                *
                            </span>
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.name && touched.name
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
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
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.name}
                                </div>
                            )}
                        </div>

                        <label
                            htmlFor="fatherOrHusbandName"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Father's/Husband's name
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.fatherOrHusbandName &&
                                        touched.fatherOrHusbandName
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="text"
                                id="fatherOrHusbandName"
                                name="fatherOrHusbandName"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.fatherOrHusbandName}
                            />
                            {errors.fatherOrHusbandName &&
                                touched.fatherOrHusbandName && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.fatherOrHusbandName}
                                    </div>
                                )}
                        </div>

                        <label
                            htmlFor="motherName"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Mother's Name
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.motherName && touched.motherName
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="text"
                                id="motherName"
                                name="motherName"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.motherName}
                            />
                            {errors.motherName && touched.motherName && (
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.motherName}
                                </div>
                            )}
                        </div>

                        <label
                            htmlFor="wifeName"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Wife's Name
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.wifeName && touched.wifeName
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="text"
                                id="wifeName"
                                name="wifeName"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.wifeName}
                            />
                            {errors.wifeName && touched.wifeName && (
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.wifeName}
                                </div>
                            )}
                        </div>

                        <label
                            htmlFor="dob"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Date of Birth
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.dob && touched.dob
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="date"
                                id="dob"
                                name="dob"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.dob}
                            />
                            {errors.dob && touched.dob && (
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.dob}
                                </div>
                            )}
                        </div>

                        <label
                            htmlFor="phoneNumber"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Phone Number
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.phoneNumber && touched.phoneNumber
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
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
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.phoneNumber}
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="w-full">
                        <label
                            htmlFor="alternatePhoneNumber"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Alternate Phone Number
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.alternatePhoneNumber &&
                                        touched.alternatePhoneNumber
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
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
                            {errors.alternatePhoneNumber &&
                                touched.alternatePhoneNumber && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.alternatePhoneNumber}
                                    </div>
                                )}
                        </div>

                        <label
                            htmlFor="religion"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Religion
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.religion && touched.religion
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
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
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.religion}
                                </div>
                            )}
                        </div>

                        <label
                            htmlFor="email"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Email
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.email && touched.email
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
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
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.email}
                                </div>
                            )}
                        </div>

                        <br />
                        <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block my-2">
                            Handicapped:
                            <Field
                                type="checkbox"
                                name="handicapped"
                                className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                            />
                        </label>

                        {/* <br /> */}

                        <label
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                            htmlFor="gender"
                        >
                            Gender
                        </label>
                        <select
                            className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
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
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                            htmlFor="maritalStatus"
                        >
                            Marital Status
                        </label>
                        <select
                            className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
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
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                            htmlFor="bloodGroup"
                        >
                            Blood Group
                        </label>
                        <select
                            className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
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
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Pan Number
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.panNumber && touched.panNumber
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
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
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.panNumber}
                                </div>
                            )}
                        </div>

                        <label
                            htmlFor="drivingLicence"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Driving Licence
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.drivingLicence &&
                                        touched.drivingLicence
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="text"
                                maxLength={16}
                                id="drivingLicence"
                                name="drivingLicence"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.drivingLicence}
                            />
                            {errors.drivingLicence &&
                                touched.drivingLicence && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.drivingLicence}
                                    </div>
                                )}
                        </div>

                        <label
                            htmlFor="passport"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Passport
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.passport && touched.passport
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
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
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.passport}
                                </div>
                            )}
                        </div>

                        <label
                            htmlFor="aadhaar"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Aadhaar
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.aadhaar && touched.aadhaar
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
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
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.aadhaar}
                                </div>
                            )}
                        </div>
                        <label
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                            htmlFor="educationQualification"
                        >
                            Educational Qualification
                        </label>
                        <select
                            className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 my-1 block"
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
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Technical Qualification
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.technicalQualification &&
                                        touched.technicalQualification
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="text"
                                id="technicalQualification"
                                maxLength={50}
                                name="technicalQualification"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.technicalQualification}
                            />
                            {errors.technicalQualification &&
                                touched.technicalQualification && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.technicalQualification}
                                    </div>
                                )}
                        </div>

                        <label
                            htmlFor="localAddress"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Local Address
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.localAddress && touched.localAddress
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
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
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.localAddress}
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="w-full">
                        <label
                            htmlFor="localDistrict"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Local District
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.localDistrict &&
                                        touched.localDistrict
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
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
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.localDistrict}
                                </div>
                            )}
                        </div>

                        <label
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                            htmlFor="localStateOrUnionTerritory"
                        >
                            Local State or UT
                        </label>
                        <select
                            className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
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
                            <option value="AN">
                                Andaman and Nicobar Islands
                            </option>
                            <option value="CH">Chandigarh</option>
                            <option value="DN">Dadra and Nagar Haveli</option>
                            <option value="DD">Daman and Diu</option>
                            <option value="DL">Delhi</option>
                            <option value="LD">Lakshadweep</option>
                            <option value="PY">Puducherry</option>
                        </select>

                        <label
                            htmlFor="localPincode"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Local Pin Code
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.localPincode && touched.localPincode
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
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
                                <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                    {errors.localPincode}
                                </div>
                            )}
                        </div>

                        <br />
                        <label className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block my-2">
                            Permanent and local same?
                            <input
                                type="checkbox"
                                id="sameAsPermanent"
                                name="sameAsPermanent"
                                checked={sameAsLocal}
                                onChange={handleSameAsLocal}
                                className="rounded w-4 h-4 accent-teal-600 mx-4 translate-y-0.5"
                            />
                        </label>
                        <label
                            htmlFor="permanentAddress"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Permanent Address
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.permanentAddress &&
                                        touched.permanentAddress
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="text"
                                id="permanentAddress"
                                name="permanentAddress"
                                disabled={sameAsLocal}
                                maxLength={250}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={
                                    sameAsLocal
                                        ? values.localAddress
                                        : values.permanentAddress
                                }
                            />
                            {errors.permanentAddress &&
                                touched.permanentAddress && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.permanentAddress}
                                    </div>
                                )}
                        </div>

                        <label
                            htmlFor="permanentDistrict"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Permanent District
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.permanentDistrict &&
                                        touched.permanentDistrict
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                )}
                                type="text"
                                id="permanentDistrict"
                                name="permanentDistrict"
                                disabled={sameAsLocal}
                                value={
                                    sameAsLocal
                                        ? values.localDistrict
                                        : values.permanentDistrict
                                }
                                maxLength={30}
                                onChange={handleChange}
                                onBlur={handleBlur}
                            />
                            {errors.permanentDistrict &&
                                touched.permanentDistrict && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.permanentDistrict}
                                    </div>
                                )}
                        </div>

                        <label
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                            htmlFor="permanentStateOrUnionTerritory"
                        >
                            Permanent State or UT
                        </label>
                        <select
                            className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                            name="permanentStateOrUnionTerritory"
                            id="permanentStateOrUnionTerritory"
                            onChange={handleChange}
                            value={
                                sameAsLocal
                                    ? values.localStateOrUnionTerritory
                                    : values.permanentStateOrUnionTerritory
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
                            <option value="AN">
                                Andaman and Nicobar Islands
                            </option>
                            <option value="CH">Chandigarh</option>
                            <option value="DN">Dadra and Nagar Haveli</option>
                            <option value="DD">Daman and Diu</option>
                            <option value="DL">Delhi</option>
                            <option value="LD">Lakshadweep</option>
                            <option value="PY">Puducherry</option>
                        </select>

                        <label
                            htmlFor="permanentPincode"
                            className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                        >
                            Permanent Pin Code
                        </label>
                        <div className="relative">
                            <input
                                className={classNames(
                                    errors.permanentPincode &&
                                        touched.permanentPincode
                                        ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                        : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                    "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full custom-number-input"
                                )}
                                type="number"
                                id="permanentPincode"
                                name="permanentPincode"
                                maxLength={6}
                                onChange={handleChange}
                                onBlur={handleBlur}
                                disabled={sameAsLocal}
                                value={
                                    sameAsLocal
                                        ? values.localPincode
                                        : values.permanentPincode
                                }
                            />
                            {errors.permanentPincode &&
                                touched.permanentPincode && (
                                    <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                        {errors.permanentPincode}
                                    </div>
                                )}
                        </div>
                    </div>
                </section>
                {errorMessage && errorMessage.error && (
                    <p className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                        {errorMessage.error}
                    </p>
                )}

                <section className="flex flex-row gap-4 mt-4 mb-2">
                    <button
                        className={classNames(
                            isValid
                                ? "dark:hover:bg-teal-600  hover:bg-teal-600"
                                : "opacity-40",
                            "dark:bg-teal-700 rounded w-20 p-2 text-base font-medium bg-teal-500"
                        )}
                        type="submit"
                        disabled={!isValid }
                        onClick={handleSubmit}
                    >
                        {isEditing ? "Update" : "Add"}
                    </button>
                    <button
                        type="button"
                        className="bg-zinc-400 hover:bg-zinc-500 dark:bg-zinc-600 rounded w-20 p-2 text-base font-medium dark:hover:bg-zinc-700"
                        onClick={() => {
                            cancelButtonClicked(isEditing);
                            setErrorMessage("");
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
