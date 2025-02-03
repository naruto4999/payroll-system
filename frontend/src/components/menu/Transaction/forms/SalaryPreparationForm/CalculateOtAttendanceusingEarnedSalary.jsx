import React, { useMemo, useEffect, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Field, ErrorMessage, FieldArray, Formik } from 'formik';

import {
    useGetAllEmployeeMonthlyAttendanceDetailsQuery,
    useGetAllEmployeeSalaryEarningsQuery,
    useEmployeeBulkSalaryPreparedMutation,
    useGetAllEmployeePfEsiDetailsQuery,
    useCalculateOtAttendanceUsingTotalEarnedMutation,
    useGetEmployeePreparedSalaryQuery,
} from '../../../../authentication/api/salaryPreparationApiSlice';
import { useGetAllEmployeeSalaryDetailQuery } from '../../../../authentication/api/timeUpdationApiSlice';
import BigNumber from 'bignumber.js';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import DeductionsForCalculateOtAttendanceUsingEarnedSalary from './DeductionsForCalculateOtAttendanceUsingEarnedSalary';
import NetSalary from './NetSalary';
import ReactModal from 'react-modal';
import InsertTotalEarnedModal from './InsertTotalEarnedModal';
import LoadingSpinner from '../../../../UI/LoadingSpinner';

const classNames = (...classes) => {
    return classes.filter(Boolean).join(' ');
};

