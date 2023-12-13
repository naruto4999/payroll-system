import { useCallback } from 'react';

const calculateAttendance = (day, lateMinValue, values, setFieldValue, present, absent, getShift, getTimeInDateObj) => {
	const manualMode = values.attendance[day]?.manualMode;
	if (!manualMode) {
		// const manualIn = values.attendance[day]?.manualIn;
		const manualIn =
			values.attendance[day]?.manualIn != ''
				? values.attendance[day]?.manualIn
				: values.attendance[day]?.machineIn;
		// console.log(values.attendance[day]?.machineIn);
		// const manualOut = values.attendance[day]?.manualOut;
		const manualOut =
			values.attendance[day]?.manualOut != ''
				? values.attendance[day]?.manualOut
				: values.attendance[day]?.machineOut;
		const shift = getShift(values.year, values.month, day);
		const shiftBeginningTime = getTimeInDateObj(shift.beginningTime, day);
		const shiftEndTime = getTimeInDateObj(
			shift.endTime,
			shift.beginningTime < shift.endTime ? parseInt(day) : parseInt(day) + 1
		);
		const manualInObj =
			manualIn < shift.endTime.slice(0, 5)
				? getTimeInDateObj(manualIn, shift.beginningTime < shift.endTime ? parseInt(day) : parseInt(day) + 1)
				: getTimeInDateObj(manualIn, shift.beginningTime < shift.endTime ? parseInt(day) - 1 : parseInt(day));
		const manualOutObj =
			manualOut >= shift.beginningTime.slice(0, 5)
				? getTimeInDateObj(manualOut, day)
				: getTimeInDateObj(
						manualOut,
						shift.beginningTime < shift.endTime ? parseInt(day) + 1 : parseInt(day) + 1
				  );

		// console.log('Manual In:', manualIn, 'Manual Out:', manualOut);
		// console.log('Shift End: ', shift.beginningTime.slice(0, 5));
		// console.log(manualOut > shift.beginningTime.slice(0, 5));
		if (manualInObj && manualOutObj) {
			const effectiveStartTime = Math.max(manualInObj, shiftBeginningTime);
			const effectiveEndTime = Math.min(manualOutObj, shiftEndTime);
			const durationMilliseconds = Math.max(effectiveEndTime - effectiveStartTime, 0);
			const durationMinutes = Math.floor(durationMilliseconds / (1000 * 60));
			if (durationMinutes >= parseInt(shift.fullDayMinimumMinutes)) {
				if (lateMinValue <= shift.maxLateAllowedMin) {
					setFieldValue(`attendance.${day}.firstHalf`, present.id);
					setFieldValue(`attendance.${day}.secondHalf`, present.id);
				} else if (lateMinValue > shift.maxLateAllowedMin) {
					setFieldValue(`attendance.${day}.firstHalf`, absent.id);
					setFieldValue(`attendance.${day}.secondHalf`, present.id);
				}
			} else if (
				durationMinutes >= parseInt(shift.halfDayMinimumMinutes) &&
				durationMinutes < parseInt(shift.fullDayMinimumMinutes)
			) {
				if (lateMinValue <= shift.maxLateAllowedMin) {
					setFieldValue(`attendance.${day}.firstHalf`, present.id);
					setFieldValue(`attendance.${day}.secondHalf`, absent.id);
				} else if (lateMinValue > parseInt(shift.maxLateAllowedMin)) {
					setFieldValue(`attendance.${day}.firstHalf`, absent.id);
					setFieldValue(`attendance.${day}.secondHalf`, present.id);
				}
			} else if (durationMinutes < parseInt(shift.halfDayMinimumMinutes)) {
				setFieldValue(`attendance.${day}.firstHalf`, absent.id);
				setFieldValue(`attendance.${day}.secondHalf`, absent.id);
			}
		}
	}
};

export default calculateAttendance;
