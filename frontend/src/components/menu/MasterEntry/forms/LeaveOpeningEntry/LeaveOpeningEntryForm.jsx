import React, { useState, useMemo, useEffect } from 'react';
import EmployeeTable from './EmployeeTable';
import { FaCheck, FaWindowMinimize } from 'react-icons/fa';
import { useDispatch, useSelector } from 'react-redux';
import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import {
  useAddFullAndFinalMutation,
  useGenerateFullAndFinalReportMutation,
} from '../../../../authentication/api/fullAndFinalApiSlice';
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
import { useOutletContext } from 'react-router-dom';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { authActions } from '../../../../authentication/store/slices/auth';
//import ConfirmationModal from '../../../../UI/ConfirmationModal';
import ReactModal from 'react-modal';
//import { ConfirmationModalSchema } from '../TimeUpdationForm/TimeUpdationSchema';
import { useUpdateResignationMutation, useUnresignMutation } from '../../../../authentication/api/resignationApiSlice';
import { FaCircleNotch } from 'react-icons/fa';
import {
  useGetLeaveGradesQuery,
  useAddLeaveGradeMutation,
  useUpdateLeaveGradeMutation,
  useDeleteLeaveGradeMutation,
} from '../../../../authentication/api/leaveGradeEntryApiSlice';
import { useAddOrUpdateLeaveOpeningMutation } from '../../../../authentication/api/leaveOpeningApiSlice';
import {
  useGetAllEmployeeLeaveOpeningQuery,
} from '../../../../authentication/api/timeUpdationApiSlice';
import YearSelector from './YearSelector';
import LeaveOpeningCountCell from './LeaveOpeningCountCell';


ReactModal.setAppElement('#root');

const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};





