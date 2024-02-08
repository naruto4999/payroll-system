import React from 'react';

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
}) => {
	const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
	const firstDayOfMonth = new Date(selectedDate.year, selectedDate.month - 1, 1);
	const daysInMonth = new Date(selectedDate.year, selectedDate.month, 0).getDate();
	const dayArray = Array.from({ length: daysInMonth }, (_, index) => index + 1);
	const dayOfWeek = firstDayOfMonth.getDay();
	return (
		<div>
			<form
				action=""
				className="flex flex-col justify-center gap-2"
				//  onSubmit={handleSubmit}
			>
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
					{dayArray.map((day) => (
						<div className="h-fit w-full" key={day}>
							{/* <MonthDays
									day={day}
									shifts={shifts}
									shiftValue={values?.dayWiseShifts[day]}
									fieldName={`dayWiseShifts.${day}`}
								/> */}
							1
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
