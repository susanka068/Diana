import React, { Component } from 'react'
import ProductIndividual from './ProductIndividual';
import NordStormData from '../data/stage_4.json'
export class ProductPanel extends Component {
    render() {
        //console.log(NordStormData)
        return (
            <div >
            {
                NordStormData.items.map(item => ( <ProductIndividual data={item} /> ))
            }
            </div>
        )
    }
}

export default ProductPanel