const LeaveOpeningEntryForm = () => {
  const globalCompany = useSelector((state) => state.globalCompany);
  const auth = useSelector((state) => state.auth);
  const dispatch = useDispatch();
  const [showLoadingBar, setShowLoadingBar] = useOutletContext();
  const [employeeToResign, setEmployeeToResign] = useState(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [data, setData] = useState([]);
  const [initialData, setInitialData] = useState([])
  const [year, setYear] = useState(new Date().getFullYear())
  const {
    data: fetchedData,
    isLoading,
    isSuccess,
    isError,
    error,
    isFetching,
    refetch,
  } = useGetEmployeePersonalDetailsQuery(globalCompany);

  const {
    data: leaveGrades,
    isLoading: isLoadingLeaveGrades,
    isSuccess: isSuccessLeaveGrades,
    isError: isErrorLeaveGrades,
  } = useGetLeaveGradesQuery(globalCompany);

  const [
    addOrUpdateLeaveOpening,
    {
      isLoading: isAddingOrUpdatingLeaveOpening,
      // isError: errorRegisteringRegular,
      isSuccess: isAddingOrUpdatingLeaveOpeningSuccess,
    },
  ] = useAddOrUpdateLeaveOpeningMutation();

  const earliestMonthAndYear = useMemo(() => {
    let earliestDate = Infinity; // Initialize earliestDate to a very large value
    let earliestMonth = '';
    let earliestYear = '';
    if (fetchedData) {
      for (const employee of fetchedData) {
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
  }, [fetchedData]);

  const {
    data: allEmployeeLeaveOpening,
    isLoading: isLoadingAllEmployeeLeaveOpening,
    isSuccess: isAllEmployeeLeaveOpeningSuccess,
    isFetching: isFetchingAllEmployeeLeaveOpening,
  } = useGetAllEmployeeLeaveOpeningQuery(
    {
      company: globalCompany.id,
      year: year,
    },
    {
      skip: globalCompany === null || globalCompany === '' || year == '',
    }
  );


  const columnHelper = createColumnHelper();

  const columns = useMemo(() => {
    const columns = [
      columnHelper.accessor('id', {
        header: () => 'ID',
        cell: (props) => props.renderValue(),
        enableHiding: true,
        //   footer: info => info.column.id,
      }),

      columnHelper.accessor('paycode', {
        header: () => 'Paycode',
        cell: (props) => props.renderValue(),
        //   footer: props => props.column.id,
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
      columnHelper.accessor('dateOfJoining', {
        header: () => 'DOJ',
        cell: (props) => props.renderValue(),
        //   footer: info => info.column.id,
      }),
      columnHelper.accessor('resignationDate', {
        header: () => 'Resign Date',
        cell: (props) => props.renderValue(),
        //   footer: info => info.column.id,
      }),
      columnHelper.accessor('designation', {
        header: () => 'Designation',
        cell: (props) => props.renderValue(),
        //   footer: info => info.column.id,
      }),

    ];
    const dynamicColumns = (leaveGrades ?? []).map(grade => {
      if (grade.generateFrequency !== null) {
        //console.log(grade.id)
        return columnHelper.accessor(`${grade.id}`, {
          id: grade.id,
          header: () => `${grade.name}`,
          cell: (props) => {
            // //console.log(props?.cell?.row?.original?.id)
            // const foundEmployee = allEmployeeLeaveOpening?.find(employee => {
            //   return employee.employee === props?.cell?.row?.original?.id && employee.leave === grade.id;
            // });
            //
            // const result = foundEmployee ? foundEmployee.leaveCount : 0;
            const resignationDateString = props.row.original.resignationDate
            const resignationYear = resignationDateString?.split("-")[0]
            return props.row.original.resignationDate == null || (resignationYear != undefined && resignationYear >= year) ? (
              <LeaveOpeningCountCell
                getValue={props.getValue}
                row={props.row}
                column={props.column}
                table={props.table}
              />
            ) : (
              ''
            );
          },

          meta: {
            type: 'number',
          }
          //             style: classNames(value != undefined && value > 0 ? 'text-green-400' : '', 'inline w-10 cursor-pointer rounded border-2 border-gray-800 border-opacity-25 bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-700 dark:focus:border-opacity-75'),
        })
      }
      // Return null for excluded columns
      return null;
    }).filter(column => column !== null); // Filter out null values


    return [...columns, ...dynamicColumns];
  }, [fetchedData, allEmployeeLeaveOpening, leaveGrades]);

  useEffect(() => {
    if (fetchedData !== undefined && allEmployeeLeaveOpening !== undefined && leaveGrades != undefined) {
      // Create a copy of fetchedData to avoid mutating the original array
      const generativeLeaves = leaveGrades.filter((grade) => {
        return grade.generateFrequency !== null;
      });

      const updatedData = fetchedData.map(employee => {
        // Filter leave openings for the current employee
        const employeeLeaveOpenings = allEmployeeLeaveOpening.filter(opening => opening.employee === employee.id);

        // Create a new object to hold the updated employee data
        let updatedEmployee = { ...employee };

        // Iterate over each leave opening for the employee
        employeeLeaveOpenings.forEach(opening => {
          // Check if the leave id is not already present as a key in the employee object
          if (!(opening.leave in updatedEmployee)) {
            // Add the leave id as a key and its corresponding leave count as value
            updatedEmployee = { ...updatedEmployee, [opening.leave]: opening.leaveCount / 2 };
          }
        });
        generativeLeaves.forEach(leave => {
          if (!(leave.id in updatedEmployee)) {
            updatedEmployee = { ...updatedEmployee, [leave.id]: 0 };
          }
        });
        return updatedEmployee;
      });

      setData(updatedData);
      setInitialData(updatedData)
    } else {
      setData([]); // Set data to an empty array if fetchedData or allEmployeeLeaveOpening is undefined
    }
  }, [fetchedData, allEmployeeLeaveOpening, leaveGrades]);


  //console.log(allEmployeeLeaveOpening)



  // const data = useMemo(() => (fetchedData ? [...fetchedData] : []), [fetchedData]);

  const table = useReactTable({
    data,
    columns,
    initialState: {
      sorting: [{ id: 'name', desc: false }],
      columnVisibility: { id: false },
    },
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    enableSortingRemoval: false,
    meta: {
      updateData: (rowIndex, columnId, value) =>
        setData((prev) =>
          prev.map((row, index) =>
            index == rowIndex
              ? {
                ...prev[rowIndex],
                [columnId]: value,
              }
              : row
          ))
    }
    // meta: {
    //   updateData: (rowIndex, columnId, value) => {
    //     setData((old) =>
    //       old.map((row, index) => {
    //         if (index === rowIndex) {
    //           return {
    //             ...old[rowIndex],
    //             [columnId]: value,
    //           };
    //         }
    //         return row;
    //       })
    //     );
    //   },
    //},
  });

  // console.log(table.getRowModel().rows[0]?._getAllCellsByColumnId())
  //
  const findAndFormatChangedData = (generativeLeaves) => {
    const initialLeaveCounts = {};
    initialData.forEach(employee => {
      initialLeaveCounts[employee.id] = { ...employee };
    });

    const toSend = {
      leaveOpenings: [],
      company: globalCompany.id,
      year: year
    };

    data.forEach(employee => {
      const initialEmployee = initialLeaveCounts[employee.id];
      if (!initialEmployee) {
        generativeLeaves.forEach(leave => {
          const leaveId = leave.id;
          const leaveCount = employee[leaveId];
          toSend.leaveOpenings.push({
            employee: employee.id,
            leave: leaveId,
            leave_count: leaveCount
          });
        });
      } else {
        generativeLeaves.forEach(leave => {
          const leaveId = leave.id;
          const initialLeaveCount = initialEmployee[leaveId];
          const currentLeaveCount = employee[leaveId];
          if (initialLeaveCount !== currentLeaveCount) {
            toSend.leaveOpenings.push({
              employee: employee.id,
              leave: leaveId,
              leave_count: currentLeaveCount
            });
          }
        });
      }
    });

    return toSend;
  };

  const saveButtonClicked = async () => {
    const generativeLeaves = leaveGrades.filter((grade) => {
      return grade.generateFrequency !== null;
    });
    const toSend = findAndFormatChangedData(generativeLeaves)
    if (initialData.length != 0) {
      console.log('yes ready')
    }

    console.log(toSend);
    if (toSend.leaveOpenings.length != 0) {
      try {
        const data = await addOrUpdateLeaveOpening(toSend).unwrap();
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
          message: 'Already Saved',
          type: 'Success',
          duration: 3000,
        })
      );

    }
  }
  useEffect(() => {
    setShowLoadingBar(
      isLoadingAllEmployeeLeaveOpening ||
      isAddingOrUpdatingLeaveOpening ||
      isLoading ||
      isLoadingLeaveGrades
    );
  }, [isLoadingAllEmployeeLeaveOpening,
    isAddingOrUpdatingLeaveOpening,
    isLoading,
    isLoadingLeaveGrades
  ]);



  if (globalCompany.id == null) {
    return (
      <section className="flex flex-col items-center">
        <h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
          Please Select a Company First
        </h4>
      </section>
    );
  }
  if (isLoading || isLoadingLeaveGrades || isLoadingAllEmployeeLeaveOpening) {
    return <div></div>;
  } else {
    return (
      <section className="mt-4 w-full">
        <div className="ml-4 flex flex-row flex-wrap place-content-between">
          <div className="mr-4">
            <h1 className="text-3xl font-medium">Leave Opening</h1>
            <p className="my-2 text-sm">Manage leave openings of the employees here</p>
          </div>
        </div>
        <main className='mx-4'>
          <div className='max-w-7xl mx-auto flex justify-between'>

            <YearSelector year={year} setYear={setYear} earliestMonthAndYear={earliestMonthAndYear} />
            <div>
              {isAddingOrUpdatingLeaveOpening && (
                <FaCircleNotch className="my-auto mr-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
              )}
              <button
                className={classNames(
                  true ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
                  'h-8 w-32 rounded bg-teal-500 py-1 px-4 text-sm font-medium dark:bg-teal-700'
                )}
                type="submit"
                //disabled={!isValid}
                onClick={saveButtonClicked}
              >
                Save
              </button></div>
          </div>
          <EmployeeTable table={table} flexRender={flexRender} />
        </main>
      </section>)
  }

}

export default LeaveOpeningEntryForm
