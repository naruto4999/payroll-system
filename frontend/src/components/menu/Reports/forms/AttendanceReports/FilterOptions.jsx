import React, { useEffect } from 'react';
import { Field, ErrorMessage, FieldArray } from 'formik';
import { FaCircleNotch } from 'react-icons/fa';
import { useSelector } from 'react-redux';

const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};
const FilterOptions = ({ handleChange, values, isValid, handleSubmit, isSubmitting, selectedDate, setIgnoreMonthField, setFilterMissPunchEmployees, setFieldValue }) => {
  // console.log(values);
  // useEffect(() => {
  // 	setFieldValue('filters.monthFromDate', 1);
  // 	setFieldValue('filters.monthToDate', new Date(selectedDate.year, selectedDate.month, 0).getDate());
  // }, [selectedDate.month]);
  const auth = useSelector((state) => state.auth);
  useEffect(() => {
    if (values.reportType === 'form_14') {
      setIgnoreMonthField(true);
    } else {
      setIgnoreMonthField(false);
    }
    if (values.reportType === 'miss_punch') {
      setFilterMissPunchEmployees(true)
    } else {
      setFilterMissPunchEmployees(false)
    }
  }, [values.reportType, setIgnoreMonthField]);

  return (
    <div className="flex flex-col gap-2">
      <div>
        <label
          htmlFor="reportType"
          className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
        >
          Report Type :
        </label>
        <Field
          as="select"
          id="reportType"
          className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
          name="reportType"
        >
          <option value="attendance_register">Attendance Register</option>
          <option value="present_report">Present Report</option>
          <option value="absent_report">Absent Report</option>
          {auth.account.role == 'OWNER' && (
            <option value="overtime_sheet_daily">{'Over Time Sheet (Daily)'}</option>
          )}
          <option value="form_14">{'Form-14 (Leave Register)'}</option>
          <option value="bonus_calculation_sheet">Bonus Calculation Sheet</option>
          <option value="bonus_form_c">Bonus Form C</option>
          <option value="miss_punch">Miss Punch</option>
        </Field>
      </div>
      {(values.reportType == 'present_report' || values.reportType == 'overtime_sheet_daily' || values.reportType == 'absent_report') && (
        <div>
          <label
            htmlFor="filters.date"
            className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
          >
            Date :
          </label>
          <Field
            className="custom-number-input w-14 rounded border-2 border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
            type="number"
            name="filters.date"
            id="filters.date"
          />
        </div>
      )}
      {/* <div>
				<label
					htmlFor="monthFromDate"
					className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
				>
					Date From:
				</label>
				<Field
					className="custom-number-input w-14 rounded border-2 border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
					type="number"
					name="filters.monthFromDate"
					id="monthFromDate"
				/>
				<label
					htmlFor="monthToDate"
					className="mx-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
				>
					To:
				</label>
				<Field
					className="custom-number-input w-14 rounded border-2 border-gray-800 border-opacity-25 bg-zinc-200  bg-opacity-50   p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75"
					type="number"
					name="filters.monthToDate"
					id="monthToDate"
				/>
			</div> */}
      <div>
        <label
          htmlFor="sortBy"
          className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
        >
          Sort By :
        </label>
        <Field
          as="select"
          id="sortBy"
          className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
          name="filters.sortBy"
        >
          <option value="paycode">Paycode</option>
          <option value="attendance_card_no">Attendance Card No.</option>
          <option value="employee_name">Employee Name</option>
        </Field>
      </div>
      <div>
        <label
          htmlFor="groupBy"
          className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
        >
          Group By :
        </label>
        <Field
          as="select"
          id="groupBy"
          className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
          name="filters.groupBy"
        >
          <option value="none">None</option>
          <option value="department">Department</option>
        </Field>
      </div>
      <div>
        <label
          htmlFor="resignationFilter"
          className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
        >
          Resignation Filter :
        </label>
        <Field
          as="select"
          id="resignationFilter"
          className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
          name="filters.resignationFilter"
        >
          <option value="all">All</option>
          <option value="without_resigned">Without Resigned Employees</option>
          <option value="only_resigned">Only Resigned Employees</option>
        </Field>
      </div>

      <section>
        <div className="mt-4 mb-2 flex w-fit flex-row gap-4">
          <button
            className={classNames(
              isValid ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
              'h-10 w-fit rounded bg-teal-500 p-2 px-4 text-base font-medium dark:bg-teal-700'
            )}
            type="submit"
            disabled={!isValid}
            onClick={handleSubmit}
          >
            Generate
            {isSubmitting && (
              <FaCircleNotch className="my-auto ml-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
            )}
          </button>
        </div>
      </section>
    </div>
  );
};

export default FilterOptions;
