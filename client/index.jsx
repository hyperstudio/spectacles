'use strict'; var React = require('react');
var DOM = require('react-dom');


class IndexPage extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
  }

  render() {
    return <div className="index-page main">
        <div className="header">
          <div className="toolbar">
            <div className="toolbar-user">
              {(this.props.user) ?
                <p> Logged in as <a href={"/activity/" + this.props.user.id}>{this.props.user.name}</a> </p>
                : <a href="/auth/login"> Log In </a>
              }
            </div>
          </div>
          <h1> Spectacles </h1>
          <h3 className="tagline"> Assisting Speculative Analysis in Active Archives </h3>
        </div>
        <div className="body">
        <p> A <a href="http://hyperstudio.mit.edu"> Hyperstudio </a> Project </p>
        <p> <a href="/documents"> View Documents </a> </p>
        </div>
      </div>;
  }

}


DOM.render(
  <IndexPage {...PROPS}/>,
  document.getElementById('react-root'));
