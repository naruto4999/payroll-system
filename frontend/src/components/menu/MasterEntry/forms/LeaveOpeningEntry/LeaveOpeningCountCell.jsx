import React, { useState, useEffect } from 'react'

const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};


const LeaveOpeningCountCell = ({ getValue, row, column, table }) => {
  const initialValue = getValue() == null ? '' : getValue();
  const [value, setValue] = useState('');
  useEffect(() => {
    setValue(initialValue);
  }, [initialValue]);
  const onBlur = () => {
    table.options.meta?.updateData(row.index, column.id, isNaN(parseFloat(value)) ? 0 : parseFloat(value));
  };
  return (
    <>
      {/* {console.log(row.original.dateOfJoining)} */}
      <>
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onBlur={onBlur}
          className={classNames(value != undefined && value > 0 ? 'text-amber-400' : 'text-slate-400', 'inline w-10 cursor-text custom-number-input rounded border-[1px] border-gray-800 border-opacity-25 bg-zinc-50 bg-opacity-50 p-1 outline-none transition focus:border-opacity-100 dark:border-slate-100 dark:border-opacity-25 dark:bg-zinc-800 dark:focus:border-opacity-75')}

          type={column.columnDef.meta?.type || 'text'}
        />
      </>
    </>
  );
}

export default LeaveOpeningCountCell
