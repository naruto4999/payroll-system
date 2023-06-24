import * as yup from "yup";

export const BankSchema = yup.object().shape({
    bankName: yup.string().min(2, "Bank name must be atleast 2 characters long").required("Required")
});