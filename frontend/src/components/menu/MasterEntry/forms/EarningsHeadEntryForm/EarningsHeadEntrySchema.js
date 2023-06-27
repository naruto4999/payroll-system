import * as yup from "yup";

export const EarningsHeadSchema = yup.object().shape({
    earningsHeadName: yup.string().min(2, "Earnings Head name must be atleast 2 characters long").required("Required")
});