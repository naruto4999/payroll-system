import React, { useEffect, useId, useState } from 'react';
import { FaChevronDown } from 'react-icons/fa';
import { NavLink, useLocation } from 'react-router-dom';

const containsRoute = (item, pathname) =>
	item.path
		? pathname === item.path || pathname.startsWith(`${item.path}/`)
		: item.children?.some((child) => containsRoute(child, pathname));

const SidebarItem = ({ item, onNavigate }) => {
	const { pathname } = useLocation();
	const isCurrentSection = containsRoute(item, pathname);
	const [expanded, setExpanded] = useState(isCurrentSection);
	const submenuId = useId();

	useEffect(() => {
		if (isCurrentSection) setExpanded(true);
	}, [pathname, isCurrentSection]);

	const icon = item.icon ? <item.icon className="sidebar-icon" aria-hidden="true" /> : null;

	if (item.children) {
		return (
			<div className="sidebar-group">
				<button
					type="button"
					className={`sidebar-link sidebar-group-toggle${isCurrentSection ? ' sidebar-current-section' : ''}`}
					aria-expanded={expanded}
					aria-controls={submenuId}
					onClick={() => setExpanded((value) => !value)}
				>
					{icon}
					<span className="sidebar-label">{item.title}</span>
					<FaChevronDown
						className={`sidebar-chevron${expanded ? ' sidebar-chevron-open' : ''}`}
						aria-hidden="true"
					/>
				</button>
				<div id={submenuId} className="sidebar-submenu" hidden={!expanded}>
					{item.children.map((child) => (
						<SidebarItem key={child.path || child.title} item={child} onNavigate={onNavigate} />
					))}
				</div>
			</div>
		);
	}

	return (
		<NavLink
			to={item.path}
			className={({ isActive }) => `sidebar-link${isActive ? ' sidebar-link-active' : ''}`}
			onClick={onNavigate}
		>
			{icon}
			<span className="sidebar-label">{item.title}</span>
		</NavLink>
	);
};

export default SidebarItem;
