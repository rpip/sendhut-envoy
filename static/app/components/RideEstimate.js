var _ = require('lodash');
import React from 'react'
import ReactDOM from 'react-dom'
import { GoogleApiWrapper } from 'google-maps-react'
import styled from 'styled-components';

import MapContainer from './Map.js'

import LocationIcon from  '../../images/icons/location.svg'
import ArrowRightIcon from '../../images/icons/arrow-right.svg'
import API from './api'

const MapsAPIKey = 'AIzaSyDVZn9gbIfivvhXOI1eAY1tu2M-yo2LO9w'

const fadeAnimationStyle = styled.div`
  animation: FadeAnimation 1s ease-in .2s forwards;

  @keyframes FadeAnimation {
    0% {
      opacity: 1;
      visibility: visible;
    }

    100% {
      opacity: 0;
      visibility: hidden;
    }
  }
}
`

const FadeAnimation = ({content}) => (
  // TODO(yao): render children components instead
  <div>{content}</div>
)

class RideEstimate extends React.Component {
  constructor(props) {
    super(props);
    this.pickupRef = React.createRef()
    this.dropoffRef = React.createRef()
    this.mapRef = React.createRef()
    this.google = this.props.google
    this.map = null
    this.markers = []

    this.state = {
      pickup: null,
      dropoff: null,
      quote: null,
      error: null
    }
  }

  componentDidMount() {
    this.map = this.mapRef.current.mapRef.current.map
    this.renderAutoComplete();
  }

  componentDidUpdate(prevProps, prevState) {
      this.updateWithMarkers();
  }

  onSubmit = (e) => {
    e.preventDefault();
    this.updateWithMarkers()
  }

  getQuote(pickup, dropoff) {
    // TODO(yao): cache lookups locally. key expires after 30 minutes
    API.post('quotes-v1/', {pickup: pickup, dropoffs: [dropoff]})
      .then(res => {
        // TODO(yao): create TimeoutError type
        // a lot can happen in 1 second
        // ideal: 1 second. uber 1.03
        // ok: 2
        // quotes is the pricing, magic sauce
        // ASAP: PERFECT THIS
        // good pricing in itself is the product. the real value
        // - cache most common quotes
        // - check nearest server/peer client (driver or customer) for quote
        // - on app start, load quotes from server
        this.setState((prevState, props) => {
          return { ...prevState, quote: res.data}
        })
      }).catch((error) => {
        this.setRequestError()
        console.log(error)
      })
  }

  setRequestError() {
    const error_msg = "Error, please try again."
    this.setState((prevState, props) => {
      return {...prevState, error: error_msg}
    })
    // TODO(yao): after 3 second dynamuically change CSS or delete component
    setTimeout(function() {}, 200)
    this.setState((prevState, props) => {
      return {...prevState, error: null}
    })
  }

  renderAutoComplete() {
    const {google, map} = this

    if (!google || !map) return;

    this.poly = new this.google.maps.Polyline({
      strokeColor: '#ffb600',
      strokeOpacity: 1.0,
      strokeWeight: 3,
      map: this.map
    })

    this.setupAutoComplete(this.pickupRef.current, 'pickup')
    this.setupAutoComplete(this.dropoffRef.current, 'dropoff')
  }

  setupAutoComplete(elem, addressType) {
    const {google, map} = this
    // restrict the search to geographical location types {types: ['geocode']}
    var autocomplete = new google.maps.places.Autocomplete(elem)

    autocomplete.bindTo('bounds', map);
    autocomplete.addListener('place_changed', () => {
      const place = autocomplete.getPlace();
      if (!place.geometry) return;
      if (place.geometry.viewport) map.fitBounds(place.geometry.viewport);
      else {
        map.setCenter(place.geometry.location);
        map.setZoom(14);
      }
      this.setState({[addressType]: place })
    });
  }

