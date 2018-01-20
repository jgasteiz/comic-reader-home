import React from "react";

import BatmanSpinner from './batman-spinner';
import ComicPage from './comic-page';
import Navigation from './navigation';
import fetchPageSrc from '../services/comic-service';
import ReadingControls from "./reading-controls";


// TODO: look at doing this in a different way?
const READER = document.getElementById('reader');


/**
 * Main app component.
 */
export default class ReaderApp extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            pageSrc: '',
            readingMode: 'standard-view',
            comicPath: READER.dataset.comicPath,
            currentPage: parseInt(READER.dataset.comicPage, 10),
            hasPreviousPage: false,
            hasNextPage: true,
            readingControlsVisible: false,
        };

        // Bind the event handlers to `this`
        this.previousPageHandler = this.previousPageHandler.bind(this);
        this.nextPageHandler = this.nextPageHandler.bind(this);
        this.readingModeHandler = this.readingModeHandler.bind(this);
        this.onPageClickHandler = this.onPageClickHandler.bind(this);
    }

    /**
     * Render the ComicPage, Navigation, BatmanSpinner and ReadingControls components.
     *
     * Also render the reading mode class modifiers depending on the
     * readingMode state value
     *
     * @returns {*}
     */
    render() {
        return (
            <div className={
                `reader reader--${this.state.readingMode} reader--${this.state.pageSrc ? 'show' : 'loading'}`}>
                <ComicPage
                    pageSrc={this.state.pageSrc}
                    onPageClickHandler={this.onPageClickHandler}
                />
                <Navigation
                    previousPageHandler={this.previousPageHandler}
                    nextPageHandler={this.nextPageHandler}
                    hasPreviousPage={this.state.hasPreviousPage}
                    hasNextPage={this.state.hasNextPage}
                />
                <BatmanSpinner/>
                <ReadingControls
                    readingModeHandler={this.readingModeHandler}
                    readingControlsVisible={this.state.readingControlsVisible}
                />
            </div>
        );
    }

    /**
     * When the component is ready and mounted, initialize key bindings:
     * - arrow right: next page handler
     * - arrow left: previous page handler
     */
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

    /**
     * Uses the fetchPageSrc service function for fetching the given pageNumber
     * image source.
     * @param pageNumber
     */
    fetchPage(pageNumber) {
        fetchPageSrc(
            pageNumber,
            this.state.comicPath,
            (newState) => this.setState(newState)
        );
    }

    /**
     * Event handlers
     */

    /**
     * Set the readingMode state property to the given reading mode.
     * This will change how the page looks like on the screen: fit height,
     * fit width or standard view.
     * @param readingMode
     */
    readingModeHandler(readingMode) {
        this.setState({
            readingMode: readingMode
        });
    }

    /**
     * Navigate to the previous page, if there's one.
     */
    previousPageHandler() {
        if (!this.state.hasPreviousPage) {
            return;
        }
        this.setState({
            pageSrc: '',
        });
        this.fetchPage(this.state.currentPage - 1);
    }

    /**
     * Navigate to the next page, if there's one.
     */
    nextPageHandler() {
        if (!this.state.hasNextPage) {
            return;
        }
        this.setState({
            pageSrc: '',
        });
        this.fetchPage(this.state.currentPage + 1);
    }

    /**
     * Toggle the state value readingControlsVisible to show/hide
     * the reading controls.
     */
    onPageClickHandler() {
        this.setState({
            readingControlsVisible: !this.state.readingControlsVisible
        });
    }
}
