'use strict';
var React = require('react');
var DOM = require('react-dom');


class IndexPage extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
  }

  render() {
    return <div className="index-page main">
      <h1> Spectacles </h1>
      <p> A <a href="http://hyperstudio.mit.edu"> Hyperstudio </a> Project </p>
      <p> <a href="/documents"> View Documents </a> </p>
      {(this.props.user) ?
        <p> Logged in as <a href={"/user/" + this.props.user.id}>{this.props.user.name}</a> </p>
        : <a href="/auth/login"> Log In </a>
      }
    </div>;
  }

}


DOM.render(
  <IndexPage {...PROPS}/>,
  document.getElementById('react-root'));
