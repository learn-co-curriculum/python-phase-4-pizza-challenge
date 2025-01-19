// src/components/Home.js

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import RestaurantList from './RestaurantList'; 

function Home() {
  const [restaurants, setRestaurants] = useState([]);

  // Fetch restaurants from the API when the component mounts
  useEffect(() => {
    fetch('http://localhost:5555/restaurants')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(setRestaurants)
      .catch((error) => console.error('Error fetching restaurants:', error));
  }, []);

  // Handle restaurant deletion
  function handleDelete(id) {
    fetch(`http://localhost:5555/restaurants/${id}`, {
      method: 'DELETE',
    })
      .then((response) => {
        if (response.ok) {
          setRestaurants((prevRestaurants) =>
            prevRestaurants.filter((restaurant) => restaurant.id !== id)
          );
        } else {
          console.error('Error deleting restaurant');
        }
      })
      .catch((error) => console.error('Error deleting restaurant:', error));
  }

  return (
    <section className="container">
      <h1>Welcome to Our Pizza Restaurant App</h1>
      {restaurants.length === 0 ? (
        <p>No restaurants available.</p>
      ) : (
        <RestaurantList restaurants={restaurants} />
      )}
    </section>
  );
}

export default Home;