  updateWithMarkers() {
    const {pickup, dropoff} = this.state
    this.clearMarkers()
    if (pickup) this.addMarker(this.getLatLng(pickup))
    if (dropoff) this.addMarker(this.getLatLng(dropoff))
    if (!pickup || !dropoff) return;

    let latlng1 = this.getLatLng(pickup)
    let latlng2 = this.getLatLng(dropoff)

    this.setPolyLine(latlng1, latlng2)
    const bounds = new this.google.maps.LatLngBounds(latlng1, latlng2)
    this.map.fitBounds(bounds)
    //this.map.setZoom(14);

    let params = {
      pickup: pickup.formatted_address,
      dropoff: dropoff.formatted_address
    }
    if (_.isEqual(this.prevLookup, params)) return;

    console.log('prevlookup ' + this.prevLookup)
    this.getQuote(params.pickup, params.dropoff)
    this.prevLookup = params
  }

  getLatLng(place) {
    const lat = place.geometry.location.lat()
    const lng = place.geometry.location.lng()
    return new google.maps.LatLng(lat, lng)
  }

  pruneAddress(place) {
    let picks = [
      'address_components',
      'formatted_address',
      'name',
      'plus_code',
      'place_id',
      'types',
      'reviews',
      'rating'
    ]
    let obj = _.pick(place, picks)
    return _.merge(obj, {latlng: latlngFromPlace(place)})
  }

  setPolyLine(pickup, dropoff) {
    this.poly.setMap(null);
    this.poly.setMap(this.map)
    this.poly.setPath([pickup, dropoff])
  }

  // Adds a marker to the map and push to the array.
  addMarker(location) {
    var marker = new google.maps.Marker({
      position: location,
      map: this.map
    });
    this.markers.push(marker);
  }

  // Sets the map on all markers in the array.
  setMapOnAll(map) {
    for (var i = 0; i < this.markers.length; i++) {
      this.markers[i].setMap(map);
    }
  }

  // Removes the markers from the map, but keeps them in the array.
  clearMarkers() {
    this.setMapOnAll(null);
  }

  // Shows any markers currently in the array.
  showMarkers() {
    this.setMapOnAll(map);
  }

  // Deletes all markers in the array by removing references to them.
  deleteMarkers() {
    this.clearMarkers();
    this.markers = [];
  }

  render() {
    return (
      <div className="col-md-11">
        <div className="row">
          <div className="col-md-5 offset-md-1 align-middle" id="estimate-form-wrapper">
            <h4>Get a price estimate</h4>
            <div className="row">
              <div className="col-1">
                <svg height="100" width="190">
                  <line className="line" x1="20" y1="20" x2="20" y2="90"></line>
                  <marker id="marker-start" markerWidth="8" markerHeight="8" refX="5" refY="5">
                    <circle className="foreground" cx="5" cy="5" r="1" />
                  </marker>
                  <marker id="marker-end" markerWidth="8" markerHeight="8" refX="5" refY="5">
                    <circle className="foreground" cx="5" cy="5" r="1" />
                  </marker>
                </svg>
              </div>
              <div className="col-10">
                <form onSubmit={this.onSubmit}>
                  <div className="input-group">
                    <input type="text" className="form-control" placeholder="Enter pickup location"
                           id="pickup" ref={this.pickupRef} />
                    <span className="input-group-addon" id="pickup-addon">
                      <img className="icon" src={LocationIcon} />
                    </span>
                  </div>
                  <div className="input-group">
                    <input type="text" className="form-control" placeholder="Enter destination"
                           ref={this.dropoffRef}/>
                    <span className="input-group-addon" id="dropoff-addon">
                      <img className="icon" src={ArrowRightIcon} />
                    </span>
                  </div>
                  <div>
                    {this.state.error?
                      <FadeAnimation style={fadeAnimationStyle} content={this.state.error} /> :
                        <div>
                            {this.state.quote &&
                              <div>
                                  <small className="form-text text-muted">
                                      Estimates do not reflect variations due to discounts, demand or other factors.</small>
                                    <h3>{this.state.quote.pricing}</h3>
                                </div>
                                }
                          </div>
                      }
                  </div>
                  <input type="submit" hidden />
               </form>
              </div>
            </div>
          </div>
          <div className="col-md-6" id="estimate-map">
            <MapContainer google={this.props.google} ref={this.mapRef} />
          </div>
        </div>
      </div>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: MapsAPIKey,
})(RideEstimate)
