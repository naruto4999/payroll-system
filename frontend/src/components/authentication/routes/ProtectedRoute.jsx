import { Navigate, Outlet } from 'react-router-dom';
import { useSelector } from "react-redux";


export const ProtectedRoute = ({ children }) => {
  const auth = useSelector((state) => state.auth);
  if (auth.account === null) {
    // user is not authenticated
    return <Navigate to="/login" />;
  }
  return children;
};

export default ProtectedRoute;