import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useOutletContext } from 'react-router-dom';
import { Formik } from 'formik';
import { Field, ErrorMessage } from 'formik';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { FaCircleNotch } from 'react-icons/fa';
import {
    useGetExtraFeaturesConfigQuery,
    useAddExtraFeaturesConfigMutation,
    useUpdateExtraFeaturesConfigMutation,
} from '../../../../authentication/api/extraFeaturesConfigApiSlice';
// import { AttendanceMachineConfigSchema } from './AttendanceMachineConfigSchema';

const classNames = (...classes) => {
    return classes.filter(Boolean).join(' ');
};

const ExtraFeaturesConfigForm = () => {
    const dispatch = useDispatch();
    const globalCompany = useSelector((state) => state.globalCompany);
    const auth = useSelector((state) => state.auth);
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const {
        data: { company, ...extraFeaturesConfig } = {},
        isLoading: isLoadingExtraFeaturesConfig,
        isSuccess: isExtraFeaturesConfigSuccess,
        isError: isExtraFeaturesConfigError,
        isFetching: isFetchingExtraFeaturesConfig,
    } = useGetExtraFeaturesConfigQuery(globalCompany.id);

    const [
        addExtraFeaturesConfig,
        {
            isLoading: isAddingExtraFeaturesConfig,
            // isError: errorRegisteringRegular,
            isSuccess: isAddExtraFeaturesConfigSuccess,
        },
    ] = useAddExtraFeaturesConfigMutation();
    const [
        updateExtraFeaturesConfig,
        {
            isLoading: isUpdatingExtraFeaturesConfig,
            // isError: errorRegisteringRegular,
            isSuccess: isUpdateExtraFeaturesConfigSuccess,
        },
    ] = useUpdateExtraFeaturesConfigMutation();

    const updateButtonClicked = async (values, formikBag) => {
        console.log(values);
        if (isExtraFeaturesConfigSuccess) {
            try {
                const data = await updateExtraFeaturesConfig({
                    ...values,
                    company: globalCompany.id,
                }).unwrap();
                console.log(data);
                dispatch(
                    alertActions.createAlert({
                        message: 'Saved',
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
        } else if (!isExtraFeaturesConfigSuccess) {
            try {
                const data = await addExtraFeaturesConfig({
                    ...values,
                    company: globalCompany.id,
                }).unwrap();
                console.log(data);
                dispatch(
                    alertActions.createAlert({
                        message: 'Saved',
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
        }
    };

    useEffect(() => {
        setShowLoadingBar(isLoadingExtraFeaturesConfig || isAddingExtraFeaturesConfig || isUpdatingExtraFeaturesConfig);
    }, [isLoadingExtraFeaturesConfig, isAddingExtraFeaturesConfig, isUpdatingExtraFeaturesConfig]);

    if (isLoadingExtraFeaturesConfig) {
        return (
            <div className="fixed inset-0 z-50 mx-auto my-auto flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium">
                <FaCircleNotch className="mr-2 animate-spin text-white" />
                Processing...
            </div>
        );
    } else if (globalCompany.id == null) {
        return (
            <section className="flex flex-col items-center">
                <h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
                    Please Select a Company First
                </h4>
            </section>
        );
    } else {
        return (
            <section className="mx-5 mt-2">
                <div className="flex flex-row flex-wrap place-content-between">
                    <div className="mr-4">
                        <h1 className="text-3xl font-medium">Extra Features Configuration</h1>
                        <p className="my-2 text-sm">Enable or Disable Extra Features here.</p>
                    </div>
                </div>
                {/* Formik Implementation */}
                {auth.account.role === 'OWNER' && (
                    <Formik
                        initialValues={
                            isExtraFeaturesConfigSuccess
                                ? {
                                    ...extraFeaturesConfig,
                                }
                                : {
                                    enableCalculateOtAttendanceUsingEarnedSalary: false,
                                }
                        }
                        validationSchema={''}
                        onSubmit={updateButtonClicked}
                    >
                        {({ handleSubmit, errors, touched, values, isValid }) => (
                            <form id="" className="mt-2" onSubmit={handleSubmit}>
                                <div className="flex w-full flex-col gap-2">
                                    {auth.account.role === 'OWNER' && (
                                        <div>
                                            <div className="my-auto w-full font-medium text-amber-600 dark:text-amber-600">
                                                {'Enable Calculate Overtime And Attendance using Earned Salary'}

                                                <Field
                                                    type="checkbox"
                                                    name={`enableCalculateOtAttendanceUsingEarnedSalary`}
                                                    className="my-auto ml-4 inline h-4 w-4 rounded accent-teal-600"
                                                />
                                            </div>
                                        </div>
                                    )}

                                    <div className="my-1 text-xs font-bold text-red-500 dark:text-red-700">
                                        <ErrorMessage name={`enableCalculateOtAttendanceUsingEarnedSalary`} />
                                    </div>
                                    <div>
                                        <button
                                            className={classNames(
                                                isValid ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
                                                'w-20 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
                                            )}
                                            type="submit"
                                            disabled={!auth.account.role === 'OWNER' || !isValid}
                                        >
                                            {isExtraFeaturesConfigSuccess ? 'Update' : 'Create'}
                                        </button>
                                    </div>
                                </div>
                                {console.log(errors)}
                            </form>
                        )}
                    </Formik>
                )}
            </section>
        );
    }
};

export default ExtraFeaturesConfigForm;
