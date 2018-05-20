import React from 'react';
import { BrowserRouter, Route } from 'react-router-dom';

import Directory from './Directory';
import Reader from './Reader';


const App = () => (
    <BrowserRouter
        basename="/"
    >
        <div>
            <Route exact path="/" component={Directory} />
            <Route path="/dir/:id" component={Directory}/>
            <Route path="/comic/:id/:pageNum?" component={Reader}/>
        </div>
    </BrowserRouter>
);

export default App;
