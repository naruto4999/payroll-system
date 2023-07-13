import { useRef, useEffect, useState } from "react";
import { FaUserPlus } from "react-icons/fa6";
import { useGetDepartmentsQuery } from "../../../../authentication/api/departmentEntryApiSlice";
import { useGetDesignationsQuery } from "../../../../authentication/api/designationEntryApiSlice";
import { useGetCategoriesQuery } from "../../../../authentication/api/categoryEntryApiSlice";
import { useGetSalaryGradesQuery } from "../../../../authentication/api/salaryGradeEntryApiSlice";
import { useGetShiftsQuery } from "../../../../authentication/api/shiftEntryApiSlice";
import { FaCircleNotch } from "react-icons/fa6";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};
const timeFormat = (time) => {
    const timeParts = time.split(":");
    const formattedTime = `${timeParts[0]}:${timeParts[1]}`;
    return formattedTime;
};
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
}) => {
    const { data: fetchedDepartments, isLoading: isLoadingDepartments } =
        useGetDepartmentsQuery(globalCompany);

    const { data: fetchedDesignations, isLoading: isLoadingDesignations } =
        useGetDesignationsQuery(globalCompany);

    const { data: fetchedCategories, isLoading: isLoadingCategories } =
        useGetCategoriesQuery(globalCompany);

    const { data: fetchedSalaryGrades, isLoading: isLoadingSalaryGrade } =
        useGetSalaryGradesQuery(globalCompany);

    const { data: fetchedShifts, isLoading: isLoadingShifts } =
        useGetShiftsQuery(globalCompany);
    // const inputRef = useRef(null);
    console.log(dirty);
    // console.log(errors);
    const [sameAsLocal, setSameAsLocal] = useState(false);
    // useEffect(() => {
    //     inputRef.current.focus();
    // }, []);

    useEffect(() => {
        setShowLoadingBar(
            isLoadingDepartments ||
                isLoadingDesignations ||
                isLoadingCategories ||
                isLoadingSalaryGrade
        );
    }, [
        isLoadingDepartments,
        isLoadingDesignations,
        isLoadingCategories,
        isLoadingSalaryGrade,
    ]);

    useEffect(() => {
        if (values.dateOfJoining !== "") {
            let selectedDate = new Date(values.dateOfJoining);
            selectedDate.setMonth(selectedDate.getMonth() + 6);
            selectedDate.setDate(selectedDate.getDate() - 1);
            setFieldValue(
                "dateOfConfirm",
                selectedDate.toISOString().slice(0, 10)
            );
        }
    }, [values.dateOfJoining]);
    console.log(addedEmployeeId);

    useEffect(() => {}, []);

    if (
        isLoadingDepartments ||
        isLoadingDesignations ||
        isLoadingCategories ||
        isLoadingSalaryGrade
    ) {
        return (
            <div>
                <div className="bg-blueAccent-600 dark:bg-blueAccent-700 w-fit h-fit rounded flex p-2 items-center mx-auto">
                    <FaCircleNotch className="animate-spin text-gray-900 dark:text-slate-100 mr-2" />
                    <p className="text-gray-900 dark:text-slate-100">
                        Processing...
                    </p>
                </div>
            </div>
        );
    } else if (!addedEmployeeId && !isEditing) {
        return (
            <div className="mt-1 text-xl dark:text-redAccent-600 text-redAccent-500 font-bold mx-auto">
                Please add Personal Details First
            </div>
        );
    } else {
        return (
            <div className="text-gray-900 dark:text-slate-100">
                {/* <h1 className="font-medium text-2xl mb-2">Add Employee</h1> */}
                <form
                    action=""
                    className="flex flex-col gap-2 justify-center"
                    onSubmit={handleSubmit}
                >
                    <section className="flex flex-row gap-10 flex-wrap lg:flex-nowrap justify-center">
                        <div className="w-fit">
                            <label
                                htmlFor="dateOfJoining"
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                            >
                                Date of Joining
                            </label>
                            <div className="relative">
                                <input
                                    className={classNames(
                                        errors.dateOfJoining &&
                                            touched.dateOfJoining
                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                    )}
                                    type="date"
                                    id="dateOfJoining"
                                    name="dateOfJoining"
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    value={values.dateOfJoining}
                                />
                                {errors.dateOfJoining &&
                                    touched.dateOfJoining && (
                                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                            {errors.dateOfJoining}
                                        </div>
                                    )}
                            </div>
                            <label
                                htmlFor="dateOfConfirm"
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                            >
                                Date of Confirm
                            </label>
                            <div className="relative">
                                <input
                                    className={classNames(
                                        errors.dateOfConfirm &&
                                            touched.dateOfConfirm
                                            ? "border-red-500 dark:border-red-700 border-opacity-100 dark:border-opacity-75"
                                            : "border-gray-800 dark:border-slate-100 border-opacity-25 dark:border-opacity-25",
                                        "rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-800  border-2   p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                                    )}
                                    type="date"
                                    id="dateOfConfirm"
                                    name="dateOfConfirm"
                                    onChange={handleChange}
                                    onBlur={handleBlur}
                                    value={values.dateOfConfirm}
                                    disabled={true}
                                />
                                {errors.dateOfConfirm &&
                                    touched.dateOfConfirm && (
                                        <div className="mt-1 text-xs dark:text-red-700 text-red-500 font-bold">
                                            {errors.dateOfConfirm}
                                        </div>
                                    )}
                            </div>

                            <label
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                                htmlFor="department"
                            >
                                department
                            </label>
                            <select
                                className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                                name="department"
                                id="department"
                                onChange={handleChange}
                                value={values.department}
                            >
                                <option value="">-- Select an option --</option>
                                {fetchedDepartments?.map((department) => (
                                    <option
                                        key={department.id}
                                        value={department.id}
                                    >
                                        {department.name}
                                    </option>
                                ))}
                            </select>

                            <label
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                                htmlFor="designation"
                            >
                                Designation
                            </label>
                            <select
                                className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                                name="designation"
                                id="designation"
                                onChange={handleChange}
                                value={values.designation}
                            >
                                <option value="">-- Select an option --</option>
                                {fetchedDesignations?.map((designation) => (
                                    <option
                                        key={designation.id}
                                        value={designation.id}
                                    >
                                        {designation.name}
                                    </option>
                                ))}
                            </select>

                            <label
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                                htmlFor="category"
                            >
                                Category
                            </label>
                            <select
                                className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                                name="category"
                                id="category"
                                onChange={handleChange}
                                value={values.category}
                            >
                                <option value="">-- Select an option --</option>
                                {fetchedCategories?.map((category) => (
                                    <option
                                        key={category.id}
                                        value={category.id}
                                    >
                                        {category.name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="w-fit">
                            <label
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                                htmlFor="salaryGrade"
                            >
                                Salary Grade
                            </label>
                            <select
                                className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                                name="salaryGrade"
                                id="salaryGrade"
                                onChange={handleChange}
                                value={values.salaryGrade}
                            >
                                <option value="">-- Select an option --</option>
                                {fetchedSalaryGrades?.map((salaryGrade) => (
                                    <option
                                        key={salaryGrade.id}
                                        value={salaryGrade.id}
                                    >
                                        {salaryGrade.name}
                                    </option>
                                ))}
                            </select>

                            <label
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                                htmlFor="shift"
                            >
                                Shift
                            </label>
                            <select
                                className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                                name="shift"
                                id="shift"
                                onChange={handleChange}
                                value={values.shift}
                            >
                                <option value="">-- Select an option --</option>
                                {fetchedShifts?.map((shift) => (
                                    <option key={shift.id} value={shift.id}>
                                        {shift.name}
                                        {` [${timeFormat(
                                            shift.beginningTime
                                        )} - ${timeFormat(shift.endTime)}]`}
                                    </option>
                                ))}
                            </select>

                            <label
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                                htmlFor="weeklyOff"
                            >
                                Weekly Off
                            </label>
                            <select
                                className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                                name="weeklyOff"
                                id="weeklyOff"
                                onChange={handleChange}
                                value={values.weeklyOff}
                            >
                                <option value="no_off">No Off</option>
                                <option value="mon">Monday</option>
                                <option value="tue">Tuesday</option>
                                <option value="wed">Wednesday</option>
                                <option value="thu">Thursday</option>
                                <option value="fri">Friday</option>
                                <option value="sat">Saturday</option>
                                <option value="sun">Sunday</option>
                            </select>

                            <label
                                className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm block"
                                htmlFor="extraOff"
                            >
                                Extra Off
                            </label>
                            <select
                                className="p-1 rounded-md bg-opacity-50 bg-zinc-50 dark:bg-zinc-700 block my-1"
                                name="extraOff"
                                id="extraOff"
                                onChange={handleChange}
                                value={values.extraOff}
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
                            </select>
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
                                isValid && dirty
                                    ? "dark:hover:bg-teal-600  hover:bg-teal-600"
                                    : "opacity-40",
                                "dark:bg-teal-700 rounded w-20 p-2 text-base font-medium bg-teal-500"
                            )}
                            type="submit"
                            disabled={!isValid || !dirty}
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
    }
};
export default EmployeeProfessionalDetail;
