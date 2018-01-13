import React from "react";


export default class ReadingControls extends React.Component {
    constructor(props) {
        super(props);

        // Bind the event handlers to `this`
        this.fitPageHeight = this.fitPageHeight.bind(this);
        this.fitPageWidth = this.fitPageWidth.bind(this);
        this.standardView = this.standardView.bind(this);
    }

    render() {
        return (
            <div className="reading-controls">
                <button onClick={this.fitPageHeight}>Fit page height</button>
                <button onClick={this.fitPageWidth}>Fit page width</button>
                <button onClick={this.standardView}>Standard view</button>
            </div>
        );
    }

    fitPageHeight() {
        this.props.readingModeHandler('fit-height');
    }

    fitPageWidth() {
        this.props.readingModeHandler('fit-width');
    }

    standardView() {
        this.props.readingModeHandler('standard-view');
    }
}
