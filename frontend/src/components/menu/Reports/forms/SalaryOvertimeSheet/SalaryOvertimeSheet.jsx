import React, { useState, useMemo, useEffect } from 'react';
// import { useGetCompanyStatisticsQuery } from '../../../authentication/api/salaryOvertimeSheetApiSlice';
import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import {
  useGenerateSalaryOvertimeSheetMutation,
  useGetPreparedSalariesQuery,
  useGetEmployeesForYearlyAdvanceReportQuery
} from '../../../../authentication/api/salaryOvertimeSheetApiSlice';
import { authActions } from '../../../../authentication/store/slices/auth';
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
import EmployeeTable from '../EmployeeTable';
import { FaCheck, FaWindowMinimize } from 'react-icons/fa';
import MonthYearSelector from '../MonthYearSelector';
import FilterOptions from './FilterOptions';
import { Formik } from 'formik';
import { useDispatch, useSelector } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { useOutletContext } from 'react-router-dom';

const SalaryOvertimeSheet = () => {
  const globalCompany = useSelector((state) => state.globalCompany);
  const auth = useSelector((state) => state.auth);
  const dispatch = useDispatch();
  const [showLoadingBar, setShowLoadingBar] = useOutletContext();
  const [filterYearlyAdvanceEmployees, setFilterYearlyAdvanceEmployees] = useState(false);

  const [selectedDate, setSelectedDate] = useState({
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1,
  });


  const {
    data: employeePersonalDetails,
    isLoading: isLoadingEmployeePersonalDetails,
    isSuccess: isSuccessEmployeePersonalDetails,
  } = useGetEmployeePersonalDetailsQuery(globalCompany);

  const {
    data: employeesForYearlyAdvanceReport,
    isLoading: isLoadingEmployeesForYearlyAdvanceReport,
    isFetching: isFetchingEmployeesForYearlyAdvanceReport,
    isSuccess: isSuccessEmployeesForYearlyAdvanceReport,
  } = useGetEmployeesForYearlyAdvanceReportQuery({ company: globalCompany.id, year: selectedDate.year });
  console.log(employeesForYearlyAdvanceReport)

  const {
    data: employeePreparedSalaries,
    isLoading: isLoadingEmployeePreparedSalaries,
    isSuccess: isSuccessEmployeePreparedSalaries,
  } = useGetPreparedSalariesQuery({ company: globalCompany.id, month: selectedDate.month, year: selectedDate.year });
  //console.log(employeePreparedSalaries);
  //console.log(employeePersonalDetails);
  // const [
  // 	generateSalaryOvertimeSheet,
  // 	{
  // 		isLoading: isGeneratingSalaryOvertimeSheet,
  // 		// isError: errorRegisteringRegular,
  // 		isSuccess: isGenerateSalaryOvertimeSheetSuccess,
  // 	},
  // ] = useGenerateSalaryOvertimeSheetMutation();

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
        if (filterYearlyAdvanceEmployees == true) {
          const isYearlyAdvanceEmployee = employeesForYearlyAdvanceReport?.employeeIds?.some((id) => id === employee.id);
          return isYearlyAdvanceEmployee
        }
        else {
          const comparisonDate = new Date(Date.UTC(selectedDate.year, parseInt(selectedDate.month) - 1, 1));
          // Extract the year and month from the original dateOfJoining
          const [year, month] = employee.dateOfJoining.split('-').map(Number);
          if (employee.resignationDate) {
            const [resignYear, resignMonth] = employee.resignationDate.split('-').map(Number);
            const resignDate = new Date(Date.UTC(resignYear, resignMonth, 0));
            if (resignDate < comparisonDate) {
              return false;
            }
          }
          const dateOfJoiningOfEmployee = new Date(Date.UTC(year, month - 1, 1));
          // Check if employee.id exists in the array
          const idExists = employeePreparedSalaries?.some((obj) => obj.employee === employee.id);

          return dateOfJoiningOfEmployee <= comparisonDate && idExists;
        }
      } else {
        return false;
      }
    });

    return filteredData;
  }, [employeePersonalDetails, selectedDate, employeePreparedSalaries, filterYearlyAdvanceEmployees]);

  const generateButtonClicked = async (values, formikBag) => {
    setShowLoadingBar(true);
    const toSend = {
      ...values,
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
          `${import.meta.env.VITE_BACKEND_URL}api/generate-salary-overtime-sheet`,
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
                `${import.meta.env.VITE_BACKEND_URL}api/generate-salary-overtime-sheet`,
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
                dispatch(
                  alertActions.createAlert({
                    message: 'Generated',
                    type: 'Success',
                    duration: 8000,
                  })
                );

                window.open(pdfUrl, '_blank');
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
        } else if (!response.ok) {
          console.error('Request failed with status: ', response.status);
          // console.error(response.);
          response.json().then((data) => {
            console.log('Error:', data.detail);

            if (response.status == 404) {
              dispatch(
                alertActions.createAlert({
                  message: data.detail,
                  type: 'Error',
                  duration: 5000,
                })
              );
            }
          });

          // throw new Error('Request failed');
        } else if (response.status == 200) {
          if (values.reportType == 'payment_sheet' && values.filters.format == 'xlsx') {
            let fileName = 'payment_sheet.xlsx';
            const excelData = await response.arrayBuffer();
            const excelBlob = new Blob([excelData], {
              type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            });
            const excelUrl = URL.createObjectURL(excelBlob);

            const downloadLink = document.createElement('a');
            downloadLink.href = excelUrl;
            downloadLink.download = fileName;
            document.body.appendChild(downloadLink);

            // Trigger the click event on the anchor element to initiate download
            downloadLink.click();

            // Remove the temporary anchor element from the DOM
            document.body.removeChild(downloadLink);
          } else {
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
        }
      } catch (error) {
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

  // const selectedRows = table.getSelectedRowModel().flatRows;
  // console.log(selectedRows);

  const generateInitialValues = () => {
    const initialValues = {
      filters: {
        groupBy: 'none',
        sortBy: 'paycode',
        paymentMode: 'all',
        resignationFilter: 'all',
        language: 'english',
        format: 'pdf',
        overtime: 'with_ot',
      },
      reportType: 'salary_sheet',
    };
    return initialValues;
  };
  const initialValues = useMemo(() => generateInitialValues(), []);

  useEffect(() => {
    setShowLoadingBar(
      isLoadingEmployeePersonalDetails ||
      isLoadingEmployeesForYearlyAdvanceReport || isFetchingEmployeesForYearlyAdvanceReport
    );
  }, [isLoadingEmployeePersonalDetails,
    isLoadingEmployeesForYearlyAdvanceReport, isFetchingEmployeesForYearlyAdvanceReport
  ]);



  if (globalCompany.id == null) {
    return (
      <section className="flex flex-col items-center">
        <h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
          Please Select a Company First
        </h4>
      </section>
    );
  } else if (isLoadingEmployeePersonalDetails, isLoadingEmployeesForYearlyAdvanceReport) {
    return <div></div>;
  } else {
    return (
      <section className="mt-4">
        <div className="ml-4 flex flex-row flex-wrap place-content-between">
          <div className="mr-4">
            <h1 className="text-3xl font-medium">Salary Overtime Sheet</h1>
            <p className="my-2 text-sm">Create Salary and Overtime Sheets here</p>
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
              component={(props) => <FilterOptions {...props} setFilterYearlyAdvanceEmployees={setFilterYearlyAdvanceEmployees} />}
            />
          </div>
        </div>
      </section>
    );
  }
};

export default SalaryOvertimeSheet;
