'use strict';
var React = require('react');

export class Navigation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return <div className="page-header header">
      <div className="header-left">
        <a className="nav-item nav-archive" href="/documents"> Example Archive </a>
        <span className="nav-item nav-spacer"> > </span>
        <a className="nav-item nav-document" href={"/documents/" + this.props.doc.id}> {this.props.doc.title} </a>
      </div>
      <div className="header-center"></div>
      <div className={"header-right annotations"}>
        <div className="state-choice choice-info">Information</div>
        <div className="state-choice choice-sim">Similar Documents</div>
        <div className="state-choice choice-ann">Annotations</div>
      </div>
    </div>
  }
}
