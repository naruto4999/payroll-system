import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { useSelector } from 'react-redux';
import { authActions } from '../authentication/store/slices/auth';
import { globalCompanyActions } from '../authentication/store/slices/globalCompany';
import { FaRegWindowClose, FaRegBuilding, FaChevronDown, FaBars, FaSignOutAlt } from 'react-icons/fa';
import SidebarItem from './SidebarItem';
import menuItems from './SidebarData';
import { Outlet } from 'react-router-dom';
import { NavLink } from 'react-router-dom';
import SwitchToggle from '../UI/ToggleSwitch';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const Sidebar = () => {
	const dispatch = useDispatch();
	const handleLogout = () => {
		// dispatch(authActions.logout());
		// dispatch(globalCompanyActions.deselectComapny());
		dispatch({ type: 'RESET' });
	};

	const auth = useSelector((state) => state.auth);

	let items = menuItems
		.map((main_menu_item) => {
			if (main_menu_item.title === 'Admin Controls') {
				return auth.account.role === 'OWNER' && auth.account.is_admin === true ? main_menu_item : null;
			} else {
				return main_menu_item;
			}
		})
		.filter(Boolean)
		.map((main_menu_item) => {
			return main_menu_item.title === 'Master Entry'
				? {
						...main_menu_item,
						children: main_menu_item.children.filter((item) => {
							return item.title === 'Setup Entry' ? auth.account.role === 'OWNER' : true;
						}),
				  }
				: main_menu_item;
		});

	// console.log(auth)
	// if (auth.account.role == 'OWNER' && auth.account.is_admin == true) {
	// 	items = menuItems;
	// 	// const items = itemsWithoutAdminControl
	// }
	const [showSidebar, setShowSidebar] = useState(false);
	const [showLoadingBar, setShowLoadingBar] = useState(false);
	const sidebarHandler = () => {
		setShowSidebar(!showSidebar);
	};
	console.log();

	const [theme, setTheme] = useState('dark');

	// useEffect(() => {
	// 	if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
	// 		setTheme('dark');
	// 	} else {
	// 		setTheme('light');
	// 	}
	// }, []);

	useEffect(() => {
		if (theme == 'dark') {
			document.documentElement.classList.add('dark');
		} else {
			document.documentElement.classList.remove('dark');
		}
	}, [theme]);

	const themeSwitch = () => {
		setTheme(theme === 'dark' ? 'light' : 'dark');
	};

	return (
		<>
			<div className={classNames(showSidebar == false ? '' : 'hidden', 'relative z-40 cursor-pointer px-4')}>
				<FaBars
					className="fixed mt-2 -translate-x-2 p-1 text-3xl hover:rounded hover:border hover:text-teal-600"
					onClick={sidebarHandler}
				/>
				<div className="fixed right-4 z-20 mt-2 flex flex-row items-center gap-2 text-xs dark:text-slate-100 dark:text-opacity-70 sm:text-base">
					Dark
					<SwitchToggle theme={theme} switch={themeSwitch} />
				</div>
			</div>
			<section className="relative flex flex-row gap-0">
				<div>
					{/* <button
                className="absolute bottom-0 right-0 bg-teal-700 h-10 rounded-lg p-2 hover:bg-teal-600"
                onClick={handleLogout}
            >
                Bish me Logout uwu
            </button> */}

					<div
						className={classNames(
							showSidebar == false ? '-ml-80' : 'md:flex-shrink-0',
							'scrollbar fixed top-0 bottom-0 z-20 h-screen w-[300px] overflow-y-auto bg-zinc-200 bg-opacity-70 p-2 transition-all duration-300 dark:bg-black dark:bg-opacity-90 md:sticky md:dark:bg-opacity-40'
						)}
					>
						<div className="text-xl">
							<div className="mt-1 flex items-center p-2.5">
								<h1 className="ml-3 text-xl font-bold">PAY-PER</h1>
								<FaRegWindowClose
									className="absolute right-0 mx-4 cursor-pointer"
									onClick={sidebarHandler}
								/>
							</div>

							{/* Line Divide */}
							<div className="my-2 h-[1px] bg-gray-600"></div>
						</div>

						<NavLink
							className="mt-3 flex cursor-pointer items-center rounded-md p-2.5 px-4 duration-300 hover:bg-teal-500 dark:hover:bg-teal-600"
							to="/home/select-company"
						>
							<FaRegBuilding />
							<span className="ml-4 text-[15px] font-bold">Select Company</span>
						</NavLink>

						<div className="my-4 h-[1px] bg-gray-600"></div>

						{/* Sidebar Items go here */}
						{items.map((item, index) => (
							<SidebarItem key={index} item={item} />
						))}

						<div
							className="mt-3 flex cursor-pointer items-center rounded-md p-2.5 px-4 duration-300 hover:bg-teal-500 dark:hover:bg-teal-600"
							onClick={handleLogout}
						>
							<FaSignOutAlt />
							<span className="ml-4 text-[15px] font-bold">Logout</span>
						</div>
					</div>
				</div>
				<div
					className={classNames(
						showLoadingBar == true ? '' : 'hidden',
						'overflow-x:hidden fixed top-0 z-50 h-1 w-10 animate-[loading-bar_1s_infinite_linear] rounded bg-orange-700 dark:bg-orange-200 sm:w-14 sm:animate-[loading-bar_1.5s_infinite_linear] md:animate-loading-bar'
					)}
				></div>

				<div className="relative grow">
					<div className="top-0 h-[30px]"></div>
					<Outlet context={[showLoadingBar, setShowLoadingBar]} />
				</div>
			</section>
		</>
	);
};

export default Sidebar;
