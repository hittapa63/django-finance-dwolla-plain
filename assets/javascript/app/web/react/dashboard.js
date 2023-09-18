import React, {useState, useEffect, useCallback} from "react";
import { Modal, Button, Form, Container, Row, Col, Alert } from "react-bootstrap";
import {getAction} from "../../../api";
import {API_ROOT} from "../const";
import LoadingScreen from "../../../utilities/Loading";
import PlaidLink from "./plaidLink";


const Dashboard = function(props) {
  const client = props.client;
  const [isLoading, setIsLoading] = useState(true);
  const [isCalling, setIsCalling] = useState(false);
  const [showAlertModal, setShowAlertModal] = useState(false);
  const [showAlert, setShowAlert] = useState(false);
  const [message, setMessage] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showBankModal, setShowBankModal] = useState(false);
  const [showDepositModal, setShowDepositModal] = useState(false);
  const [showWithDrawModal, setShowWithdrawModal] = useState(false);
  const [createInfo, setCreateInfo] = useState({
    'customer_id': 'customer_id',
    'first_name': '',
    'last_name': '',
    'email': '',
    'type': 'personal',
    'address1': '',
    'city': '',
    'state': '',
    'postal_code': '',
    'date_of_birth': '',
    'ssn': '',
  });
  const [customer, setCustomer] = useState(null);
  const [amount, setAmount] = useState('');
  const [fundings, setFundings] = useState(null);
  const [balance, setBalance] = useState(null);
  const [linkToken, setLinkToken] = useState('');

  useEffect(() => {
    getPrimaryInfo();
  }, []);

  const getPrimaryInfo = () => {
      getCustomer().then(res_c => {
          if (res_c.results && res_c.results.length > 0) {
              getFundings().then(res_f => {
                if (res_f.results && res_f.results.length > 0) {
                    getBalance().then(res_b => {
                        console.log(res_b);
                        setIsLoading(false);
                    })
                } else {
                    setIsLoading(false);
                }
              })
          } else {
              setIsLoading(false);
          }
      });
  }

  const handleClose = () => {
    setShowCreateModal(false);
    setShowBankModal(false);
    setShowDepositModal(false);
    setShowWithdrawModal(false);
  };
  const handleCreateShow = () => setShowCreateModal(true);
  const handleDepositShow = () => {
    setAmount('');
    setShowDepositModal(true);
  }
  const handleWithdrawShow = () => {
    setAmount('');
    setShowWithdrawModal(true);
  }

  const handleCreateChange = (event) => {
    let fieldName = event.target.name;
    let fleldVal = event.target.value;
    setCreateInfo({...createInfo, [fieldName]: fleldVal});
  }

  const handleDepositeChange = (event) => {
    let fieldName = event.target.name;
    let fleldVal = event.target.value;
    setAmount(fleldVal);
  }

  const validateEmail = (email) => {
    const filter = /(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)/
    if (filter.test(email)){
        return true;
    };
    return false;
  }

  const validateAge = (year) => {
      if (year === null && year.length != 10){
          return false;
      }
      /// dwolla account must be 18~125 years
      let age = new Date().getFullYear() - parseInt(year);
      if (age <= 18 || age >= 125) {
          return false;
      } else {
        return true;
      }        
  }

  const createCustomer = () => {
    if (createInfo.first_name === '' || 
        createInfo.last_name === '' ||
        createInfo.email === '' ||
        createInfo.address1 === '' ||
        createInfo.city === '' ||
        createInfo.state === '' ||
        createInfo.postal_code === '' ||
        createInfo.date_of_birth === '' ||
        createInfo.ssn === ''
    ) {
        setMessage('Please input the fields');
        setShowAlertModal(true);
        return;
    }
    if (!validateEmail(createInfo.email)) {
        setMessage('Please input the validate email');
        setShowAlertModal(true);
        return;
    }
    if (createInfo.state.length != 2) {
        setMessage('The State must be 2 charachters');
        setShowAlertModal(true);
        return;
    }
    if (createInfo.postal_code.length != 5) {
        setMessage('Please input the valid postal code');
        setShowAlertModal(true);
        return;
    }
    if (!validateAge(createInfo.date_of_birth)) {
        setMessage('Your age must be between 18 and 120');
        setShowAlertModal(true);
        return;
    }
    if (createInfo.ssn.length != 4) {
        setMessage('Please input the valid ssn');
        setShowAlertModal(true);
        return;
    }
    let action = getAction(API_ROOT, ["customers", "create"]);
    setIsLoading(true);
    client.action(window.schema, action, createInfo).then((result) => {
      setMessage(result.message);
      if (result.status) {
        handleClose();
        setShowAlert(true);
        setCustomer(result.data);
      } else {
          setShowAlertModal(true);
      }
      setIsLoading(false);
    });
  }

  // dwolla apis
  const getCustomer = () => {
    const action = getAction(API_ROOT, ["customers", "list"]);
    return client.action(window.schema, action).then((result) => {
        if (result && result.count > 0 && result.results && result.results.length > 0) {
            setCustomer(result.results[0]);
        }       
        return result;
    });
  }

  const getFundings = () => {
    const action = getAction(API_ROOT, ["funding_sources", "list"]);
    return client.action(window.schema, action).then((result) => {
        if (result && result.count > 0 && result.results && result.results.length > 0) {
           setFundings(result.results);
        }
        return result;
    });
  }

  const getBalance = () => {
    const action = getAction(API_ROOT, ["funding_sources", "read"]);
    const params = { id : 1 }
    return client.action(window.schema, action, params).then((result) => {
        if (result && result.status && result.data) {
           setBalance(result.data);
        }
        return result;
    });
  }

  // plaid part
  
  const handleBankShow = () => {
      if (isCalling) {
          return true;
      }
      setIsCalling(true);
    let params = { id: 1};
    const action = getAction(API_ROOT, ["plaid", "read"]);
    client.action(window.schema, action, params).then((result) => {
      if (result.status) {
          setLinkToken(result.link_token);
          setShowBankModal(true);
      } else {
          setMessage(result.message);
          setShowAlert(true);
      }
      setIsCalling(false);
    });

  };

  const handleDeposite = () => {
    if (amount == '' || amount < 1) {
        setMessage('Please input the deposit mount');
        setShowAlertModal(true);
        return true;
    }
    setMessage('');
    setShowAlertModal(false);
    if (isCalling) {
        return true;
    }
    setIsCalling(true);
    let params = { amount: amount, funding_id: fundings[0]['funding_id'], type: "deposit"};
    const action = getAction(API_ROOT, ["transfer_sources", "create"]);
    client.action(window.schema, action, params).then((result) => {
        if (result.status) {
            setShowDepositModal(false);
            setMessage(result.message);
            setShowAlert(true);
            getBalance();
        } else {
            setMessage(result.message);
            setShowAlert(true);
        }
        setIsCalling(false);
    });
  }

  const handleWithdraw = () => {
    if (amount == '' || amount < 1) {
        setMessage('Please input the withdraw mount');
        setShowAlertModal(true);
        return true;
    }
    if (parseFloat(balance) < amount) {
        setMessage('You can withraw less than balance.');
        setShowAlertModal(true);
        return true;
    }
    setMessage('');
    setShowAlertModal(false);
    if (isCalling) {
        return true;
    }
    setIsCalling(true);
    let params = { amount: amount, funding_id: fundings[0]['funding_id'], type: "withdraw"};
    const action = getAction(API_ROOT, ["transfer_sources", "create"]);
    client.action(window.schema, action, params).then((result) => {
        if (result.status) {
            setShowWithdrawModal(false);
            setMessage(result.message);
            setShowAlert(true);
            getBalance();
        } else {
            setMessage(result.message);
            setShowAlert(true);
        }
        setIsCalling(false);
    });
  }

  if (isLoading) {
    return <LoadingScreen/>
    //   return (
    //       <div>
    //           <section className="app-card">
    //               <div className="text-center" style={{paddingTop: 100, paddingBottom: 100}}>
    //                 { isLoading && <Spinner animation="border" role="status">
    //                     <span className="visually-hidden">Loading...</span>
    //                     </Spinner> 
    //                 }
    //               </div>
    //           </section>
              
    //       </div>
    //   );
  }

  
  
  return (
    <div>            
        { showAlert && <Alert variant="success" onClose={() => setShowAlert(false)} dismissible>
            <p>{message}</p>
        </Alert> }
        <section className="app-card">
            <div className="pg-columns">
            <div className="pg-column-one-third">
                <div className="pg-balance-box">
                <h2 className="text-center">Balance</h2>
                
                <h4 className="text-center">$ { balance != null ? balance : "0" }</h4>
                { customer === null && <button className="pg-button-primary" onClick={handleCreateShow}>
                    Become a customer
                </button> }
                </div>
            </div>
            <div className="pg-column-one-third">
                <div className="pg-balance-box">
                { fundings!=null && fundings.length>0 ? <button className="pg-button-secondary">
                    Connected { fundings[0]['bank_name'] }
                </button> : customer!=null ? <button className="pg-button-primary" onClick={handleBankShow}>
                    Connect Bank Account
                </button> : <button className="pg-button-primary" onClick={handleCreateShow}>
                    Connect Bank Account
                </button> }
                <br></br>
                { fundings!=null && fundings.length>0 ? <button className="pg-button-primary" onClick={handleDepositShow}>
                    Deposit Funds
                </button> : customer != null ? <button className="pg-button-primary" onClick={handleBankShow}>
                    Deposit Funds
                </button> : <button className="pg-button-primary" onClick={handleCreateShow}>
                    Deposit Funds
                </button> }
                </div>
            </div>
            <div className="pg-column-one-third">
                <div className="pg-balance-box">
                    { fundings != null && fundings.length > 0 ? <button className="pg-button-primary" onClick={handleWithdrawShow}>
                    Withdraw Funds
                </button> : <button className="pg-button-primary" onClick={handleWithdrawShow}>
                    Withdraw Funds
                </button> }
                </div>
            </div>
            </div>            
            <Modal show={showCreateModal} size="lg" onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Create a Account</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h5 className="text-center">Please Input your Information</h5>
                    { showAlertModal && <Alert variant="warning" onClose={() => setShowAlertModal(false)} dismissible>
                        <Alert.Heading></Alert.Heading>
                        <p>{message}</p>
                    </Alert> }
                    <Container fluid="md">
                    <Row>
                        <Col>
                        <Form.Group className="mb-3" controlId="first_name">
                            <Form.Label>First Name</Form.Label>
                            <Form.Control type="text" name='first_name' onChange={handleCreateChange.bind(this)}  />
                        </Form.Group>
                        </Col>
                        <Col>
                        <Form.Group className="mb-3" controlId="last_name">
                        <Form.Label>Last Name</Form.Label>
                        <Form.Control type="text" name='last_name' onChange={handleCreateChange.bind(this)}  />
                        </Form.Group>
                        </Col>
                    </Row>
                    </Container>
                    <Container fluid="md">
                    <Form.Group className="mb-3" controlId="email">
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email" placeholder="Enter email" name='email' onChange={handleCreateChange.bind(this)}  />
                    </Form.Group>
                    </Container>
                    <Container fluid="md">
                    <Form.Group className="mb-3" controlId="address1">
                        <Form.Label>Address</Form.Label>
                        <Form.Control type="text" name='address1' onChange={handleCreateChange.bind(this)}  />
                    </Form.Group>
                    </Container>
                    <Container fluid="md">
                    <Row>
                        <Col>
                        <Form.Group className="mb-3" controlId="city">
                            <Form.Label>City</Form.Label>
                            <Form.Control type="text" name='city' onChange={handleCreateChange.bind(this)}  />
                        </Form.Group>
                        </Col>
                        <Col>
                        <Form.Group className="mb-3" controlId="state">
                            <Form.Label>State</Form.Label>
                            <Form.Control type="text" name='state' onChange={handleCreateChange.bind(this)}  />
                        </Form.Group>
                        </Col>
                    </Row>
                    </Container>
                    <Container fluid="md">
                    <Row>
                        <Col>
                        <Form.Group className="mb-3" controlId="postal_code">
                            <Form.Label>Postal Code</Form.Label>
                            <Form.Control type="number" min="1000" max="99999" name='postal_code' onChange={handleCreateChange.bind(this)}  />
                        </Form.Group>
                        </Col>
                        <Col>
                        <Form.Group className="mb-3" controlId="date_of_birth">
                            <Form.Label>Birthday</Form.Label>
                            <Form.Control type="date" name='date_of_birth' onChange={handleCreateChange.bind(this)}  />
                        </Form.Group>
                        </Col>
                        <Col>
                        <Form.Group className="mb-3" controlId="ssn">
                            <Form.Label>SSN</Form.Label>
                            <Form.Control type="text" name='ssn' onChange={handleCreateChange.bind(this)}  />
                            <Form.Text className="text-muted">
                            Last four-digits social security number.
                            </Form.Text>
                        </Form.Group>
                        </Col>
                    </Row>
                    </Container>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                    Close
                    </Button>
                    <Button variant="primary" onClick={createCustomer}>
                    Create
                    </Button>
                </Modal.Footer>
            </Modal>
            <Modal show={showBankModal} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Connect a Bank</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Container>
                        <PlaidLink {...props} token={linkToken} customer={customer}/>
                    </Container>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                    Close
                    </Button>
                    <Button variant="primary" onClick={handleClose}>
                    Connect
                    </Button>
                </Modal.Footer>
            </Modal>
            <Modal show={showDepositModal} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Deposit Funds</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h5 className="text-center">Please Input Deposit Amount</h5>
                    { showAlertModal && <Alert variant="warning" onClose={() => setShowAlertModal(false)} dismissible>
                        <Alert.Heading></Alert.Heading>
                        <p>{message}</p>
                    </Alert> }
                    <Form.Group className="mb-3" controlId="depositAmount">
                    <Form.Label>Amount</Form.Label>
                    <Form.Control type="number" name="amount" min="1" onChange={handleDepositeChange.bind(this)}/>
                    </Form.Group>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                    Close
                    </Button>
                    <Button variant="primary" onClick={handleDeposite}>
                    Submit
                    </Button>
                </Modal.Footer>
            </Modal>
            <Modal show={showWithDrawModal} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Withdraw Funds</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <h5 className="text-center">Please Input Withdraw Amount</h5>
                    { showAlertModal && <Alert variant="warning" onClose={() => setShowAlertModal(false)} dismissible>
                        <Alert.Heading></Alert.Heading>
                        <p>{message}</p>
                    </Alert> }
                    <Form.Group className="mb-3" controlId="withdrawAmount">
                    <Form.Label>Amount</Form.Label>
                    <Form.Control type="number" name="amount" min="1" onChange={handleDepositeChange.bind(this)}/>
                    </Form.Group>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                    Close
                    </Button>
                    <Button variant="primary" onClick={handleWithdraw}>
                    Submit
                    </Button>
                </Modal.Footer>
            </Modal>
        </section>

        <section className="app-card">
            <div className="pg-columns">
                <h4>
                    Next scope
                </h4>
                <br></br>
                <h6>Need to improve from sandbox to prod</h6>
                <p>- set the real dwolla account <br/>get real api key and set real bank <br/>check the api again for prod env</p>
                <p>- set the real plaid account <br/>get real api key, client id and bank info<br/>check the get token and verify bank api</p>
                <p>- changed the value of env file with prod values</p>
                <p>- check the apis again in dwolla</p>
            </div>
        </section>
    </div>
  );
};

export default Dashboard;