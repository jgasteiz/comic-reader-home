import React from "react";
import { Link } from "react-router-dom";


/**
 * This component renders a set of reading controls at the bottom of the page
 * to switch between "page fitting" modes and toggling full screen mode.
 */
export default class ReadingControls extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            mode: 'standard-view'
        };

        // Bind the event handlers to `this`
        this.fitPageHeight = this.fitPageHeight.bind(this);
        this.fitPageWidth = this.fitPageWidth.bind(this);
        this.standardView = this.standardView.bind(this);
    }

    render() {
        const pageSelectorOptions = Array(this.props.numPages).fill().map((_, pageNum) => {
            return (<option key={pageNum} value={pageNum}>{pageNum + 1}</option>);
        });

        return (
            <div className={`reading-controls reading-controls--${this.props.readingControlsVisible ? 'visible': 'hidden'}`}>
                <div className="btn-group" role="group" aria-label="Basic example">
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={this.fitPageHeight}
                        disabled={this.state.mode === 'fit-height'}
                    >
                        <i className="material-icons">panorama_vertical</i>
                    </button>
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={this.fitPageWidth}
                        disabled={this.state.mode === 'fit-width'}
                    >
                        <i className="material-icons">panorama_horizontal</i>
                    </button>
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={this.standardView}
                        disabled={this.state.mode === 'standard-view'}
                    >
                        <i className="material-icons">panorama_fish_eye</i>
                    </button>
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={this.props.bookMarkPageHandler}
                    >
                        <i className="material-icons">bookmark</i>
                    </button>
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={this.props.toggleFullScreenHandler}
                    >
                        <i className="material-icons">
                            {this.props.isFullscreen ? 'fullscreen_exit' : 'fullscreen'}
                        </i>
                    </button>
                    <Link
                        className="btn btn-danger btn-sm"
                        to={`/dir/${this.props.comicParentPath}/`}
                    >
                        <i className="material-icons">exit_to_app</i>
                    </Link>
                </div>
                <select
                    className="reading-controls__page-selector"
                    value={this.props.currentPage}
                    onChange={this.props.pageSelectorHandler}
                >
                    {pageSelectorOptions}
                </select>
            </div>
        );
    }

    /**
     * Fit page height: the comic page will match the screen height and center
     * in the middle of the screen.
     */
    fitPageHeight() {
        this.setState({
            mode: 'fit-height'
        });
        this.props.readingModeHandler('fit-height');
    }

    /**
     * Fit page width: makes the page as wide as the screen.
     */
    fitPageWidth() {
        this.setState({
            mode: 'fit-width'
        });
        this.props.readingModeHandler('fit-width');
    }

    /**
     * Standard view: the page won't be wider than 1200px. It's a good
     * max-width in most computers and some tablets.
     */
    standardView() {
        this.setState({
            mode: 'standard-view'
        });
        this.props.readingModeHandler('standard-view');
    }
}