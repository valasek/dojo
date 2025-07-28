// netlify/functions/forum-proxy.js
exports.handler = async (event, context) => {
  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  // Only allow GET requests
  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    // Fetch data from Discourse
    const response = await fetch('https://komunita.dojo.sk/t/aktualne-programy/12.json', {
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible)',
        'Accept': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const firstPost = data.post_stream?.posts?.[0];

    if (firstPost && firstPost.cooked) {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ content: firstPost.cooked })
      };
    } else {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({ content: null })
      };
    }

  } catch (error) {
    console.error('Error fetching forum content:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ content: null, error: error.message })
    };
  }
};
