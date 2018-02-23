'use strict';
var React = require('react');
var DOM = require('react-dom');
// Contributed from other scripts
var $ = window.$;

import {setupCSRF, createAnnotator} from './util.jsx';
import {Annotation} from './components/annotation.jsx';
import {AnnotationSearch} from './components/annotationSearch.jsx';


let sortByTransform = (f) => (a, b) => {
  if (f(a) < f(b)) return -1;
  if (f(a) > f(b)) return 1;
  return 0;
};

class UserPage extends React.Component {
  constructor(props) {
    super(props);
    console.log(this.props);
  }

  searchResult(ann) {
    return <Annotation key={ann.uuid} {...ann}/>;
  }

  render() {
    this.props.annotations.sort(
      sortByTransform((x) => new Date(x.updated_at)),
      -1
    );

    return <div className="user-page main">
        <AnnotationSearch
          creator_id={this.props.user.id}
          resultfn={this.searchResult.bind(this)}
          annotations={this.props.annotations}
        />
    </div>;
  }
}

setupCSRF($);
DOM.render(
  <UserPage {...PROPS}/>,
  document.getElementById('react-root'));
