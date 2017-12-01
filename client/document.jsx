'use strict';
var React = require('react');
var DOM = require('react-dom');
var $ = require('jquery');



class Document extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
    this.state = {};
  }
  componentDidMount() {
    console.log('componentDidMount()\n');
    this.initializeAnnotator();
  }
  componentDidUpdate() {
    console.log('componentDidUpdate()\n');
    this.initializeAnnotator();
  }

  initializeAnnotator() {
    let ann = new Annotator(this.refs.documentContent)
      .addPlugin('Auth', {
        tokenUrl: '/api/token',
      })
      .addPlugin('Store', {
        prefix: '/api',
        urls: {
          create: '/annotations',
          update: '/annotations/:id',
          destroy: '/annotations/:id',
          search: '/search',
        },
        annotationData: {
          // TODO: what to do about this ID?
          uri: this.props.document.id,
        },
        loadFromSearch: {
          uri: this.props.document.id,
        },
      });
    this.state.ann = ann;
  }

  render() {
    let doc = this.props.document;
    console.log(doc);
    if (!doc) {
      return <div>Missing Document</div>;
    }
    return <div className="document">
      <div className="document-title">{doc.title}</div>
      <div className="document-author">{doc.author}</div>
      <div className="document-content"
           ref="documentContent"
           dangerouslySetInnerHTML={{__html: doc.text}}>
      </div>
    </div>;
  }
}

DOM.render(
  <Document {...PROPS}/>,
  document.getElementById('react-root'));
