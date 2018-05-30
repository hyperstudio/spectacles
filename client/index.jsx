'use strict'; var React = require('react');
var DOM = require('react-dom');


class IndexPage extends React.Component {
  constructor(props) {
    super(props);
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
          <div className='hero'>
            <img src="/static/img/hero.png" width="1000px" height="auto"/>
          </div>
          <p> <b>Spectacles makes digital archives usable.</b> With powerful <i>fuzzy search</i> for finding just the right text, <i>annotation tools</i> for making rich notes in-line as you read, and <i>artifical intelligence</i> that helps guide you to exactly the documents most relevant to your research interests, Spectacles transforms the experience of performing research in a digital archive. Unlike other systems, Spectacles is <i>collaborative</i>, allowing researchers to see and respond to eachother's notes, just like they were all in the same room together. Most importantly, it's free, easy to use, and scales to any number of documents.</p>
          <p> Spectacles is open source software that anyone can use to host their own digital archive. If you're interested, <a href="https://github.com/hyperstudio/spectacles">check out Spectacles on Github</a>. </p>
          <p> This website is currently hosting a demonstration archive to get an idea of how Spectacles can be used. If you'd like to try it out, <a href="/auth/register">sign up here</a>. </p>
          <p> Spectacles was created as a student research project &mdash; if you want to read a paper about it, <a href="/static/spectacles-whitepaper.pdf">just click here</a>. </p>
        </div>
      </div>;
  }

}


DOM.render(
  <IndexPage {...PROPS}/>,
  document.getElementById('react-root'));
