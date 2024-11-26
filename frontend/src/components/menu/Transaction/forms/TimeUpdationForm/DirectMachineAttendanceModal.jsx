import React, { useState, useEffect } from 'react'
import { FaCircleNotch } from 'react-icons/fa6';
//import ProgressBar from "@ramonak/react-progress-bar";
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

const DirectMachineAttendanceModal = (
  {
    manualFromDate,
    manualToDate,
    month,
    year,
    setShowDirectMachineAttendanceModal,
    updateEmployeeId
  }
) => {
  const { handleSubmit, handleChange, values, isValid, errors, isSubmitting } = useFormikContext();
  const [loading, setLoading] = useState(false); // To show loading spinner
  const [error, setError] = useState(null); // To capture errors
  const [attendanceData, setAttendanceData] = useState(null); // To store the response data


  console.log(errors);
  console.log(new Date(Date.UTC(year, month - 1, manualFromDate)))
  console.log(new Date(Date.UTC(year, month - 1, manualToDate)))


  const fetchUsers = async () => {
    setLoading(true);
    setError(null); // Reset error state before making a new request
    try {
      const response = await fetch('http://127.0.0.1:9000/attendance-api/get-all-users/');
      console.log(response)
      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }
      const data = await response.json();
      setAttendanceData(data); // Set the response data
    } catch (err) {
      setError(err.message); // Capture error if the request fails
    } finally {
      setLoading(false); // Stop loading spinner
    }
  };
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
        <h1 className="mb-2 text-2xl font-medium">Machine Attendance Direct</h1>
        <h3 className="mb-2 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70">Attendance Period: {<span className='text-amber-500 font-bold'>{formatDate(new Date(Date.UTC(year, month - 1, manualFromDate)))}</span>} To {<span className='text-amber-500 font-bold'>{formatDate(new Date(Date.UTC(year, month - 1, manualToDate)))}</span>}</h3>

        <form action="" className="flex flex-col justify-center gap-2"></form>
        <button
          type="button"
          className="h-8 w-32 rounded bg-blueAccent-400 p-1 text-base font-medium hover:bg-blueAccent-500 dark:bg-blueAccent-700 dark:hover:bg-blueAccent-600"
          onClick={fetchUsers}
        >
          Test Conn

          {loading && <FaCircleNotch className="mx-2 inline animate-spin text-white" />}
        </button>
        {/* Show attendance data or errors */}
        {error && <div className="text-red-500">{error}</div>}
        {attendanceData && (
          <div className="mt-4">
            <h3 className="text-lg font-semibold">Fetched Users:</h3>
            <pre>{JSON.stringify(attendanceData, null, 2)}</pre>
          </div>
        )}
      </div>
    )
  }
}

export default DirectMachineAttendanceModal;
