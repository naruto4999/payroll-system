import * as yup from "yup";

export const addDesignationSchema = yup.object().shape({
    newDesignation: yup.string().min(3, "Designation name must be atleast 3 characters long").required("Required")
});

export const editDesignationSchema = yup.object().shape({
    updatedDesignation: yup.string().min(3, "Designation name must be atleast 3 characters long").required("Required")
});