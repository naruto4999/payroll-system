import { Field, ErrorMessage } from 'formik';

const MonthDays = ({ day, shifts, values, fieldName }) => {
	// console.log(values?.dayWiseShifts[day]);
	const shiftValue = values?.dayWiseShifts[day];

	// Check if the shiftValue is not an empty string before rendering the select box
	const shouldRenderSelect = shiftValue !== '';
	return (
		<div className="relative h-20 rounded-sm border dark:border-slate-400 dark:border-opacity-30">
			<h6 className=" absolute left-0 right-0 mx-auto w-fit text-blueAccent-600 dark:text-blueAccent-500">
				{day}
			</h6>
			{shouldRenderSelect && (
				<Field
					as="select"
					name={fieldName}
					id={fieldName}
					className="my block h-full w-full rounded-md bg-zinc-300 bg-opacity-100 p-1 text-xs transition-colors duration-300 hover:bg-zinc-200 dark:bg-zinc-800 dark:hover:bg-zinc-700 sm:text-base"
				>
					{shifts?.map((shift, index) => {
						return (
							<option key={index} value={shift.id}>
								{shift.name}
							</option>
						);
					})}
				</Field>
			)}
			{/* <div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
				<ErrorMessage name={'salaryDetail.overtimeType'} />
			</div> */}
		</div>
	);
};

export default MonthDays;
