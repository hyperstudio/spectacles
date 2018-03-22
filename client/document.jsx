'use strict';
var React = require('react');
var DOM = require('react-dom');
// Contributed from other scripts
var $ = window.$;

import {setupCSRF, createAnnotator} from './util.jsx';
import {Annotation} from './components/annotation.jsx';
import {AnnotationSearch} from './components/search/annotations.jsx';
var X = window.X;
var Y = window.Y;


class DocumentPage extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
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
    console.log(this.state.annotations);
    let onUpdate = (action) => (ann) => {
      if (!ann) {
        return;
      }
      var new_annotations = dp.state.annotations.slice();
      console.log('action =', action);
      console.log('ann.id =', ann.id);
      if (action === 'update') {
        var changed = false;
        var i;
        for (i = 0; i < new_annotations.length; i++) {
          var x = new_annotations[i];
          if (x.id == ann.id) {
            new_annotations[i] = Object.assign(x, ann);
            console.log('updated x!');
            changed = true;
            break;
          }
        }
        if (changed) {
          dp.setState({annotations: new_annotations});
        }
        return;
      }

      if (action === 'delete') {
        var new_annotations = dp.state.annotations.filter((x) => x.id !== ann.id);
        console.log(new_annotations.length);
        console.log(dp.state.annotations.length);
        dp.setState({
          annotations: new_annotations,
        });
        console.log('forcing update!');
        return;
      }

      if (action === 'create') {
        console.error('TODO: automatically update list on create');
        // This is going to involve re-implenting the Store plugin,
        // to fire these callbacks AFTER the HTTP requests to the server
        // have completed. Right now, newly created annotations don't have any
        // kind of Creator information, or UUIDs.
        return;
        //var new_annotations = dp.state.annotations.slice();
        //new_annotations.push(ann);
        //dp.setState({
        //  annotations: new_annotations,
        //});
        //console.log('CREATE: forcing update!');
        //dp.forceUpdate();
        //return;
      }
      // TODO: Figure out if the annotation was created or deleted
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
    console.log('RE-RENDERING DOCUMENT PAGE');
    return <div className="document-page main">
      <div className="page-header">
        <div className="header-left">
          <a className="nav-item nav-archive" href="/documents"> Example Archive </a>
          <span className="nav-item nav-spacer"> > </span>
          <a className="nav-item nav-document" href={"/documents/" + doc.id}> {doc.title} </a>
        </div>
        <div className="header-center"></div>
        <div className={"header-right " + dp.state.columnView}>
          <div className="state-choice choice-info">Information</div>
          <div className="state-choice choice-sim">Similar Documents</div>
          <div className="state-choice choice-ann">Annotations</div>
        </div>
      </div>
      <div className="page-content content">
        <div className="box">
          {/* Document pane */}
          <div className="column document-pane">
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
            className="column annotations-pane"
            resultfn={this.searchResult.bind(this)}
            payload={{
              document_id: dp.props.document.id,
            }}
            defaultResults={{
              annotations: dp.state.annotations,
            }}
            f={dp.state.annotations}
          />
        </div>
      </div>
    </div>;
  }
}


setupCSRF($);
DOM.render(
  <DocumentPage {...PROPS}/>,
  document.getElementById('react-root'));
