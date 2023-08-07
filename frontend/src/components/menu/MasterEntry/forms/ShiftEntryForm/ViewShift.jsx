import { useRef, useEffect } from 'react';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const ViewShift = ({ viewShiftPopoverHandler, shift }) => {
	console.log(shift);
	return (
		<div className="text-gray-900 dark:text-slate-100">
			<section className="flex flex-row justify-center gap-2">
				<div className="w-full">
					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							Shift Name
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.name}
						</p>
					</div>

					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							Beginning Time
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.beginningTime
								.split(':')
								.slice(0, 2)
								.join(':')}
						</p>
					</div>

					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							End Time
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.endTime.split(':').slice(0, 2).join(':')}
						</p>
					</div>

					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							Lunch Time
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.lunchTime}
						</p>
					</div>

					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							Tea Time
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.teaTime}
						</p>
					</div>

					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							Late Grace
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.lateGrace}
						</p>
					</div>
				</div>

				<div className="w-full">
					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							Over Time Begins After
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.otBeginAfter}
						</p>
					</div>

					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							Next Shift Delay
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.nextShiftDealy}
						</p>
					</div>

					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							Accidental Punch Buffer
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.accidentalPunchBuffer}
						</p>
					</div>

					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							Half Day Minimum Minutes{' '}
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.halfDayMinimumMinutes}
						</p>
					</div>

					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							Full Day Minimum Minutes{' '}
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.fullDayMinimumMinutes}
						</p>
					</div>

					<div className="rounded p-2 hover:bg-zinc-400 dark:hover:bg-zinc-700">
						<h3 className="rounded text-sm font-bold text-blueAccent-600 text-opacity-100 dark:text-blueAccent-500 dark:text-opacity-70 sm:text-base">
							Short Leaves{' '}
						</h3>
						<p className="text-sm font-medium sm:text-base">
							{shift?.shortLeaves}
						</p>
					</div>
				</div>
			</section>
			<section className=" mt-4 mb-2">
				<button
					type="button"
					className="w-20 rounded bg-zinc-400 p-2 text-base font-medium hover:bg-zinc-500 dark:bg-zinc-600 dark:hover:bg-zinc-700"
					onClick={() =>
						viewShiftPopoverHandler({
							id: null,
						})
					}
				>
					Cancel
				</button>
			</section>
		</div>
	);
};
export default ViewShift;
