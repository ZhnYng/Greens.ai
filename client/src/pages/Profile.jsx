import axios from "axios";
import React from "react";
import BigButton from "../components/BigButton";
import Navbar from "../components/Navbar";
import Alert from "../components/Alert";
import { useNavigate } from "react-router-dom";
import { DeviceFrameset } from "react-device-frameset";
import Search from "../components/Search";
import placeholderImg from "../assets/vertical-shot-bazaar-full-different-vegetables.jpg";
import tabbar from "../assets/Tabbar2.png";
import Footer from "../components/Footer";

export default function Profile() {
  const navigate = useNavigate()
  const [search, setSearch] = React.useState({
    model: "Any",
    vegetable_name: "Any",
  });
  const [searchResults, setSearchResults] = React.useState([]);
  const [change, setChange] = React.useState('');
  const [alert, setAlert] = React.useState({});
  const [profile, setProfile] = React.useState({
    name: "",
    email: "",
    id: "",
  });
  const [activeRow, setActiveRow] = React.useState('');

  React.useEffect(() => {
    if(!localStorage.getItem('access_token')){
      navigate('/signin')
    }
  }, [])

  React.useEffect(() => {
    axios
      .get(`/getCurrentUser`, {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
      })
      .then((res) => {
        const userData = res.data;
        setProfile(userData);

        axios
          .get(`/getUserPredictions`, {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("access_token"),
            },
          })
          .then((res) => {
            setSearchResults(res.data.success);
          })
          .catch((err) => console.error(err));
      })
      .catch((err) => console.error(err));
  }, [change]);

  const handleShowModal = (id) => {
    document.getElementById('delete-model').showModal()
    setActiveRow(id)
  }

  const handleDelete = (id) => {
    axios
      .delete(`/removePastPrediction/${id}`, {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
      })
      .then((res) => {
        setChange(!change);
        document.getElementById('delete-model').close()
        setAlert({'success': 'Delete successful!'})
        setTimeout(() => {
          setAlert({})
        }, 5000);
      })
      .catch((err) => {
        console.error(err)
        setAlert(err.response.data)
        setTimeout(() => {
          setAlert({})
        }, 5000);
      });
  };

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
                Personalized dashboards to display your past predictions.
              </h1>
              <p className="text-lg my-10">
                Individually altered to fit the usage to each user.
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
                <div className="flex flex-col items-center mt-6">
                  <img src={placeholderImg} className="rounded-full w-24 h-24 m-4"/>
                  <h1 className="font-bold text-center text-xl">{profile.name}</h1>
                  <h3 className="text-gray-100 font-light">Email: {profile.email}</h3>
                </div>
                <div className="flex flex-col items-center mt-10">
                  <h3 className="text-gray-100 font-medium text-md">Photos & classifications</h3>
                  <h3 className="text-gray-100 font-light">{searchResults.length} shots</h3>
                </div>
                <Search search={search} setSearch={setSearch} setSearchResults={setSearchResults} userId={profile.id}/>
                {/* Modal for delete row */}
                <dialog id="delete-model" className="modal">
                  <div className="modal-box bg-error flex flex-col">
                    <h3 className="font-bold text-lg">Warning</h3>
                    <p className="py-4">Would you like to delete this row?</p>
                    <div className="modal-action">
                      <form method="dialog">
                        {/* if there is a button in form, it will close the modal */}
                        {/* <button className="btn">Close</button> */}
                        <button 
                          className="btn text-error bg-gray-200 border-white self-end"
                          onClick={() => handleDelete(activeRow)}
                        >
                          DELETE
                        </button>
                      </form>
                    </div>
                  </div>
                  <form method="dialog" className="modal-backdrop">
                    <button>close</button>
                  </form>
                </dialog>
                <div className="relative overflow-x-auto sm:rounded-lg">
                  <table className="w-full table-fixed text-center">
                    <thead>
                      <tr>
                        <th>Image</th>
                        <th>Model</th>
                        <th>Prediction</th>
                      </tr>
                    </thead>
                    <tbody>
                      {searchResults.length > 0 ? 
                        searchResults.map((data, id) => (
                          <tr key={id+1} className="hover:bg-purple-900 hover:cursor-pointer" onClick={()=>handleShowModal(data.id)}>
                            <td className="py-2">
                              {displayImage(data.image_details.id, id)}
                              <img id={id} className="aspect-square mx-auto"/>
                            </td>
                            <td>
                              {data.model}
                            </td>
                            <td>
                              {data.predicted_vegetable}
                            </td>
                          </tr>
                        ))
                      :
                        <tr>
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
