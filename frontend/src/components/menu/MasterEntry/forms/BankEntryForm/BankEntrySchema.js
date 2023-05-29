import * as yup from "yup";

export const addBankSchema = yup.object().shape({
    newBank: yup.string().min(3, "Salary grade name must be atleast 3 characters long").required("Required")
});

export const editBankSchema = yup.object().shape({
    updatedBank: yup.string().min(3, "Salary grade name must be atleast 3 characters long").required("Required")
});