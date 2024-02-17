import React from "react";
import axios from "axios";

export default function Search({ search, setSearch, setSearchResults, userId }) {
  const vegetables = ['Bean', 'Bitter_Gourd', 'Bottle_Gourd', 'Brinjal', 'Broccoli', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Cucumber', 'Papaya', 'Potato', 'Pumpkin', 'Radish', 'Tomato']

  React.useEffect(() => {
    function constructUrl(baseUrl, userId, vegetableName = 'Any', model = 'Any') {
      // Convert 'Any' to empty string if provided
      vegetableName = (vegetableName === 'Any') ? '' : vegetableName;
      model = (model === 'Any') ? '' : model;
      userId = (userId === undefined) ? '' : userId;
  
      // Construct the URL with the query parameters
      var queryParams = '';
  
      if (userId !== '') {
          queryParams += `userId=${userId}&`;
      }
  
      if (vegetableName !== '') {
          queryParams += `vegetable_name=${vegetableName}&`;
      }
  
      if (model !== '') {
          queryParams += `model=${model}&`;
      }
  
      // Remove the trailing '&' if present
      if (queryParams.endsWith('&')) {
          queryParams = queryParams.slice(0, -1);
      }
  
      // Append the query parameters to the base URL if any are present
      var url = baseUrl;
      if (queryParams !== '') {
          url += '?' + queryParams;
      }
  
      return url;
    }
    
    axios
      .get(
        constructUrl(
          "/searchForPrediction", 
          userId, 
          search.vegetable_name,
          search.model
        )
      )
      .then((res) => {
        setSearchResults(res.data.success);
      })
      .catch((err) => console.error(err));
  }, [search]);

  const handleSearch = (e) => {
    const {name, value} = e.target
    setSearch(prevSearch => ({
      ...prevSearch,
      [name]: value,
    }));
  };

  return (
    <div className="flex items-center my-4 gap-4">
      <div className="flex flex-col w-full gap-1">
        <span className="label-text-alt text-gray-300">Model</span>
        <select 
          className="select w-full max-w-xs bg-purple-700 select-sm" 
          name="model"
          onChange={handleSearch}
          value={search.model}
        >
          <option disabled>Model</option>
          <option>31x31</option>
          <option>128x128</option>
          <option>Any</option>
        </select>
      </div>
      <div className="flex flex-col w-full gap-1">
        <span className="label-text-alt text-gray-300">Vegetable</span>
        <select 
          className="select w-full max-w-xs bg-purple-700 select-sm" 
          onChange={handleSearch}
          value={search.vegetable_name}
          name="vegetable_name"
        >
          <option disabled>Vegetable</option>
          {vegetables.map((vegetable, id) => (
            <option key={id}>{vegetable}</option>
          ))}
          <option>Any</option>
        </select>
      </div>
    </div>
  );
}
