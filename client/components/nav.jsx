'use strict';
var React = require('react');

let defaultArchive = {
  name: 'Example Archive',
  link: '/archive',
};

export class Navigation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  renderUser() {
    if (this.props.user) {
      let name = this.props.user.name;
      let email = this.props.user.email;
      let id = this.props.user.id;
      return <a href={"/activity/" + id}>{name} ({email})</a>
    }
    return <a href="/auth/login">Log In</a>;
  }

  renderArchive() {
    let archive = this.props.archive || defaultArchive;
    return <a className="nav-item nav-archive" href={archive.link}>{archive.name}</a>;
  }

  renderDocument() {
    let doc = this.props.doc;
    if (!doc || !doc.id) {
      return '';
    }
    return <span>
      <span className="nav-item nav-spacer"> > </span>
      <a className="nav-item nav-document" href={"/documents/" + doc.id}> {doc.title} </a>
    </span>;
  }

  render() {
    return <div className="page-header header">
      <div className="header-left">
        {this.renderArchive()}
        {this.renderDocument()}
      </div>
      <div className="header-center"></div>
      <div className="header-right">
        {this.renderUser()}
      </div>
    </div>
  }
}
