import React, {Component} from "react"

const MapContext = React.createContext()

const reducer = (state, action) => {

  switch (action.type) {
    case 'CLOSE_INFOWINDOW':
      console.log("close window");
      return {
        ...state,
        infoWindow: -1
      }

    case 'OPEN_INFOWINDOW':
      console.log("open window");
      return {
        ...state,
        infoWindow: action.payload
      }

    default:
      return {
        ...state,
      }

  }

}

export class MapProvider extends Component {

  constructor(props) {
    super(props);
    this.state = {
      infoWindow: -1,
      dispatch: async action => {
        this.setState(state => reducer(state, action))
      }
    }
  }

  render() {
    return (
      <MapContext.Provider value={this.state}>
        {this.props.children}
      </MapContext.Provider>
    )

  }

}

export const MapConsumer = MapContext.Consumer
