import { useRef, useEffect } from "react";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const ViewShift = ({ viewShiftPopoverHandler, shift }) => {
    return (
        <div className="text-gray-900 dark:text-slate-100">
            <section className="flex flex-row justify-center gap-2">
                <div className="w-full">
                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            Shift Name
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.name}
                        </p>
                    </div>

                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            Beginning Time
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.beginning_time
                                .split(":")
                                .slice(0, 2)
                                .join(":")}
                        </p>
                    </div>

                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            End Time
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.end_time.split(":").slice(0, 2).join(":")}
                        </p>
                    </div>

                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            Lunch Time
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.lunch_time}
                        </p>
                    </div>

                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            Tea Time
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.tea_time}
                        </p>
                    </div>

                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            Late Grace
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.late_grace}
                        </p>
                    </div>
                </div>

                <div className="w-full">
                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            Over Time Begins After
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.ot_begin_after}
                        </p>
                    </div>

                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            Next Shift Delay
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.next_shift_dealy}
                        </p>
                    </div>

                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            Accidental Punch Buffer
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.accidental_punch_buffer}
                        </p>
                    </div>

                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            Half Day Minimum Minutes{" "}
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.half_day_minimum_minutes}
                        </p>
                    </div>

                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            Full Day Minimum Minutes{" "}
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.full_day_minimum_minutes}
                        </p>
                    </div>

                    <div className="dark:hover:bg-zinc-700 hover:bg-zinc-400 p-2 rounded">
                        <h3 className="dark:text-blueAccent-500 rounded text-blueAccent-600 font-bold text-opacity-100 dark:text-opacity-70 text-sm sm:text-base">
                            Short Leaves{" "}
                        </h3>
                        <p className="font-medium text-sm sm:text-base">
                            {shift?.short_leaves}
                        </p>
                    </div>
                </div>
            </section>
            <section className=" mt-4 mb-2">
                    <button
                        type="button"
                        className="bg-zinc-400 hover:bg-zinc-500 dark:bg-zinc-600 rounded w-20 p-2 text-base font-medium dark:hover:bg-zinc-700"
                        onClick={() => viewShiftPopoverHandler({
                            id: null
                        })}
                    >
                        Cancel
                    </button>
                </section>
        </div>
    );
};
export default ViewShift;
