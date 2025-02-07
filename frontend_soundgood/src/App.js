import Home from './Pages/Home';
import Profile from './Pages/Profile';
import Forum from './Pages/Forum';
import SavedSongs from './Pages/SavedSongs';
import './App.css';
import { Route, Routes } from 'react-router-dom';
import DiscoveredSongs from './Pages/DiscoveredSongs';
import Register from './Pages/Register.js';
import Login from './Pages/Login.js';

function App() {
  return (
    <div className='App'>
      {localStorage.getItem('userToken') != null ? (
        <div>
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/profile' element={<Profile />} />
            <Route path='/savedSongs' element={<SavedSongs />} />
            <Route path='/forum' element={<Forum />} />
            <Route path='/discoveredSongs' element={<DiscoveredSongs />} />
          </Routes>
        </div>
      ) : (
        <div>
          <Routes>
            <Route path='/login' element={<Login />} />
            <Route path='/register' element={<Register />} />
          </Routes>
        </div>
      )}
    </div>
  );
}

export default App;
