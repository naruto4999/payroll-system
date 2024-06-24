import { Field, ErrorMessage } from 'formik';
import { memo } from 'react';

const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};

const AttendanceMonthDays = memo(
  ({
    day,
    year,
    month,
    shift,
    leaveGrades,
    otMin,
    lateMin,
    holidays,
    memoizedExtraOffDate,
    firstHalf,
    secondHalf,
    absent,
    setFieldValue
  }) => {
    const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const date = new Date(Date.UTC(year, month - 1, day));
    const weekdayIndex = date.getDay();
    const daysInMonth = new Date(year, month, 0).getDate();
    const isHoliday = holidays.some((holiday) => new Date(holiday.date).getTime() === date.getTime());
    const isExtraOff = memoizedExtraOffDate?.getDate() == parseInt(day);

    //To make sure that the value returned by the select field is an interger (when using the manual mode)
    const handleSelectChange = (event) => {
      const { name, value } = event.target;
      setFieldValue(name, parseInt(value, 10));
    };

    // const OtDisplayhours = Math.floor(otMin / 60);
    // const OtDisplayMinutes = otMin % 60;
    return (
      <div
        className={classNames(
          day == daysInMonth ? '' : 'border-b-0',
          'relative h-6 rounded-sm border  dark:border-slate-400 dark:border-opacity-30 focus-within:dark:bg-zinc-900 hover:dark:bg-zinc-800 ',
          weekdayIndex == 0 || isHoliday || isExtraOff ? 'dark:bg-red-700 dark:bg-opacity-40' : ''
        )}
      >
        <h6
          className={classNames(
            weekdayIndex == 0 || isHoliday || isExtraOff ? 'dark:text-red-600' : '',
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
            className="h-full w-fit cursor-not-allowed rounded-sm  bg-transparent pl-2 pr-2 text-xs outline-none transition-colors duration-300 sm:text-base"
          />
          {/* <div></div> */}

          <Field
            type="time"
            name={`attendance.${day}.machineOut`}
            id={`attendance.${day}.machineOut`}
            disabled={true}
            className="h-full w-fit cursor-not-allowed rounded-sm bg-transparent pl-2 pr-2 text-xs outline-none transition-colors duration-300  sm:text-base"
          />

          <Field
            type="time"
            name={`attendance.${day}.manualIn`}
            id={`attendance.${day}.manualIn`}
            className="h-full w-fit rounded-sm bg-transparent pl-2 pr-2 text-xs outline-none transition-colors duration-300 hover:bg-zinc-200 dark:hover:bg-zinc-700 focus:dark:bg-zinc-700 sm:text-base"
          />

          <Field
            type="time"
            name={`attendance.${day}.manualOut`}
            id={`attendance.${day}.manualOut`}
            className="h-full w-fit rounded-sm bg-transparent pl-2 pr-2 text-xs outline-none transition-colors duration-300 hover:bg-zinc-200 dark:hover:bg-zinc-700 focus:dark:bg-zinc-700 sm:text-base"
          />
          <div className="my-auto w-24 pl-2 pr-2">
            <h6 className="mx-auto w-fit cursor-default  text-xs">{shift}</h6>
          </div>

          <Field
            as="select"
            name={`attendance.${day}.firstHalf`}
            id={`attendance.${day}.firstHalf`}
            className={`h-full w-20 rounded-sm bg-transparent pl-2 pr-2 text-xs outline-none transition-colors duration-300 hover:bg-zinc-200 dark:text-xs dark:hover:bg-zinc-700 focus:dark:bg-zinc-700 sm:text-base ${firstHalf == absent.id ? 'text-red-600' : ''
              }`}
            onChange={handleSelectChange}
          >
            {/* <option value={''}>N/A</option> */}
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
            className={`h-full w-20 rounded-sm bg-transparent pl-2 pr-2 text-xs outline-none transition-colors duration-300 hover:bg-zinc-200 dark:text-xs dark:hover:bg-zinc-700 focus:dark:bg-zinc-700 sm:text-base ${secondHalf == absent.id ? 'text-red-600' : ''
              }`}
            onChange={handleSelectChange}
          >
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
              ? `${String(Math.floor(otMin / 60)).padStart(2, '0')}:${String(otMin % 60).padStart(
                2,
                '0'
              )}`
              : ''}
          </h6>
          <h6 className="my-auto w-20 cursor-default pl-2 pr-2 text-xs dark:text-orange-600">
            {lateMin !== ''
              ? `${String(Math.floor(lateMin / 60)).padStart(2, '0')}:${String(lateMin % 60).padStart(
                2,
                '0'
              )}`
              : ''}
          </h6>
          <div className="pl-2 pr-2">
            <Field
              type="checkbox"
              name={`attendance.${day}.manualMode`}
              className="my-auto h-4 w-4 rounded accent-teal-600"
            />
          </div>
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
