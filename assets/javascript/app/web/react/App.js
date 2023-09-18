import React, {useState, useEffect} from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
} from "react-router-dom";
import {getAction} from "../../../api";
import {API_ROOT} from "../const";
import LoadingScreen from "../../../utilities/Loading";
import Dashboard from "./dashboard";


const HomeDashboard = function(props) {

  const getDefaultView = function() {
    return <Dashboard {...props}/>;
  };

  return (
    <Router basename={props.urlBase}>
      <Switch>
        <Route path="/">
          {getDefaultView()}
        </Route>
       </Switch>
    </Router>
  );
};


export default HomeDashboard;
