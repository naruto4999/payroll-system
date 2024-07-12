import React, { useState, useMemo, useEffect } from 'react';
import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import { useGetPreparedSalariesQuery } from '../../../../authentication/api/salaryOvertimeSheetApiSlice';
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

const PfEsiReports = () => {
  const auth = useSelector((state) => state.auth);
  const globalCompany = useSelector((state) => state.globalCompany);
  const dispatch = useDispatch();
  const [showLoadingBar, setShowLoadingBar] = useOutletContext();
  const [pfEsiFilter, setPfEsiFilter] = useState('pfAllow');
  const [reportType, setReportType] = useState('pf_statement');
  const [selectedDate, setSelectedDate] = useState({
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1,
  });
  console.log(pfEsiFilter);

  const {
    data: employeePreparedSalaries,
    isLoading: isLoadingEmployeePreparedSalaries,
    isSuccess: isSuccessEmployeePreparedSalaries,
  } = useGetPreparedSalariesQuery({ company: globalCompany.id, month: selectedDate.month, year: selectedDate.year });
  console.log(employeePreparedSalaries);

  const {
    data: employeePersonalDetails,
    isLoading: isLoadingEmployeePersonalDetails,
    isSuccess: isSuccessEmployeePersonalDetails,
  } = useGetEmployeePersonalDetailsQuery(globalCompany);

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
      if (employee.dateOfJoining && (employee[`${pfEsiFilter}`] == true || reportType == 'pf_exempt')) {
        const comparisonDate = new Date(Date.UTC(selectedDate.year, parseInt(selectedDate.month) - 1, 1));
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
        // const idExists = employeePreparedSalaries?.some((obj) => {
        //   console.log(obj)
        //   // if (pfEsiFilter == 'pfAllow' && reportType == 'pf_exempt') {
        //   //   console.log(obj.pfDeducted)
        //   //   return obj.pfDeducted === 0
        //   // }
        //   return obj.employee === employee.id
        // });
        const employeePreparedSalary = employeePreparedSalaries?.find((obj) => {
          return obj.employee === employee.id;
        });

        // if (employeePreparedSalary) {
        //   // Do something with employeePreparedSalary
        //   console.log(employeePreparedSalary);
        // }

        if (reportType == 'pf_exempt') {
          return dateOfJoiningOfEmployee <= comparisonDate && employeePreparedSalary && employeePreparedSalary?.pfDeducted == 0;
        }
        return dateOfJoiningOfEmployee <= comparisonDate && employeePreparedSalary;
      } else {
        return false;
      }
    });

    return filteredData;
  }, [employeePersonalDetails, selectedDate, pfEsiFilter, employeePreparedSalaries, reportType]);

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
        // groupBy: 'none',
        sortBy: 'paycode',
        format: 'xlsx',
        // resignationFilter: 'all',
      },
      reportType: 'pf_statement',
    };
    return initialValues;
  };

  const initialValues = useMemo(() => generateInitialValues(), []);

  const generateButtonClicked = async (values, formikBag) => {
    setShowLoadingBar(true);
    // console.log(values);
    const toSend = {
      ...values,
      filters: {
        ...values.filters,
        // monthFromDate: parseInt(values.filters.monthFromDate),
        // monthToDate: parseInt(values.filters.monthToDate),
        // date: values.filters.date === '' ? null : values.filters.date,
      },
      employee_ids: table.getSelectedRowModel().flatRows.map((row) => row.id),
      company: globalCompany.id,
      month: parseInt(selectedDate.month),
      year: selectedDate.year,
    };
    console.log(toSend);
    let fileName = '';

    const reportTypeFormatMap = {
      pf_statement: {
        default: 'pf_statement.xlsx',
        txt: 'pf_statement.txt',
      },
      esi_statement: 'esi_statement.xlsx',
      pf_exempt: 'pf_exempt.xlsx',
    };

    const reportType = values.reportType;
    const format = values.filters?.format;

    if (reportType in reportTypeFormatMap) {
      if (typeof reportTypeFormatMap[reportType] === 'object') {
        fileName = reportTypeFormatMap[reportType][format] || reportTypeFormatMap[reportType].default;
      } else {
        fileName = reportTypeFormatMap[reportType];
      }
    }

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

    const generateReport = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}api/generate-pf-esi-reports`,
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
                dispatch(
                  alertActions.createAlert({
                    message: 'Generated',
                    type: 'Success',
                    duration: 8000,
                  })
                );
                const pdfData = await refreshedResponse.arrayBuffer();
                const pdfBlob = new Blob([pdfData], { type: 'application/pdf' });
                const pdfUrl = URL.createObjectURL(pdfBlob);
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
        } else if (response.status != 200) {
          console.error('Request failed with status: ', response.status);
          response.json().then((data) => {
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
        } else if (response.status === 200) {
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

          dispatch(
            alertActions.createAlert({
              message: 'Generated',
              type: 'Success',
              duration: 8000,
            })
          );
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

    // Call the generateReport function to initiate the request
    generateReport();
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
            <h1 className="text-3xl font-medium">PF / ESI Reports</h1>
            <p className="my-2 text-sm">Generate Reports related to PF and ESI</p>
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
              component={(props) => (
                <FilterOptions
                  {...props}
                  setReportType={setReportType}
                  pfEsiFilter={pfEsiFilter}
                  setPfEsiFilter={setPfEsiFilter}
                  selectedDate={selectedDate}
                />
              )}
            />
          </div>
        </div>
      </section>
    );
  }
};

export default PfEsiReports;
