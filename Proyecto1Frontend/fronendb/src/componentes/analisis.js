import React, { Component, useEffect  ,useState } from 'react';
import '../css/comun.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/esm/Container';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col'
import axios from 'axios'
const URL = "http://localhost:5000/serv"

export default function Analisis(){
    const [valor,setvalue] = useState('');
    const [valor2,SetValor] = useState('');
    
    async function analizar(){
        const obj = {valor}
        const {data} = await axios.post(URL,obj)
        console.log(data)
        SetValor( data)
    }
    async function ast(){
        const obj = {valor}
        const {data} = await axios.post(URL+"/ast",obj)
        console.log(data)
    }
    async function tablaSimbolo(){
        const {data} = await axios.get(URL + '/simbolo')
        console.log(data)
    }
    async function tablaErrores(){
        const {data} = await axios.get(URL + '/error')
        console.log(data)
    }

    const readFile = (e) =>{
        const file = e.target.files[0];
        if(!file) return;
        const fileReader = new FileReader();
        fileReader.readAsText(file)

        fileReader.onload = () =>{
            console.log(fileReader.result)
            setvalue(fileReader.result)
        }

        fileReader.onerror =()=>{
            console.log(fileReader.error)
        }

    }

        return (
            <>
                <Container> <Row>
                        <Col>
                        <div className="form-group">
                        <Form.Label style={{ color: 'black' }} >Entrada</Form.Label>  <br />
                            <Form.Control as="textarea" rows={3} name="analizador"  value = {valor} onChange = {(e)=> setvalue(e.target.value)}/><br />
                            <input type = "file" multiple= {false} onChange={readFile} />
                        </div>
                        </Col>
                        <Col>
                        <div className="form-group">
                        <Form.Label style={{ color: 'black' }}>Consola</Form.Label>  <br />
                            <Form.Control as="textarea" rows={3} name="consola" value = {valor2} onChange = {(e)=> SetValor(e.target.valor2)} /><br />
                        </div>
                            <Button variant="primary" onClick={analizar}> Analizar</Button> &nbsp;
                            <Button variant="secondary" onClick={tablaSimbolo}> Tabla Simbolos</Button> &nbsp;
                            <Button variant="danger" onClick={tablaErrores}> Tabla Errores</Button> &nbsp;
                            <Button variant="success" onClick={ast}> AST</Button><br/>
                        </Col>
                    </Row>
                </Container>
            </>
        );
    
}
