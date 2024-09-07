import React, { useEffect } from 'react';
import { Field, ErrorMessage, FieldArray } from 'formik';
import { FaCircleNotch } from 'react-icons/fa';

const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};
const FilterOptions = ({ handleChange, values, isValid, handleSubmit, isSubmitting, setFilterYearlyAdvanceEmployees }) => {
  console.log(values);
  useEffect(() => {
    if (values.reportType === 'yearly_advance_report') {
      setFilterYearlyAdvanceEmployees(true)
    } else {
      setFilterYearlyAdvanceEmployees(false)
    }
  }, [values.reportType]);
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
          <option value="salary_sheet">Salary Sheet</option>
          <option value="payment_sheet">Payment Sheet</option>
          <option value="payslip">Payslip</option>
          <option value="overtime_sheet">Over Time Sheet</option>
          <option value="advance_report">Advance Report</option>
          <option value="yearly_advance_report">Yearly Advance Report</option>
        </Field>
      </div>
      {values.reportType == 'salary_sheet' && (
        <div>
          <label
            htmlFor="filters.overtime"
            className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
          >
            Overtime :
          </label>
          <Field
            as="select"
            id="filters.overtime"
            className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
            name="filters.overtime"
          >
            <option value="with_ot">With OT</option>
            <option value="without_ot">Without OT</option>
          </Field>
        </div>
      )}
      {values.reportType == 'payment_sheet' && (
        <div>
          <label
            htmlFor="format"
            className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
          >
            Format :
          </label>
          <Field
            as="select"
            id="format"
            className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
            name="filters.format"
          >
            <option value="pdf">PDF</option>
            <option value="xlsx">MS Excel</option>
          </Field>
        </div>
      )}
      {values.reportType == 'payslip' && (
        <div>
          <label
            htmlFor="filters.language"
            className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
          >
            Language :
          </label>
          <Field
            as="select"
            id="filters.language"
            className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
            name="filters.language"
          >
            <option value="english">English</option>
            <option value="hindi">Hindi</option>
          </Field>
        </div>
      )}
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
          htmlFor="paymentMode"
          className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
        >
          Payment Mode :
        </label>
        <Field
          as="select"
          id="paymentMode"
          className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
          name="filters.paymentMode"
        >
          <option value="all">All</option>
          <option value="bank_transfer">Bank Transfer</option>
          <option value="cheque">Cheque</option>
          <option value="cash">Cash</option>
          <option value="rtgs">RTGS</option>
          <option value="neft">NEFT</option>
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
