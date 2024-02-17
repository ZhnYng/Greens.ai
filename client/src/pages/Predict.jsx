import React, { useState } from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";
import Alert from "../components/Alert";
import { DeviceFrameset } from "react-device-frameset";
import "react-device-frameset/styles/marvel-devices.min.css";
import placeholderImg from "../assets/vertical-shot-bazaar-full-different-vegetables.jpg";
import tabbar from "../assets/Tabbar2.png";

export default function Predict() {
  const navigate = useNavigate();
  const location = useLocation();

  const [alert, setAlert] = React.useState({});
  const [model, setModel] = React.useState("31x31");
  const [prediction, setPrediction] = React.useState(null);
  const [file, setFile] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
 
  React.useEffect(() => {
    if (!localStorage.getItem("access_token")) {
      navigate("/signin");
    }

    if (location.state?.origin == "signin") {
      setAlert({ success: "Login Success!" });
      setTimeout(() => {
        setAlert({});
      }, 5000);
    }
  }, []);

  const handleFileChange = (e) => {
    setPrediction(null)
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (file) {
      setLoading(true)
      console.log("Uploading file...");

      const formData = new FormData();
      formData.append("image", file);

      axios
        .post("/upload", formData)
        .then((res) => {
          const imageId = res.data.image_id;
          setAlert({ success: `Image ${file.name} as been uploaded!` });
          axios
            .post(`/predict/${model}`, { image_id: imageId }, {
              headers: {
                Authorization: "Bearer " + localStorage.getItem("access_token"),
              },
            })
            .then((res) => {
              setLoading(false)
              const prediction = res.data.success
              setPrediction(prediction)
              setAlert({ success: `Predicted vegetable: ${res.data.success}` });
              setTimeout(() => {
                setAlert({});
              }, 5000);
              console.log(res.data);
            })
            .catch((err) => {
              setLoading(false)
              console.error(err.response);
              setAlert(err.response.data.error);
            });
        })
        .catch((err) => {
          setLoading(false)
          console.error(err.response);
          setAlert(err.response.data.error);
          setTimeout(() => {
            setAlert({});
          }, 5000);
        });
    }
  };

  return (
    <>
      {alert.error ? (
        <Alert message={`Error: ${alert.error}`} status="error" />
      ) : alert.success ? (
        <Alert message={`${alert.success}`} status="success" />
      ) : null}
      <div className="min-h-screen w-full flex flex-col items-center bg-purple-700">
        <Navbar />
        <div className="flex justify-center items-center">
          <div className="w-3/5 m-28">
            <div className="text-white self-center mb-60">
              <h1 className="text-6xl font-bold">
                State-of-the-art accuracy predictions
              </h1>
              <p className="text-lg my-10">
                Trained for success. Coming to mobile.
              </p>
              <p className="text-lg font-medium">You can use the emulation on the right just like a full app.</p>
              <p className="text-lg ml-10">
                <ul className="max-w-xl list-decimal">
                  <li>Click on the upload button to choose the image you want to classify</li>
                  <li>Choose the model you want to use. Defaults to 31x31.</li>
                  <li>Click on the big white button to initiate the prediction.</li>
                  <li>To make more predictions, simply click the upload button again.</li>
                  <li>Finally, to view your own predictions, go to the navigation bar, and click "Profile".</li>
                  <li>To view everybody's predictions, go to the navigation bar, and click "Past Predictions".</li>
                </ul>
              </p>
            </div>
          </div>
          <div className="w-2/5 m-20">
            <DeviceFrameset device="iPhone X">
              <div className="bg-purple-950 h-full text-white">
                {file ? (
                  <div
                    className="bg-purple-950 h-3/4 flex flex-col justify-center items-center"
                  >
                    <img src={URL.createObjectURL(file)} alt="your image" className="w-full h-full"/>
                    <label className="flex max-w-xs my-4">
                      <span  className="btn bg-purple-700 text-white mr-2">Upload</span>
                      <input id="uploadImage" type="file"  className="file-input file-input-bordered
                      [&::file-selector-button]:hidden p-2.5 bg-gray-100 text-purple-950"
                      onChange={handleFileChange}/>
                    </label>
                  </div>
                ) : (
                  <div
                    className="bg-purple-950 h-3/4 flex flex-col justify-center items-center"
                  >
                    <img src={placeholderImg} alt="your image" className="w-full h-full"/>
                    <label className="flex max-w-xs my-4">
                      <span  className="btn bg-purple-700 text-white mr-2">Upload</span>
                      <input id="uploadImage" type="file"  className="file-input file-input-bordered
                      [&::file-selector-button]:hidden p-2.5 bg-gray-100 text-purple-950"
                      onChange={handleFileChange}/>
                    </label>
                  </div>
                )}
                <div className="py-2 flex flex-col justify-evenly gap-3 items-center">
                  <div className="flex gap-2 items-center">
                    {!prediction ? 
                        !loading ? 
                          <>
                          <h3 className="font-medium text-center ">Make a prediction with the</h3>
                          <div className="dropdown">
                            <div tabIndex={0} role="button" className="btn-sm btn bg-purple-500 text-white ">
                              {model}
                            </div>
                            <ul
                              tabIndex={0}
                              className="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-20"
                            >
                              <li>
                                <a onClick={()=>setModel('31x31')}>31x31</a>
                              </li>
                              <li>
                                <a onClick={()=>setModel('128x128')}>128x128</a>
                              </li>
                            </ul>
                          </div>
                          <h3 className="font-medium text-center">model.</h3>
                          </>
                          :
                          <>
                          <h3 className="font-medium text-center animate-pulse">Loading...</h3>
                          </>
                      :
                      <>
                      <h3 className="font-medium text-center">Predicted vegetable: {prediction}</h3>
                      </>
                    }
                  </div>
                  <div className="flex items-center justify-start gap-24 w-full ml-10">
                    <div className="w-10 h-10 rounded-xl bg-white bg-[url('./assets/vertical-shot-bazaar-full-different-vegetables.jpg')]"></div>
                    <div
                      className="bg-white rounded-full w-16 h-16 btn-circle hover:bg-gray-400 hover:cursor-pointer"
                      onClick={handleUpload}
                    ></div>
                  </div>
                </div>
                <div className="flex justify-center mt-3">
                  <img src={tabbar} />
                </div>
              </div>
            </DeviceFrameset>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}
