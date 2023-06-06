import * as yup from "yup";

export const addBankSchema = yup.object().shape({
    newBank: yup.string().min(2, "Bank name must be atleast 2 characters long").required("Required")
});

export const editBankSchema = yup.object().shape({
    updatedBank: yup.string().min(2, "Bank name must be atleast 2 characters long").required("Required")
});