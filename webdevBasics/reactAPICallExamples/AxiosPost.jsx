import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AxiosPost() {
  const [resp, setResp] = useState([]);

  // Add relevant headers below
  const headers = {
    'Content-Type': 'application/json',
    Accept: '*/*',
    Authorization: 'Auth Header',
  };

  // Add body
  const data = {
    key: {
      childKey: 'val',
      childKey2: 'val',
    },
  };

  useEffect(() => {
    axios
      .post(
        'https://api-url',
        data,
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

export default AxiosPost;
