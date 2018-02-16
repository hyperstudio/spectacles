'use strict';
var React = require('react');
var Cookie = require('js-cookie');
var request = require('browser-request');

// TODO: extract out a Search component that can be used
export class DocumentSearch extends React.Component {
  constructor(props) {
    super(props);
    this.debounce = 500 /*ms*/;
    this.confirmation = 2000 /*ms*/;
    this.defaultResults = {
      annotations: [],
      documents: this.props.documents || [],
    };
    this.state = {
      query: this.props.query || '',
      results: this.defaultResults,
      timeout: null,
      counter: 1,
      complete: this.props.query ? 'done' : 'never',
    };

    this.onQuery = this.onQuery.bind(this);
    this.makeQuery = this.makeQuery.bind(this);
    this.sendQuery = this.sendQuery.bind(this);
  }
  done() {
    return this.state.complete === 'done' || this.state.complete === 'never';
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
      S.setState({complete: 'never', results: this.defaultResults});
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
      document_id: this.props.document_id || undefined,
    };
    request({
      method: 'POST',
      uri: '/api/search/documents',
      body: payload,
      headers: {
        'X-CSRFToken': Cookie.get('csrftoken'),
      },
      json: true,
    }, function(error, response, body) {
      if (error) {
        console.error(error, response, body);
        S.setState({
          results: {},
          complete: 'done',
        });
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
      return '';
    }
    if (this.inProgress()) {
      return 'Loading'
    }
    return ''
  }

  displayDocuments(documents) {
    if (!documents || documents.length == 0) {
      return;
    }
    return documents.map(this.props.resultfn);
  }


  render() {
    let r = this.state.results;
    let docs = r.documents || [];
    return <div className="search-page">
      <div className="body gray">
        <div className="search-bar body gray">
          <div className="search-bar-input">
            <input className="search-bar-query"
                   type="text"
                   placeholder="Filter Documents"
                   value={this.state.query}
                   onChange={this.onQuery} autoFocus/>
          </div>
          <p className="search-bar-results">
            {this.renderStatus()}
          </p>
        </div>
      </div>
      <div className="search-results body white">
        {this.displayDocuments(docs)}
      </div>
    </div>;
  }
}
