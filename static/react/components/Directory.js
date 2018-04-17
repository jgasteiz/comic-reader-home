import React from 'react';
import { Link } from "react-router-dom";

import DirectoryService from '../services/Directory.Service';


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
        return (
            <div>
                {this._renderHeader()}

                <section className="container">
                    <header>
                        <div className="row">
                            <h1 className="col">
                                {this.state.directoryName}
                            </h1>
                            <div className="col-auto">
                                {this._renderBackLink()}
                            </div>
                        </div>
                    </header>

                    {this._renderComics()}
                    {this._renderDirectories()}
                </section>
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

    // Custom render functions

    _renderHeader() {
        return (
            <header className="navbar navbar-dark bg-dark sticky-top navbar-expand-md">
                <div className="container d-flex justify-content-between">
                    <a href="/"
                       className="navbar-brand d-flex align-items-center">
                        <strong>Comic Reader</strong>
                    </a>
                </div>
            </header>
        );
    }

    _renderBackLink() {
        const component = this;
        return  (function() {
            if (component.state.parentPath) {
                return (
                    <Link className="btn btn-secondary" to={`/dir/${component.state.parentPath}/`}>Back</Link>
                );
            } else {
                return '';
            }
        })();
    }

    _renderComics() {
        if (this.state.comics.length === 0) {
            return '';
        }
        const comicRows = this.state.comics.map(function (comic, index) {
            return (<tr key={comic.path}>
                <td>
                    {index + 1}
                </td>
                <td>
                    {comic.name}
                </td>
                <td className="text-right">
                    <Link to={`/comic/${comic.path}/`} className="btn btn-primary btn-sm">
                        Read
                    </Link>
                </td>
            </tr>);
        });

        return (
            <div>
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
            </div>
        );
    }

    _renderDirectories() {
        if (this.state.directories.length === 0) {
            return '';
        }
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

        return (
            <div>
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


}
