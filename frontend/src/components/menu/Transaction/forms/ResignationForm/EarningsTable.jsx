import React from 'react';
import { useGetEarningsHeadsQuery } from '../../../../authentication/api/earningsHeadEntryApiSlice';
import { useEarnedAmountWithPreparedSalaryQuery } from '../../../../authentication/api/fullAndFinalApiSlice';

const EarningsTable = ({ globalCompany, fullAndFinalEmployeeId }) => {
  const {
    data: earningsHeads,
    isLoading: isLoadingEarningsHeads,
    isSuccess: isEarningsHeadsSuccess,
    isError: isEarningsHeadsError,
    error: earningsHeadsError,
  } = useGetEarningsHeadsQuery(globalCompany);

  const {
    data: earnedAmountWithPreparedSalary,
    isLoading: isLoadingEarnedAmountWithPreparedSalary,
    isSuccess: isEarnedAmountWithPreparedSalarySuccess,
    isError: isEarnedAmountWithPreparedSalaryError,
  } = useEarnedAmountWithPreparedSalaryQuery({ company: globalCompany.id, employee: fullAndFinalEmployeeId });
  return (
    <div>
      <table className="w-full border-collapse text-center text-xs">
        <thead className="sticky top-0 z-20 bg-yellow-600 text-slate-200 dark:bg-yellow-700 dark:bg-opacity-40">
          <tr>
            <th className="border border-slate-400 border-opacity-60 px-4 py-1.5 font-medium">
              Earning Head
            </th>
            <th className="border border-slate-400 border-opacity-60 px-4 py-1.5 font-medium">Rate</th>
            <th className="border border-slate-400 border-opacity-60 px-4 py-1.5 font-medium">Arear</th>
            <th className="border border-slate-400 border-opacity-60 px-4 py-1.5 font-medium">Earned</th>
          </tr>
        </thead>
        <tbody className="max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50 ">
          {earnedAmountWithPreparedSalary
            ?.slice() // Create a shallow copy to avoid mutating the original array
            .sort((a, b) => a.earningsHead.id - b.earningsHead.id) // Sort by id
            .map((earning, index) => (
              <tr
                key={index}
                className="hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50"
              >
                <td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 font-normal text-slate-200">
                  {earning.earningsHead.name}
                </td>
                <td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 text-right font-normal text-blueAccent-500">
                  {earning.rate}
                </td>
                <td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 text-right font-normal text-blueAccent-500">
                  {earning.arearAmount}
                </td>
                <td className="relative border border-slate-400 border-opacity-60 px-4 py-1.5 text-right font-normal dark:text-green-600">
                  {earning.earnedAmount}
                </td>
              </tr>
            ))}
        </tbody>
      </table>
      <div className="mt-1.5 text-sm font-medium text-slate-200">
        Incentive:{' '}
        <span className="dark:text-green-600">
          {earnedAmountWithPreparedSalary?.[0]?.salaryPrepared.incentiveAmount}
        </span>
      </div>
    </div>
  );
};

export default EarningsTable;
