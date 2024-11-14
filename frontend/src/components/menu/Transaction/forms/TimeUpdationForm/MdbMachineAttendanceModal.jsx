import React, { useState, useEffect } from 'react'
import { FaCircleNotch } from 'react-icons/fa6';
// import ProgressBar from "@ramonak/react-progress-bar";
import { Field, ErrorMessage, useFormikContext } from 'formik';


const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};

function formatDate(date) {
  const day = date.getDate();
  const month = date.toLocaleString('default', { month: 'long' });
  const year = date.getFullYear();

  return `${day} ${month}, ${year}`;
}

const MdbMachineAttendance = ({ manualFromDate,
  manualToDate,
  month,
  year,
  setShowMdbMachineAttendanceModal,
  updateEmployeeId }) => {
  const { handleSubmit, handleChange, values, isValid, errors, isSubmitting } = useFormikContext();

  console.log(errors);
  console.log(new Date(Date.UTC(year, month - 1, manualFromDate)))
  console.log(new Date(Date.UTC(year, month - 1, manualToDate)))
  console.log(new Date(Date.UTC(year, month, 0)).getUTCDate())
  if (manualFromDate == '' || manualFromDate == null || manualFromDate == undefined || manualToDate == '' || manualToDate == null || manualToDate == undefined) {
    return (
      <div className='w-full'>
        <div className="mx-auto text-base font-bold text-red-500 dark:text-red-700 w-fit">
          Please Enter From and To Date first</div>
      </div>
    )
  }
  else if (updateEmployeeId == null || updateEmployeeId == undefined) {
    return (
      <div className='w-full'>
        <div className="mx-auto text-base font-bold text-red-500 dark:text-red-700 w-fit">
          Please Select an Employee first</div>
      </div>
    )

  }
  else if (new Date(Date.UTC(year, month - 1, manualFromDate)) > new Date(Date.UTC(year, month - 1, manualToDate))) {
    return (
      <div className='w-full'>
        <div className="mx-auto text-base font-bold text-red-500 dark:text-red-700 w-fit">
          From Date cannot be greater than To Date
        </div>
      </div>
    )
  }
  else if (manualToDate > new Date(Date.UTC(year, month, 0)).getUTCDate()) {
    return (
      <div className='w-full'>
        <div className="mx-auto text-base font-bold text-red-500 dark:text-red-700 w-fit">
          To Date exeedes the number of days in selected month
        </div>
      </div>
    )
  }

  else {
    return (
      <div className="text-gray-900 dark:text-slate-100">
        <h1 className="mb-2 text-2xl font-medium">Machine Attendance MDB File</h1>
        <h3 className="mb-2 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">Attendance Period: {<span className='text-amber-500 font-bold'>{formatDate(new Date(Date.UTC(year, month - 1, manualFromDate)))}</span>} To {<span className='text-amber-500 font-bold'>{formatDate(new Date(Date.UTC(year, month - 1, manualToDate)))}</span>}</h3>

        <form action="" className="flex flex-col justify-center gap-2">


          <Field
            type="file"
            name="machineAttendanceUpload"
            id="machineAttendanceUpload"
            value={undefined}
            onChange={(event) => {
              handleChange(event);
              handleFileChange(event);
            }}
            className="block w-full cursor-pointer rounded border border-gray-300 bg-gray-50 text-sm file:border-0 file:bg-zinc-600 file:py-1 file:px-4 file:text-sm file:font-semibold file:text-white hover:file:cursor-pointer hover:file:bg-zinc-700 focus:outline-none dark:border-gray-600 dark:bg-zinc-900 dark:placeholder-gray-400"
          />
          <div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
            <ErrorMessage name="machineAttendanceUpload" />
          </div>

          <label className="my-auto block text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">
            All employees:
            <Field
              type="checkbox"
              name="allEmployeesMachineAttendance"
              className="ml-2.5 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
            />
          </label>
          <div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
            <ErrorMessage name="allEmployeesMachineAttendance" />
          </div>


          <label
            htmlFor="userInput"
            className="text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
          >
            {`Please type "Confirm" to update attendance using machine (MDB File)`}
          </label>
          <div className="relative">
            <input
              className="w-full rounded border-2 border-gray-800  border-opacity-25 bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-700 dark:focus:border-opacity-75"
              type="text"
              id="userInput"
              name="userInput"
              placeholder=""
              onChange={handleChange}
            // ref={inputRef}
            />
          </div>
          {isValid ? (
            ''
          ) : (
            <p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">{errors.userInput}</p>)}
          <section className="mt-4 mb-2 flex flex-row gap-4">
            <button
              className={classNames(
                isValid && !isSubmitting ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
                'w-24 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
              )}
              onClick={handleSubmit}
              type="submit"
              disabled={isSubmitting}
            >
              Confirm
              <FaCircleNotch
                className={classNames(isSubmitting ? '' : 'hidden', 'mx-2 inline animate-spin text-white')}
              />
            </button>
            <button
              className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
              type="button"
              onClick={() => {
                setShowMdbMachineAttendanceModal(false || isSubmitting);
              }}
            >
              Cancel
            </button>
          </section>

        </form>

      </div >
    )
  }
}

export default MdbMachineAttendance;
