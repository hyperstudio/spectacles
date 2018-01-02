'use strict';
var React = require('react');
var DOM = require('react-dom');
var Cookie = require('js-cookie');
var request = require('browser-request');
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
                <SearchPane/>
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

class SearchPane extends React.Component {
  constructor(props) {
    super(props);

    this.debounce = 500 /*ms*/;
    this.confirmation = 2000 /*ms*/;
    this.state = {
      query: this.props.query || '',
      results: this.props.results || [],
      timeout: null,
      counter: 1,
      complete: this.props.query ? 'done' : 'never',
    };

    this.onQuery = this.onQuery.bind(this);
    this.makeQuery = this.makeQuery.bind(this);
    this.sendQuery = this.sendQuery.bind(this);
  }
  done() {
    return this.state.complete === 'done';
  }

  inProgress() {
    return this.state.complete === 'prog';
  }

  onQuery(event) {
    let S = this;
    let query = event.target.value;
    let counter = this.state.counter + 1;
    S.setState({query: query, counter: counter, complete: 'prog'});
    if (S.state.timeout !== null) {
      clearTimeout(S.state.timeout);
    }
    if (query) {
      let timeout = setTimeout(S.makeQuery(query, counter), S.debounce);
      S.setState({timeout: timeout});
    } else {
      S.setState({complete: 'never'});
    }
  }

  makeQuery(query, counter) {
    let S = this;
    return function() {
      S.sendQuery(query, counter);
    };
  }

  sendQuery(query, counter) {
    let S = this;
    let payload = {
      query: query,
    };
    request({
      method: 'POST',
      uri: '/api/search',
      body: payload,
      headers: {
        'X-CSRFToken': Cookie.get('csrftoken'),
      },
      json: true,
    }, function(error, response, body) {
      if (error) {
        console.error(error, response, body);
        return;
      }
      if (S.state.counter !== counter) {
        console.error('response too old:', body);
        return;
      }
      // TODO: better state replacement over time
      //let url = '/search/' + encodeURI(query);
      //history.replaceState({}, '', url);
      console.log(body);
      S.setState({
        results: body,
        complete: 'done',
      });
    });
  }

  renderStatus() {
    if (this.done()) {
      return ''
      //return `${this.state.results.length} results`
    }
    if (this.inProgress()) {
      return 'Loading'
    }
    return ''
  }


  render() {
    let r = this.state.results;
    let anns = r.annotations || [];
    let docs = r.documents || [];
    return <div className="search-page">
      <div className="body gray">
        <div className="search-bar body gray">
          <div className="search-bar-input">
            <input className="search-bar-query"
                   type="text"
                   placeholder="What are you looking for?"
                   value={this.state.query}
                   onChange={this.onQuery} autoFocus/>
          </div>
          <p className="search-bar-results">
            {this.renderStatus()}
          </p>
        </div>
      </div>
      <div className="search-results body white">
        {anns.map(ann => {
          return <AnnResult key={ann._meta.id} ann={ann}/>;
        })}
      </div>
    </div>;
  }
}

class DocResult extends React.Component {
  render() {
    return <span></span>;
  }
}
class AnnResult extends React.Component {
  constructor(props) {
      super(props);
      this.state = {};
  }
  render() {
      let ann = this.props.ann;
      return <div className='annotation active' key={ann.uuid}>
        <div className="annotation-info">
          <div className="annotation-creator">{ann.creator.name}</div>
        </div>
        <div className="annotation-quote">{ann.quote}</div>
        <div className="annotation-text"
             dangerouslySetInnerHTML={{__html: ann.text}}>
        </div>
        <div className="annotation-tags">
          {(ann.tags || []).map(t => <div className="annotation-tag" key={t + ann._meta.uuid}>{t}</div>)}
        </div>
      </div>;
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
