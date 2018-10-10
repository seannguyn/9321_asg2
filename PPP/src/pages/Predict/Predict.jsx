import React, { Component } from 'react';
import './Predict.scss';
import * as Common from '../../Common';
import Slogon from '../../components/Slogon';
import { CircularProgress, Snackbar, } from '@material-ui/core';
import axios from 'axios';

export default class Home extends Component {
  static displayName = 'Home';

  constructor(props) {
    super(props);
    this.data = JSON.parse(decodeURIComponent(escape(atob(this.props.match.params.data))));
    this.state = {};
  }

  componentDidMount() {
    axios.get(Common.BACKEND_URL + '/predictPffrice',
      { params: { ...this.data } }
    )
      .then((response) => {
        console.log(response.data.data)
        this.setState({ data: response.data.data });
      })
      .catch((e) => {
        let errorMsg;
        if (e.response && e.response.data) {
          console.error(e.response);
          errorMsg = e.response.data['msg'];
        } else {
          console.error(e);
          errorMsg = 'Opps! Unknow error happens...';
        }
        this.setState({
          isSnackBarOpen: true,
          snackBarMsg: errorMsg,
        });
      });
  }

  render() {
    return (
      <div className='predict-page'>
        <Slogon
          style={{
            margin: 'auto',
          }}
        />
        <Snackbar
          anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
          autoHideDuration={1500}
          open={this.state.isSnackBarOpen}
          message={this.state.snackBarMsg}
          onClose={() => {
            this.setState({
              isSnackBarOpen: false,
              snackBarMsg: null,
            });
          }}
        />
        {
          this.state.data ?
            <div>
              <div className='predict-result'>
                Our algorithm has calculated that the price will be
                <div className='price'>
                  $ {this.state.data.prediction.main.price}
                </div>
                for your <span className='filter'>{this.data.type}</span> with <span className='filter'>{this.data.bedroom}</span> bedroom, <span className='filter'>{this.data.bathroom}</span> bathroom, <span className='filter'>{this.data.carpark}</span> car space in the area <span className='filter'>{this.data.suburb}</span>
              </div>
            </div>
            :
            <CircularProgress
              size={50}
              style={{
                display: 'table',
                margin: 'auto',
              }}
            />
        }
      </div>
    );
  }
}