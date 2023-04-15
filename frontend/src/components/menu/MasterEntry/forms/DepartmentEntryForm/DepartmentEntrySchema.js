import * as yup from "yup";

export const addDepartmentSchema = yup.object().shape({
    newDepartment: yup.string().min(3, "Department name must be atleast 3 characters long").required("Required")
});

export const editDepartmentSchema = yup.object().shape({
    newDepartment: yup.string().min(3, "Department name must be atleast 3 characters long").required("Required")
});