import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import {Map, Marker} from 'google-maps-react';

export default class MapContainer extends Component {

  constructor(props) {
    super(props);
    this.google = props.google
    this.mapRef = React.createRef()
    //this.state = {}
  }

  render() {
    return (
      <Map

        ref={this.mapRef}
        google={this.google}
        zoom={11}
        initialCenter={{
          lat: 6.50,
          lng: 3.37
        }}
        mapType='roadmap'
        mapTypeControl={false}
        style={{ height: '100%', position: 'relative', width: '100%' }}
        >
      </Map>
    );
  }
}
