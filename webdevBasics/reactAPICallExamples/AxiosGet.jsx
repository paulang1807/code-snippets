import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { v4 as uuid } from 'uuid';

function AxiosGet() {
  const [resp, setResp] = useState([]);
  const guid = uuid();

  // Add relevant headers below
  const headers = {
    'Content-Type': 'application/json',
    Accept: '*/*',
    requestId: guid,
    Authorization: 'Auth Header',
  };

  useEffect(() => {
    axios
      .get(
        'https://api-url',
        { headers, },
      )
      .then((response) => {
        setResp(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      {resp ? <pre>{JSON.stringify(resp, null, 2)}</pre> : 'Loading...'}
    </div>
  );
}

export default AxiosGet;
