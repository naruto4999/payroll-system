import { FaRegTrashAlt, FaPen, FaAngleUp, FaAngleDown, FaEye } from 'react-icons/fa';
import { FaCircleCheck } from 'react-icons/fa6';
import { useRef, useEffect, useState, useMemo } from 'react';
import {
	useGetAllEmployeeLeaveOpeningQuery,
	useGetAllEmployeePresentCountQuery,
	useGetAllEmployeeGenerativeLeaveRecordQuery,
} from '../../../../authentication/api/timeUpdationApiSlice';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const GenerativeLeaveTable = ({ globalCompany, year, updateEmployeeId, month }) => {
	const {
		data: allEmployeeGenerativeLeaveRecord,
		isLoading: isLoadingAllEmployeeGenerativeLeaveRecord,
		isSuccess: isAllEmployeeGenerativeLeaveRecordSuccess,
		isFetching: isFetchingAllEmployeeGenerativeLeaveRecord,
	} = useGetAllEmployeeGenerativeLeaveRecordQuery(
		{
			company: globalCompany.id,
			year: year,
		},
		{
			skip: globalCompany === null || globalCompany === '' || year == '',
		}
	);
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
	const {
		data: allEmployeePresentCount,
		isLoading: isLoadingAllEmployeePresentCount,
		isSuccess: isAllEmployeePresentCountSuccess,
		isFetching: isFetchingAllEmployeePresentCount,
	} = useGetAllEmployeePresentCountQuery(
		{
			company: globalCompany.id,
			year: year,
		},
		{
			skip: globalCompany === null || globalCompany === '' || year == '',
		}
	);
	console.log(allEmployeeGenerativeLeaveRecord);
	console.log(allEmployeeLeaveOpening);
	console.log(allEmployeePresentCount);

	const currentEmployeePresentCount = useMemo(() => {
		// First, filter the array to get objects that belong to the selected employee.
		const selectedEmployeeData = allEmployeePresentCount?.filter((item) => item.employee === updateEmployeeId);

		// Create an empty object to store the memoized data.
		const currentEmployeePresentCount = {
			monthly: {},
			yearly: 0,
		};

		// Iterate through the selected employee's data and populate the currentEmployeePresentCount.
		selectedEmployeeData?.forEach((item) => {
			const dateParts = item.date.split('-'); // Split date into parts (year, month, day)
			const year = dateParts[0];
			const month = dateParts[1];

			// Initialize or update the monthly presentCount.
			if (!currentEmployeePresentCount.monthly[year]) {
				currentEmployeePresentCount.monthly[year] = {};
			}
			currentEmployeePresentCount.monthly[year][month] =
				(currentEmployeePresentCount.monthly[year][month] || 0) + item.presentCount;

			// Update the yearly cumulative sum.
			console.log('Present Count: ', item.presentCount);
			currentEmployeePresentCount.yearly += item.presentCount;
		});
		console.log('yoooo');

		// Return the memoized object.
		return currentEmployeePresentCount;
	}, [allEmployeePresentCount, updateEmployeeId]);

	console.log(currentEmployeePresentCount);

	const currentEmployeeGenerativeLeaveCount = useMemo(() => {
		const memoizedObject = {};
		// let firstIteration = true;
		// let leaveIdForTotalPresent;

		allEmployeeGenerativeLeaveRecord?.forEach((item) => {
			if (item.employee === updateEmployeeId) {
				const leaveId = item.leave.id;
				const leaveName = item.leave.name;
				const date = item.date;
				const leaveCount = item.leaveCount;
				const generateFrequency = item.leave.generateFrequency;

				// Extract month and year from the date
				const [year, month] = date.split('-').map(Number);

				// Initialize memoizedObject structure if not present
				if (!memoizedObject[leaveId]) {
					memoizedObject[leaveId] = {
						name: leaveName,
						generateFrequency: generateFrequency,
						monthly: {},
						yearly: 0,
					};
				}

				// Initialize monthly object if not present
				if (!memoizedObject[leaveId].monthly[year]) {
					memoizedObject[leaveId].monthly[year] = {};
				}

				// Assign leaveCount for the specific month
				memoizedObject[leaveId].monthly[year][month] = leaveCount;
				memoizedObject[leaveId].yearly += leaveCount;
			}
		});

		return memoizedObject;
	}, [allEmployeeGenerativeLeaveRecord, updateEmployeeId]);
	console.log(currentEmployeeGenerativeLeaveCount);

	return (
		<div className="scrollbar mx-auto max-h-[30dvh] max-w-full overflow-y-auto rounded border border-black border-opacity-50 shadow-md lg:max-h-[30dvh]">
			<table className="w-full border-collapse text-center text-xs">
				<thead className="sticky top-0 z-20 bg-yellow-600 dark:bg-yellow-700 dark:bg-opacity-40">
					<tr>
						<th className="px-4 py-2 font-medium">Leave</th>
						<th className="px-4 py-2 font-medium">Open</th>
						<th className="px-4 py-2 font-medium">Earned</th>
						<th className="px-4 py-2 font-medium">{'Taken (Yearly)'}</th>
						<th className="px-4 py-2 font-medium">{'Taken (Monthly)'}</th>
						<th className="px-4 py-2 font-medium">Balance</th>
					</tr>
				</thead>
				<tbody className="max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50 ">
					{Object.keys(currentEmployeeGenerativeLeaveCount).map((key) => (
						<tr
							key={key}
							className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50"
						>
							<td className="relative px-4 py-2 font-normal">
								{currentEmployeeGenerativeLeaveCount?.[key]?.name}
							</td>
							<td className="relative px-4 py-2 font-normal">0</td>
							<td className="relative px-4 py-2 font-normal">
								{Math.floor(
									parseInt(currentEmployeePresentCount.yearly) /
										2 /
										parseInt(currentEmployeeGenerativeLeaveCount?.[key]?.generateFrequency)
								)}
							</td>
							<td className="relative px-4 py-2 font-normal">
								{currentEmployeeGenerativeLeaveCount?.[key]?.yearly / 2}
							</td>
							<td className="relative px-4 py-2 font-normal">
								{currentEmployeeGenerativeLeaveCount?.[key]?.monthly?.[year]?.[month] !== undefined
									? currentEmployeeGenerativeLeaveCount[key].monthly[year][month] / 2
									: 0}
							</td>

							{/* Balance */}
							<td className="relative px-4 py-2 font-normal">
								{Math.floor(
									parseInt(currentEmployeePresentCount.yearly) /
										2 /
										parseInt(currentEmployeeGenerativeLeaveCount?.[key]?.generateFrequency)
								) -
									currentEmployeeGenerativeLeaveCount?.[key]?.yearly / 2}
							</td>
						</tr>
					))}
					{/* <tr>
						<td>Data 1</td>
						<td>Data 2</td>
						<td>Data 3</td>
					</tr> */}
				</tbody>
			</table>
		</div>
	);
};

export default GenerativeLeaveTable;
