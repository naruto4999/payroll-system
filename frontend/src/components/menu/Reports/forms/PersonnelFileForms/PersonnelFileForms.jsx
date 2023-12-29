import React, { useState, useMemo, useEffect } from 'react';
import EmployeeTable from '../EmployeeTable';
import { FaCheck, FaWindowMinimize } from 'react-icons/fa';
import { useDispatch, useSelector } from 'react-redux';
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
import DateSelector from './DateSelector';
import FilterOptions from './FilterOptions';
import { Formik } from 'formik';
import { useGeneratePersonnelFileReportsMutation } from '../../../../authentication/api/personnelFileReportsApiSlice';
import { useOutletContext } from 'react-router-dom';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { authActions } from '../../../../authentication/store/slices/auth';

const PersonnelFileForms = () => {
	const [fromDate, setFromDate] = useState(new Date(Date.UTC(1970, 0, 1)));
	const [toDate, setToDate] = useState(new Date(new Date().setUTCDate(new Date().getUTCDate() + 1)));
	const globalCompany = useSelector((state) => state.globalCompany);
	const auth = useSelector((state) => state.auth);
	const dispatch = useDispatch();
	const [showLoadingBar, setShowLoadingBar] = useOutletContext();

	const {
		data: employeePersonalDetails,
		isLoading: isLoadingEmployeePersonalDetails,
		isSuccess: isSuccessEmployeePersonalDetails,
	} = useGetEmployeePersonalDetailsQuery(globalCompany);

	const [
		generatePersonnelFileReports,
		{
			isLoading: isGeneratingPersonnelFileReports,
			// isError: errorRegisteringRegular,
			isSuccess: isGeneratePersonnelFileReportsSuccess,
		},
	] = useGeneratePersonnelFileReportsMutation();

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
				const [year, month, day] = employee.dateOfJoining.split('-').map(Number);
				const employeeDateOfJoining = new Date(Date.UTC(year, month - 1, day));
				// console.log(employeeDateOfJoining);
				return fromDate <= employeeDateOfJoining && toDate >= employeeDateOfJoining;
			} else {
				return false;
			}
		});

		return filteredData;
	}, [employeePersonalDetails, fromDate, toDate]);
	console.log(toDate);

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
				language: 'hindi',
				orientation: 'landscape',
				personnelFileReportsSelected: [],
			},
			reportType: 'personnel_file_reports',
		};
		return initialValues;
	};
	const initialValues = useMemo(() => generateInitialValues(), []);

	const generateButtonClicked = async (values, formikBag) => {
		console.log(values);
		setShowLoadingBar(true);
		const toSend = {
			...values,
			employee_ids: table.getSelectedRowModel().flatRows.map((row) => row.id),
			company: globalCompany.id,
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

		const generatePersonnelFileForms = async () => {
			try {
				const response = await fetch(
					`${import.meta.env.VITE_BACKEND_URL}api/generate-personnel-file-reports`,
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
								`${import.meta.env.VITE_BACKEND_URL}api/generate-personnel-file-reports`,
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
				} else if (!response.ok) {
					console.error('Request failed with status: ', response.status);
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

		// Call the generatePersonnelFileForms function to initiate the request
		generatePersonnelFileForms();
	};

	return (
		<section className="mt-4 w-full">
			<div className="ml-4 flex flex-row flex-wrap place-content-between">
				<div className="mr-4">
					<h1 className="text-3xl font-medium">Personnel File Forms</h1>
					<p className="my-2 text-sm">Generate Personnel File Forms here</p>
				</div>
			</div>

			<div className="mx-4 flex flex-row flex-wrap gap-8 lg:flex-nowrap">
				<div className="w-1/2 ">
					<div className=" flex w-full flex-row justify-between">
						<div>
							<label
								htmlFor="fromDate"
								className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								From :
							</label>
							<DateSelector date={fromDate} setDate={setFromDate} id={'fromDate'} name={'toDate'} />
						</div>
						<div>
							<label
								htmlFor="toDate"
								className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
							>
								To :
							</label>
							<DateSelector date={toDate} setDate={setToDate} id={'toDate'} name={'toDate'} />
						</div>
					</div>
					<EmployeeTable table={table} flexRender={flexRender} />
				</div>
				<div className="mt-4 w-1/2">
					<Formik
						initialValues={initialValues}
						validationSchema={''}
						onSubmit={generateButtonClicked}
						component={(props) => <FilterOptions {...props} />}
					/>
				</div>
			</div>
		</section>
	);
};

export default PersonnelFileForms;
