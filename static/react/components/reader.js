import React from "react";

import BatmanSpinner from './batman-spinner';
import ComicPage from './comic-page';
import Navigation from './navigation';
import fetchPageSrc from '../services/comic-service';


const READER = document.getElementById('reader');


export default class Reader extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            pageSrc: '',
            comicPath: READER.dataset.comicPath,
            currentPage: parseInt(READER.dataset.comicPage, 10),
            hasPreviousPage: false,
            hasNextPage: true,
        };

        // Bind the event handlers to `this`
        this.previousPageHandler = this.previousPageHandler.bind(this);
        this.nextPageHandler = this.nextPageHandler.bind(this);
    }

    render() {
        return (
            <div className={"reader reader--" + (this.state.pageSrc ? 'show' : 'loading')}>
                <ComicPage
                    pageSrc={this.state.pageSrc}
                />
                <Navigation
                    previousPageHandler={this.previousPageHandler}
                    nextPageHandler={this.nextPageHandler}
                    hasPreviousPage={this.state.hasPreviousPage}
                    hasNextPage={this.state.hasNextPage}
                />
                <BatmanSpinner/>
            </div>
        );
    }

    previousPageHandler() {
        if (!this.state.hasPreviousPage) {
            return;
        }
        this.setState({
            pageSrc: '',
        });
        this.fetchPage(this.state.currentPage - 1);
    }

    nextPageHandler() {
        if (!this.state.hasNextPage) {
            return;
        }
        this.setState({
            pageSrc: '',
        });
        this.fetchPage(this.state.currentPage + 1);
    }

    componentDidMount() {
        const component = this;

        this.fetchPage(this.state.currentPage);

        // Listen for key events and go to next/previous page when
        // pressing certain keys.
        document.addEventListener('keydown', function(ev) {
            const keyName = ev.key;
            if (keyName === 'ArrowRight') {
                component.nextPageHandler();
                ev.preventDefault();
            } else if (keyName === 'ArrowLeft') {
                component.previousPageHandler();
                ev.preventDefault();
            }
        });
    }

    fetchPage(pageNumber) {
        fetchPageSrc(
            pageNumber,
            this.state.comicPath,
            (newState) => this.setState(newState)
        );
    }
}
