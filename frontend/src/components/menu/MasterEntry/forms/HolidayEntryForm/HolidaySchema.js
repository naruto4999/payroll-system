import * as yup from "yup";

export const HolidaySchema = yup.object().shape({
    holidayName: yup
        .string()
        .min(1, "Holiday name must be atleast 1 characters long")
        .required("Required"),
    holidayDate: yup.date().required("Date is required"),
});
