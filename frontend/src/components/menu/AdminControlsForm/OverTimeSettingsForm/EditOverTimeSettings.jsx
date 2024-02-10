import React, { useEffect } from 'react';
import MonthDays from './MonthDays';
import { useGetOverTimeSettingsQuery } from '../../../authentication/api/overTimeSettingsApiSlice';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const EditOverTimeSettings = ({
	handleSubmit,
	values,
	errors,
	isValid,
	touched,
	setFieldValue,
	isSubmitting,
	selectedDate,
	globalCompany,
	resetForm,
}) => {
	const {
		data: overTimeSettings,
		isLoading: isLoadingoverTimeSettings,
		isSuccess: isSuccessoverTimeSettings,
	} = useGetOverTimeSettingsQuery({ company: globalCompany.id, year: selectedDate.year, month: selectedDate.month });
	console.log(overTimeSettings);
	const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
	const firstDayOfMonth = new Date(selectedDate.year, selectedDate.month - 1, 1);
	const dayOfWeek = firstDayOfMonth.getDay();

	useEffect(() => {
		if (!isSubmitting) {
			resetForm();
			if (overTimeSettings && overTimeSettings.length != 0) {
				console.log('Component did mount');
				overTimeSettings.forEach((element) => {
					const date = new Date(element.date);
					const day = parseInt(date.getDate().toString());
					console.log(day);
					if (selectedDate.month - 1 == date.getMonth()) {
						setFieldValue(`dayArray[${day - 1}]`, { day: day, maxOtHrs: element.maxOtHrs });
					}
				});
			}
		}
	}, [overTimeSettings]);
	console.log(values);
	return (
		<div>
			<form action="" className="flex flex-col justify-center gap-2" onSubmit={handleSubmit}>
				<section className="container grid max-w-full grid-cols-7 gap-1">
					{weekdays.map((weekday, index) => {
						return (
							<div key={index} className="w-full rounded-sm border border-slate-400 border-opacity-30">
								<h2 className="mx-auto hidden w-fit font-bold sm:block">{weekday}</h2>
								<h2 className="mx-auto w-fit font-bold sm:hidden">{weekday.slice(0, 3)}</h2>
							</div>
						);
					})}
					{Array.from({ length: dayOfWeek }).map((_, index) => (
						<div className="h-fit w-full" key={index}>
							{/* <MonthDays /> */}
						</div>
					))}
					{values.dayArray.map((element, index) => (
						<div className="h-fit w-full" key={index}>
							<MonthDays element={element} index={index} />
							{/* {element.maxOtHrs} */}
						</div>
					))}
				</section>
				<section className="mt-4 mb-2 flex flex-row gap-4">
					<button
						className={classNames(
							true ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
							'w-20 rounded bg-teal-500 p-2 text-base font-medium dark:bg-teal-700'
						)}
						type="submit"
						// disabled={!isValid}
						// onClick={handleSubmit}
					>
						Update
					</button>
					<button
						type="button"
						className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
						onClick={() => {
							cancelButtonClicked(isEditing);
							setErrorMessage('');
						}}
					>
						Cancel
					</button>
				</section>
			</form>
		</div>
	);
};

export default EditOverTimeSettings;
