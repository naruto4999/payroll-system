import dayjs from 'dayjs';
import customParseFormat from 'dayjs/plugin/customParseFormat.js';
import timezone from 'dayjs/plugin/timezone.js';
import utc from 'dayjs/plugin/utc.js';

dayjs.extend(customParseFormat);
dayjs.extend(utc);
dayjs.extend(timezone);

const toPayrollDateTime = ({ year, month, day, time, payrollTimezone }) => {
	const wallTime = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')} ${time.slice(0, 5)}`;
	const value = dayjs.tz(wallTime, 'YYYY-MM-DD HH:mm', payrollTimezone);
	if (!value.isValid() || value.format('YYYY-MM-DD HH:mm') !== wallTime) {
		throw new Error(`${wallTime} is not a valid time in ${payrollTimezone}.`);
	}
	return value;
};

const exactInterval = (start, end, exclusions = []) => ({
	startDatetime: start.format(),
	endDatetime: end.format(),
	...(exclusions.length > 0 ? { exclusions } : {}),
});

const splitOffDayInterval = (start, end, exclusion) => {
	if (!exclusion) return [exactInterval(start, end)];

	const intervals = [];
	let segmentStart = start;
	while (segmentStart.isBefore(end)) {
		const nextMidnight = segmentStart.add(1, 'day').startOf('day');
		const segmentEnd = end.isBefore(nextMidnight) ? end : nextMidnight;
		const exclusionStart = exclusion.start.isAfter(segmentStart) ? exclusion.start : segmentStart;
		const exclusionEnd = exclusion.end.isBefore(segmentEnd) ? exclusion.end : segmentEnd;
		const segmentMinutes = segmentEnd.diff(segmentStart, 'minute');
		const segmentExcludedMinutes = Math.max(exclusionEnd.diff(exclusionStart, 'minute'), 0);

		// Overtime details require positive eligible minutes, so a fully excluded
		// payroll-date segment has no detail row of its own.
		if (segmentExcludedMinutes < segmentMinutes) {
			const exclusions = segmentExcludedMinutes > 0
				? [{
					startDatetime: exclusionStart.format(),
					endDatetime: exclusionEnd.format(),
					exclusionReason: 'MEAL_BREAK',
					exclusionNote: '',
				}]
				: [];
			intervals.push(exactInterval(segmentStart, segmentEnd, exclusions));
		}
		segmentStart = segmentEnd;
	}
	return intervals;
};

export const roundOvertimeMinutes = (minutes, increment = 30, roundUpFrom = 16) => {
	const value = Number(minutes);
	const roundingIncrement = Number(increment);
	const roundUpThreshold = Number(roundUpFrom);
	if (
		!Number.isFinite(value) ||
		!Number.isFinite(roundingIncrement) ||
		!Number.isFinite(roundUpThreshold) ||
		roundingIncrement <= 0 ||
		roundUpThreshold < 1 ||
		roundUpThreshold > roundingIncrement
	) {
		return value;
	}

	const remainder = value % roundingIncrement;
	return Math.floor(value / roundingIncrement) * roundingIncrement +
		(remainder >= roundUpThreshold ? roundingIncrement : 0);
};

export const calculatePolicyRoundedOvertime = ({ components = [], policy }) => {
	const rulesByDayType = new Map(
		(policy?.dayRules || []).map((rule) => [rule.dayType, String(rule.multiplier)])
	);
	const minutesByMultiplier = new Map();
	for (const component of components) {
		const multiplier = rulesByDayType.get(component.dayType);
		const eligibleMinutes = Number(component.eligibleMinutes) || 0;
		if (multiplier == null || eligibleMinutes <= 0) continue;
		minutesByMultiplier.set(multiplier, (minutesByMultiplier.get(multiplier) || 0) + eligibleMinutes);
	}

	let total = 0;
	for (const minutes of minutesByMultiplier.values()) {
		total += roundOvertimeMinutes(
			minutes,
			policy?.roundingIncrementMinutes,
			policy?.roundUpFromMinutes
		);
	}
	return total;
};

