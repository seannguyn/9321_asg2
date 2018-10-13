import React from 'react'
import PropTypes from 'prop-types'
import NotFound from '../NotFound/NotFound'
import Chart from "react-google-charts";
import axios from 'axios'
import * as Common from '../../Common';


class Metric extends React.Component {

  static displayName = 'Metric';

  constructor(props) {
    super(props)
    this.state = {
      login: false,
      init: false,
    }
  }


  async componentDidMount() {
    const res = await axios.get(Common.BACKEND_URL + '/trendRecord');
    if (this.props.location.state !== undefined && this.props.location.state.login === true) {
      this.setState({
        login: true,
        init: true,
        data: res.data.data,
        options: res.data.options
      })
    } else {
      this.setState({
        init: true,
      })
    }
  }

  render () {
    if (this.state.login === true && this.state.init === true) {
      return (
        <div>
          <Chart
          chartType="PieChart"
          width="100%"
          height="400px"
          data={this.state.data}
          options={this.state.options}
          />
        </div>
      )
    } else if (this.state.init === false) {
      return (
        <h1>loading...</h1>
      )
    } else {
      return (
        <NotFound/>
      )
    }

  }
}

export default Metric;
