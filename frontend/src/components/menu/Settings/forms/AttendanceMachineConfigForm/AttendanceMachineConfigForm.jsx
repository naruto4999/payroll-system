import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useOutletContext } from 'react-router-dom';
import { Formik } from 'formik';
import { Field, ErrorMessage } from 'formik';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { FaCircleNotch } from 'react-icons/fa';
import { useGetAttendanceMachineConfigQuery, useAddAttendanceMachineConfigMutation, useUpdateAttendanceMachineConfigMutation } from '../../../../authentication/api/attenadanceMachineConfigApiSlice';
import { AttendanceMachineConfigSchema } from './AttendanceMachineConfigSchema';

const classNames = (...classes) => {
  return classes.filter(Boolean).join(" ");
};
const AttendanceMachineConfigForm = () => {
  const dispatch = useDispatch();
  const globalCompany = useSelector((state) => state.globalCompany);
  const [showLoadingBar, setShowLoadingBar] = useOutletContext();
  const {
    data: { company, ...attendanceMachineConfig } = {},
    isLoading: isLoadingAttendanceMachineConfig,
    isSuccess: isAttendanceMachineConfigSuccess,
    isError: isAttendanceMachineConfigError,
    isFetching: isFetchingAttendanceMachineConfig,
  } = useGetAttendanceMachineConfigQuery(globalCompany.id);
  console.log(attendanceMachineConfig);
  console.log(isAttendanceMachineConfigSuccess);

  const [
    addAttendanceMachineConfig,
    {
      isLoading: isAddingAttendanceMachineConfig,
      // isError: errorRegisteringRegular,
      isSuccess: isAddAttendanceMachineConfigSuccess,
    },
  ] = useAddAttendanceMachineConfigMutation();
  const [
    updateAttendanceMachineConfig,
    {
      isLoading: isUpdatingAttendanceMachineConfig,
      // isError: errorRegisteringRegular,
      isSuccess: isUpdateAttendanceMachineConfigSuccess,
    },
  ] = useUpdateAttendanceMachineConfigMutation();


  const updateButtonClicked = async (values, formikBag) => {
    console.log(values);
    if (isAttendanceMachineConfigSuccess) {
      try {
        const data = await updateAttendanceMachineConfig({
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
    } else if (!isAttendanceMachineConfigSuccess) {
      try {
        const data = await addAttendanceMachineConfig({
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
    setShowLoadingBar(isLoadingAttendanceMachineConfig || isAddingAttendanceMachineConfig || isUpdatingAttendanceMachineConfig);
  }, [isLoadingAttendanceMachineConfig, isAddingAttendanceMachineConfig, isUpdatingAttendanceMachineConfig]);


  if (isLoadingAttendanceMachineConfig) {
    return (
      <div className="fixed inset-0 z-50 mx-auto my-auto flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium">
        <FaCircleNotch className="mr-2 animate-spin text-white" />
        Processing...
      </div>
    );
  } else {
    return (
      <section className="mx-5 mt-2">
        <div className="flex flex-row flex-wrap place-content-between">
          <div className="mr-4">
            <h1 className="text-3xl font-medium">Attendance Machine Configuration</h1>
            <p className="my-2 text-sm">Configure Attendance (Biometric) Machine here.</p>
          </div>
        </div>

        {/* Formik Implementation */}
        <Formik
          initialValues={
            isAttendanceMachineConfigSuccess
              ? {
                ...attendanceMachineConfig,
              }
              : {
                machineIp: "192.168.0.100",
              }
          }
          validationSchema={AttendanceMachineConfigSchema}
          onSubmit={updateButtonClicked}
        >
          {({ handleSubmit, errors, touched, values, isValid }) => (
            < form id="" className="mt-2" onSubmit={handleSubmit}>
              <div className="flex w-full flex-col gap-2">
                <div>
                  <label
                    htmlFor="machineIp"
                    className="my-auto block font-medium text-blueAccent-700 dark:text-blueAccent-400"
                  >
                    Machine IP Address
                  </label>
                  <Field
                    type="text"
                    name={`machineIp`}
                    id={`machineIp`}
                    className="h-full w-fit rounded border border-slate-100 border-opacity-50 bg-zinc-800 pl-2 pr-2 text-xs duration-300 sm:text-base"
                  // placeholder="Enter IPv4 address (e.g., 192.168.0.1)"
                  />

                  <div className="my-1 text-xs font-bold text-red-500 dark:text-red-700">
                    <ErrorMessage name={`machineIp`} />
                  </div>
                </div>
                <div>
                  <button
                    className={classNames(
                      isValid
                        ? 'hover:bg-teal-600  dark:hover:bg-teal-600'
                        : 'opacity-40',
                      'w-20 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
                    )}

                    type="submit"
                    disabled={!isValid}
                  >
                    {isAttendanceMachineConfigSuccess ? 'Update' : 'Create'}
                  </button>
                </div>
              </div>
              {console.log(errors)}
            </form>
          )}
        </Formik>
      </section >
    )
  }
}

export default AttendanceMachineConfigForm
