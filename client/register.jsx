'use strict';
var React = require('react');
var DOM = require('react-dom');


class RegisterPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: this.props.username || '',
      password: this.props.password || '',
      name: this.props.name || '',
    };
  }

  renderError() {
    if (this.props.error) {
      return <h4 className="error">
        An account for {this.props.username} already exists. Perhaps you meant to <a href="/auth/login"> log in? </a>
      </h4>
    }
  }
  renderNext() {
    if (this.props.next) {
      return <input type="hidden" name="next" value={this.props.next}/>
    }
  }

  onChange(path) {
    return (event) => {
      let change = {};
      change[path] = event.target.value;
      x.setState(change);
    };
  }

  render() {
    return <div>
      <div className="body">
        <div className="register form">
          <h3 className="title">Register for Spectacles</h3>
          {this.renderError()}
          <form method="post" action='/auth/register'>
            <input type="hidden"
                 name="csrfmiddlewaretoken"
                 value={this.props.csrftoken}/>
            {this.renderNext()}
            <table>
              <tbody>
                <tr>
                  <td className="label">Name:</td>
                  <td className="input">
                    <input type="text" name="name" required autoFocus value={this.state.name} onChange={this.onChange('name')}/>
                  </td>
                </tr>
                <tr>
                  <td className="label">Email:</td>
                  <td className="input">
                    <input type="text" name="username" required value={this.state.username} onChange={this.onChange('username')}/>
                  </td>
                </tr>
                <tr>
                  <td className="label">Password:</td>
                  <td className="input">
                    <input type="password" name="password" required value={this.state.password} onChange={this.onChange('password')}/>
                  </td>
                </tr>
              </tbody>
            </table>
            <input type="submit" value="register" className="button"/>
          </form>
        </div>
      </div>
    </div>;
  }
}


DOM.render(
    <RegisterPage {...PROPS}/>,
    document.getElementById('react-root'));