const CalculateOtAttendanceusingEarnedSalary = ({
    updateEmployeeId,
    globalCompany,
    earliestMonthAndYear,
    setSelectedDate,
    selectedDate,
}) => {
    const auth = useSelector((state) => state.auth);
    const months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
    ];
    const dispatch = useDispatch();
    const [showInsertTotalEarnedModal, setShowInsertTotalEarnedModal] = useState(false);
    const initialFormValues = useMemo(
        () => ({
            year: selectedDate.year,
            month: selectedDate.month,
            employeeSalaryPrepared: {
                incentiveAmount: 0,
                pfDeducted: 0,
                esiDeducted: 0,
                vpfDeducted: 0,
                advanceDeducted: 0,
                tdsDeducted: 0,
                labourWelfareFundDeducted: 0,
                othersDeducted: 0,
                netOtMinutesMonthly: 0,
                netOtAmountMonthly: 0,
                paymentMode: '',
            },
            earnedAmount: [],
        }),
        [selectedDate.year, selectedDate.month]
    );

    const [formValues, setFormValues] = useState(initialFormValues);

    const {
        data: employeePreparedSalary,
        isLoading: isLoadingEmployeePreparedSalary,
        isSuccess: isEmployeePreparedSalarySuccess,
        isFetching: isFetchingEmployeePreparedSalary,
    } = useGetEmployeePreparedSalaryQuery(
        {
            company_id: globalCompany?.id,
            employee_id: updateEmployeeId,
            year: selectedDate?.year,
            month: selectedDate?.month,
        },
        {
            skip:
                globalCompany === null ||
                globalCompany === '' ||
                updateEmployeeId == null ||
                updateEmployeeId == undefined ||
                selectedDate.month == null ||
                selectedDate.month == undefined ||
                selectedDate.year == null ||
                selectedDate.year == undefined,
        }
    );

    const isDateWithinRange = (fromDate, toDate) => {
        const dateSelected = new Date(Date.UTC(selectedDate.year, selectedDate.month - 1, 1));
        const fromDateObj = new Date(fromDate);
        const toDateObj = new Date(toDate);
        return dateSelected >= fromDateObj && dateSelected <= toDateObj;
    };
    const {
        data: allEmployeeSalaryEarnings,
        isLoading: isLoadingAllEmployeeSalaryEarnings,
        isSuccess: isAllEmployeeSalaryEarningsSuccess,
        isFetching: isFetchingAllEmployeeSalaryEarnings,
    } = useGetAllEmployeeSalaryEarningsQuery(
        {
            company: globalCompany?.id,
            year: selectedDate?.year,
        },
        {
            skip: globalCompany === null || globalCompany === '' || selectedDate?.year == undefined,
        }
    );

    const {
        data: allEmployeeMonthlyAttendanceDetails,
        isLoading: isLoadingAllEmployeeMonthlyAttendanceDetails,
        isSuccess: isAllEmployeeMonthlyAttendanceDetailsSuccess,
        isFetching: isFetchingAllEmployeeMonthlyAttendanceDetails,
    } = useGetAllEmployeeMonthlyAttendanceDetailsQuery(
        {
            company: globalCompany?.id,
            year: selectedDate?.year,
        },
        {
            skip: globalCompany === null || globalCompany === '' || selectedDate?.year == undefined,
        }
    );

    const {
        data: allEmployeeSalaryDetails,
        isLoading: isLoadingAllEmployeeSalaryDetails,
        isSuccess: isAllEmployeeSalaryDetailsSuccess,
        isFetching: isFetchingAllEmployeeSalaryDetails,
    } = useGetAllEmployeeSalaryDetailQuery(
        {
            company: globalCompany?.id,
        },
        {
            skip: globalCompany === null || globalCompany === '',
        }
    );

    const {
        data: allEmployeePfEsiDetails,
        isLoading: isLoadingAllEmployeePfEsiDetails,
        isSuccess: isAllEmployeePfEsiDetailsSuccess,
        isFetching: isFetchingAllEmployeePfEsiDetails,
    } = useGetAllEmployeePfEsiDetailsQuery(
        {
            company: globalCompany?.id,
        },
        {
            skip: globalCompany === null || globalCompany === '',
        }
    );

    const [
        calculateOtAttendanceUsingTotalEarned,
        {
            isLoading: isCalculatingOtAttendanceUsingTotalEarned,
            // isError: errorRegisteringRegular,
            isSuccess: isCalculateOtAttendanceUsingTotalEarnedSuccess,
        },
    ] = useCalculateOtAttendanceUsingTotalEarnedMutation();

    const currentEmployeeSalaryEarning = useMemo(() => {
        const currentEmployeeSalaryEarning =
            allEmployeeSalaryEarnings?.filter(
                (item) => item.employee === updateEmployeeId && isDateWithinRange(item.fromDate, item.toDate)
            ) ?? [];
        return currentEmployeeSalaryEarning;
    }, [allEmployeeSalaryEarnings, updateEmployeeId]);

    const currentEmployeePfEsiDetails = useMemo(() => {
        const selectedEmployeeData = allEmployeePfEsiDetails?.filter((item) => item.employee === updateEmployeeId);
        return selectedEmployeeData;
    }, [allEmployeePfEsiDetails, updateEmployeeId]);

    const currentEmployeeSalaryDetails = useMemo(() => {
        const matchingItem = allEmployeeSalaryDetails?.find((item) => item.employee === updateEmployeeId);
        return matchingItem || null; // Return null (or another default value) when no match is found
    }, [allEmployeeSalaryDetails, updateEmployeeId]);

    const currentEmployeeMonthlyAttendanceDetails = useMemo(() => {
        if (allEmployeeMonthlyAttendanceDetails && updateEmployeeId) {
            const selectedEmployeeData = allEmployeeMonthlyAttendanceDetails.filter((item) => {
                const dateOfInstance = new Date(item.date);
                const currentSelectedDate = new Date(Date.UTC(selectedDate.year, selectedDate.month - 1, 1));
                return item.employee === updateEmployeeId && dateOfInstance.getTime() === currentSelectedDate.getTime();
            });
            return selectedEmployeeData;
        }
        // handleReset();
        return [];
    }, [allEmployeeMonthlyAttendanceDetails, updateEmployeeId]);

    const optionsForYear = useMemo(() => {
        if (earliestMonthAndYear) {
            const options = [];
            for (let i = earliestMonthAndYear.earliestYear; i <= new Date().getFullYear(); i++) {
                options.push(
                    <option key={i} value={i}>
                        {i}
                    </option>
                );
            }
            return options;
        }
    }, [earliestMonthAndYear]);

    const calculateButtonClicked = async (values, formikBag) => {
        let toSend = {
            company: globalCompany.id,
            employeeIds: [updateEmployeeId],
            manuallyInsertedTotalEarned: values.manuallyInsertedTotalEarned,
            markAttendance: true,
            month: selectedDate.month,
            year: selectedDate.year,
        };

        try {
            const data = await calculateOtAttendanceUsingTotalEarned(toSend).unwrap();
            console.log(data);
            dispatch(
                alertActions.createAlert({
                    message: data?.message,
                    type: 'Success',
                    duration: 3000,
                })
            );
            setShowInsertTotalEarnedModal(false);
        } catch (err) {
            console.log(err);
            let message = 'Error Occurred';
            console.log(err.data?.message);
            if (err.data?.message) {
                message = err.data?.message;
            }
            dispatch(
                alertActions.createAlert({
                    message: message,
                    type: 'Error',
                    duration: 6000,
                })
            );
        }
    };

    // Memoized API data transformation
    const apiFormValues = useMemo(() => {
        if (!isEmployeePreparedSalarySuccess || !employeePreparedSalary) return null;

        return {
            year: selectedDate.year,
            month: selectedDate.month,
            employeeSalaryPrepared: {
                incentiveAmount: employeePreparedSalary.incentiveAmount || 0,
                pfDeducted: employeePreparedSalary.pfDeducted || 0,
                esiDeducted: employeePreparedSalary.esiDeducted || 0,
                vpfDeducted: employeePreparedSalary.vpfDeducted || 0,
                advanceDeducted: employeePreparedSalary.advanceDeducted || 0,
                tdsDeducted: employeePreparedSalary.tdsDeducted || 0,
                labourWelfareFundDeducted: employeePreparedSalary.labourWelfareFundDeducted || 0,
                othersDeducted: employeePreparedSalary.othersDeducted || 0,
                netOtMinutesMonthly: employeePreparedSalary.netOtMinutesMonthly || 0,
                netOtAmountMonthly: employeePreparedSalary.netOtAmountMonthly || 0,
                paymentMode: employeePreparedSalary.paymentMode || '',
            },
            earnedAmount: (employeePreparedSalary.earnedAmounts || []).map((earned) => ({
                earningsHead: earned.earningsHead || null, // Already camelCased from API
                rate: earned.rate || 0,
                earnedAmount: earned.earnedAmount || 0,
                arearAmount: earned.arearAmount || 0,
            })),
        };
    }, [employeePreparedSalary, isEmployeePreparedSalarySuccess, selectedDate]);

    // Memoized default values from currentEmployeeSalaryEarning
    const defaultEarnedAmounts = useMemo(() => {
        if (currentEmployeeSalaryEarning?.length === 0) return [];

        return currentEmployeeSalaryEarning.map((item) => ({
            earningsHead: item.earningsHead,
            rate: item.value,
            earnedAmount: 0,
            arearAmount: 0,
        }));
    }, [currentEmployeeSalaryEarning]);

    // Combined effect for updating form values
    useEffect(() => {
        if (apiFormValues) {
            // Prioritize API data when available
            setFormValues(apiFormValues);
        } else if (defaultEarnedAmounts.length > 0) {
            // Fallback to default earned amounts
            setFormValues({
                ...initialFormValues, // Reset all fields to defaults
                earnedAmount: defaultEarnedAmounts, // Only override earnedAmount
            });
        } else {
            // Reset to initial values
            setFormValues(initialFormValues);
        }
    }, [apiFormValues, defaultEarnedAmounts, initialFormValues]);
    if (
        isLoadingEmployeePreparedSalary ||
        isFetchingEmployeePreparedSalary ||
        isLoadingAllEmployeeSalaryEarnings ||
        isFetchingAllEmployeeSalaryEarnings ||
        isLoadingAllEmployeeMonthlyAttendanceDetails ||
        isFetchingAllEmployeeMonthlyAttendanceDetails ||
        isLoadingAllEmployeeSalaryDetails ||
        isFetchingAllEmployeeSalaryDetails ||
        isLoadingAllEmployeePfEsiDetails ||
        isFetchingAllEmployeePfEsiDetails
    ) {
        return (
            <div className="mx-auto">
                <LoadingSpinner />
            </div>
        );
    } else if (
        currentEmployeeSalaryEarning?.length == 0 ||
        currentEmployeeSalaryDetails == null ||
        currentEmployeePfEsiDetails?.length == 0
    ) {
        return (
            <div>
                <section>
                    <label
                        htmlFor="year"
                        className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
                    >
                        Month and Year :
                    </label>
                    <select
                        name="month"
                        id="month"
                        value={selectedDate.month}
                        onChange={(e) => {
                            setSelectedDate((prevValue) => ({ ...prevValue, month: e.target.value }));
                        }}
                        className="my-1 mr-2 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
                    >
                        {months.map((month, index) => {
                            return (
                                <option key={index} value={index + 1}>
                                    {month}
                                </option>
                            );
                        })}
                    </select>

                    <select
                        name="year"
                        id="year"
                        onChange={(e) => {
                            setSelectedDate((prevValue) => ({ ...prevValue, year: e.target.value }));
                        }}
                        value={selectedDate.year}
                        className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
                    >
                        {optionsForYear}
                    </select>
                    <section>
                        {currentEmployeePfEsiDetails?.length == 0 && (
                            <h2 className="mx-auto text-lg dark:text-red-600">
                                PF ESI Details haven't been added for this employee
                            </h2>
                        )}
                        {!currentEmployeeSalaryDetails && (
                            <h2 className="mx-auto text-lg dark:text-red-600">
                                Salary Details hasn't been added for this employee
                            </h2>
                        )}
                    </section>
                </section>
            </div>
        );
    } else {
        return (
            <div>
                <section>
                    <label
                        htmlFor="year"
                        className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
                    >
                        Month and Year :
                    </label>
                    <select
                        name="month"
                        id="month"
                        value={selectedDate.month}
                        onChange={(e) => {
                            setSelectedDate((prevValue) => ({ ...prevValue, month: e.target.value }));
                        }}
                        className="my-1 mr-2 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
                    >
                        {months.map((month, index) => {
                            return (
                                <option key={index} value={index + 1}>
                                    {month}
                                </option>
                            );
                        })}
                    </select>

                    <select
                        name="year"
                        id="year"
                        onChange={(e) => {
                            setSelectedDate((prevValue) => ({ ...prevValue, year: e.target.value }));
                        }}
                        value={selectedDate.year}
                        className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
                    >
                        {optionsForYear}
                    </select>
                </section>
                <section className="mt-2 flex flex-row gap-4">
                    <div className="w-full">
                        <table className="w-full border-collapse text-center text-xs">
                            <thead className="sticky top-0 z-20 bg-yellow-600 dark:bg-yellow-700 dark:bg-opacity-40">
                                <tr>
                                    <th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">
                                        Earning Head
                                    </th>
                                    <th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">
                                        Rate
                                    </th>
                                    <th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">
                                        Arear
                                    </th>
                                    <th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">
                                        Earned
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50 ">
                                {formValues?.earnedAmount
                                    ?.sort((a, b) => a.earningsHead.id - b.earningsHead.id)
                                    ?.map((earning, index) => {
                                        return (
                                            <tr
                                                key={index}
                                                className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50"
                                            >
                                                <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
                                                    {earning.earningsHead.name}
                                                </td>
                                                <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
                                                    {earning.rate}
                                                </td>
                                                <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
                                                    {earning.arearAmount}
                                                </td>
                                                <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal dark:text-green-600">
                                                    {earning.earnedAmount}
                                                </td>
                                            </tr>
                                        );
                                    })}
                                {/* Calculate total rate */}
                                <tr>
                                    <td className="relative  px-4 py-2 font-medium text-orange-500">Total</td>
                                    <td className="relative  px-4 py-2 font-medium text-orange-500">
                                        {formValues.earnedAmount?.reduce((total, earning) => total + earning.rate, 0)}
                                    </td>
                                    <td className="relative  px-4 py-2 font-medium text-orange-500">
                                        {formValues.earnedAmount?.reduce((total, earning) => {
                                            if (
                                                earning.arearAmount != '' &&
                                                earning.arearAmount != null &&
                                                earning.arearAmount != undefined
                                            ) {
                                                return total + earning.arearAmount;
                                            }
                                            return total;
                                        }, 0)}
                                    </td>
                                    <td className="relative  px-4 py-2 font-medium text-orange-500">
                                        {formValues.earnedAmount?.reduce(
                                            (total, earning) => total + earning.earnedAmount,
                                            0
                                        )}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <DeductionsForCalculateOtAttendanceUsingEarnedSalary
                        globalCompany={globalCompany}
                        updateEmployeeId={updateEmployeeId}
                        formValues={formValues}
                        currentEmployeeSalaryDetails={currentEmployeeSalaryDetails}
                        currentEmployeePfEsiDetails={currentEmployeePfEsiDetails}
                    />
                </section>
                <section className="mt-10 flex flex-row justify-between">
                    <div className="flex flex-col gap-4">
                        <div>
                            <h5 className="inline dark:text-slate-300">Paid Days: </h5>
                            <span className=" m-1 font-bold dark:text-green-600">
                                {currentEmployeeMonthlyAttendanceDetails?.[0]?.paidDaysCount / 2 || 0}
                            </span>
                        </div>
                        <div>
                            <label
                                htmlFor={`employeeSalaryPrepared.incentiveAmount`}
                                className=" font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
                            >
                                Incentive:{' '}
                            </label>
                            {formValues?.employeeSalaryPrepared?.incentiveAmount}
                        </div>
                    </div>

                    <div className="flex flex-col gap-4">
                        <div>
                            <h5 className="inline dark:text-slate-300">Overtime Duration: </h5>
                            <span className="ml-1 font-bold dark:text-green-600">
                                {`${String(
                                    Math.floor(formValues.employeeSalaryPrepared.netOtMinutesMonthly / 60)
                                ).padStart(
                                    2,
                                    '0'
                                )}:${String(formValues.employeeSalaryPrepared.netOtMinutesMonthly % 60).padStart(2, '0')}`}
                            </span>
                        </div>

                        <div>
                            <h5 className="inline dark:text-slate-300">Overtime Amount: </h5>
                            <span className="ml-1 font-bold dark:text-green-600">
                                {formValues.employeeSalaryPrepared.netOtAmountMonthly}
                            </span>
                        </div>
                    </div>
                </section>
                <section className="w-full">
                    <p className="mx-auto mt-6 w-fit dark:text-yellow-600">
                        Total Before Deductions :{' '}
                        {formValues?.employeeSalaryPrepared?.netOtAmountMonthly +
                            (formValues?.employeeSalaryPrepared?.incentiveAmount === ''
                                ? 0
                                : Number(formValues?.employeeSalaryPrepared?.incentiveAmount)) +
                            formValues?.earnedAmount?.reduce((accumulator, item) => {
                                // Convert the earnedAmount property to a number and add it to the accumulator
                                return accumulator + Number(item.earnedAmount || 0); // Use 0 as a default value if earnedAmount is undefined or falsy
                            }, 0)}
                    </p>
                    {/* Using Same Net Salary Component as in Default Mode */}
                    <NetSalary values={formValues} updateEmployeeId={updateEmployeeId} />
                </section>
                <section>
                    <div className="mt-4 mb-2 flex w-fit flex-row gap-4">
                        <button
                            className={classNames(
                                ' bg-blueAccent-400 hover:bg-blueAccent-500  dark:bg-blueAccent-700 dark:hover:bg-blueAccent-600',
                                'h-10 w-fit rounded p-2 px-4 text-base font-medium'
                            )}
                            type="submit"
                            // disabled={!isValid}
                            onClick={() => setShowInsertTotalEarnedModal(true)}
                        >
                            Calculate
                            {false && (
                                <FaCircleNotch className="my-auto ml-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
                            )}
                        </button>
                    </div>
                    <ReactModal
                        className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
                        isOpen={showInsertTotalEarnedModal}
                        onRequestClose={() => setShowInsertTotalEarnedModal(false)} //|| isBulkPreparingEmployeeSalaries)}
                        style={{
                            overlay: {
                                backgroundColor: 'rgba(0, 0, 0, 0.75)',
                                zIndex: 30,
                            },
                        }}
                    >
                        <Formik
                            initialValues={{ manuallyInsertedTotalEarned: '' }}
                            validationSchema={''}
                            onSubmit={calculateButtonClicked}
                            component={(props) => (
                                <InsertTotalEarnedModal
                                    {...props}
                                    setShowInsertTotalEarnedModal={setShowInsertTotalEarnedModal}
                                />
                            )}
                        />
                    </ReactModal>
                </section>
            </div>
        );
    }
};

export default CalculateOtAttendanceusingEarnedSalary;
