import React from "react";
import Navbar from "../components/Navbar";
import axios from "axios";
import BigButton from "../components/BigButton";
import Footer from "../components/Footer";
import { DeviceFrameset } from "react-device-frameset";
import placeholderImg from "../assets/vertical-shot-bazaar-full-different-vegetables.jpg";
import Search from "../components/Search";
import tabbar from "../assets/Tabbar2.png";

export default function PastPredictions() {
  // const [pastPredictions, setPastPredictions] = React.useState([]);
  const [searchResults, setSearchResults] = React.useState([]);
  const [search, setSearch] = React.useState({
    model: "Any",
    vegetable_name: "Any",
  });

  function displayImage(id, image_id) {
    axios.get(`/get_image/${id}`, {
        responseType: 'blob',
        headers: {
            Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
    })
    .then(res => {
        var imageUrl = URL.createObjectURL(res.data);
        document.getElementById(image_id).src = imageUrl; // Set the src attribute of the img element
    })
    .catch(err => {
        console.error('Error fetching image:', err);
    });
  }

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
                Accurate past prediction storage systems
              </h1>
              <p className="text-lg my-10">
                Stored in reliable databases. Built to last.
              </p>
              <p className="text-lg font-medium">You can use the emulation on the right just like a full app.</p>
              <p className="text-lg ml-10">
                <ul className="max-w-xl list-disc">
                  <li>Search for the prediction results of any of our two models with the "Model" dropdown.</li>
                  <li>Search for the prediction results of any of our supported vegetables with the "Vegetable" dropdown.</li>
                  <li>View the results from Greens.ai!</li>
                </ul>
              </p>
            </div>
          </div>
          <div className="w-2/5 m-20">
            <DeviceFrameset device="iPhone X">
              <div className="bg-purple-950 h-full text-white p-6 overflow-y-auto">
                <h1 className="text-xl font-bold text-center m-10">See what the community has used Greens.ai for!</h1>
                <div className="flex flex-col items-center">
                  <h3 className="text-gray-100 font-medium">All photos & classifications</h3>
                </div>
                <Search search={search} setSearch={setSearch} setSearchResults={setSearchResults}/>
                <div className="relative overflow-x-auto sm:rounded-lg">
                  <table className="w-full table-fixed text-center">
                    <thead>
                      <tr>
                        <th>Image</th>
                        <th>Model</th>
                        <th>Prediction</th>
                        <th>By</th>
                      </tr>
                    </thead>
                    <tbody>
                      {searchResults.length > 0 ? 
                        searchResults.map((data, id) => (
                          <tr key={id+1}>
                            <td className="py-2">
                              {displayImage(data.image_details.id, id)}
                              <img id={id} className="aspect-square mx-auto"/>
                              {/* {data.image_details.name} */}
                            </td>
                            <td>
                              {data.model}
                            </td>
                            <td>
                              {data.predicted_vegetable}
                            </td>
                            <td>
                              {data.user_details.name}
                            </td>
                          </tr>
                        ))
                      :
                        <tr>
                          <td>No results</td>
                          <td>No results</td>
                          <td>No results</td>
                          <td>No results</td>
                        </tr>
                      }
                    </tbody>
                  </table>
                </div>
                <div className="flex justify-center mt-10">
                  <img src={tabbar} />
                </div>
              </div>
            </DeviceFrameset>
          </div>
        </div>
        <Footer />
      </div>
    </>
  );
}
