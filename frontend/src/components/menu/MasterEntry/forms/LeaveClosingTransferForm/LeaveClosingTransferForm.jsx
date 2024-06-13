import React, { useState, useMemo, useEffect } from 'react';
import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
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
import EmployeeTable from '../../../Reports/forms/EmployeeTable';
import MonthYearSelector from '../../../Reports/forms/MonthYearSelector';
import { FaCheck, FaWindowMinimize } from 'react-icons/fa';
//import YearSelector from '../LeaveOpeningEntry/YearSelector';
import FromYearSelector from './FromYearSelector';
import FilterOptions from './FilterOptions';
import { useTransferLeaveClosingMutation } from '../../../../authentication/api/leaveClosingTransferApiSlice';

const LeaveClosingTransferForm = () => {
  const auth = useSelector((state) => state.auth);
  const globalCompany = useSelector((state) => state.globalCompany);
  console.log(globalCompany)
  const dispatch = useDispatch();
  const [showLoadingBar, setShowLoadingBar] = useOutletContext();



  const {
    data: employeePersonalDetails,
    isLoading: isLoadingEmployeePersonalDetails,
    isSuccess: isSuccessEmployeePersonalDetails,
  } = useGetEmployeePersonalDetailsQuery(globalCompany);
  // console.log(employeePersonalDetails);
  const [year, setYear] = useState(new Date().getFullYear())

  const [
    transferLeaveClosing,
    {
      isLoading: isTransferringLeaveClosing,
      // isError: errorRegisteringRegular,
      isSuccess: isTransferringLeaveClosingSuccess,
    },
  ] = useTransferLeaveClosingMutation();


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
  console.log(year)
  const data = useMemo(() => {
    if (!employeePersonalDetails || !year) return [];

    const filteredData = employeePersonalDetails.filter((employee) => {
      if (employee.dateOfJoining) {
        const comparisonDate = new Date(Date.UTC(year, 0, 1));
        // Extract the year and month from the original dateOfJoining
        const [dojYear, month] = employee.dateOfJoining.split('-').map(Number);
        if (employee.resignationDate) {
          const [resignYear, resignMonth] = employee.resignationDate.split('-').map(Number);
          const resignDate = new Date(Date.UTC(resignYear, resignMonth, 0));
          //if (resignDate < comparisonDate) {
          if (resignYear <= year) {
            return false;

          }
        }
        const dateOfJoiningOfEmployee = new Date(Date.UTC(dojYear, month - 1, 1));
        //return dateOfJoiningOfEmployee <= comparisonDate;
        return dojYear <= year;
      } else {
        return false;
      }
    });

    return filteredData;
  }, [employeePersonalDetails, year]);

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

  const generateButtonClicked = async (values, formikBag) => {
    console.log(values);
    let toSend = {
      leaveIds: [...values.leavesSelected],
      employeeIds: table.getSelectedRowModel().flatRows.map((row) => row.id),
      company: globalCompany.id,
      fromYear: year
    }
    console.log(toSend);
    if (toSend.employeeIds.length != 0 && toSend.leaveIds.length != 0) {
      try {
        const data = await transferLeaveClosing(toSend).unwrap();
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
    } else {
      dispatch(
        alertActions.createAlert({
          message: 'Employees or Leaves are not selected',
          type: 'Error',
          duration: 3000,
        })
      );

    }
  }

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
      leavesSelected: [],
    };
    return initialValues;
  };
  const initialValues = useMemo(() => generateInitialValues(), []);
  return (
    <section className="mt-4">
      <div className="ml-4 flex flex-row flex-wrap place-content-between">
        <div className="mr-4">
          <h1 className="text-3xl font-medium">Leave Closing Transfer</h1>
          <p className="my-2 text-sm">Transfer Leaves from one year to the next here.</p>
        </div>
      </div>
      <div className="ml-4">
        <div className='w-2/5 flex flex-row justify-between '>
          <FromYearSelector year={year} setYear={setYear} earliestMonthAndYear={earliestMonthAndYear} />
          <div className=''>
            <p
              className="mt-2.5 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
            >
              To Year : <span className='text-amber-500'>{parseInt(year) + 1}</span>
            </p>

          </div>

        </div>
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
            component={(props) => <FilterOptions {...props} globalCompany={globalCompany} />}
          />
        </div>

      </div>
    </section>

  )
}

export default LeaveClosingTransferForm
