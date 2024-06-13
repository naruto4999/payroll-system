import React, { useMemo } from 'react';

const FromYearSelector = React.memo(({ setYear, year, earliestMonthAndYear }) => {

  const optionsForYear = useMemo(() => {
    if (earliestMonthAndYear) {
      const options = [];
      for (let i = earliestMonthAndYear.earliestYear; i <= new Date().getFullYear(); i++) {
        options.push(
          <option key={i} value={i}>
            {i}
          </option>
        );
      }
      return options;
    }
  }, [earliestMonthAndYear]);
  return (
    <div className=''>
      <label
        htmlFor="year"
        className="mr-4 text-sm font-medium text-black text-opacity-100 dark:text-white dark:text-opacity-70"
      >
        From Year :
      </label>

      <select
        name="year"
        id="year"
        onChange={(e) => {
          setYear(e.target.value);
        }}
        value={year}
        className="my-1 w-20 rounded-md bg-zinc-50 bg-opacity-50 p-1 dark:bg-zinc-700"
      >
        {optionsForYear}
      </select>
    </div>
  );
});

export default FromYearSelector;

