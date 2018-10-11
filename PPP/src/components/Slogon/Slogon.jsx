
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
        <div className='app-desc'>
          Trying to find a property to purchase in Melbourne?<br />
          Let us know what you're looking for and<br />
          we'll suggest how much it will cost to but your dream home!<br />
        </div>
      </div>
    );
  }
}