import { FaBars } from 'react-icons/fa';
import { FiBriefcase, FiMoon, FiSun } from 'react-icons/fi';
import { useSelector } from 'react-redux';
import SwitchToggle from '../UI/ToggleSwitch';

const WorkspaceTopBar = ({ showSidebar, openButtonRef, onOpenNavigation, theme, onThemeChange, children }) => {
	const company = useSelector((state) => state.globalCompany);
	const companyName = company.name || 'Select a company';

	return (
		<div className="workspace-topbar-row">
			<div>
				{!showSidebar && (
					<button
						type="button"
						ref={openButtonRef}
						className="sidebar-open-button"
						aria-label="Open navigation"
						aria-expanded={showSidebar}
						aria-controls="payroll-sidebar"
						onClick={onOpenNavigation}
					>
						<FaBars aria-hidden="true" />
					</button>
				)}
			</div>
			<header className="workspace-topbar" aria-label="Workspace controls">
				<div
					className="workspace-topbar-company"
					title={companyName}
				>
					<FiBriefcase aria-hidden="true" />
					<span>{companyName}</span>
				</div>
				{/* Space for subscription information and other workspace status. */}
				<div className="workspace-topbar-status">{children}</div>
				<div className="workspace-theme-control">
					{theme === 'dark' ? <FiMoon aria-hidden="true" /> : <FiSun aria-hidden="true" />}
					<span>{theme === 'dark' ? 'Dark' : 'Light'}</span>
					<SwitchToggle compact theme={theme} switch={onThemeChange} />
				</div>
			</header>
			<div aria-hidden="true" />
		</div>
	);
};

export default WorkspaceTopBar;
