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
                : <a href="/auth/login?next=/documents"> Log In </a>
              }
            </div>
            <div className="toolbar-docs">
              <a href="/documents">View Documents</a>
            </div>
          </div>
          <h1> Spectacles </h1>
          <h3 className="tagline"> Assisting Speculative Analysis in Active Archives </h3>
        </div>
        <div className="body">
          <img src="/static/img/hero.jpg" width="1000px" height="auto"/>
          <p> <b>Spectacles makes digital archives usable.</b> With powerful <i>fuzzy search</i>, <i>annotation tools</i> for making rich notes in-line as you read, and <i>artifical intelligence</i> that helps guide you to exactly the documents most relevant to your research interests, Spectacles transforms the experience of performing research in a digital archive. Unlike other systems, Spectacles is <i>collaborative</i>, allowing researchers to see and respond to eachother's notes, just like they were all in the same room together. It supports <i>speculative analysis</i>, allowing you to quickly filter through hundreds or thousands of texts and their annotations to find exactly the content that's relevant to your interests, even if what you're interested in is changing as you read. Most importantly, it's free, easy to use, and scales to any number of documents. </p>
        </div>
      </div>;
  }

}


DOM.render(
  <IndexPage {...PROPS}/>,
  document.getElementById('react-root'));
