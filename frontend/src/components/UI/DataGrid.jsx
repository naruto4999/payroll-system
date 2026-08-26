import React from 'react';
import { flexRender } from '@tanstack/react-table';
import { FaAngleDown, FaAngleUp } from 'react-icons/fa';
import { FaCircleCheck } from 'react-icons/fa6';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const DataGrid = React.memo(
	({
		table,
		tbodyRef,
		getRowId = (row) => row.id,
		selectedRowId,
		selectedIndicatorColumnId,
		onRowClick,
		onRowKeyDown,
		maxHeightClassName = 'max-h-[70dvh]',
		containerClassName,
		tableClassName,
		emptyMessage = 'No records found',
	}) => {
		const rows = table.getRowModel().rows;
		const visibleColumns = table.getVisibleLeafColumns();
		const visibleColumnCount = visibleColumns.length;

		return (
			<div className="py-2">
				<div
					className={classNames(
						'scrollbar mx-auto max-w-full overflow-y-auto rounded border border-black border-opacity-50 shadow-md',
						maxHeightClassName,
						containerClassName
					)}
				>
					<table className={classNames('w-full border-collapse text-center text-xs', tableClassName)}>
						<colgroup>
							{visibleColumns.map((column) => (
								<col key={column.id} className={column.columnDef.meta?.columnClassName} />
							))}
						</colgroup>
						<thead className="sticky top-0 z-20 bg-blueAccent-600 dark:bg-blueAccent-700">
							{table.getHeaderGroups().map((headerGroup) => (
								<tr key={headerGroup.id}>
									{headerGroup.headers.map((header) => {
										const headerMeta = header.column.columnDef.meta || {};
										const headerContentClassName = header.column.getCanSort()
											? headerMeta.headerContentClassName || 'justify-center'
											: headerMeta.headerContentClassName;

										return (
											<th
												key={header.id}
												scope="col"
												className={classNames('px-3 py-2 font-medium', headerMeta.headerClassName)}
											>
												{header.isPlaceholder ? null : (
													<div
														className={classNames(
															header.column.getCanSort()
																? 'flex cursor-pointer select-none flex-row'
																: '',
															headerContentClassName
														)}
														onClick={header.column.getToggleSortingHandler()}
													>
														{flexRender(header.column.columnDef.header, header.getContext())}

														{header.column.getCanSort() && (
															<div className="relative pl-2">
																<FaAngleUp
																	className={classNames(
																		header.column.getIsSorted() === 'asc' ? 'text-teal-700' : '',
																		'absolute -translate-y-2 text-sm'
																	)}
																/>
																<FaAngleDown
																	className={classNames(
																		header.column.getIsSorted() === 'desc' ? 'text-teal-700' : '',
																		'absolute translate-y-2 text-sm'
																	)}
																/>
															</div>
														)}
													</div>
												)}
											</th>
										);
									})}
								</tr>
							))}
						</thead>
						<tbody
							ref={tbodyRef}
							className="max-h-20 divide-y divide-black divide-opacity-50 overflow-y-auto border-t border-black border-opacity-50"
						>
							{rows.length === 0 ? (
								<tr>
									<td colSpan={visibleColumnCount} className="px-4 py-6 text-center text-slate-500 dark:text-slate-400">
										{emptyMessage}
									</td>
								</tr>
							) : (
								rows.map((row) => {
									const rowId = getRowId(row);
									const isSelected = String(rowId) === String(selectedRowId);

									return (
										<tr
											className={classNames(
														'outline-none hover:bg-zinc-200 dark:hover:bg-zinc-800 dark:focus:bg-teal-800 dark:focus:bg-opacity-50',
												isSelected ? 'bg-blueAccent-100 bg-opacity-60 dark:bg-blueAccent-900 dark:bg-opacity-40' : ''
											)}
											key={rowId}
											id={rowId}
											onKeyDown={(event) => onRowKeyDown?.(event, row)}
											tabIndex={-1}
											data-row-id={rowId}
											onClick={(event) => onRowClick?.(event, row)}
										>
											{row.getVisibleCells().map((cell) => {
												const showSelectedIndicator =
													isSelected &&
													selectedIndicatorColumnId &&
													cell.id.includes(selectedIndicatorColumnId);
												const renderedValue = flexRender(cell.column.columnDef.cell, cell.getContext());
												const rawValue = cell.getValue();
												const title = typeof rawValue === 'string' || typeof rawValue === 'number' ? String(rawValue) : undefined;

												return (
													<td
														className={classNames(
															showSelectedIndicator ? 'pl-8' : '',
															'relative px-3 py-2 font-normal',
															cell.column.columnDef.meta?.cellClassName
														)}
														key={cell.id}
														title={title}
													>
														{showSelectedIndicator && (
															<div className="absolute left-2">
																<FaCircleCheck className="scale-150 text-blueAccent-600" />
															</div>
														)}
														<div className={classNames('text-xs', cell.column.columnDef.meta?.cellContentClassName)}>
															<div className="font-medium">
																{renderedValue}
															</div>
														</div>
													</td>
												);
											})}
										</tr>
									);
								})
							)}
						</tbody>
					</table>
				</div>
			</div>
		);
	}
);

export default DataGrid;
