import React, { useEffect } from 'react';
import { useGetCompaniesQuery } from '../../../../authentication/api/newCompanyEntryApiSlice';
import { globalCompanyActions } from '../../../../authentication/store/slices/globalCompany';
import { useSelector, useDispatch } from 'react-redux';
import { useOutletContext } from 'react-router-dom';
import { FiCheck } from 'react-icons/fi';
import { HiOutlineOfficeBuilding } from 'react-icons/hi';

const SelectCompany = () => {
	const { data: companies = [], isLoading, isError, refetch } = useGetCompaniesQuery();
	const [, setShowLoadingBar] = useOutletContext();
	const globalCompany = useSelector((state) => state.globalCompany);
	const dispatch = useDispatch();

	useEffect(() => {
		setShowLoadingBar(isLoading);
	}, [isLoading, setShowLoadingBar]);

	return (
		<section className="mx-4 pb-6 sm:mx-5" aria-labelledby="select-company-heading">
			<header className="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-200 pb-2 dark:border-zinc-800">
				<div>
					<h1
						id="select-company-heading"
						className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100"
					>
						Select a company
					</h1>
					<p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
						Choose the company you want to work with.
					</p>
				</div>
				{!isLoading && !isError && (
					<span className="rounded-full border border-zinc-200 bg-white px-2.5 py-1 text-xs font-medium text-zinc-600 dark:border-zinc-700/70 dark:bg-zinc-800/50 dark:text-zinc-400">
						{companies.length} {companies.length === 1 ? 'company' : 'companies'}
					</span>
				)}
			</header>

			{isLoading ? (
				<div role="status" className="mt-4">
					<span className="sr-only">Loading companies</span>
					<div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3" aria-hidden="true">
						{[0, 1].map((index) => (
							<div
								key={index}
								className="h-44 rounded-xl border border-zinc-200 bg-zinc-100 motion-safe:animate-pulse dark:border-zinc-800 dark:bg-zinc-800/50"
							/>
						))}
					</div>
				</div>
			) : isError ? (
				<div
					role="alert"
					className="mt-4 rounded-xl border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900"
				>
					<p className="text-sm text-zinc-600 dark:text-zinc-400">
						Unable to load your companies. Please try again.
					</p>
					<button
						type="button"
						onClick={refetch}
						className="mt-2 rounded text-sm font-medium text-teal-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 dark:text-teal-400"
					>
						Try again
					</button>
				</div>
			) : companies.length === 0 ? (
				<div className="mt-4 rounded-xl border border-dashed border-zinc-300 p-6 text-center dark:border-zinc-700">
					<HiOutlineOfficeBuilding className="mx-auto mb-2 h-6 w-6 text-zinc-400" aria-hidden="true" />
					<p className="text-sm font-medium">No companies available</p>
					<p className="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
						Your companies will appear here once they have been added.
					</p>
				</div>
			) : (
				<>
					<div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
						{companies.map((company) => {
							const isSelected = globalCompany.id == company.id;
							return (
								<button
									key={company.id}
									type="button"
									aria-pressed={isSelected}
									onClick={() =>
										dispatch(
											globalCompanyActions.setCompany({ id: company.id, name: company.name })
										)
									}
									className={`group flex min-w-0 flex-col rounded-xl border p-4 text-left transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500 focus-visible:ring-offset-2 motion-reduce:transition-none dark:focus-visible:ring-offset-zinc-900 ${
										isSelected
											? 'border-teal-500/70 bg-gradient-to-br from-teal-50 to-white shadow-sm dark:border-teal-500/50 dark:from-teal-900/30 dark:to-zinc-900'
											: 'border-zinc-200 bg-white hover:border-teal-400 hover:bg-teal-50/40 dark:border-zinc-700/60 dark:bg-zinc-800/30 dark:hover:border-teal-500/50 dark:hover:bg-zinc-800/70'
									}`}
								>
									<div className="mb-3 flex w-full items-center justify-between gap-2">
										<span
											className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${isSelected ? 'bg-teal-100 text-teal-700 dark:bg-teal-400/10 dark:text-teal-300' : 'bg-zinc-100 text-zinc-500 group-hover:text-teal-600 dark:bg-zinc-700/40 dark:text-zinc-400 dark:group-hover:text-teal-300'}`}
										>
											<HiOutlineOfficeBuilding className="h-5 w-5" aria-hidden="true" />
										</span>
										{isSelected && (
											<span className="flex items-center gap-1 rounded-full bg-teal-100 px-2 py-0.5 text-[11px] font-medium text-teal-800 dark:bg-teal-400/10 dark:text-teal-300">
												<FiCheck className="h-3 w-3" aria-hidden="true" /> Selected
											</span>
										)}
									</div>
									<span className="block w-full break-words text-sm font-semibold leading-5 text-zinc-900 dark:text-zinc-100">
										{company.name}
									</span>
								</button>
							);
						})}
					</div>
				</>
			)}
		</section>
	);
};
export default SelectCompany;
