import { Field, ErrorMessage } from 'formik';
import { memo } from 'react';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const AttendanceMonthDays = memo(
	({ day, year, month, shift, leaveGrades, otMin, lateMin }) => {
		// console.log(shift);
		const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
		const date = new Date(`${year}-${month}-${day}`);
		const weekdayIndex = date.getDay();
		const daysInMonth = new Date(year, month, 0).getDate();
		console.log(otMin);

		// const OtDisplayhours = Math.floor(otMin / 60);
		// const OtDisplayMinutes = otMin % 60;
		return (
			<div
				className={classNames(
					day == daysInMonth ? '' : 'border-b-0',
					'relative h-6 rounded-sm border  dark:border-slate-400 dark:border-opacity-30'
				)}
			>
				<h6
					className={classNames(
						weekdayIndex == 0 ? 'dark:text-red-600' : '',
						' absolute -left-14 top-[20%] my-auto w-fit text-xs text-blueAccent-600 dark:text-blueAccent-500'
					)}
				>
					{`${day} ${weekdays[weekdayIndex]}`}
				</h6>
				<section className="flex h-full flex-row divide-x divide-dashed divide-blueAccent-600/80">
					<Field
						type="time"
						name={`attendance.${day}.machineIn`}
						id={`attendance.${day}.machineIn`}
						disabled={true}
						className="h-full w-fit cursor-not-allowed rounded-sm bg-zinc-300 bg-opacity-100 pl-2 pr-2 text-xs outline-none transition-colors duration-300    dark:bg-zinc-800 sm:text-base"
					/>
					{/* <div></div> */}

					<Field
						type="time"
						name={`attendance.${day}.machineOut`}
						id={`attendance.${day}.machineOut`}
						disabled={true}
						className="h-full w-fit cursor-not-allowed rounded-sm bg-zinc-300 bg-opacity-100 pl-2 pr-2 text-xs outline-none transition-colors duration-300    dark:bg-zinc-800 sm:text-base"
					/>

					<Field
						type="time"
						name={`attendance.${day}.manualIn`}
						id={`attendance.${day}.manualIn`}
						className="h-full w-fit rounded-sm bg-zinc-300 bg-opacity-100 pl-2 pr-2 text-xs outline-none transition-colors duration-300 hover:bg-zinc-200   dark:bg-zinc-800 dark:hover:bg-zinc-700 sm:text-base"
					/>

					<Field
						type="time"
						name={`attendance.${day}.manualOut`}
						id={`attendance.${day}.manualOut`}
						className="h-full w-fit rounded-sm bg-zinc-300 bg-opacity-100 pl-2 pr-2 text-xs outline-none transition-colors duration-300 hover:bg-zinc-200   dark:bg-zinc-800 dark:hover:bg-zinc-700 sm:text-base"
					/>
					<div className="my-auto w-24 pl-2 pr-2">
						<h6 className="mx-auto w-fit cursor-default  text-xs">
							{shift}
						</h6>
					</div>

					<Field
						as="select"
						name={`attendance.${day}.firstHalf`}
						id={`attendance.${day}.firstHalf`}
						className={classNames(
							weekdayIndex == 0
								? 'dark:bg-red-700 dark:bg-opacity-40'
								: '',
							'h-full w-20 rounded-sm bg-zinc-300 bg-opacity-100 pl-2 pr-2 text-xs outline-none transition-colors duration-300 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-xs dark:hover:bg-zinc-700 sm:text-base'
						)}
					>
						<option value={''}>N/A</option>
						{leaveGrades?.map((leaveGrade, index) => {
							return (
								<option key={index} value={leaveGrade.id}>
									{leaveGrade.name}
								</option>
							);
						})}
					</Field>
					<Field
						as="select"
						name={`attendance.${day}.secondHalf`}
						id={`attendance.${day}.secondHalf`}
						className="h-full w-20 rounded-sm bg-zinc-300 bg-opacity-100 pl-2 pr-2 text-xs outline-none transition-colors duration-300 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-xs dark:hover:bg-zinc-700 sm:text-base"
					>
						<option value={''}>N/A</option>
						{leaveGrades?.map((leaveGrade, index) => {
							return (
								<option key={index} value={leaveGrade.id}>
									{leaveGrade.name}
								</option>
							);
						})}
					</Field>

					<h6 className="my-auto w-20 cursor-default pl-2 pr-2 text-xs dark:text-green-600">
						{otMin !== ''
							? `${String(Math.floor(otMin / 60)).padStart(
									2,
									'0'
							  )}:${String(otMin % 60).padStart(2, '0')}`
							: ''}
					</h6>
					<h6 className="my-auto w-20 cursor-default pl-2 pr-2 text-xs dark:text-yellow-600">
						{lateMin}
					</h6>
				</section>

				{/* </Field> */}

				<div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
					<ErrorMessage name={'salaryDetail.overtimeType'} />
				</div>
			</div>
		);
	}
);

export default AttendanceMonthDays;
