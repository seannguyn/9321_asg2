
import React, { Component } from 'react';
import './Slogon.scss';

export default class Slogon extends Component {
  static displayName = 'Slogon';

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className='slogon-view'
        style={this.props.style}>
        <img className='app-logo'
          src={require('./images/logo.png')} />
        <div className='app-name'>
          Property Price Predictor
        </div>
      </div>
    );
  }
}