export const buildPolicyOvertimeComponents = ({ intervals = [], payrollTimezone, classifyWorkDate }) => {
	const components = [];
	for (const interval of intervals) {
		let segmentStart = dayjs(interval.startDatetime).tz(payrollTimezone);
		const intervalEnd = dayjs(interval.endDatetime).tz(payrollTimezone);
		while (segmentStart.isBefore(intervalEnd)) {
			const nextMidnight = segmentStart.add(1, 'day').startOf('day');
			const segmentEnd = intervalEnd.isBefore(nextMidnight) ? intervalEnd : nextMidnight;
			const grossMinutes = segmentEnd.diff(segmentStart, 'minute');
			let excludedMinutes = 0;
			for (const exclusion of interval.exclusions || []) {
				const exclusionStart = dayjs(exclusion.startDatetime).tz(payrollTimezone);
				const exclusionEnd = dayjs(exclusion.endDatetime).tz(payrollTimezone);
				const overlapStart = exclusionStart.isAfter(segmentStart) ? exclusionStart : segmentStart;
				const overlapEnd = exclusionEnd.isBefore(segmentEnd) ? exclusionEnd : segmentEnd;
				excludedMinutes += Math.max(overlapEnd.diff(overlapStart, 'minute'), 0);
			}
			if (!(interval.exclusions || []).length && segmentEnd.isSame(intervalEnd)) {
				excludedMinutes = Number(interval.excludedMinutes) || 0;
			}
			const eligibleMinutes = grossMinutes - excludedMinutes;
			const workDate = segmentStart.format('YYYY-MM-DD');
			if (eligibleMinutes > 0) {
				components.push({
					workDate,
					dayType: classifyWorkDate(workDate),
					grossMinutes,
					excludedMinutes,
					eligibleMinutes,
				});
			}
			segmentStart = segmentEnd;
		}
	}
	return components;
};

export const buildPunchOvertime = ({
	year,
	month,
	day,
	punchIn,
	punchOut,
	shift,
	fullSpanOffDay,
	payrollTimezone,
}) => {
	if (!punchIn || !punchOut || !shift || !payrollTimezone) {
		return { intervals: [], grossMinutes: 0, excludedMinutes: 0 };
	}

	const shiftStart = toPayrollDateTime({
		year,
		month,
		day,
		time: shift.beginningTime.slice(0, 5),
		payrollTimezone,
	});
	let shiftEnd = toPayrollDateTime({
		year,
		month,
		day,
		time: shift.endTime.slice(0, 5),
		payrollTimezone,
	});
	if (!shiftEnd.isAfter(shiftStart)) shiftEnd = shiftEnd.add(1, 'day');

	let effectiveIn = toPayrollDateTime({ year, month, day, time: punchIn, payrollTimezone });
	let effectiveOut = toPayrollDateTime({ year, month, day, time: punchOut, payrollTimezone });
	if (effectiveIn.isAfter(shiftEnd)) effectiveIn = effectiveIn.subtract(1, 'day');
	if (effectiveOut.isBefore(shiftStart)) effectiveOut = effectiveOut.add(1, 'day');
	if (!effectiveOut.isAfter(effectiveIn)) {
		return { intervals: [], grossMinutes: 0, excludedMinutes: 0 };
	}

	const thresholdMinutes = parseInt(shift.otBeginAfter, 10) || 0;
	if (fullSpanOffDay) {
		const grossMinutes = effectiveOut.diff(effectiveIn, 'minute');
		if (grossMinutes <= thresholdMinutes) {
			return { intervals: [], grossMinutes: 0, excludedMinutes: 0 };
		}

		let exclusion = null;
		let excludedMinutes = 0;
		if (shift.lunchBeginningTime && parseInt(shift.lunchDuration, 10) > 0) {
			let lunchStart = toPayrollDateTime({
				year,
				month,
				day,
				time: shift.lunchBeginningTime.slice(0, 5),
				payrollTimezone,
			});
			if (lunchStart.isBefore(shiftStart)) lunchStart = lunchStart.add(1, 'day');
			const lunchEnd = lunchStart.add(parseInt(shift.lunchDuration, 10), 'minute');
			const exclusionStart = effectiveIn.isAfter(lunchStart) ? effectiveIn : lunchStart;
			const exclusionEnd = effectiveOut.isBefore(lunchEnd) ? effectiveOut : lunchEnd;
			excludedMinutes = Math.max(exclusionEnd.diff(exclusionStart, 'minute'), 0);
			if (excludedMinutes > 0 && excludedMinutes < grossMinutes) {
				exclusion = { start: exclusionStart, end: exclusionEnd };
			} else {
				excludedMinutes = 0;
			}
		}

		return {
			intervals: splitOffDayInterval(effectiveIn, effectiveOut, exclusion),
			grossMinutes,
			excludedMinutes,
		};
	}

	const intervals = [];
	let grossMinutes = 0;
	const earlyMinutes = shiftStart.diff(effectiveIn, 'minute');
	if (earlyMinutes > thresholdMinutes) {
		intervals.push(exactInterval(effectiveIn, shiftStart));
		grossMinutes += earlyMinutes;
	}
	const lateMinutes = effectiveOut.diff(shiftEnd, 'minute');
	if (lateMinutes > thresholdMinutes) {
		intervals.push(exactInterval(shiftEnd, effectiveOut));
		grossMinutes += lateMinutes;
	}

	return { intervals, grossMinutes, excludedMinutes: 0 };
};
