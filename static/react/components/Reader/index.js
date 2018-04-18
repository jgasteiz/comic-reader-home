import React from 'react';

import ComicPage from './ComicPage';
import ReadingControls from './ReadingControls';
import Spinner from './Spinner';
import ComicService from '../../services/Comic.Service';


/**
 * Reader component.
 */
export default class Reader extends React.Component {
    constructor(props) {
        super(props);

        const pageNum = this.props.match.params.pageNum ? parseInt(this.props.match.params.pageNum, 10) : 0;

        this.state = {
            pageSrc: '',
            readingMode: 'standard-view',
            comicPath: this.props.match.params.comicPath,
            parentPath: '',
            currentPage: pageNum,
            numPages: 0,
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
        this.pageSelectorHandler = this.pageSelectorHandler.bind(this);
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
            <div id="reader" className={
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
                    pageSelectorHandler={this.pageSelectorHandler}
                    currentPage={this.state.currentPage}
                    numPages={this.state.numPages}
                    isFullscreen={this.state.isFullscreen}
                    readingControlsVisible={this.state.readingControlsVisible}
                    comicParentPath={this.state.parentPath}
                />
            </div>
        );
    }

    componentDidMount() {
        ComicService.getComicDetails(this.props.match.params.comicPath, (res) => {
            this.setState({
                numPages: res['num_pages'],
                parentPath: res['parent_path'],
            });
            this.setPageSrc(this.state.currentPage);
        });
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
        ComicService.bookmarkPage(this.state.currentPage, this.state.comicPath);
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
     * Set the new given page num as the current page number.
     *
     * @param newPageNum
     */
    goToPage(newPageNum) {
        this.setState({
            pageSrc: '',
        });
        this.setPageSrc(newPageNum);
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

    /**
     * Handler for the page number change on the reading controls.
     *
     * @param event
     */
    pageSelectorHandler(event) {
        this.goToPage(parseInt(event.currentTarget.value, 10));
    }
}
