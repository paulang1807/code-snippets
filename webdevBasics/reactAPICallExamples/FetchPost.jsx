import React, { useState, useEffect } from 'react';
import { v4 as uuid } from 'uuid';

function FetchPost() {
  const [data, setData] = useState(null);
  const guid = uuid();
  const bodyJson = {
    key: {
      childKey: 'val',
      childKey2: 'val',
    },
  };
  const options = {
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      requestId: guid,
      Authorization: 'Auth Header',
    },
    method: 'POST',
    body: JSON.stringify(bodyJson),
    credentials: 'include',   // include cookies
  };

  useEffect(() => {
    fetch(
      'https://api-url',
      options,
    )
      .then((response) => response.json())
      .then((json) => setData(json))
      .catch((error) => console.error(error));
  }, []);

  return (
    <div>
      {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : 'Loading...'}
    </div>
  );
}

export default FetchPost;
