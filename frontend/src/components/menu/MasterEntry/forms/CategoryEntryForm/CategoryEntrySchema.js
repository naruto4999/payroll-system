import * as yup from "yup";

export const addCategorySchema = yup.object().shape({
    newCategory: yup.string().min(3, "Salary grade name must be atleast 3 characters long").required("Required")
});

export const editCategorySchema = yup.object().shape({
    updatedCategory: yup.string().min(3, "Salary grade name must be atleast 3 characters long").required("Required")
});