import assert from 'node:assert/strict';
import test from 'node:test';
import { attendanceRowsMatchScope, getAttendanceScope, isAttendanceReady } from './attendanceScope.js';

const form = () => ({
	year: 2026,
	month: '10',
	attendanceScope: getAttendanceScope(65, 2618, 2026, 10),
	attendanceRequestId: 'loaded-request',
	attendance: { 1: { employee: 2618, company: 65, date: '2026-10-01' } },
});
const query = { status: 'fulfilled', requestId: 'loaded-request' };

test('only the loaded employee, company, and month can be submitted', () => {
	const values = form();
	assert.equal(isAttendanceReady(values, 65, '2618', query), true);
	assert.equal(isAttendanceReady(values, 65, 2619, query), false);
	assert.equal(isAttendanceReady(values, 43, 2618, query), false);
	assert.equal(isAttendanceReady({ ...values, month: 11 }, 65, 2618, query), false);
	assert.equal(isAttendanceReady({ ...values, year: 2025 }, 65, 2618, query), false);
});

test('refreshing, failed, and not-yet-hydrated results cannot be submitted', () => {
	const values = form();
	assert.equal(isAttendanceReady(values, 65, 2618, { ...query, status: 'pending' }), false);
	assert.equal(isAttendanceReady(values, 65, 2618, { ...query, status: 'rejected' }), false);
	assert.equal(isAttendanceReady(values, 65, 2618, { ...query, requestId: 'new-result' }), false);
	assert.equal(isAttendanceReady({ ...values, attendanceScope: null }, 65, 2618, query), false);
});

test('rows retain their own identity instead of being relabelled at submission', () => {
	const values = form();
	assert.equal(attendanceRowsMatchScope(values, 65, '2618'), true);
	assert.equal(attendanceRowsMatchScope(values, 65, 2619), false);
	assert.equal(attendanceRowsMatchScope(values, 43, 2618), false);
	assert.equal(attendanceRowsMatchScope({ ...values, month: 11 }, 65, 2618), false);
	values.attendance[2] = { employee: 2619, company: 65, date: '2026-10-02' };
	assert.equal(attendanceRowsMatchScope(values, 65, 2618), false);
	assert.equal(attendanceRowsMatchScope({ ...values, attendance: {} }, 65, 2618), false);
});
