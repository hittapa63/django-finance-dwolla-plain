'use strict';
import React from "react";
import ReactDOM from "react-dom";
import HomeDashboard from "./App";
import {getApiClient} from "../../../api";


const domContainer = document.querySelector('#object-home');


domContainer ? ReactDOM.render(
  <HomeDashboard client={getApiClient()} urlBase={urlBase}/>
  , domContainer) : null;
