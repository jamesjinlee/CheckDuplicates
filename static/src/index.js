import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

const divStyle = {
  margin: '40px',
};

const DupSet = (props) => {
  const items = props.items;
  const listItems = items.map((item) =>
  <div style={divStyle}>
    <li>{item[0]}</li>
    <li>{item[1]}</li>
  </div>
  );
  return (
    <ul>{listItems}</ul>
  );
}

class App extends Component{
  constructor(props) {
    super(props);

    this.state= {
      duplicates: [],
      nearDuplicates: []
    };
    this.checkDups=this.checkDups.bind(this);

  }

  checkDups() {
    axios.get('http://127.0.0.1:5000/duplicates')
    .then(response => this.setState({duplicates: response.data.duplicates, nearDuplicates: response.data.nearDuplicates}));
    console.log(this.state.duplicates);
    console.log(this.state.nearDuplicates);
  };
  render(){
    return (
      <div>
        <button onClick={this.checkDups}> Click to Check Duplicates </button>
      <h3>Duplicates</h3>
      <DupSet items={this.state.duplicates} />
      <h3>Near Duplicates</h3>
      <DupSet items={this.state.nearDuplicates} />
    </div>
    );
  };
};

ReactDOM.render(<App />, document.getElementById('main'));
