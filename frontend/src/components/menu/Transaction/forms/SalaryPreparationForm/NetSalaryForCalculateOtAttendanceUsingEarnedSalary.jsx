import React, { useEffect, useState } from 'react';
import BigNumber from 'bignumber.js';

const NetSalaryForCalculateOtAttendanceUsingEarnedSalary = React.memo(({ formValues, updateEmployeeId }) => {
    const [netPayableSalary, setNetPayableSalary] = useState(0);

    useEffect(() => {
        if (updateEmployeeId) {
            let netSalary = new BigNumber(0);
            console.log(formValues);
            const totalEarned = new BigNumber(
                formValues?.earnedAmount?.reduce((accumulator, item) => {
                    return accumulator + Number(item.earnedAmount || 0);
                }, 0)
            );
            // Deductions
            const labourWelfareFundDeducted = new BigNumber(
                formValues.employeeSalaryPrepared.labourWelfareFundDeducted
            );
            const pfDeducted = new BigNumber(
                typeof formValues.employeeSalaryPrepared.pfDeducted == 'number'
                    ? formValues.employeeSalaryPrepared.pfDeducted
                    : 0
            );
            const esiDeducted = new BigNumber(
                typeof formValues.employeeSalaryPrepared.esiDeducted == 'number'
                    ? formValues.employeeSalaryPrepared.esiDeducted
                    : 0
            );
            const vpfDeducted = new BigNumber(
                typeof formValues.employeeSalaryPrepared.vpfDeducted == 'number'
                    ? formValues.employeeSalaryPrepared.vpfDeducted
                    : 0
            );
            const advanceDeducted = new BigNumber(
                typeof formValues.employeeSalaryPrepared.advanceDeducted == 'number'
                    ? formValues.employeeSalaryPrepared.advanceDeducted
                    : 0
            );
            const tdsDeducted = new BigNumber(
                typeof formValues.employeeSalaryPrepared.tdsDeducted == 'number'
                    ? formValues.employeeSalaryPrepared.tdsDeducted
                    : 0
            );
            const othersDeducted = new BigNumber(
                typeof formValues.employeeSalaryPrepared.othersDeducted == 'number'
                    ? formValues.employeeSalaryPrepared.othersDeducted
                    : 0
            );
            const incentiveAmount = new BigNumber(
                typeof formValues.employeeSalaryPrepared.incentiveAmount == 'number'
                    ? formValues.employeeSalaryPrepared.incentiveAmount
                    : 0
            );
            netSalary = netSalary
                .plus(totalEarned)
                .minus(pfDeducted)
                .minus(labourWelfareFundDeducted)
                .minus(esiDeducted)
                .minus(vpfDeducted)
                .minus(advanceDeducted)
                .minus(tdsDeducted)
                .minus(othersDeducted)
                .plus(incentiveAmount);
            setNetPayableSalary(netSalary.toNumber());
        }
    }, [
        formValues.earnedAmount.map((item) => item.earnedAmount).join(','),
        formValues.employeeSalaryPrepared.incentiveAmount,
        formValues.employeeSalaryPrepared.labourWelfareFundDeducted,
        formValues.employeeSalaryPrepared.pfDeducted,
        formValues.employeeSalaryPrepared.esiDeducted,
        formValues.employeeSalaryPrepared.advanceDeducted,
        formValues.employeeSalaryPrepared.tdsDeducted,
        formValues.employeeSalaryPrepared.othersDeducted,
        formValues.employeeSalaryPrepared.vpfDeducted,
    ]);
    return (
        <>
            <div className="mx-auto mt-4 w-fit">
                <h2 className="inline text-lg dark:text-slate-300">Net Salary:</h2>
                <span className="ml-2 text-xl font-bold dark:text-green-600">{netPayableSalary || 0}</span>
            </div>
            <div className="mx-auto w-fit">
                <h2 className="inline text-lg dark:text-slate-300">Net Payable (incl* of OT):</h2>
                <span className="ml-2 text-xl font-bold dark:text-blueAccent-600">
                    {(netPayableSalary || 0) + (formValues?.employeeSalaryPrepared?.netOtAmountMonthly || 0)}
                </span>
            </div>
        </>
    );
});

export default NetSalaryForCalculateOtAttendanceUsingEarnedSalary;
