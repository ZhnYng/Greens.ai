import axios from "axios";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

export default function Navbar() {
  const navigate = useNavigate();
  let isLoggedIn = false;
  if (localStorage.getItem("access_token")) {
    let token = localStorage.getItem("access_token");
    let decodedToken = jwtDecode(token);
    let currentDate = new Date();
  
    // JWT exp is in seconds
    if (decodedToken.exp * 1000 < currentDate.getTime()) {
      localStorage.removeItem('access_token')
      navigate('/signin')
    } else {
      isLoggedIn = true;
    }
  }

  const handleLogout = () => {
    axios
      .post("/logout", [], {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
      })
      .then((res) => {
        console.log(res.data);
        localStorage.removeItem("access_token");
        navigate("/");
      })
      .catch((err) => console.error(err));
  };

  return (
    <div className="navbar bg-purple-700">
      <div className="flex-1">
        <a
          className="btn btn-ghost text-xl text-white"
          onClick={() => navigate("/")}
        >
          Greens.ai
        </a>
      </div>
      <div className="flex-none">
        <ul className="menu menu-horizontal px-1 text-white text-md font-medium">
          <li className="px-3">
            <a
              onClick={() => navigate("/predict")}
              className="hover:cursor-pointer"
            >
              Make a Prediction
            </a>
          </li>
          <li className="px-3">
            <a
              onClick={() => navigate("/past-predictions")}
              className="hover:cursor-pointer"
            >
              Past Predictions
            </a>
          </li>
          {!isLoggedIn ? (
            <div className="flex">
              <li className="px-3">
                <a
                  onClick={() => navigate("/signin")}
                  className="hover:cursor-pointer"
                >
                  Sign In
                </a>
              </li>
              <li className="px-3">
                <a
                  onClick={() => navigate("/signup")}
                  className="hover:cursor-pointer"
                >
                  Sign Up
                </a>
              </li>
            </div>
          ) : (
            <div className="flex">
              <li className="px-3">
                <a
                  onClick={() => navigate("/profile")}
                  className="hover:cursor-pointer"
                >
                  Profile
                </a>
              </li>
              <li className="px-3">
                <a onClick={handleLogout} className="hover:cursor-pointer">
                  Logout
                </a>
              </li>
            </div>
          )}
        </ul>
      </div>
    </div>
  );
}
