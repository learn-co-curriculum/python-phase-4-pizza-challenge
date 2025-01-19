import { Route, Switch } from "react-router-dom"; // Ensure you import from 'react-router-dom'
import Home from "./Home";
import Navbar from "./Navbar";
import Restaurant from "./Restaurant";
import RestaurantList from "./RestaurantList"; // Import the new RestaurantList component

function App() {
  return (
    <>
      <Navbar />
      <Switch>
        <Route exact path="/restaurants/:id">
          <Restaurant />
        </Route>
        <Route exact path="/">
          <Home />
          <RestaurantList /> {/* Display the restaurant list on the home page */}
        </Route>
      </Switch>
    </>
  );
}

export default App;