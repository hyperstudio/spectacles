'use strict';
var React = require('react');


export class Annotation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    let ann = this.props;
    return <div className='annotation active' key={ann.uuid}>
      <div className="annotation-info">
        <div className="annotation-creator">
          <a href={`/activity/${ann.creator.id}`}>{ann.creator.name}</a>
        </div>
        <div className="annotation-timestamp">{ann.updated_at}</div>
      </div>
      <div className="annotation-quote">{ann.quote}</div>
      <div className="annotation-text"
           dangerouslySetInnerHTML={{__html: ann.text}}>
      </div>
      <div className="annotation-tags">
        {(ann.tags || []).map((t, i) => <div className="annotation-tag" key={t + '_' + i}>{t}</div>)}
      </div>
    </div>;
  }
}
