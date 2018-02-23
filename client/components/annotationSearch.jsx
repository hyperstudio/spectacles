'use strict';
var React = require('react');
var Cookie = require('js-cookie');
var request = require('browser-request');


export class AnnotationSearch extends React.Component {
  constructor(props) {
    super(props);
    this.debounce = 500 /*ms*/;
    this.confirmation = 2000 /*ms*/;
    this.defaultResults = {
      annotations: this.props.annotations || [],
      documents: [],
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
      creator_id: this.props.creator_id || undefined,
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

  displayAnnotations(annotations) {
    let fn;
    if (!annotations || annotations.length == 0) {
      return;
    }
    console.log(annotations);
    if (this.props.resultfn) {
      fn = this.props.resultfn;
    } else {
      fn = (ann) => {
        return <AnnotationSearchResult key={ann.id} ann={ann}/>;
      }
    }
    return annotations.map(fn);
  }


  render() {
    let r = this.state.results;
    console.log('R:', r);
    let anns = r.annotations || [];
    let docs = r.documents || [];
    return <div className="search-page">
      <div className="body gray">
        <div className="search-bar body gray">
          <div className="search-bar-input">
            <input className="search-bar-query"
                   type="text"
                   placeholder="Filter Annotations"
                   value={this.state.query}
                   onChange={this.onQuery} autoFocus/>
          </div>
          <p className="search-bar-results">
            {this.renderStatus()}
          </p>
        </div>
      </div>
      <div className="search-results body white">
        {this.displayAnnotations(anns)}
      </div>
    </div>;
  }
}

export class AnnotationSearchResult extends React.Component {
  constructor(props) {
      super(props);
      this.state = {};
  }
  render() {
    let ann = this.props.ann;
    return <div className='annotation active' key={ann.uuid}>
      <div className="annotation-info">
        <div className="annotation-creator">{ann.creator.name}</div>
        <a href={`/documents/${ann.document_id}`} className="annotation-link">View Document</a>
      </div>
      <div className="annotation-quote">{ann.quote}</div>
      <div className="annotation-text"
           dangerouslySetInnerHTML={{__html: ann.text}}>
      </div>
      <div className="annotation-tags">
        {(ann.tags || []).map(t => <div className="annotation-tag" key={t + ann.uuid}>{t}</div>)}
      </div>
    </div>;
  }
}
