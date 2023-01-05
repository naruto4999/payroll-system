import React from "react";
import { useDispatch } from "react-redux";
// import { useHistory } from "react-router";
import Container from "react-bootstrap/Container";
import { Col, Row, Form, Button } from "react-bootstrap";
import authSlice from "./store/slices/auth";
import { Navigate } from "react-router-dom";

const Profile = () => {
  const dispatch = useDispatch();
  const history = useHistory();
  const handleLogout = () => {
    dispatch(authSlice.actions.logout());
    <Navigate to={"/login"} />;
  };

  return (
    <Container>
      <Button variant="primary" onClick={handleLogout}>
        Logout
      </Button>
    </Container>
  );
};

export default Profile;
