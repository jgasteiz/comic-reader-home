import React from "react";

import Spinner from './spinner';
import ComicPage from './comic-page';
import ComicService from '../services/comic-service';
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
            parentPath: READER.dataset.parentPath,
            currentPage: parseInt(READER.dataset.comicPage, 10),
            numPages: parseInt(READER.dataset.numPages, 10),
            hasPreviousPage: false,
            hasNextPage: false,
            readingControlsVisible: false,
            isFullscreen: false,
        };

        // Bind the event handlers to `this`
        this.previousPageHandler = this.previousPageHandler.bind(this);
        this.nextPageHandler = this.nextPageHandler.bind(this);
        this.readingModeHandler = this.readingModeHandler.bind(this);
        this.bookMarkPageHandler = this.bookMarkPageHandler.bind(this);
        this.onPageClickHandler = this.onPageClickHandler.bind(this);
        this.toggleFullScreenHandler = this.toggleFullScreenHandler.bind(this);
    }

    /**
     * Render the ComicPage, Navigation, Spinner and ReadingControls components.
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
                    hasPreviousPage={this.state.hasPreviousPage}
                    hasNextPage={this.state.hasNextPage}
                    previousPageHandler={this.previousPageHandler}
                    nextPageHandler={this.nextPageHandler}
                />
                <Spinner/>
                <ReadingControls
                    readingModeHandler={this.readingModeHandler}
                    bookMarkPageHandler={this.bookMarkPageHandler}
                    toggleFullScreenHandler={this.toggleFullScreenHandler}
                    isFullscreen={this.state.isFullscreen}
                    readingControlsVisible={this.state.readingControlsVisible}
                    comicParentPath={this.state.parentPath}
                />
            </div>
        );
    }

    componentDidMount() {
        this.setPageSrc(this.state.currentPage);
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
     * Bookmark the current page in the current comic.
     *
     * There can only be one bookmark per comic.
     */
    bookMarkPageHandler() {
        ComicService.bookmarkPage(
            this.state.currentPage,
            this.state.comicPath,
            (newState) => this.setState(newState)
        )
    }

    /**
     * Navigate to the previous page, if there's one.
     */
    previousPageHandler() {
        if (this.state.currentPage > 0) {
            this.setState({
                pageSrc: '',
            });
            this.setPageSrc(this.state.currentPage - 1);
        }
    }

    /**
     * Navigate to the next page, if there's one.
     */
    nextPageHandler() {
        if (this.state.currentPage < this.state.numPages - 1) {
            this.setState({
                pageSrc: '',
            });
            this.setPageSrc(this.state.currentPage + 1);
        }
    }

    /**
     * Update the page src with the given page number.
     * @param pageNumber
     */
    setPageSrc(pageNumber) {
        const component = this;

        ComicService.fetchPageImage(pageNumber, this.state.comicPath, function () {
            component.setState({
                currentPage: pageNumber,
                pageSrc: ComicService.getPageSrc(pageNumber, component.state.comicPath),
                hasPreviousPage: pageNumber > 0,
                hasNextPage: pageNumber < component.state.numPages - 1
            });
            ComicService.updatePageUrl(pageNumber, component.state.comicPath);
        });
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

    /**
     * Toggle the full screen mode.
     */
    toggleFullScreenHandler() {
        const doc = window.document;
        const docEl = doc.documentElement;

        const requestFullScreen = docEl.requestFullscreen || docEl.mozRequestFullScreen || docEl.webkitRequestFullScreen || docEl.msRequestFullscreen;
        const cancelFullScreen = doc.exitFullscreen || doc.mozCancelFullScreen || doc.webkitExitFullscreen || doc.msExitFullscreen;

        // Otherwise, toggle.
        if (!doc.fullscreenElement && !doc.mozFullScreenElement && !doc.webkitFullscreenElement && !doc.msFullscreenElement) {
            requestFullScreen.call(docEl);
            this.setState({isFullscreen: true});
        } else {
            cancelFullScreen.call(doc);
            this.setState({isFullscreen: false});
        }
    }
}
