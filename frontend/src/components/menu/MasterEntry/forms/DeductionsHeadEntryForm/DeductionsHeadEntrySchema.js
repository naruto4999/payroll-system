import * as yup from "yup";

export const DeductionsHeadSchema = yup.object().shape({
    deductionsHeadName: yup.string().min(2, "Deductions Head name must be atleast 2 characters long").required("Required")
});