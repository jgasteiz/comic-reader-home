import React from 'react';
import { Link } from "react-router-dom";

import DirectoryService from '../services/directory-service';


export default class Directory extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            directories: [],
            comics: [],
            directoryPath: null,
            parentPath: null,
            directoryName: null,
        };
    }


    render() {
        const comicRows = this.state.comics.map(function (comic, index) {
            return (<tr key={comic.path}>
                <td>
                    {index + 1}
                </td>
                <td>
                    {comic.name}
                </td>
                <td className="text-right">
                    <a className="btn btn-primary btn-sm">
                        Read
                    </a>
                </td>
            </tr>);
        });

        const directoryRows = this.state.directories.map(function (directory, index) {
            return (<tr key={directory.path}>
                <td>
                    {index + 1}
                </td>
                <td>
                    {directory.name}
                </td>
                <td className="text-right">
                    <Link to={`/dir/${directory.path}/`} className="btn btn-secondary btn-sm">
                        Go
                    </Link>
                </td>
            </tr>);
        });

        const component = this;
        const backLink = (function() {
            if (component.state.parentPath) {
                return (
                    <Link className="btn btn-secondary" to={component.state.parentPath}>Back</Link>
                );
            } else {
                return '';
            }
        })();

        return (
            <div>
                <header>
                    <div className="row">
                        <h1 className="col">
                            {this.state.directoryName}
                        </h1>
                        <div className="col-auto">
                            {backLink}
                        </div>
                    </div>
                </header>

                <h2>Comics</h2>

                <table className="table table-striped">
                    <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Comic name</th>
                        <th scope="col" className="text-right">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                        {comicRows}
                    </tbody>
                </table>

                <h2>Directories</h2>

                <table className="table table-striped">
                    <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Directory name</th>
                        <th scope="col" className="text-right">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                        {directoryRows}
                    </tbody>
                </table>
            </div>
        );
    }

    componentDidMount() {
        DirectoryService.getDirectoryDetails(this.props.match.params.dirPath, (res) => {
            this.setState({
                directories: res['path_contents']['directories'],
                comics: res['path_contents']['comics'],
                directoryPath: res['directory_path'],
                parentPath: res['parent_path'],
                directoryName: res['path_contents']['name'],
            });
        });
    }


}
