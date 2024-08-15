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
import ConfirmationModal from '../../../../UI/ConfirmationModal';
import ReactModal from 'react-modal';
import { ConfirmationModalSchema } from '../TimeUpdationForm/TimeUpdationSchema';
import { useUpdateResignationMutation, useUnresignMutation } from '../../../../authentication/api/resignationApiSlice';
import FullAndFinal from './FullAndFinal';
import { FaCircleNotch } from 'react-icons/fa';

ReactModal.setAppElement('#root');

const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};

const ResignDateToBeAssigned = ({ getValue, row, column, table }) => {
  const initialValue = getValue() == null ? '' : getValue();
  const [value, setValue] = useState('');
  useEffect(() => {
    setValue(initialValue);
  }, [initialValue]);
  const onBlur = () => {
    table.options.meta?.updateData(row.index, column.id, value);
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
            <div className="flex justify-center gap-4">
              {props.row.original.resignationDate == null && (
                <>
                  <button
                    className={classNames(
                      true ? 'dark:hover:bg-redAccent-600' : 'opacity-40',
                      'h-10 w-fit rounded bg-redAccent-500 p-2 px-4 text-base font-medium   dark:bg-redAccent-700'
                    )}
                    type="submit"
                    // disabled={!isValid}
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
                    {false && (
                      <FaCircleNotch className="my-auto ml-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
                    )}
                  </button>
                </>
              )}
              {props.row.original.resignationDate != null && (
                <>
                  <button
                    className={
                      'h-10 w-fit rounded bg-teal-600 p-2 text-slate-100 hover:bg-teal-700 dark:bg-teal-700 dark:hover:bg-teal-600'
                    }
                    type="submit"
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
                  </button>
                  <button
                    className={
                      'h-10 w-fit rounded bg-blueAccent-400 p-2 font-medium text-slate-100 hover:bg-blueAccent-500 dark:bg-blueAccent-700 dark:hover:bg-blueAccent-600'
                    }
                    type="submit"
                    onClick={() => {
                      setEmployeeToResign(props.row.original.id);
                      setShowConfirmModal(true);
                      setConfirmType('unresign');
                    }}
                  >
                    Unresign
                  </button>
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
  }, [fetchedData]);

  useEffect(() => {
    if (fetchedData != undefined) {
      console.log('yes setting');
      setData(fetchedData);
    }
    // fetchedData != undefined ? setData(fetchedData) : '';
  }, [fetchedData]);

  // const data = useMemo(() => (fetchedData ? [...fetchedData] : []), [fetchedData]);

  const table = useReactTable({
    data,
    columns,
    initialState: {
      sorting: [{ id: 'name', desc: false }],
    },
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    enableSortingRemoval: false,
    meta: {
      updateData: (rowIndex, columnId, value) => {
        setData((old) =>
          old.map((row, index) => {
            if (index === rowIndex) {
              return {
                ...old[rowIndex],
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
    let row = table.getRowModel().rows.find((rowModel) => {
      if (rowModel.original.id === employeeToResign) {
        // console.log(rowModel.original);
        return true; // Return true to include the row
      }
      return false; // Return false to exclude the row
    });
    let toSend = {
      company: globalCompany.id,
      employee: employeeToResign,
      resigned: true,
      resignationDate: row.original.Date,
    };
    table.options.meta?.updateData(row.index, 'Date', '');

    console.log(row.original.Date);
    try {
      const data = await updateResignation(toSend).unwrap();

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
  console.log(fullAndFinalInitialValues);

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
      <section className="mt-4 w-full">
        <div className="ml-4 flex flex-row flex-wrap place-content-between">
          <div className="mr-4">
            <h1 className="text-3xl font-medium">Resignation</h1>
            <p className="my-2 text-sm">Change status of employees to resign here</p>
          </div>
        </div>
        <EmployeeTable table={table} flexRender={flexRender} />;
        <ReactModal
          className="items-left fixed inset-0 mx-2 my-auto flex h-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
          isOpen={showConfirmModal}
          onRequestClose={() => {
            setShowConfirmModal(false);
            setEmployeeToResign(null);
          }}
          style={{
            overlay: {
              backgroundColor: 'rgba(0, 0, 0, 0.75)',
            },
          }}
        >
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
        </ReactModal>
        <ReactModal
          className="items-left sm:max-w-8xl fixed inset-0 mx-2 my-auto flex h-fit w-fit flex-col gap-4 rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto"
          isOpen={showFullAndFinalModal}
          onRequestClose={() => {
            setShowFullAndFinalModal(false);
          }}
          style={{
            overlay: {
              backgroundColor: 'rgba(0, 0, 0, 0.75)',
            },
          }}
        >
          <Formik
            initialValues={fullAndFinalInitialValues}
            validationSchema={''}
            onSubmit={saveFullAndFinalButtonClicked}
            component={(props) => (
              <FullAndFinal
                {...props}
                // displayHeading={
                // 	confirmType == 'resign'
                // 		? 'Resign Employee (All the attendances for this employee after the resignation date will be deleted)'
                // 		: 'Unresign Employee'
                // }
                setShowFullAndFinalModal={setShowFullAndFinalModal}
                fullAndFinalEmployeeId={fullAndFinalEmployeeId}
                globalCompany={globalCompany}
                generateButtonClicked={generateButtonClicked}
              />
            )}
          />
        </ReactModal>
      </section>
    );
  }
};

export default ResignationForm;
