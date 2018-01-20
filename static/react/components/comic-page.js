import React from "react";

/**
 * This component is for displaying the page <img> element.
 */
export default class ComicPage extends React.Component {
    render() {
        return (
            <img className="comic-page"
                 src={this.props.pageSrc}
                 onClick={this.props.onPageClickHandler}
            />
        );
    }
}
