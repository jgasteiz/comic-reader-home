import React from "react";


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
        ReadingControls.toggleFullScreen = ReadingControls.toggleFullScreen.bind(this);
    }

    render() {
        return (
            <div className={`reading-controls reading-controls--${this.props.readingControlsVisible ? 'visible': 'hidden'}`}>
                <div className="btn-group" role="group" aria-label="Basic example">
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={this.fitPageHeight}
                        disabled={this.state.mode === 'fit-height'}
                    >
                        Fit page height
                    </button>
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={this.fitPageWidth}
                        disabled={this.state.mode === 'fit-width'}
                    >
                        Fit page width
                    </button>
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={this.standardView}
                        disabled={this.state.mode === 'standard-view'}
                    >
                        Standard view
                    </button>
                    <button
                        className="btn btn-secondary btn-sm"
                        onClick={ReadingControls.toggleFullScreen}
                    >
                        Toggle full screen
                    </button>
                </div>
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

    /**
     * If the browser supports full screen mode, toggles it.
     */
    static toggleFullScreen() {
        if (!document.fullscreenElement) {
            try {
                document.documentElement.requestFullscreen();
            } catch(error) {
                document.documentElement.webkitRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                try {
                    document.exitFullscreen();
                } catch(error) {
                    document.webkitExitFullscreen();
                }
            }
        }
    }
}
