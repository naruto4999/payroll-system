import * as yup from "yup";

export const addCompanySchema = yup.object().shape({
    newCompany: yup.string().min(3, "Company name must be atleast 3 characters long").required("Required")
});

export const editCompanySchema = yup.object().shape({
    updatedCompany: yup.string().min(3, "Company name must be atleast 3 characters long").required("Required")
});