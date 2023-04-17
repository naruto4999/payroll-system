import * as yup from "yup";

export const addSalaryGradeSchema = yup.object().shape({
    newSalaryGrade: yup.string().min(3, "Salary grade name must be atleast 3 characters long").required("Required")
});

export const editSalaryGradeSchema = yup.object().shape({
    updatedSalaryGrade: yup.string().min(3, "Salary grade name must be atleast 3 characters long").required("Required")
});