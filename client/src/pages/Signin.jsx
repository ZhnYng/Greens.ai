import React from "react";
import BigButton from "../components/BigButton";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";
import Alert from "../components/Alert";

export default function Signup() {
  const navigate = useNavigate();
  const location = useLocation();
  const [errMsg, setErrMsg] = React.useState("");
  const [alert, setAlert] = React.useState({});
  const [formData, setFormData] = React.useState({
    // email: "",
    // password: "",
    // rememberMe: false
    email: "test@gmail.com",
    password: "Testingg1",
    rememberMe: true,
  });

  React.useEffect(() => {
    if (location.state?.origin == "signup") {
      setAlert({ success: "Sign up successful!" });
      setTimeout(() => {
        setAlert({});
      }, 5000);
    }
  }, []);

  // Event handler to update form data when inputs change
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (type === "checkbox") {
      // For checkboxes, use 'checked' instead of 'value'
      setFormData({
        ...formData,
        [name]: checked,
      });
    } else {
      // For other input types, use 'value'
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  // Event handler for form submission
  const handleSubmit = () => {
    function camelToSnake(str) {
      return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
    }

    const formDataInfo = {};
    for (const key in formData) {
      if (Object.hasOwnProperty.call(formData, key)) {
        const snakeKey = camelToSnake(key);
        formDataInfo[snakeKey] = formData[key];
      }
    }
    axios
      .post("/login", formDataInfo)
      .then((res) => {
        localStorage.setItem("access_token", res.data.access_token);
        navigate("/predict", { state: { origin: "signin" } });
      })
      .catch((err) => setErrMsg(err.response.data.error));
  };

  return (
    <>
      {alert.success ? (
        <Alert message={alert.success} status="success" />
      ) : null}
      <div className="min-h-screen w-full bg-purple-600 flex flex-col items-center justify-center">
        <div className="text-white flex flex-col justify-center items-center h-full">
          <h3 className="text-3xl font-bold my-8 text-white">Greens.ai</h3>
          <div className="flex flex-col items-center border-whitew-1/3 text-purple-950">
            {errMsg ? (
              <div role="alert" className="alert alert-error max-w-sm mb-8">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="stroke-current shrink-0 h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span>{errMsg}</span>
              </div>
            ) : null}
            <div className="mb-3 w-72">
              <p className="mb-2 text-white">Email</p>
              <input
                type="text"
                placeholder="Enter your email"
                className="input w-full bg-white"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
              />
            </div>
            <div className="my-3 mb-6 w-72">
              <p className="mb-2 text-white">Password</p>
              <input
                type="password"
                placeholder="Enter your password"
                className="input w-full bg-white"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-control mb-3">
              <label className="label cursor-pointer">
                <span className="label-text mr-2 text-white">Remember me</span>
                <input
                  type="checkbox"
                  name="rememberMe"
                  checked={formData.rememberMe}
                  onChange={handleInputChange}
                  className="checkbox checkbox-success"
                />
              </label>
            </div>
            <BigButton text="Login" onClick={handleSubmit} />
            <div className="flex items-center gap-5 text-white mt-36">
              <p>Don't have an account?</p>
              <button 
                className="btn btn-outline border-purple-200 text-purple-200 
                hover:bg-transparent hover:border-purple-300 hover:text-white"
                onClick={() => navigate('/signup')}
              >
                Get access
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
