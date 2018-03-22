'use strict';
var React = require('react');
var Cookie = require('js-cookie');
var request = require('browser-request');

export class AbstractSearch extends React.Component {
  static defaultProps = {
    debounce: 500 /*ms*/,
    confirmation: 2000 /*ms*/,
    defaultResults: {},
    className: 'search-component',
    payload: {},
    headers: {},
    endpoint: '/api/search/DEFAULT-BROKEN-XXX',
  };

  constructor(props) {
    super(props);
    this.state = {
      query: this.props.query || '',
      results: this.props.defaultResults,
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
  empty() {
    return this.state.complete === 'never';
  }
  inProgress() {
    return this.state.complete === 'in-progress';
  }
  getResults() {
    return (this.empty() ? this.props.defaultResults : this.state.results) || {};
  }

  onQuery(event) {
    let query = event.target.value;
    let counter = this.state.counter + 1;
    let timeout = this.state.timeout;
    let complete;
    let results = {};
    // If any previous request is still in flight, cancel it
    if (timeout !== null) {
      clearTimeout(timeout);
      timeout = null;
    }
    if (query) {
      timeout = setTimeout(this.makeQuery(query, counter), this.props.debounce);
      complete = 'in-progress';
    } else {
      timeout = null;
      complete = 'never';
    }
    this.setState({
      query: query,
      counter: counter,
      timeout: timeout,
      complete: complete,
      results: results,
    });
  }

  makeQuery(query, counter) {
    let S = this;
    return function() {
      S.sendQuery(query, counter);
    }
  }

  sendQuery(query, counter) {
    let S = this;
    let payload = Object.assign({}, this.props.payload);
    Object.assign(payload, {
      query: query,
    });
    let headers = Object.assign({}, this.props.headers);
    Object.assign(headers, {
      'X-CSRFToken': Cookie.get('csrftoken'),
    });

    request({
      method: 'POST',
      uri: this.props.endpoint,
      body: payload,
      headers: headers,
      json: true,
    }, function(error, response, body) {
      // Ignore results that have been superceded
      if (S.state.counter !== counter) {
        console.error('response too old:', counter, body);
        return;
      }
      if (error) {
        console.error(error, response, body);a
        S.setState({
          results:  {},
          complete: 'done',
        });
        return;
      }
      S.setState({
        results: body,
        complete: 'done',
      });
    });
  }

  render() {
    throw "Not Implemented: render()";
  }
}

