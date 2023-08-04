import * as yup from "yup";

export const WeeklyOffHolidayOffSchema = yup.object().shape({
    minDaysForHolidayOff: yup
        .number()
        .min(0, "Must Be 0 or greater")
        .max(7, "Must be 7 or less")
        .required("Required"),
    minDaysForWeeklyOff: yup
        .number()
        .min(0, "Must Be 0 or greater")
        .max(7, "Must be 7 or less")
        .required("Required"),
});
