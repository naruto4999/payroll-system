import { flexRender } from '@tanstack/react-table';
import { FaRegTrashAlt, FaPen, FaAngleUp, FaAngleDown, FaEye } from 'react-icons/fa';
import { FaCircleCheck } from 'react-icons/fa6';
import { useRef, useEffect, useState } from 'react';

const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};

const EmployeeTable = ({
  table,
  tbodyRef,
  handleKeyDown,
  focusedRowRef,
  // isTableFilterInputFocused,
  onRowClick,
  memoizedSelectedDate,
}) => {
  // useEffect(() => {
  //   if (focusedRowRef.current && !isTableFilterInputFocused) {
  //     // focusedRowRef.current.focus();
  //     const rowToFocus = tbodyRef.current?.children.namedItem(focusedRowRef.current);
  //
  //     if (rowToFocus) {
  //       rowToFocus.focus();
  //     }
  //   }
  // }, [])

  return (
    <div className="py-2">
      <div className="scrollbar mx-auto max-h-[30dvh] max-w-full overflow-y-auto rounded border border-black border-opacity-50 shadow-md lg:max-h-[30dvh]">
        <table className="w-full border-collapse text-center text-xs">
          <thead className="z-10 sticky top-0 bg-blueAccent-600 dark:bg-blueAccent-700">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <th key={header.id} scope="col" className="px-4 py-2 font-medium">
                    {header.isPlaceholder ? null : (
                      <div className="">
                        <div
                          {...{
                            className: header.column.getCanSort()
                              ? 'cursor-pointer select-none flex flex-row justify-center'
                              : '',
                            onClick: header.column.getToggleSortingHandler(),
                          }}
                        >
                          {flexRender(header.column.columnDef.header, header.getContext())}

                          {header.column.getCanSort() ? (
                            <div className="relative pl-2">
                              <FaAngleUp
                                className={classNames(
                                  header.column.getIsSorted() == 'asc'
                                    ? 'text-teal-700'
                                    : '',
                                  'absolute -translate-y-2 text-sm'
                                )}
                              />
                              <FaAngleDown
                                className={classNames(
                                  header.column.getIsSorted() == 'desc'
                                    ? 'text-teal-700'
                                    : '',
                                  'absolute translate-y-2 text-sm'
                                )}
                              />
                            </div>
                          ) : (
                            ''
                          )}
                        </div>
                      </div>
                    )}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody
            ref={tbodyRef}
            className="max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50"
          >
            {table.getRowModel().rows.map((row) => (
              <tr
                className=" hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50"
                key={row.original.id}
                id={row.original.id}
                onKeyDown={(e) => handleKeyDown(e, row)}
                tabIndex={-1}
                data-row-id={row.original.id}
                onClick={(e) => {
                  onRowClick(e, row);
                }}
              >
                {row.getVisibleCells().map((cell) => (
                  <td className="relative px-4 py-2 font-normal" key={cell.id}>
                    {/* {row.original.id == */}
                    {/*   tbodyRef.current?.children */}
                    {/*     .namedItem(focusedRowRef.current) */}
                    {/*     ?.getAttribute('data-row-id') && */}
                    {/*   cell.id.includes('paycode') && ( */}
                    {/*     <div className="absolute "> */}
                    {/*       <FaCircleCheck className="absolute scale-150 text-blueAccent-600" /> */}
                    {/*     </div> */}
                    {/*   )} */}
                    {row.original.id ==
                      focusedRowRef.current &&
                      cell.id.includes('paycode') && (
                        <div className="absolute left-2">
                          <FaCircleCheck className="scale-150 text-blueAccent-600" />
                        </div>
                      )}
                    <div className="text-xs">
                      <div className="font-medium">
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </div>
                    </div>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
export default EmployeeTable;
