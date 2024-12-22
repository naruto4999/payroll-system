import { Field, ErrorMessage } from 'formik';
import { memo } from 'react';

const classNames = (...classes) => {
    return classes.filter(Boolean).join(' ');
};

const AttendanceHeader = memo(() => {
    return (
        <div className="relative h-6 rounded-sm border border-b-0  dark:border-slate-400 dark:border-opacity-30 dark:bg-zinc-900 dark:bg-opacity-70">
            <section className="flex h-full flex-row divide-x divide-dashed divide-blueAccent-600/80">
                <div className="my-auto w-[92px] pl-2 pr-2">
                    <h6 className="mx-auto w-fit cursor-default text-xs font-medium">Machine In</h6>
                </div>
                <div className="my-auto w-[92px] pl-2 pr-2">
                    <h6 className="mx-auto w-fit cursor-default  text-xs font-medium">Machine Out</h6>
                </div>
                <div className="my-auto w-[92px] pl-2 pr-2">
                    <h6 className="mx-auto w-fit cursor-default  text-xs font-medium">Manual In</h6>
                </div>
                <div className="my-auto w-[92px] pl-2 pr-2">
                    <h6 className="mx-auto w-fit cursor-default  text-xs font-medium">Manual Out</h6>
                </div>
                <div className="my-auto w-24 pl-2 pr-2">
                    <h6 className="mx-auto w-fit cursor-default  text-xs font-medium">Shift</h6>
                </div>
                <div className="my-auto w-20 pl-2 pr-2">
                    <h6 className="mx-auto w-fit cursor-default  text-xs font-medium">1st Half</h6>
                </div>
                <div className="my-auto w-20 pl-2 pr-2">
                    <h6 className="mx-auto w-fit cursor-default  text-xs font-medium">2nd Half</h6>
                </div>
                <div className="my-auto w-20 pl-2 pr-2">
                    <h6 className="mx-auto w-fit cursor-default  text-xs font-medium">OT Hrs</h6>
                </div>
                <div className="my-auto w-20 pl-2 pr-2">
                    <h6 className="mx-auto w-fit cursor-default  text-xs font-medium">Late Hrs</h6>
                </div>
                {/* <div></div> */}

                {/* <Field
            type="time"
            name={`attendance.${day}.machineOut`}
            id={`attendance.${day}.machineOut`}
            className="h-full w-fit rounded-sm bg-zinc-300 bg-opacity-100 pl-2 pr-2 text-xs outline-none transition-colors duration-300 hover:bg-zinc-200   dark:bg-zinc-800 dark:hover:bg-zinc-700 sm:text-base"
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
            className="h-full w-fit rounded-sm bg-zinc-300 bg-opacity-100 pl-2 pr-2 text-xs outline-none transition-colors duration-300 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-xs dark:hover:bg-zinc-700 sm:text-base"
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
            className="h-full w-fit rounded-sm bg-zinc-300 bg-opacity-100 pl-2 pr-2 text-xs outline-none transition-colors duration-300 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-xs dark:hover:bg-zinc-700 sm:text-base"
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

        <h6 className="my-auto cursor-default pl-2 pr-2 text-xs">
            OT hrs
        </h6>
        <h6 className="my-auto cursor-default pl-2 pr-2 text-xs">
            Late hrs
        </h6> */}
            </section>

            {/* </Field> */}

            <div className="mt-1 text-xs font-bold text-red-500 dark:text-red-700">
                <ErrorMessage name={'salaryDetail.overtimeType'} />
            </div>
        </div>
    );
});
export default AttendanceHeader;
