import React from 'react';
import { FaCircleCheck } from 'react-icons/fa6';
import { FaRegTrashAlt, FaPen, FaAngleUp, FaAngleDown, FaEye } from 'react-icons/fa';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};
const EmployeeTable = ({ table, flexRender }) => {
	return (
		<div className="scrollbar mx-auto max-h-[80dvh] max-w-7xl overflow-y-auto rounded border border-black border-opacity-50 shadow-md lg:max-h-[84dvh]">
			<table className="w-full border-collapse text-center text-sm">
				<thead className="sticky top-0 bg-blueAccent-600 dark:bg-blueAccent-700">
					{table.getHeaderGroups().map((headerGroup) => (
						<tr key={headerGroup.id}>
							{headerGroup.headers.map((header) => (
								<th key={header.id} scope="col" className="px-4 py-4 font-medium">
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

												{/* {console.log(
                                                            header.column.getIsSorted()
                                                        )} */}
												{header.column.getCanSort() ? (
													<div className="relative pl-2">
														<FaAngleUp
															className={classNames(
																header.column.getIsSorted() == 'asc'
																	? 'text-teal-700'
																	: '',
																'absolute -translate-y-2 text-lg'
															)}
														/>
														<FaAngleDown
															className={classNames(
																header.column.getIsSorted() == 'desc'
																	? 'text-teal-700'
																	: '',
																'absolute translate-y-2 text-lg'
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
				<tbody className="max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50">
					{table.getRowModel().rows.map((row) => (
						<tr
							className={`hover:bg-zinc-200 dark:hover:bg-zinc-800 ${
								row.original.resignationDate ? 'text-redAccent-500' : ''
							}`}
							key={row.id}
						>
							{row.getVisibleCells().map((cell) => (
								<td className="px-4 py-4 font-normal" key={cell.id}>
									<div className="text-sm">
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
	);
};

export default EmployeeTable;
