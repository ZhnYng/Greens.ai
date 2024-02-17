import {
  createHashRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";
import Home from './pages/Home'
import Signup from './pages/Signup'
import Signin from './pages/Signin'
import Predict from './pages/Predict'
import PastPredictions from "./pages/PastPredictions";
import Profile from "./pages/Profile";

export default function App(){
  const router = createHashRouter(
    createRoutesFromElements(
      <>
      <Route path="/" element={<Home />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/signin" element={<Signin />} />
      <Route path="/predict" element={<Predict />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/past-predictions" element={<PastPredictions />} />
      </>
    )
  );

  return <RouterProvider router={router}/>
}