import React, { Component } from 'react';
import './SuggestSuburb.scss';
import Slogon from '../../components/Slogon';

export default class SuggestSuburb extends Component {
  static displayName = 'SuggestSuburb';

  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div className='suggest-page'>
        <Slogon
          style={{
            margin: 'auto',
          }}
        />
        {SuggestSuburb.displayName}
      </div>
    );
  }
}