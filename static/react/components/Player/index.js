import React from 'react';

import FileItemService from '../../services/FileItem.Service';


/**
 * Player component.
 */
export default class Player extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            name: null,
            videoId: null,
            parentId: null,
        };
    }

    /**
     * Render the video to play.
     *
     * @returns {*}
     */
    render() {
        if (!this.state.videoPath) {
            return 'Loading';
        }
        return (
            <div id="player" className="player">
                <h1>{this.state.name}</h1>
                <video controls>
                    <source src={`/api/video/${this.state.videoId}/`} type="video/mp4"/>
                </video>
            </div>
        );
    }

    componentDidMount() {
        FileItemService.getFileItemDetails(this.props.match.params.id, (res) => {
            this.setState({
                name: res['name'],
                videoId: res['pk'],
                videoPath: res['encoded_path'],
                parentId: res['parent'],
            });
        });
    }

}
