import React from 'react';
import { BrowserRouter, Route } from 'react-router-dom';

import Directory from './Directory';
import Reader from './Reader';
import Player from './Player';


const App = () => (
    <BrowserRouter
        basename="/"
    >
        <div>
            <Route exact path="/" component={Directory} />
            <Route path="/dir/:id" component={Directory}/>
            <Route path="/video/:id/" component={Player}/>
            <Route path="/comic/:id/:pageNum?" component={Reader}/>
        </div>
    </BrowserRouter>
);

export default App;
