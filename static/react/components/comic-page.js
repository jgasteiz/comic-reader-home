import React from "react";


export default class ComicPage extends React.Component {
    render() {
        return (
            <img className="comic-page"
                 src={this.props.pageSrc}
            />
        );
    }
}
