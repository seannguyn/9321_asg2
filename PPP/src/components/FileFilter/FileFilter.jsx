import React, { Component } from 'react';
import './FileFilter.scss';
import * as Common from '../../Common';
import { Snackbar, CircularProgress, Select, MenuItem } from '@material-ui/core';
import axios from 'axios';
import TextField from '@material-ui/core/TextField';

export default class FileFilter extends Component {
  static displayName = 'FileFilter';

  constructor(props) {
    super(props);
    this.state = {
      floorPlan: "",
    }
  }

  handleChange = event => {
    console.log(event.target.name,"uploading files...",event.target.value);

    this.setState({ [event.target.name]: event.target.value });

    if (this.props.onChange) {
      this.props.onChange(event.target.name, event.target.value);
    }

  };

  render() {
    return (
      <div className='basic-filter-container'
        style={this.props.style}
      >
        <div className='basic-filters'>
          <div className='basic-filter'>
            <div className='basic-filter-title'>
              Floor Plan
            </div>
            <TextField
              multiline
              rowsMax="5"
              value={this.state.floorPlan}
              onChange={this.handleChange}
              type="text"
              name="floorPlan"
            />
          </div>
        </div>
        
      </div>
    );
  }
}
