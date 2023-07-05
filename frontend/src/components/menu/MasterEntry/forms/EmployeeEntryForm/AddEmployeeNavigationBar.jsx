import React from "react";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const AddEmployeeNavigationBar = ({
    addEmployeePopover,
    addEmployeePopoverHandler,
    editEmployeePopover,
    editEmployeePopoverHandler,
    isEditing,
    updateEmployeeId,
}) => {
    return (
        // <h1>HI</h1>
        <div className=" h-10 w-fit flex flex-row justify-center gap-8 mt-6 md:mt-0 mx-auto">
            <div>
                <button
                    onClick={() => {
                        isEditing
                            ? editEmployeePopoverHandler({
                                  popoverName: "editEmployeePersonalDetail",
                                  updateEmployeeId,
                              })
                            : addEmployeePopoverHandler(
                                  "addEmployeePersonalDetail"
                              );
                    }}
                    className={classNames(
                        addEmployeePopover.addEmployeePersonalDetail ||
                            editEmployeePopover.editEmployeePersonalDetail
                            ? "text-opacity-100 dark:text-opacity-100"
                            : "text-opacity-50 dark:text-opacity-50",
                        "text-sm md:text-xl dark:text-slate-100  text-gray-900 font-semibold transition-all"
                    )}
                >
                    Personal
                    <div
                        className={classNames(
                            addEmployeePopover.addEmployeePersonalDetail ||
                                editEmployeePopover.editEmployeePersonalDetail
                                ? ""
                                : "hidden",
                            "dark:bg-blueAccent-600 h-1 mt-2 "
                        )}
                    ></div>
                </button>
            </div>

            <button
                onClick={() => {
                    isEditing
                        ? editEmployeePopoverHandler({
                              popoverName: "editEmployeeProfessionalDetail",
                              updateEmployeeId,
                          })
                        : addEmployeePopoverHandler(
                              "addEmployeeProfessionalDetail"
                          );
                }}
                className={classNames(
                    addEmployeePopover.addEmployeeProfessionalDetail ||
                        editEmployeePopover.editEmployeeProfessionalDetail
                        ? "text-opacity-100 dark:text-opacity-100"
                        : "text-opacity-50 dark:text-opacity-50",
                    "text-sm md:text-xl dark:text-slate-100  text-gray-900 font-semibold transition-all"
                )}
            >
                Professional
                <div
                    className={classNames(
                        addEmployeePopover.addEmployeeProfessionalDetail ||
                            editEmployeePopover.editEmployeeProfessionalDetail
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
