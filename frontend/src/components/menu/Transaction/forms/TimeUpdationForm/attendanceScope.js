export const getAttendanceScope = (companyId, employeeId, year, month) =>
	companyId && employeeId && year && month
		? [companyId, employeeId, year, month].map(Number).join(':')
		: null;

// A completed request is not enough: Formik must have loaded that exact result.
export const isAttendanceReady = (values, companyId, employeeId, query) => {
	const scope = getAttendanceScope(companyId, employeeId, values.year, values.month);
	return Boolean(
		scope && values.attendanceScope === scope && query.status === 'fulfilled' &&
		query.requestId && values.attendanceRequestId === query.requestId
	);
};

export const attendanceRowsMatchScope = (values, companyId, employeeId) => {
	const rows = Object.values(values.attendance);
	return rows.length > 0 && rows.every((row) => {
		const [year, month] = String(row.date).split('-').map(Number);
		return Number(row.employee) === Number(employeeId) &&
			Number(row.company) === Number(companyId) &&
			year === Number(values.year) && month === Number(values.month);
	});
};
