import React, { useEffect, useState } from 'react';
import BigNumber from 'bignumber.js';

const NetSalary = React.memo(({ values, updateEmployeeId }) => {
  const [netPayableSalary, setNetPayableSalary] = useState(0);

  useEffect(() => {
    if (updateEmployeeId) {
      let netSalary = new BigNumber(0);
      console.log(values);
      const totalEarned = new BigNumber(
        values?.earnedAmount?.reduce((accumulator, item) => {
          return accumulator + Number(item.earnedAmount || 0);
        }, 0)
      );
      // Deductions
      const labourWelfareFundDeducted = new BigNumber(values.employeeSalaryPrepared.labourWelfareFundDeducted);
      const pfDeducted = new BigNumber(
        typeof values.employeeSalaryPrepared.pfDeducted == 'number'
          ? values.employeeSalaryPrepared.pfDeducted
          : 0
      );
      const esiDeducted = new BigNumber(
        typeof values.employeeSalaryPrepared.esiDeducted == 'number'
          ? values.employeeSalaryPrepared.esiDeducted
          : 0
      );
      const vpfDeducted = new BigNumber(
        typeof values.employeeSalaryPrepared.vpfDeducted == 'number'
          ? values.employeeSalaryPrepared.vpfDeducted
          : 0
      );
      const advanceDeducted = new BigNumber(
        typeof values.employeeSalaryPrepared.advanceDeducted == 'number'
          ? values.employeeSalaryPrepared.advanceDeducted
          : 0
      );
      const tdsDeducted = new BigNumber(
        typeof values.employeeSalaryPrepared.tdsDeducted == 'number'
          ? values.employeeSalaryPrepared.tdsDeducted
          : 0
      );
      const othersDeducted = new BigNumber(
        typeof values.employeeSalaryPrepared.othersDeducted == 'number'
          ? values.employeeSalaryPrepared.othersDeducted
          : 0
      );
      const incentiveAmount = new BigNumber(
        typeof values.employeeSalaryPrepared.incentiveAmount == 'number'
          ? values.employeeSalaryPrepared.incentiveAmount
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
    values.earnedAmount.map((item) => item.earnedAmount).join(','),
    values.employeeSalaryPrepared.incentiveAmount,
    values.employeeSalaryPrepared.labourWelfareFundDeducted,
    values.employeeSalaryPrepared.pfDeducted,
    values.employeeSalaryPrepared.esiDeducted,
    values.employeeSalaryPrepared.advanceDeducted,
    values.employeeSalaryPrepared.tdsDeducted,
    values.employeeSalaryPrepared.othersDeducted,
    values.employeeSalaryPrepared.vpfDeducted,
  ]);
  return (
    <div className="mx-auto mt-4 w-fit">
      <h2 className="inline text-xl dark:text-slate-300">Net Salary:</h2>
      <span className="ml-2 text-2xl font-bold dark:text-green-600">{netPayableSalary || 0}</span>
    </div>
  );
});

export default NetSalary;
