
import './App.css';
import TextField from '@mui/material/TextField';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import { useState } from 'react';
import Button from '@mui/material/Button';

const BASE_URL = 'http://127.0.0.1:5000/';
const COMPANIES_SEARCH_ENDPOINT = 'search_companies';

interface individualSearchResult {
  cname: string,
  url: string,
  matchScore: string,
  matchFreq: string
}

function App() {
  const [technologyArea, setTechnologyArea] = useState<string>("");
  const [includeStartups, setIncludeStartups] = useState<boolean>(true);
  const [searchResults, setSearchResults] = useState<Array<individualSearchResult>>([]);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setIncludeStartups(event.target.checked);
  }

  const search = () => {
    const body = JSON.stringify({
      technologyArea, includeStartups
    })
    fetch(`${BASE_URL}${COMPANIES_SEARCH_ENDPOINT}`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      mode: "cors",
      body,
    })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      setSearchResults(data['search_results']);
    });
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to company search!</h1>
        <h3>Optimizing Google</h3>
        <h4>To get started, type in a technology area:</h4>
        <TextField 
          id="filled-basic" 
          label="Technology Area" 
          variant="filled"
          onChange={(e) => {
            setTechnologyArea(e.target.value);
          }}
          />
        <div>
          <FormControlLabel 
              control={<Checkbox 
                checked={includeStartups}
                onChange={handleChange}
                defaultChecked />}
              label="Do you want to include startups?" />
        </div>
        <Button variant="contained" onClick={search}>Search!</Button>
        {searchResults.map((element) => (
          <div className='searchResult'>
            <p>Company Name: {element.cname}</p>
            <p>Company Website: {element.url}</p>
            <p>Search Rank: {element.matchScore}</p>
            <p>Match Frequency: {element.matchFreq}</p>
            <hr />
          </div>
        ))}
      </header>
    </div>
  );
}

export default App;
