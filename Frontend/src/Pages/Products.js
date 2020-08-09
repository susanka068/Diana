import React, { Component } from 'react'
import ProductPanel from '../Component/ProductPanel'
export class Products extends Component {

    constructor(props){
        super(props);
        this.state={
            
        }
    }

    render() {
        return (
            <div>
                <ProductPanel/>
            </div>
        )
    }
}

export default Products
