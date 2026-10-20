import React, { useState, useEffect, useRef } from 'react';
import { useDispatch } from 'react-redux';
import { useSelector } from 'react-redux';
import { FaTimes, FaRegBuilding, FaSignOutAlt } from 'react-icons/fa';
import SidebarItem from './SidebarItem';
import menuItems from './SidebarData';
import { Outlet, useLocation } from 'react-router-dom';
import { NavLink } from 'react-router-dom';
import WorkspaceTopBar from './WorkspaceTopBar';
import './Sidebar.css';

const classNames = (...classes) => {
	return classes.filter(Boolean).join(' ');
};

const Sidebar = () => {
	const dispatch = useDispatch();
	const { pathname } = useLocation();
	const navigationRef = useRef(null);
	const openButtonRef = useRef(null);
	const handleLogout = () => {
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
				: main_menu_item.title === 'Settings'
					? {
							...main_menu_item,
							children: main_menu_item.children.filter(
								(item) => item.title !== 'Report Settings' || auth.account.role === 'OWNER'
							),
						}
					: main_menu_item;
		});

	const [showSidebar, setShowSidebar] = useState(false);
	const [showLoadingBar, setShowLoadingBar] = useState(false);
	const sidebarHandler = () => {
		setShowSidebar(!showSidebar);
	};
	const closeSidebar = () => {
		setShowSidebar(false);
		requestAnimationFrame(() => openButtonRef.current?.focus());
	};
	const handleNavigate = () => {
		if (window.innerWidth < 768) closeSidebar();
	};

	useEffect(() => {
		if (!showSidebar) return;
		const frame = requestAnimationFrame(() => {
			navigationRef.current?.querySelector('[aria-current="page"]')?.scrollIntoView({ block: 'nearest' });
		});
		const handleKeyDown = (event) => {
			if (event.key === 'Escape') closeSidebar();
		};
		window.addEventListener('keydown', handleKeyDown);
		return () => {
			cancelAnimationFrame(frame);
			window.removeEventListener('keydown', handleKeyDown);
		};
	}, [showSidebar, pathname]);

	const [theme, setTheme] = useState('dark');

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
		<section className="workspace-shell relative flex flex-row gap-0">
			{showSidebar && (
				<button
					type="button"
					className="sidebar-backdrop"
					aria-label="Close navigation overlay"
					onClick={closeSidebar}
				/>
			)}
			<div className="sidebar-container">
				<aside
					id="payroll-sidebar"
					className={`payroll-sidebar${showSidebar ? ' payroll-sidebar-open' : ''}`}
					aria-label="Sidebar"
				>
					<header className="sidebar-header">
						<div>
							<img
								src={`${import.meta.env.VITE_PUBLIC_URL}logo_text_dark.svg`}
								alt="PAY-PER Logo"
								className="h-4 w-auto"
							/>
						</div>
						<button
							type="button"
							className="sidebar-close-button"
							aria-label="Close navigation"
							onClick={closeSidebar}
						>
							<FaTimes aria-hidden="true" />
						</button>
					</header>
					<nav ref={navigationRef} className="sidebar-navigation scrollbar" aria-label="Main navigation">
						<NavLink
							className={({ isActive }) =>
								`sidebar-link sidebar-company${isActive ? ' sidebar-link-active' : ''}`
							}
							to="/home/select-company"
							onClick={handleNavigate}
						>
							<FaRegBuilding className="sidebar-icon" aria-hidden="true" />
							<span className="sidebar-label">Select Company</span>
						</NavLink>
						<p className="sidebar-navigation-label">Workspace</p>
						{items.map((item) => (
							<SidebarItem key={item.title} item={item} onNavigate={handleNavigate} />
						))}
						<div className="sidebar-footer">
							<button type="button" className="sidebar-link sidebar-logout" onClick={handleLogout}>
								<FaSignOutAlt className="sidebar-icon" aria-hidden="true" />
								<span className="sidebar-label">Logout</span>
							</button>
						</div>
					</nav>
				</aside>
			</div>
			<div
				className={classNames(
					showLoadingBar == true ? '' : 'hidden',
					'overflow-x:hidden fixed top-0 z-50 h-1 w-10 animate-[loading-bar_1s_infinite_linear] rounded bg-orange-700 dark:bg-orange-200 sm:w-14 sm:animate-[loading-bar_1.5s_infinite_linear] md:animate-loading-bar'
				)}
			></div>

			<div className="relative min-w-0 grow">
				<WorkspaceTopBar
					showSidebar={showSidebar}
					openButtonRef={openButtonRef}
					onOpenNavigation={sidebarHandler}
					theme={theme}
					onThemeChange={themeSwitch}
				/>
				<Outlet context={[showLoadingBar, setShowLoadingBar]} />
			</div>
		</section>
	);
};

export default Sidebar;
