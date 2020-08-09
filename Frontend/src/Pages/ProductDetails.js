import React, { Component } from 'react'
import {Image} from 'react-bootstrap'
import {ProgressBar} from 'react-bootstrap'
export class ProductDetails extends Component {
    render() {
        //console.log(this.props.location)
        const { title , details , image , comments , rating_div } = this.props.location.dataProps;
        const rating_array = Object.values(rating_div); 
        const color_scheme = ["success","info","warning","danger","success"]
        //console.log(rating_array);
        return (
            <div>
                <h1>{title}</h1>
        <p>{details[0]}</p>
                <Image src={image} />
            <ProgressBar>
                {
                    rating_array.map( ( rating , index ) => {
                        return(
                            <ProgressBar animated now={rating} variant={color_scheme[index]} />
                        )
                    } )
                }
            </ProgressBar>
            
            {
                comments.map( comment => {
                    return (
                        <div>
                        <h2>{comment.heading}</h2>
                        <p>{comment.body}</p>
                        <p>on {comment.date}</p>
                        </div>
                    )
                })
            }

            </div>
        )
    }
}

export default ProductDetails
