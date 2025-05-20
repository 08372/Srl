import React, { useEffect, useState } from 'react';

export default function Home() {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    fetch('https://srl-simulator-backend.onrender.com/api/srl/today')
      .then(res => res.json())
      .then(data => setMatches(data));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1 style={{ fontSize: '2rem', textAlign: 'center' }}>Matchs SRL simulés du jour</h1>
      {matches.map((match, index) => (
        <div key={index} style={{ border: '1px solid #ccc', borderRadius: 12, padding: 20, marginTop: 20 }}>
          <h2>{match.teams}</h2>
          <p style={{ fontWeight: 'bold' }}>{match.score}</p>
          <div style={{ maxHeight: 150, overflowY: 'auto' }}>
            {match.events.map((event, idx) => (
              <p key={idx}>{event.minute}' - {event.text}</p>
            ))}
          </div>
          <div style={{ marginTop: 10 }}>
            <a
              href={`https://srl-simulator-backend.onrender.com/api/srl/pdf/${index}`}
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'blue', textDecoration: 'underline' }}
            >
              Télécharger la fiche PDF
            </a>
          </div>
        </div>
      ))}
    </div>
  );
}
