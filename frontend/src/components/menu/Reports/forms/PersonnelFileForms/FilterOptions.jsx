import React from 'react';
import { Field, ErrorMessage, FieldArray } from 'formik';
import { FaCircleNotch } from 'react-icons/fa';

const classNames = (...classes) => {
    return classes.filter(Boolean).join(' ');
};
const FilterOptions = ({ handleChange, values, isValid, handleSubmit, isSubmitting }) => {
    console.log(values);

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
                    <option value="personnel_file_reports">Personnel File Reports</option>
                    <option value="id_card">ID card</option>
                </Field>
            </div>
            {values.reportType == 'id_card' && (
                <div>
                    <label
                        htmlFor="filters.orientation"
                        className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
                    >
                        Orientation :
                    </label>
                    <Field
                        as="select"
                        id="filters.orientation"
                        className="my-1 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
                        name="filters.orientation"
                    >
                        <option value="landscape">Landscape</option>
                        <option value="portrait">Portrait</option>
                    </Field>
                </div>
            )}
            {values.reportType == 'personnel_file_reports' && (
                <div role="group" aria-labelledby="checkbox-group" className="flex flex-row flex-wrap gap-5">
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="biodata"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Biodata
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="application_form"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Application Form
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="employee_orientation"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Employee Orientation
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="employee_personal_details"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Employee Personal Details
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="form_no_16"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Form No. 16
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="form_f_front"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Form-F Front
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="form_f_back"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Form-F Back
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="esi_form_1"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        ESI Form 1
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="confirmation_letter"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Confirmation Letter
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="duty_join"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Duty Join
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="pf_form_2_front"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        PF Form 2 Front
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="pf_form_2_back"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        PF Form 2 Back
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="probation"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Probation
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="form_11"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Form-11
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="appointment_letter_front"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Appointment Letter Front
                    </label>
                    <label>
                        <Field
                            type="checkbox"
                            name="filters.personnelFileReportsSelected"
                            value="appointment_letter_back"
                            className="mr-1 h-4 w-4 translate-y-0.5 rounded accent-teal-600"
                        />
                        Appointment Letter Back
                    </label>
                </div>
            )}
            {values.reportType == 'personnel_file_reports' && (
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
