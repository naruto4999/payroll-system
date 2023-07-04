import React from "react";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const AddEmployeeNavigationBar = ({
    addEmployeePopover,
    addEmployeePopoverHandler,
}) => {
    return (
        // <h1>HI</h1>
        <div className=" h-10 w-fit flex flex-row justify-center gap-8 mt-6 md:mt-0 mx-auto">
            <div>
                <button
                onClick={() => {
                    addEmployeePopoverHandler("addEmployeePersonalDetail");
                }}
                    className={classNames(
                        addEmployeePopover.addEmployeePersonalDetail
                            ? "text-opacity-100 dark:text-opacity-100"
                            : "text-opacity-50 dark:text-opacity-50",
                        "text-sm md:text-xl dark:text-slate-100  text-gray-900 font-semibold transition-all"
                    )}
                >
                    Personal
                    <div
                        className={classNames(
                            addEmployeePopover.addEmployeePersonalDetail
                                ? ""
                                : "hidden",
                            "dark:bg-blueAccent-600 h-1 mt-2 "
                        )}
                    ></div>
                </button>
            </div>

            <button
                onClick={() => {
                    addEmployeePopoverHandler("addEmployeeProfessionalDetail");
                }}
                className={classNames(
                    addEmployeePopover.addEmployeeProfessionalDetail
                        ? "text-opacity-100 dark:text-opacity-100"
                        : "text-opacity-50 dark:text-opacity-50",
                    "text-sm md:text-xl dark:text-slate-100  text-gray-900 font-semibold transition-all"
                )}
            >
                Professional
                <div
                    className={classNames(
                        addEmployeePopover.addEmployeeProfessionalDetail
                            ? ""
                            : "hidden",
                        "dark:bg-blueAccent-600 h-1 mt-2 "
                    )}
                ></div>
            </button>
            <button className="text-sm md:text-xl dark:text-slate-100 text-gray-900 font-semibold">
                Salary
            </button>
            <button className="text-sm md:text-xl dark:text-slate-100 text-gray-900 font-semibold">
                ESI & PF
            </button>
        </div>
    );
};

export default AddEmployeeNavigationBar;
