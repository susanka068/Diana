import React, { Component } from 'react'
import {InputGroup , FormControl , Button , Form } from 'react-bootstrap'

export class SearchBox extends Component {
    render() {
        return (
            <div style={{'width':'70%' , 'margin': '0 auto'}} >
            <Form.Label>search products</Form.Label>
            <InputGroup className="mb-3">
            <FormControl
            placeholder="Search Apparels here..."
            aria-label="keywords"
            aria-describedby="basic-addon2"
            />
            <InputGroup.Append>
            <Button variant="outline-secondary">Search</Button>
            </InputGroup.Append>
            </InputGroup>
            <Form.Text className="text-muted">
            Go on, type something 
            </Form.Text>
            </div>
        )
    }
}

export default SearchBox
