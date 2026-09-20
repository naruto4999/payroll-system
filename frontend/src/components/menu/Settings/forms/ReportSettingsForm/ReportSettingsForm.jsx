import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useOutletContext } from 'react-router-dom';
import { FaCircleNotch } from 'react-icons/fa';
import {
	useCreateReportConfigurationMutation,
	useGetReportConfigurationsQuery,
	useUpdateReportConfigurationMutation,
} from '../../../../authentication/api/reportConfigurationApiSlice';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';

const ReportSettingsForm = () => {
	const dispatch = useDispatch();
	const globalCompany = useSelector((state) => state.globalCompany);
	const [, setShowLoadingBar] = useOutletContext();
	const [otHoursDisplay, setOtHoursDisplay] = useState('actual');
	const {
		data = [],
		isLoading,
		isFetching,
	} = useGetReportConfigurationsQuery(globalCompany.id, {
		skip: globalCompany.id == null,
	});
	const [createConfiguration, { isLoading: isCreating }] = useCreateReportConfigurationMutation();
	const [updateConfiguration, { isLoading: isUpdating }] = useUpdateReportConfigurationMutation();
	const paymentSheetConfiguration = data.find(
		(configuration) => configuration.reportType === 'payment_sheet' && configuration.outputFormat === 'xlsx'
	);

	useEffect(() => {
		setOtHoursDisplay(paymentSheetConfiguration?.options?.otHoursDisplay || 'actual');
	}, [globalCompany.id, paymentSheetConfiguration]);

	useEffect(() => {
		setShowLoadingBar(isLoading || isFetching || isCreating || isUpdating);
	}, [isLoading, isFetching, isCreating, isUpdating, setShowLoadingBar]);

	const save = async (event) => {
		event.preventDefault();
		const body = {
			reportType: 'payment_sheet',
			outputFormat: 'xlsx',
			options: { otHoursDisplay },
		};
		try {
			if (paymentSheetConfiguration) {
				await updateConfiguration({
					companyId: globalCompany.id,
					configurationId: paymentSheetConfiguration.id,
					body,
				}).unwrap();
			} else {
				await createConfiguration({ companyId: globalCompany.id, body }).unwrap();
			}
			dispatch(alertActions.createAlert({ message: 'Saved', type: 'Success', duration: 3000 }));
		} catch (error) {
			dispatch(alertActions.createAlert({ message: 'Error Occurred', type: 'Error', duration: 5000 }));
		}
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
		return (
			<div className="fixed inset-0 z-50 mx-auto my-auto flex h-fit w-fit items-center rounded bg-indigo-600 p-2 font-medium">
				<FaCircleNotch className="mr-2 animate-spin text-white" />
				Processing...
			</div>
		);
	}

	return (
		<section className="mx-5 mt-2 max-w-2xl">
			<h1 className="text-3xl font-medium">Report Settings</h1>
			<p className="my-2 text-sm">Configure persistent report behavior for the selected company.</p>
			<form className="mt-6 rounded-lg border border-zinc-300 p-4 dark:border-zinc-700" onSubmit={save}>
				<h2 className="text-xl font-medium">Payment Sheet (MS Excel)</h2>
				<label className="mt-4 block font-medium" htmlFor="otHoursDisplay">
					OT Hours Display
				</label>
				<select
					id="otHoursDisplay"
					className="mt-1 rounded-md bg-zinc-50 p-2 dark:bg-zinc-700"
					value={otHoursDisplay}
					onChange={(event) => setOtHoursDisplay(event.target.value)}
				>
					<option value="actual">Actual Hours</option>
					<option value="weighted">Multiplier-Adjusted Hours</option>
				</select>
				<p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
					Multiplier-adjusted hours are the sum of each OT category's hours multiplied by its configured
					overtime multiplier.
				</p>
				<button
					className="mt-5 rounded bg-teal-500 px-4 py-2 font-medium hover:bg-teal-600 dark:bg-teal-700"
					type="submit"
					disabled={isCreating || isUpdating}
				>
					Save
				</button>
			</form>
		</section>
	);
};

export default ReportSettingsForm;
