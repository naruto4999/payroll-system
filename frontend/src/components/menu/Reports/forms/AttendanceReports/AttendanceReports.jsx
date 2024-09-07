import React, { useState, useMemo, useEffect } from 'react';
import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import { useAllEmployeeYearlyMissPunchesQuery } from '../../../../authentication/api/attendanceReportsApiSlice';
import {
  // column,
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getSortedRowModel,
  // columnFiltersState,
  getFilteredRowModel,
  // filterFn,
  // filterFns,
} from '@tanstack/react-table';
import { Formik } from 'formik';
import { useDispatch, useSelector } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { useOutletContext } from 'react-router-dom';
import EmployeeTable from '../EmployeeTable';
import MonthYearSelector from '../MonthYearSelector';
import { FaCheck, FaWindowMinimize } from 'react-icons/fa';
import FilterOptions from './FilterOptions';
import { authActions } from '../../../../authentication/store/slices/auth';

const AttendanceReports = () => {
  const auth = useSelector((state) => state.auth);
  const globalCompany = useSelector((state) => state.globalCompany);
  const dispatch = useDispatch();
  const [showLoadingBar, setShowLoadingBar] = useOutletContext();

  const {
    data: employeePersonalDetails,
    isLoading: isLoadingEmployeePersonalDetails,
    isSuccess: isSuccessEmployeePersonalDetails,
  } = useGetEmployeePersonalDetailsQuery(globalCompany);


  // console.log(employeePersonalDetails);
  const [selectedDate, setSelectedDate] = useState({
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1,
  });


  const {
    data: allEmployeeYearlyMissPunches,
    isLoading: isLoadingAllEmployeeMissPunches,
    isSuccess: isSuccessAllEmployeeMissPunches,
  } = useAllEmployeeYearlyMissPunchesQuery({ globalCompany: globalCompany, year: selectedDate.year });

  const monthlyMissPunches = useMemo(() => {
    const months = {};

    allEmployeeYearlyMissPunches?.forEach((punch) => {
      const month = new Date(punch.date).getMonth() + 1; // getMonth() returns 0-based month, so add 1 to make it 1-based

      if (!months[month]) {
        months[month] = [];
      }

      months[month].push(punch);
    });

    return months;
  }, [allEmployeeYearlyMissPunches]);
  const [ignoreMonthField, setIgnoreMonthField] = useState(false);
  const [filterMissPunchEmployees, setFilterMissPunchEmployees] = useState(false)

  const IndeterminateCheckbox = React.forwardRef(({ indeterminate, ...rest }, ref) => {
    const defaultRef = React.useRef();
    const resolvedRef = ref || defaultRef;

    React.useEffect(() => {
      resolvedRef.current.indeterminate = indeterminate;
    }, [resolvedRef, indeterminate]);

    return (
      <label className="relative flex cursor-pointer flex-col ">
        <input
          type="checkbox"
          ref={resolvedRef}
          className="peer h-5 w-5 appearance-none rounded-md border border-slate-400"
          {...rest}
        />
        {indeterminate ? (
          <FaWindowMinimize className="absolute left-[3px] bottom-[7px] text-teal-600 dark:text-teal-500" />
        ) : (
          <FaCheck className="absolute left-[3px] bottom-[3px] text-teal-600 peer-[&:not(:checked)]:hidden dark:text-teal-500" />
        )}
      </label>
    );
  });

  const columnHelper = createColumnHelper();

  const columns = [
    columnHelper.accessor('paycode', {
      header: () => 'PC',
      cell: (props) => props.renderValue(),
      //   footer: props => props.column.id,
      // filterFn: 'fuzzy',
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
    columnHelper.accessor('designation', {
      header: () => 'Designation',
      cell: (props) => props.renderValue(),
      //   footer: info => info.column.id,
    }),
    columnHelper.accessor('dateOfJoining', {
      header: () => 'DOJ',
      cell: (props) => props.renderValue(),
      // enableHiding: true,
    }),
    columnHelper.accessor('resignationDate', {
      header: () => 'Resign Date',
      cell: (props) => props.renderValue(),
      enableHiding: true,
    }),
    columnHelper.display({
      id: 'select',
      header: ({ table }) => (
        <IndeterminateCheckbox
          {...{
            checked: table.getIsAllRowsSelected(),
            indeterminate: table.getIsSomeRowsSelected(),
            onChange: table.getToggleAllRowsSelectedHandler(),
          }}
        />
      ),
      cell: ({ row }) => (
        <div>
          <IndeterminateCheckbox
            {...{
              checked: row.getIsSelected(),
              disabled: !row.getCanSelect(),
              indeterminate: row.getIsSomeSelected(),
              onChange: row.getToggleSelectedHandler(),
            }}
          />
        </div>
      ),
    }),
  ];

  const data = useMemo(() => {
    if (!employeePersonalDetails) return [];

    const filteredData = employeePersonalDetails.filter((employee) => {
      if (employee.dateOfJoining) {
        const comparisonDate = new Date(Date.UTC(selectedDate.year, parseInt(selectedDate.month) - 1, 1));
        // Extract the year and month from the original dateOfJoining
        const [year, month] = employee.dateOfJoining.split('-').map(Number);
        if (employee.resignationDate) {
          const [resignYear, resignMonth] = employee.resignationDate.split('-').map(Number);
          const resignDate = new Date(Date.UTC(resignYear, resignMonth, 0));
          if (ignoreMonthField == true) {
            if (selectedDate.year > resignYear) {
              return false;
            }
          } else {
            if (resignDate < comparisonDate) {
              return false;
            }

          }
        }
        const dateOfJoiningOfEmployee = new Date(Date.UTC(year, month - 1, 1));
        // Check if employee.id exists in the array
        if (ignoreMonthField == true) {
          return year <= selectedDate.year
        }
        else if (filterMissPunchEmployees == true) {
          return dateOfJoiningOfEmployee <= comparisonDate &&
            monthlyMissPunches?.[parseInt(selectedDate.month)]?.some(missPunch => {
              if (employee.id === missPunch.employee) {
                const [missPunchYear, missPunchMonth] = missPunch.date.split('-').map(Number);
                if (missPunchYear === selectedDate.year && missPunchMonth === parseInt(selectedDate.month)) {
                  return true
                }
              }
            });
        }
        else {
          return dateOfJoiningOfEmployee <= comparisonDate;
        }
      } else {
        return false;
      }
    });

    return filteredData;
  }, [employeePersonalDetails, selectedDate.month, selectedDate.year, ignoreMonthField, filterMissPunchEmployees, monthlyMissPunches]);

  const earliestMonthAndYear = useMemo(() => {
    let earliestDate = Infinity; // Initialize earliestDate to a very large value
    let earliestMonth = '';
    let earliestYear = '';
    if (employeePersonalDetails) {
      for (const employee of employeePersonalDetails) {
        const dateOfJoining = new Date(employee.dateOfJoining);

        if (dateOfJoining < earliestDate) {
          earliestDate = dateOfJoining;
          earliestMonth = dateOfJoining.getMonth() + 1;
          earliestYear = dateOfJoining.getFullYear();
        }
      }
    }
    return {
      earliestMonth: earliestMonth,
      earliestYear: earliestYear,
    };
  }, [employeePersonalDetails]);

  const table = useReactTable({
    data,
    columns,
    initialState: {
      sorting: [{ id: 'name', desc: false }],
      columnVisibility: { dateOfJoining: true, resignationDate: false },
      // rowSelection: { 6: true, 9: true },
    },
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getRowId: (originalRow) => originalRow.id,
    enableSortingRemoval: false,
  });

  useEffect(() => {
    if (table.getIsAllRowsSelected() == false) {
      table.toggleAllRowsSelected();
    }
  }, [data]);

  const generateInitialValues = () => {
    const initialValues = {
      filters: {
        groupBy: 'none',
        sortBy: 'paycode',
        resignationFilter: 'all',
        monthFromDate: null,
        monthToDate: null,
        date: '',
      },
      reportType: 'present_report',
    };
    return initialValues;
  };
  const initialValues = useMemo(() => generateInitialValues(), []);
  // console.log(initialValues);

  const generateButtonClicked = async (values, formikBag) => {
    setShowLoadingBar(true);
    // console.log(values);
    const toSend = {
      ...values,
      filters: {
        ...values.filters,
        monthFromDate: parseInt(values.filters.monthFromDate),
        monthToDate: parseInt(values.filters.monthToDate),
        date: values.filters.date === '' ? null : values.filters.date,
      },
      employee_ids: table.getSelectedRowModel().flatRows.map((row) => row.id),
      company: globalCompany.id,
      month: parseInt(selectedDate.month),
      year: selectedDate.year,
    };
    console.log(toSend);

    // using fetch
    const requestOptions = {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${auth.token}`,
        'Content-Type': 'application/json', // Set the Content-Type based on your request payload
        // Add any other headers as needed
      },
      body: JSON.stringify(toSend),
    };

    const generateSalarySheet = async () => {
      try {
        const startTime = performance.now();
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}api/generate-attendance-reports`,
          requestOptions
        );

        if (response.status === 401) {
          console.log('Received a 401 status, attempting to refresh the token...');

          const refreshResponse = await fetch(`${import.meta.env.VITE_BACKEND_URL}api/auth/refresh/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: auth.refreshToken }),
          });

          if (refreshResponse.status === 200) {
            const refreshData = await refreshResponse.json();

            if (refreshData.access && refreshData.refresh) {
              dispatch(
                authActions.setAuthTokens({
                  token: refreshData.access,
                  refreshToken: refreshData.refresh,
                })
              );

              const refreshedResponse = await fetch(
                `${import.meta.env.VITE_BACKEND_URL}api/generate-attendance-reports`,
                {
                  ...requestOptions,
                  headers: {
                    Authorization: `Bearer ${refreshData.access}`,
                    'Content-Type': 'application/json',
                  },
                }
              );

              if (refreshedResponse.status === 200) {

                const pdfData = await refreshedResponse.arrayBuffer();
                const pdfBlob = new Blob([pdfData], { type: 'application/pdf' });
                const pdfUrl = URL.createObjectURL(pdfBlob);
                window.open(pdfUrl, '_blank');
                dispatch(
                  alertActions.createAlert({
                    message: 'Generated',
                    type: 'Success',
                    duration: 8000,
                  })
                );
              } else if (refreshedResponse.status === 404) {
                dispatch(
                  alertActions.createAlert({
                    message: 'No Salary Prepared for the given month',
                    type: 'Error',
                    duration: 5000,
                  })
                );
              }
            }
          } else {
            console.log('Error refreshing token');
            // Handle the refresh token failure
            dispatch(
              alertActions.createAlert({
                message: 'Error Occurred',
                type: 'Error',
                duration: 5000,
              })
            );
            dispatch(authActions.logout());
          }
        } else if (response.status != 200) {
          console.error('Request failed with status: ', response.status);
          response.json().then((data) => {
            console.log(data)
            console.log('Error:', data.detail);
            dispatch(
              alertActions.createAlert({
                message: data.detail,
                type: 'Error',
                duration: 5000,
              })
            );
          });
          // throw new Error('Request failed');
        } else if (response.status == 200) {

          const pdfData = await response.arrayBuffer();
          const pdfBlob = new Blob([pdfData], { type: 'application/pdf' });
          const pdfUrl = URL.createObjectURL(pdfBlob);
          const endTime = performance.now(); // Record the end time
          const responseTime = endTime - startTime;
          const responseTimeInSeconds = (responseTime / 1000).toFixed(2);
          dispatch(
            alertActions.createAlert({
              message: `Generated, Time Taken: ${responseTimeInSeconds} seconds`,
              type: 'Success',
              duration: 8000,
            })
          );
          window.open(pdfUrl, '_blank');
        }
      } catch (error) {
        console.log(error)
        console.error('Fetch error: ', error);
        dispatch(
          alertActions.createAlert({
            message: 'Error Occurred',
            type: 'Error',
            duration: 5000,
          })
        );
      }
      setShowLoadingBar(false);
    };

    // Call the generateSalarySheet function to initiate the request
    generateSalarySheet();
  };
  if (globalCompany.id == null) {
    return (
      <section className="flex flex-col items-center">
        <h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
          Please Select a Company First
        </h4>
      </section>
    );
  } else if (isLoadingEmployeePersonalDetails) {
    return <div></div>;
  } else {
    return (
      <section className="mt-4">
        <div className="ml-4 flex flex-row flex-wrap place-content-between">
          <div className="mr-4">
            <h1 className="text-3xl font-medium">Attendance/Bonus Reports</h1>
            <p className="my-2 text-sm">Generate Reports related to attendance of the employees here</p>
          </div>
        </div>
        <div className="ml-4">
          <MonthYearSelector
            earliestMonthAndYear={earliestMonthAndYear}
            setSelectedDate={setSelectedDate}
            selectedDate={selectedDate}
          />
        </div>
        <div className="flex w-full flex-row gap-8">
          <div className="ml-4 flex w-2/5 flex-col">
            <EmployeeTable table={table} flexRender={flexRender} />
          </div>
          <div className="mt-4">
            <Formik
              initialValues={initialValues}
              validationSchema={''}
              onSubmit={generateButtonClicked}
              component={(props) => <FilterOptions {...props} selectedDate={selectedDate} setIgnoreMonthField={setIgnoreMonthField} setFilterMissPunchEmployees={setFilterMissPunchEmployees} />}
            />
          </div>
        </div>
      </section>
    );
  }
};

export default AttendanceReports;
