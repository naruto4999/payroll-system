import React from 'react';
import { useGetPfEsiSetupQuery } from '../../../../authentication/api/pfEsiSetupApiSlice';

const DeductionsForCalculateOtAttendanceUsingEarnedSalary = ({
    globalCompany,
    updateEmployeeId,
    formValues,
    currentEmployeeSalaryDetails,
    currentEmployeePfEsiDetails,
}) => {
    const {
        data: { company, ...companyPfEsiSetup } = {},
        isLoading,
        isSuccess,
        isError,
        error,
        isFetching,
    } = useGetPfEsiSetupQuery(globalCompany.id, {
        skip: globalCompany === null || globalCompany === '',
    });

    console.log(formValues);
    return (
        <table className="w-full border-collapse text-center text-xs">
            <thead className="sticky top-0 z-20 bg-red-500 dark:bg-red-500 dark:bg-opacity-40">
                <tr>
                    <th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">Deductions</th>
                    <th className="border border-slate-400 border-opacity-60 px-4 py-2 font-medium">Amount</th>
                </tr>
            </thead>
            <tbody className="h-fit max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50 ">
                <tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
                    <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">PF</td>
                    <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
                        {formValues?.employeeSalaryPrepared?.pfDeducted || 0}
                    </td>
                </tr>
                <tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
                    <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">ESI</td>
                    <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
                        {formValues?.employeeSalaryPrepared?.esiDeducted || 0}
                    </td>
                </tr>
                {companyPfEsiSetup?.enableLabourWelfareFund && currentEmployeeSalaryDetails?.labourWellfareFund && (
                    <tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
                        <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
                            LWF
                        </td>
                        <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
                            {formValues?.employeeSalaryPrepared?.labourWelfareFundDeducted || 0}
                        </td>
                    </tr>
                )}
                <tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
                    <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">VPF</td>
                    <td className="relative border border-slate-400 border-opacity-60 bg-opacity-50 p-0 font-normal dark:bg-zinc-800">
                        {formValues?.employeeSalaryPrepared?.vpf || 0}
                    </td>
                </tr>
                <tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
                    <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">
                        Advance
                    </td>
                    <td className="relative border border-slate-400 border-opacity-60 bg-opacity-50 p-0 font-normal dark:bg-zinc-800">
                        {formValues?.employeeSalaryPrepared?.advanceDeducted || 0}
                    </td>
                </tr>
                <tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
                    <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">TDS</td>
                    <td className="relative border border-slate-400 border-opacity-60 bg-opacity-50 p-0 font-normal dark:bg-zinc-800">
                        {formValues?.employeeSalaryPrepared?.tdsDeducted || 0}
                    </td>
                </tr>
                <tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
                    <td className="relative border border-slate-400 border-opacity-60 px-4 py-2 font-normal">Others</td>
                    <td className="relative border border-slate-400 border-opacity-60 bg-opacity-50 p-0 font-normal dark:bg-zinc-800">
                        {formValues?.employeeSalaryPrepared?.othersDeducted || 0}
                    </td>
                </tr>
                <tr className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50">
                    <td className="relative border-opacity-60 px-4 py-2 font-medium text-orange-500">Total</td>
                    <td className="relative border-opacity-60 px-4 py-2 font-medium text-orange-500">
                        {(formValues?.employeeSalaryPrepared?.pfDeducted || 0) +
                            (formValues?.employeeSalaryPrepared?.esiDeducted || 0) +
                            (formValues?.employeeSalaryPrepared?.vpfDeducted || 0) +
                            (formValues?.employeeSalaryPrepared?.advanceDeducted || 0) +
                            (formValues?.employeeSalaryPrepared?.tdsDeducted || 0) +
                            (formValues?.employeeSalaryPrepared?.othersDeducted || 0) +
                            (formValues?.employeeSalaryPrepared?.labourWelfareFundDeducted || 0)}
                    </td>
                </tr>
            </tbody>
        </table>
    );
};

export default DeductionsForCalculateOtAttendanceUsingEarnedSalary;
