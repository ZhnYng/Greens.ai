import Navbar from "../components/Navbar";
import BigButton from "../components/BigButton";
import Footer from "../components/Footer";
import { useNavigate } from "react-router-dom";
import predictionPage from "../assets/Prediction page.png";
import mlFeature from "../assets/coding.png"
import searchFeature from "../assets/map.png"
import historyFeature from "../assets/history-book.png"

export default function Home() {
  const navigate = useNavigate();

  const handlePredictNowBtn = () => {
    navigate("/predict");
  };

  return (
    <div className="max-w-screen min-h-screen flex flex-col items-center bg-purple-300">
      <Navbar />
      <div className="w-full max-w-7xl mb-40">
        <div className="text-purple-950 px-8 pt-28">
          <div className="flex justify-between">
            <div>
              <p className="text-sm font-medium text-purple-900 my-6">By Lim Zhen Yang</p>
              <h1 className="text-6xl font-extrabold max-w-xl">Predict your next vegetable even more accurately.</h1>
              <p className="text-lg max-w-xl my-8 font-medium">Beautifully designed, expertly trained ML models, built by the makers of deep learning assignments. The perfect beginner model to predicting vegetables.</p>
              <div className="flex gap-6">
                <button onClick={()=>navigate("/predict")} className="btn bg-purple-700 btn-wide hover:bg-purple-900 text-white text-md">Make a prediction</button>
                <button onClick={()=>navigate("/past-predictions")} className="btn bg-transparent outline-purple-900 border-purple-900 btn-wide text-purple-900 hover:bg-white hover:bg-opacity-30">View prediction results</button>
              </div>
            </div>
            <div className="w-1/3">
              <img src={predictionPage}/>
            </div>
          </div>
        </div>
        <div className="flex flex-col w-full justify-evenly my-28 text-purple-950 px-8">
          <p className="text-sm font-medium text-purple-900 my-8">Features</p>
          <h1 className="text-5xl font-extrabold max-w-xl">Beautifully optimied, expertly trained ML models, ready for your next prediction.</h1>
          <p className="text-lg max-w-xl my-8 font-medium">Over 1+ professionally designed, fully student, expertly crafted model examples you can drop into your prediction projects and customize as necessary.</p>
          <a onClick={()=>navigate("/predict")} className="link text-purple-950 hover:text-purple-600 text-lg font-medium w-fit">Make a prediction</a>
          <div className="flex justify-between my-8">
            <div className="card w-1/3 mx-6 bg-purple-700 text-white shadow-xl">
              <figure><img src={mlFeature} alt="Shoes" className="w-2/3 p-14"/></figure>
              <div className="card-body">
                <h2 className="card-title">
                  Machine Learning
                  <div className="badge text-purple-950 border-none bg-purple-400">2nd</div>
                </h2>
                <p>Use of state-of-the-art convolutional neural networks for precise predictions.</p>
                <div className="card-actions justify-end">
                  <div className="badge badge-outline">Technology</div> 
                </div>
              </div>
            </div>
            <div className="card w-1/3 mx-6 bg-purple-700 text-white shadow-xl">
              <figure><img src={searchFeature} alt="Shoes" className="w-2/3 p-14"/></figure>
              <div className="card-body">
                <h2 className="card-title">
                  Search and Filtering
                  <div className="badge text-purple-950 border-none bg-purple-400">2nd</div>
                </h2>
                <p>Specific queries for searching and filtering through past predictions.</p>
                <div className="card-actions justify-end">
                  <div className="badge badge-outline">Technology</div> 
                  <div className="badge badge-outline">Usability</div>
                </div>
              </div>
            </div>
            <div className="card w-1/3 mx-6 bg-purple-700 text-white shadow-xl">
              <figure><img src={historyFeature} alt="Shoes" className="w-2/3 p-14"/></figure>
              <div className="card-body">
                <h2 className="card-title">
                  Machine Learning
                  <div className="badge text-purple-950 border-none bg-purple-400">2nd</div>
                </h2>
                <p>Records past predictions by the public and yourself in an accessible format.</p>
                <div className="card-actions justify-end">
                  <div className="badge badge-outline">User Experience</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer/>
    </div>
  );
}
