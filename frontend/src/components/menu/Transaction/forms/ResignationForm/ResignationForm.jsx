import React, { useState, useMemo, useEffect } from 'react';
import { FaSearch, FaTimes } from 'react-icons/fa';
import { useDispatch, useSelector } from 'react-redux';
import { useGetEmployeePersonalDetailsQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import {
  useAddFullAndFinalMutation,
  useGenerateFullAndFinalReportMutation,
} from '../../../../authentication/api/fullAndFinalApiSlice';
import {
  createColumnHelper,
  getCoreRowModel,
  useReactTable,
  getSortedRowModel,
  getFilteredRowModel,
} from '@tanstack/react-table';
import { Formik } from 'formik';
import { useOutletContext } from 'react-router-dom';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { authActions } from '../../../../authentication/store/slices/auth';
import ConfirmationModal from '../../../../UI/ConfirmationModal';
import Modal from '../../../../UI/Modal';
import { ConfirmationModalSchema } from '../TimeUpdationForm/TimeUpdationSchema';
import { useUpdateResignationMutation, useUnresignMutation } from '../../../../authentication/api/resignationApiSlice';
import FullAndFinal from './FullAndFinal';
import DataGrid from '../../../../UI/DataGrid';
import Dropdown from '../../../../UI/Dropdown';
import Button from '../../../../UI/Button';

const ResignDateToBeAssigned = ({ getValue, row, column, table }) => {
  const initialValue = getValue() == null ? '' : getValue();
  const [value, setValue] = useState('');
  useEffect(() => {
    setValue(initialValue);
  }, [initialValue]);
  const onBlur = () => {
    table.options.meta?.updateData(row.original.id, column.id, value);
  };
  return (
    <>
      {/* {console.log(row.original.dateOfJoining)} */}
      {row.original.resignationDate === null && (
        <>
          <input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onBlur={onBlur}
            className={column.columnDef.meta?.style || 'text'}
            type={column.columnDef.meta?.type || 'text'}
          />
          {value != '' && value < row.original.dateOfJoining && (
            <p className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
              Cannot be smaller than DOJ
            </p>
          )}
        </>
      )}
    </>
  );
};

const ResignationForm = () => {
  const globalCompany = useSelector((state) => state.globalCompany);
  const auth = useSelector((state) => state.auth);
  const dispatch = useDispatch();
  const [showLoadingBar, setShowLoadingBar] = useOutletContext();
  const [employeeToResign, setEmployeeToResign] = useState(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [showFullAndFinalModal, setShowFullAndFinalModal] = useState(false);
  const [fullAndFinalEmployeeId, setFullAndFinalEmployeeId] = useState(null);
  const [confirmType, setConfirmType] = useState(null);
  const [data, setData] = useState([]);
  const [globalFilter, setGlobalFilter] = useState('');
  const [employeeStatus, setEmployeeStatus] = useState('all');

  const [
    updateResignation,
    {
      isLoading: isUpdatingResignation,
      // isError: errorRegisteringRegular,
      isSuccess: isUpdateResignationSuccess,
    },
  ] = useUpdateResignationMutation();

  const [
    addFullAndFinal,
    {
      isLoading: isAddingFullAndFinal,
      // isError: errorRegisteringRegular,
      isSuccess: isAddFullAndFinalSuccess,
    },
  ] = useAddFullAndFinalMutation();

  const [
    unresign,
    {
      isLoading: isUnresigning,
      // isError: errorRegisteringRegular,
      isSuccess: isUnresignSuccess,
    },
  ] = useUnresignMutation();

  const {
    data: fetchedData,
    isLoading,
    isSuccess,
    isError,
    error,
    isFetching,
    refetch,
  } = useGetEmployeePersonalDetailsQuery(globalCompany);

  const columnHelper = createColumnHelper();

  const columns = useMemo(() => {
    const columns = [
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
        meta: { headerClassName: 'whitespace-nowrap' },
        //   footer: info => info.column.id,
      }),
      columnHelper.accessor('designation', {
        header: () => 'Designation',
        cell: (props) => props.renderValue(),
        //   footer: info => info.column.id,
      }),
      {
        header: 'Date',
        cell: (props) =>
          props.row.original.resignationDate == null ? (
            <ResignDateToBeAssigned
              getValue={props.getValue}
              row={props.row}
              column={props.column}
              table={props.table}
            />
          ) : (
            ''
          ),
        meta: {
          type: 'date',
          style: 'inline w-32 cursor-pointer rounded border-2 border-gray-800 border-opacity-25 bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-700 dark:focus:border-opacity-75',
        },
      },
      columnHelper.display({
        id: 'actions',
        header: () => 'Actions',
        cell: (props) => {
          return (
            <div className="flex justify-center gap-2 whitespace-nowrap">
              {props.row.original.resignationDate == null && (
                <>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => {
                      if (props.row.original.Date) {
                        setEmployeeToResign(props.row.original.id);
                        setShowConfirmModal(true);
                        setConfirmType('resign');
                      } else {
                        dispatch(
                          alertActions.createAlert({
                            message: 'Fill the Date for resign first',
                            type: 'Error',
                            duration: 5000,
                          })
                        );
                      }
                    }}
                  >
                    Resign
                  </Button>
                </>
              )}
              {props.row.original.resignationDate != null && (
                <>
                  <Button
                    size="sm"
                    className="whitespace-nowrap"
                    onClick={() => {
                      // setEmployeeToResign(props.row.original.id);
                      setShowFullAndFinalModal(true);
                      setFullAndFinalEmployeeId(props.row.original.id);
                    }}
                  >
                    Full & Final
                    {/* {false && (
									<FaCircleNotch className="my-auto ml-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
								)} */}
                  </Button>
                  <Button
                    variant="accent"
                    size="sm"
                    onClick={() => {
                      setEmployeeToResign(props.row.original.id);
                      setShowConfirmModal(true);
                      setConfirmType('unresign');
                    }}
                  >
                    Unresign
                  </Button>
                  {/* {false && (
									<FaCircleNotch className="my-auto ml-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
								)} */}
                </>
              )}
            </div>
          );
        },
      }),
    ];

    return columns;
  }, []);

  useEffect(() => {
    if (fetchedData != undefined) {
      setData(fetchedData);
    }
    // fetchedData != undefined ? setData(fetchedData) : '';
  }, [fetchedData]);

  const filteredData = useMemo(() => {
    if (employeeStatus === 'current') {
      return data.filter((employee) => !employee.resignationDate);
    }
    if (employeeStatus === 'resigned') {
      return data.filter((employee) => Boolean(employee.resignationDate));
    }
    return data;
  }, [data, employeeStatus]);

  const table = useReactTable({
    data: filteredData,
    columns,
    initialState: {
      sorting: [{ id: 'name', desc: false }],
    },
    state: { globalFilter },
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getSortedRowModel: getSortedRowModel(),
    enableSortingRemoval: false,
    meta: {
      updateData: (employeeId, columnId, value) => {
        setData((old) =>
          old.map((row) => {
            if (row.id === employeeId) {
              return {
                ...row,
                [columnId]: value,
              };
            }
            return row;
          })
        );
      },
    },
  });

  const saveFullAndFinalButtonClicked = async (values, formikBag) => {
    console.log(values);
    try {
      const data = await addFullAndFinal({
        ...values,
        elEncashmentDays: values.elEncashmentDays * 2,
        company: globalCompany.id,
        employee: fullAndFinalEmployeeId,
      }).unwrap();
      dispatch(
        alertActions.createAlert({
          message: 'Saved',
          type: 'Success',
          duration: 3000,
        })
      );
    } catch (err) {
      console.log(err);
      let message = 'Error Occurred';
      dispatch(
        alertActions.createAlert({
          message: message,
          type: 'Error',
          duration: 5000,
        })
      );
    }
  };

  const generateButtonClicked = async (values, formikBag) => {
    setShowLoadingBar(true);
    const toSend = {
      company: globalCompany.id,
      employee: fullAndFinalEmployeeId,
    };
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

    const generateFullAndFinalReport = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}api/generate-full-and-final-report`,
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
                    message: 'No Full And Final Found',
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
        } else if (response.status == 200) {
          const pdfData = await response.arrayBuffer();
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

    // Call the generateFullAndFinalReport function to initiate the request
    generateFullAndFinalReport();
  };

  const resignButtonClicked = async (formikBag) => {
    const employee = data.find((row) => row.id === employeeToResign);
    let toSend = {
      company: globalCompany.id,
      employee: employeeToResign,
      resigned: true,
      resignationDate: employee.Date,
    };

    console.log(employee.Date);
    try {
      const data = await updateResignation(toSend).unwrap();
      table.options.meta?.updateData(employeeToResign, 'Date', '');

      dispatch(
        alertActions.createAlert({
          message: `Resigned Successfully`,
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
    setShowConfirmModal(false);
    setEmployeeToResign(null);
    // setShowConfirmModal(true);

    // deleteShift({ id: id, company: globalCompany.id });
  };

  const generateFullAndFinalInitialValues = () => {
    let initialValues = {
      fullAndFinalDate: '',
      elEncashmentDays: 0,
      elEncashmentAmount: 0,
      bonusPrevYear: 0,
      bonusCurrentYear: 0,
      gratuity: 0,
      serviceCompensationDays: 0,
      serviceCompensationAmount: 0,
      earningsNoticePeriodDays: 0,
      earningsNoticePeriodAmount: 0,
      otMin: 0,
      otAmount: 0,
      earningsOthers: 0,
      deductionsNoticePeriodDays: 0,
      deductionsNoticePeriodAmount: 0,
      deductionsOthers: 0,
    };
    return initialValues;
  };

  const fullAndFinalInitialValues = useMemo(() => generateFullAndFinalInitialValues(), []);

  const unresignButtonClicked = async (formikBag) => {
    try {
      const data = await unresign({
        company: globalCompany.id,
        employee: employeeToResign,
      }).unwrap();
      dispatch(
        alertActions.createAlert({
          message: `Unresigned Successfully`,
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
    setShowConfirmModal(false);
    setEmployeeToResign(null);
    // setShowConfirmModal(true);

    // deleteShift({ id: id, company: globalCompany.id });
  };

  if (globalCompany.id == null) {
    return (
      <section className="flex flex-col items-center">
        <h4 className="text-x mt-10 font-bold text-redAccent-500 dark:text-redAccent-600">
          Please Select a Company First
        </h4>
      </section>
    );
  }
  if (isLoading) {
    return <div></div>;
  } else {
    return (
      <section
        className="mx-4 flex h-[calc(100dvh-56px)] min-h-0 flex-col overflow-hidden sm:mx-5"
        aria-labelledby="resignation-heading"
      >
        <header className="flex shrink-0 flex-wrap items-center justify-between gap-3 border-b border-zinc-200 pb-2 dark:border-zinc-800">
          <div className="mr-4">
            <h1
              id="resignation-heading"
              className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100"
            >
              Resignation
            </h1>
            <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
              Change status of employees to resign here
            </p>
          </div>
        </header>
        <div className="relative z-30 mx-auto mt-3 flex w-full max-w-6xl shrink-0 flex-col gap-2 sm:flex-row sm:items-center">
          <div className="group relative min-w-0 flex-1">
            <FaSearch
              aria-hidden="true"
              className="pointer-events-none absolute left-3.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-zinc-400 transition-colors group-focus-within:text-teal-500 dark:text-zinc-500 dark:group-focus-within:text-teal-400"
            />
            <input
              type="search"
              value={globalFilter}
              onChange={(event) => setGlobalFilter(event.target.value)}
              className="h-10 w-full appearance-none rounded-xl border border-zinc-200 bg-zinc-100/80 pl-10 pr-10 text-sm text-zinc-900 outline-none transition placeholder:text-zinc-400 hover:border-zinc-300 focus:border-teal-500 focus:bg-white focus:ring-4 focus:ring-teal-500/10 dark:border-zinc-700 dark:bg-zinc-800/80 dark:text-zinc-100 dark:placeholder:text-zinc-500 dark:hover:border-zinc-600 dark:focus:border-teal-500 dark:focus:bg-zinc-800 dark:focus:ring-teal-500/10 [&::-webkit-search-cancel-button]:appearance-none"
              placeholder="Search by name, paycode, or ACN"
              aria-label="Search employees"
            />
            {globalFilter && (
              <button
                type="button"
                onClick={() => setGlobalFilter('')}
                className="absolute right-2.5 top-1/2 flex h-6 w-6 -translate-y-1/2 items-center justify-center rounded-lg text-zinc-400 transition hover:bg-zinc-200 hover:text-zinc-700 focus:outline-none focus:ring-2 focus:ring-teal-500/40 dark:hover:bg-zinc-700 dark:hover:text-zinc-100"
                aria-label="Clear employee search"
              >
                <FaTimes className="h-3 w-3" />
              </button>
            )}
          </div>
          <div className="flex w-full items-center gap-2 sm:w-auto">
            <span className="hidden whitespace-nowrap pl-1 text-xs font-semibold uppercase tracking-wider text-zinc-400 dark:text-zinc-500 sm:inline">
              Status
            </span>
            <Dropdown
              value={employeeStatus}
              onChange={(event) => setEmployeeStatus(event.target.value)}
              wrapperClassName="w-full sm:w-[12.5rem]"
              className="h-10 rounded-xl border-zinc-200 bg-zinc-100/80 dark:border-zinc-700 dark:bg-zinc-800/80"
              aria-label="Filter employees by employment status"
            >
              <option value="all">All employees</option>
              <option value="current">Current employees</option>
              <option value="resigned">Resigned employees</option>
            </Dropdown>
          </div>
        </div>
        <DataGrid
          table={table}
          getRowId={(row) => row.original.id}
          getRowClassName={(row) => (row.original.resignationDate ? 'text-redAccent-500' : '')}
          maxHeightClassName="max-h-full"
          wrapperClassName="relative z-0 flex min-h-0 flex-1"
          containerClassName="h-full w-full max-w-6xl"
          tableClassName="text-sm [&_td]:whitespace-nowrap [&_td]:px-2 [&_td_div]:text-sm [&_th]:px-2 [&_th]:py-4"
          density="compact"
          emptyMessage="No employees found"
        />
        <Modal
          className="w-full"
          maxWidth="lg"
          isOpen={showConfirmModal}
          onClose={() => {
            setShowConfirmModal(false);
            setEmployeeToResign(null);
          }}
        >
          <div className="p-5">
            <Formik
              initialValues={{ userInput: '' }}
              validationSchema={ConfirmationModalSchema}
              onSubmit={confirmType == 'resign' ? resignButtonClicked : unresignButtonClicked}
              component={(props) => (
                <ConfirmationModal
                  {...props}
                  displayHeading={
                    confirmType == 'resign'
                      ? 'Resign Employee (All the attendances for this employee after the resignation date will be deleted)'
                      : 'Unresign Employee'
                  }
                  setShowConfirmModal={setShowConfirmModal}
                />
              )}
            />
          </div>
        </Modal>
        <Modal
          className="w-full min-w-0"
          maxWidth="8xl"
          isOpen={showFullAndFinalModal}
          onClose={() => {
            setShowFullAndFinalModal(false);
          }}
        >
          <div className="w-max p-4">
            <Formik
              initialValues={fullAndFinalInitialValues}
              validationSchema={''}
              onSubmit={saveFullAndFinalButtonClicked}
              component={(props) => (
                <FullAndFinal
                  {...props}
                  setShowFullAndFinalModal={setShowFullAndFinalModal}
                  fullAndFinalEmployeeId={fullAndFinalEmployeeId}
                  globalCompany={globalCompany}
                  generateButtonClicked={generateButtonClicked}
                />
              )}
            />
          </div>
        </Modal>
      </section>
    );
  }
};

export default ResignationForm;
