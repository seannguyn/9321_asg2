import React, { Component } from 'react';
import './Home.scss';
import Slogon from '../../components/Slogon';
import Button from '@material-ui/core/Button';

export default class Home extends Component {
  static displayName = 'Home';

  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div className='home-page'>
        <Slogon
          style={{
            margin: 'auto',
          }}
        />
        <div className='app-desc'>
          Trying to find a property to purchase in Melbourne?<br />
          Let us know what you're looking for and we'll provide predictions and suggestions.<br />
          Here we go!
        </div>
        <div className='app-options'>
          <Button
            variant='extendedFab'
            size='large'
            color='primary'
            onClick={() => {
              this.props.history.push('/predict');
            }}
          >
            Predict Price
          </Button>
          <Button
            variant='extendedFab'
            size='large'
            color='secondary'
            onClick={() => {
              this.props.history.push('/suggest');
            }}
          >
            Suggest Suburb
          </Button>
        </div>
      </div>
    );
  }
}