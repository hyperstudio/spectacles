'use strict';
var React = require('react');
var DOM = require('react-dom');
var Cookie = require('js-cookie');
import fuzzyFilterFactory from 'react-fuzzy-filter';
const {InputFilter, FilterResults} = fuzzyFilterFactory();
// Contributed from other scripts
var $ = window.$;
function csrfSafeMethod(method) { // XXX remove duplicate code
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
const fuseConfig = {
  keys: ['author', 'title', 'creator.name', 'creator.email'],
  shouldSort: true,
};
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            var csrf = Cookie.get('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrf);
        }
    }
});



class Documents extends React.Component {
    constructor(props) {
        super(props);
        console.log(this.props);
        this.state = {};
    }

    render() {
        let inputProps = {
          placeholder: "Fuzzy filter...",
        }
        //<div className="user-info">{this.renderUser()}</div>
        return <div className="documents-page main">
          <div className="page-header">
            <div className="header-left">
              <a className="nav-item nav-archive" href="/documents"> Example Archive </a>
            </div>
            <div className="header-center"></div>
            <div className="header-right">
              <div className="state-choice">{this.renderUser()}</div>
            </div>
          </div>
          <div className="content">
            <div className="box">
              <div className="docs-pane column">
                <InputFilter inputProps={inputProps}/>
                <FilterResults items={this.props.documents} fuseConfig={fuseConfig}>
                  {filteredItems => {
                    return <div className='docs-results'>
                      {filteredItems.map(d => <DocumentEntry key={d.id} document={d}/>)}
                    </div>;
                  }}
                </FilterResults>
              </div>
              <div className="search-pane column">
                Hello world
              </div>
            </div>
          </div>
        </div>;
    }

    renderUser() {
      let name = 'Anonymous';
      let email = '?';
      if (this.props.user) {
          name = this.props.user.name;
          email = this.props.user.email;
      }
      return <span>{name} ({email})</span>
    }
}

class DocumentEntry extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }
    link() {
        return this.props.document &&
               "/documents/" + this.props.document.id;
    }
    text() {
        let doc = this.props.document;
        if (!doc) {
            return '<broken>'
        }
        return doc.title + ' - ' + doc.author + ' (' + doc.creator.email + ')';
    }
    render() {
        let doc = this.props.document;
        return <div className="document-entry">
          <div className="document-title">
            <a href={this.link()}>{doc.title}</a>
          </div>
          <div className="document-author">
            {doc.creator.name}
          </div>
          <div className="document-meta">
            <div className="document-creator"> {doc.author}</div>
            <div className="document-timestamp"> {doc.updated_at} </div>
          </div>
        </div>;
    }
}

DOM.render(
        <Documents {...PROPS}/>,
        document.getElementById('react-root'));
