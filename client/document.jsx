'use strict';
var React = require('react');
var DOM = require('react-dom');
// Contributed from other scripts
var $ = window.$;

import {setupCSRF, createAnnotator} from './util.jsx';
import {Annotation} from './components/annotation.jsx';
import {AnnotationSearch} from './components/search/annotations.jsx';
import {Navigation} from './components/nav.jsx';


class DocumentPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      annotator: null,
      annotations: this.props.annotations || [],
      columnView: 'annotations',
    };
  };

  componentDidMount() {
    this.initializeAnnotator();
  }

  initializeAnnotator() {
    let dp = this;
    let onUpdate = (action) => (ann) => {
      if (!ann) {
        return;
      }
      var new_annotations = dp.state.annotations.slice();
      if (action === 'update') {
        var changed = false;
        var i;
        for (i = 0; i < new_annotations.length; i++) {
          var x = new_annotations[i];
          if (x.id == ann.id) {
            new_annotations[i] = Object.assign(x, ann);
            changed = true;
            break;
          }
        }

        if (changed) {
          dp.setState({annotations: new_annotations});
        } else {
          var new_annotations = dp.state.annotations.slice();
          new_annotations.push(ann);
          dp.setState({
            annotations: new_annotations,
          });
        }
        return;
      }

      if (action === 'delete') {
        var new_annotations = dp.state.annotations.filter((x) => x.id !== ann.id);
        dp.setState({
          annotations: new_annotations,
        });
        return;
      }

      if (action === 'create') {
        var new_annotations = dp.state.annotations.slice();
        new_annotations.push(ann);
        dp.setState({
          annotations: new_annotations,
        });
        return;
      }
    };
    let ann = createAnnotator(
        dp.refs.documentContent,
        onUpdate,
        dp.props.user.email,
        dp.props.document.id
    );
    this.setState({annotator: ann});
  }

  searchResult(ann) {
    return <Annotation key={ann.id} {...ann}/>;
  }

  render() {
    let dp = this;
    let doc = dp.props.document;
    return <div id="ann-wrapper" className="document-page grid-container">
      <Navigation doc={doc}/>

      {/* Document pane */}
      <div className="column document-pane scroll-y">
        <div className="document-title">{doc.title}</div>
        <div className="document-author">{doc.author}</div>
        <div className="document-content" ref="documentContent">
          {/* For compatibility with existing annotation range definitions; */}
          {/* the previous site must have introduced this div wrapper */}
          <div className="document-content-inner"
               ref="documentContentInner"
               dangerouslySetInnerHTML={{__html: doc.text}}>
          </div>
        </div>
      </div>
      {/* Annotation pane */}
      <AnnotationSearch
        className="column annotations-pane scroll-y"
        resultfn={this.searchResult.bind(this)}
        payload={{
          document_id: dp.props.document.id,
        }}
        defaultResults={{
          annotations: dp.state.annotations,
        }}
      />
    </div>;
  }
}


setupCSRF($);
DOM.render(
  <DocumentPage {...PROPS}/>,
  document.getElementById('react-root'));
