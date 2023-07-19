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
    getSingleEmployeeProfessionalDetail,
    globalCompany,
}) => {
    console.log(updateEmployeeId);
    return (
        // <h1>HI</h1>
        <div className=" h-10 w-fit flex flex-row justify-center gap-8 mt-6 md:mt-0 mx-auto">
            <button
                onClick={() => {
                    isEditing
                        ? editEmployeePopoverHandler({
                              popoverName: "editEmployeePersonalDetail",
                              id: updateEmployeeId,
                          })
                        : null;
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

            <button
                onClick={() => {
                    if (isEditing) {
                        editEmployeePopoverHandler({
                            popoverName: "editEmployeeProfessionalDetail",
                            id: updateEmployeeId,
                        });
                        // getSingleEmployeeProfessionalDetail({globalCompany, id: updateEmployeeId})
                    } 
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
            <button
                onClick={() => {
                    if (isEditing) {
                        editEmployeePopoverHandler({
                            popoverName: "editEmployeeSalaryDetail",
                            id: updateEmployeeId,
                        });
                        // getSingleEmployeeProfessionalDetail({globalCompany, id: updateEmployeeId})
                    }
                }}
                className={classNames(
                    addEmployeePopover.addEmployeeSalaryDetail ||
                        editEmployeePopover.editEmployeeSalaryDetail
                        ? "text-opacity-100 dark:text-opacity-100"
                        : "text-opacity-50 dark:text-opacity-50",
                    "text-sm md:text-xl dark:text-slate-100  text-gray-900 font-semibold transition-all"
                )}
            >
                Salary
                <div
                    className={classNames(
                        addEmployeePopover.addEmployeeSalaryDetail ||
                            editEmployeePopover.editEmployeeSalaryDetail
                            ? ""
                            : "hidden",
                        "dark:bg-blueAccent-600 h-1 mt-2 "
                    )}
                ></div>
            </button>
            <button
                onClick={() => {
                    if (isEditing) {
                        editEmployeePopoverHandler({
                            popoverName: "editEmployeePfEsiDetail",
                            id: updateEmployeeId,
                        });
                    }
                }}
                className={classNames(
                    addEmployeePopover.addEmployeePfEsiDetail ||
                        editEmployeePopover.editEmployeePfEsiDetail
                        ? "text-opacity-100 dark:text-opacity-100"
                        : "text-opacity-50 dark:text-opacity-50",
                    "text-sm md:text-xl dark:text-slate-100  text-gray-900 font-semibold transition-all"
                )}
            >
                ESI & PF
                <div
                    className={classNames(
                        addEmployeePopover.addEmployeePfEsiDetail ||
                            editEmployeePopover.editEmployeePfEsiDetail
                            ? ""
                            : "hidden",
                        "dark:bg-blueAccent-600 h-1 mt-2 "
                    )}
                ></div>
            </button>
            <button
                onClick={() => {
                    if (isEditing) {
                        editEmployeePopoverHandler({
                            popoverName: "editEmployeeFamilyNomineeDetail",
                            id: updateEmployeeId,
                        });
                    }
                }}
                className={classNames(
                    addEmployeePopover.addEmployeeFamilyNomineeDetail ||
                        editEmployeePopover.editEmployeeFamilyNomineeDetail
                        ? "text-opacity-100 dark:text-opacity-100"
                        : "text-opacity-50 dark:text-opacity-50",
                    "text-sm md:text-xl dark:text-slate-100  text-gray-900 font-semibold transition-all"
                )}
            >
                Family/Nominee
                <div
                    className={classNames(
                        addEmployeePopover.addEmployeeFamilyNomineeDetail ||
                            editEmployeePopover.editEmployeeFamilyNomineeDetail
                            ? ""
                            : "hidden",
                        "dark:bg-blueAccent-600 h-1 mt-2 "
                    )}
                ></div>
            </button>
        </div>
    );
};

export default AddEmployeeNavigationBar;
