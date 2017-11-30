'use strict';
var React = require('react');
var ReactDOM = require('react-dom');


export class NavLink {
    constructor(title, url) {
        this.title = title;
        this.url = url;
    }

    key() {
        return this.url;
    }
}


export class Nav extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <header className="nav-down" id="top">
                <nav className="nav">
                    <ul>
                        <li>
                            <a href="/">
                                <img className="logo_img"
                                     id="logo_img"
                                     src="/static/img/logo.png"
                                     alt="CRTA"/>
                            </a>
                        </li>
                        <li className="divider">
                            {this.props.links.map((link) => {
                                return <a key={link.key()} href={link.url}>{link.title}</a>;
                            })}
                        </li>
                        <li className="divider"></li>
                        <UserLogin user={this.props.user}/>
                    </ul>
                </nav>
            </header>
        );
    }
}

export class UserLogin extends React.Component {
    render() {
        var user = this.props.user;
        if (!user) {
            return <li className="login"><a href="/login">Log In / Sign Up</a></li>;
        }
        return <li className="login"><a href="/home">{this.props.user.username}</a></li>;
    }


}
