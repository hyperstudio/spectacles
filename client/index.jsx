'use strict';
var React = require('react');
var DOM = require('react-dom');

var {Nav, NavLink} = require('./components/nav.jsx');
var {CollectionRow} = require('./components/collection.jsx');
var {goTo} = require('./components/utils.jsx');


class Index extends React.Component {
    constructor(props) {
        super(props);
        console.log(this.props);
        this.state = {};
    }

    render() {
        var links = new Array(
            new NavLink('About', '#about'),
            new NavLink('Gallery', '#gallery'),
            new NavLink('Team', '#team'),
            new NavLink('Contact', '#contact'),
        );
        var index = this;
        return <div>
            <Nav user={this.props.user} links={links}/>
            <div className="slideshow-container">
                <h1>Curate Your Own Collection</h1>
                <h4>Use this curator tool to boost up your great<br/>
                    ideas and make your curation awesome.
                </h4>
                <div className="button" onClick={goTo('/home')}>Try Now</div>
            </div>
            <div className="index-collections-wrapper">
                <div className="index-collections-text">
                    <h2> Or Dive Into These</h2>
                    <h4> Our visitors have been hard at work curating their own collections. Explore the museum's works throught their eyes. </h4>
                </div>
                {this.props.collections.map((c) => {
                    return <CollectionRow key={c.id} collection={c}/>;
                })}
            </div>
        </div>;
    }
}


DOM.render(
        <Index {...PROPS}/>,
        document.getElementById('react-root'));
